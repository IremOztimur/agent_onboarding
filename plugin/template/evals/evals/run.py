"""Run the eval suite, grade it, compare with the baseline, write a report.

    python evals/run.py                     # the real system, via evals/target.py
    python evals/run.py --dry-run           # offline self-test of the harness
    python evals/run.py --update-baseline   # accept this run as the new baseline

Exit 0: every criterion meets its threshold and none regressed past the
tolerance. Exit 1: a criterion failed or regressed. Exit 2: the harness is
broken (oracle did not pass, null did not fail, or every attempt errored).

--dry-run runs two fake systems through the whole pipeline: an oracle that
returns each case's `reference`, and a null that returns nothing. The oracle
must pass and the null must fail; if not, a case or grader is broken. It then
scores the oracle against the baseline, so a broken case also fails the run.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import datetime as dt
import json
import math
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Callable

sys.path.insert(0, str(Path(__file__).resolve().parent))

from graders import grade  # noqa: E402

ROOT = Path(__file__).resolve().parent


def load_cases(cases_dir: Path) -> list[dict[str, Any]]:
    cases = []
    for path in sorted(cases_dir.glob("*.jsonl")):
        for n, line in enumerate(path.read_text().splitlines(), 1):
            if line.strip():
                case = json.loads(line)
                case.setdefault("_source", f"{path.name}:{n}")
                cases.append(case)
    ids = [c["id"] for c in cases]
    dupes = {i for i in ids if ids.count(i) > 1}
    if dupes:
        sys.exit(f"duplicate case ids: {sorted(dupes)}")
    return cases


def oracle(case_input: dict[str, Any], budget: dict[str, int], case: dict[str, Any]) -> dict[str, Any]:
    ref = case["grader"].get("reference")
    return {"output": ref, "state": ref if isinstance(ref, dict) else {}, "transcript": []}


def null(case_input: dict[str, Any], budget: dict[str, int], case: dict[str, Any]) -> dict[str, Any]:
    return {"output": "", "state": {}, "transcript": []}


def attempt(target: Callable[..., dict[str, Any]], case: dict[str, Any], budget: dict[str, int]) -> dict[str, Any]:
    """One (case, rep). Infra errors are recorded as errors, never scored as failures."""
    started = time.monotonic()
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
        future = pool.submit(target, case["input"], budget, case)
        try:
            result = future.result(timeout=budget["timeout_s"])
        except concurrent.futures.TimeoutError:
            return {"status": "error", "error": f"timeout after {budget['timeout_s']}s"}
        except NotImplementedError as exc:
            sys.exit(str(exc))
        except Exception as exc:
            return {"status": "error", "error": f"{type(exc).__name__}: {exc}"}
    result["latency_s"] = round(time.monotonic() - started, 3)
    result["input"] = case["input"]
    if result.get("refused"):
        result["status"] = "refused"
        return result
    if result.get("stopped"):
        result["status"] = "stopped"  # hit a bound: counted, shown, not averaged in as wrong
        return result
    verdict = grade(case["grader"], result)
    result["grade"] = {"passed": verdict.passed, "reason": verdict.reason}
    result["status"] = {True: "pass", False: "fail", None: "ungraded"}[verdict.passed]
    return result


def wilson(passed: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return (0.0, 0.0)
    p = passed / n
    centre = (p + z * z / (2 * n)) / (1 + z * z / n)
    spread = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return (round(max(0.0, centre - spread), 3), round(min(1.0, centre + spread), 3))


def run_suite(target: Callable[..., dict[str, Any]], cases: list[dict[str, Any]], reps: int, budget: dict[str, int]) -> list[dict[str, Any]]:
    rows = []
    for case in cases:
        for rep in range(reps):
            row = attempt(target, case, budget)
            row.update(case_id=case["id"], criterion=case["criterion"], rep=rep, tags=case.get("tags", []))
            rows.append(row)
    return rows


def score(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    by_criterion: dict[str, dict[str, Any]] = {}
    for row in rows:
        s = by_criterion.setdefault(row["criterion"], {"pass": 0, "fail": 0, "error": 0, "refused": 0, "stopped": 0, "ungraded": 0})
        s[row["status"]] += 1
    for s in by_criterion.values():
        graded = s["pass"] + s["fail"]
        s["pass_rate"] = round(s["pass"] / graded, 3) if graded else None
        s["ci95"] = wilson(s["pass"], graded)
    return by_criterion


def verdicts(scores: dict[str, dict[str, Any]], criteria: dict[str, Any], baseline: dict[str, Any], tolerance: float) -> list[str]:
    problems = []
    for name, crit in criteria.items():
        s = scores.get(name)
        if s is None or s["pass_rate"] is None:
            problems.append(f"{name}: no graded attempts")
            continue
        if s["pass_rate"] < crit["threshold"]:
            problems.append(f"{name}: pass rate {s['pass_rate']} below threshold {crit['threshold']}")
        base = baseline.get(name, {}).get("pass_rate")
        if base is not None and s["pass_rate"] < base - tolerance:
            problems.append(f"{name}: regressed from {base} to {s['pass_rate']} (tolerance {tolerance})")
    return problems


def git_sha() -> str:
    try:
        return subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "nogit"


def write_report(out: Path, config: dict[str, Any], scores: dict[str, Any], baseline: dict[str, Any], criteria: dict[str, Any], problems: list[str], rows: list[dict[str, Any]]) -> None:
    out.mkdir(parents=True, exist_ok=True)
    with (out / "transcripts.jsonl").open("w") as f:
        for row in rows:
            f.write(json.dumps(row, default=str) + "\n")
    passes = [r for r in rows if r["status"] == "pass"][:3]
    fails = [r for r in rows if r["status"] == "fail"][:3]
    template = (ROOT / "report.template.md").read_text()
    table = ["| Criterion | Pass rate | 95% CI | Threshold | Baseline | Errors | Refused | Stopped |", "|---|---|---|---|---|---|---|---|"]
    for name, s in sorted(scores.items()):
        table.append(
            f"| {name} | {s['pass_rate']} | {s['ci95'][0]}–{s['ci95'][1]} | {criteria.get(name, {}).get('threshold', '—')} "
            f"| {baseline.get(name, {}).get('pass_rate', '—')} | {s['error']} | {s['refused']} | {s['stopped']} |"
        )
    sample = "\n".join(f"- `{r['case_id']}` rep {r['rep']}: {r['status']}" for r in passes + fails) or "- none"
    report = template.format(
        date=config["date"],
        sha=config["sha"],
        config="\n".join(f"- **{k}:** {v}" for k, v in config.items()),
        scores="\n".join(table),
        verdict="PASS" if not problems else "FAIL\n\n" + "\n".join(f"- {p}" for p in problems),
        sample=sample,
    )
    (out / "report.md").write_text(report)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--reps", type=int, default=5, help="runs per case; report pass rate, not one lucky run")
    parser.add_argument("--max-turns", type=int, default=20)
    parser.add_argument("--max-tokens", type=int, default=200_000)
    parser.add_argument("--timeout", type=int, default=300, help="hard wall-clock seconds per attempt")
    parser.add_argument("--tolerance", type=float, default=0.05, help="allowed drop vs baseline")
    parser.add_argument("--dry-run", action="store_true", help="offline harness self-test (oracle + null)")
    parser.add_argument("--update-baseline", action="store_true")
    args = parser.parse_args()

    cases = load_cases(ROOT / "cases")
    criteria = json.loads((ROOT / "criteria.json").read_text())
    baseline_path = ROOT / "baseline.json"
    baseline = json.loads(baseline_path.read_text()) if baseline_path.exists() else {}
    budget = {"max_turns": args.max_turns, "max_tokens": args.max_tokens, "timeout_s": args.timeout}

    if args.dry_run:
        null_rows = run_suite(null, cases, 1, budget)
        lenient = [r["case_id"] for r in null_rows if r["status"] == "pass"]
        if lenient:
            print(f"harness broken: the null system passed {lenient}; those graders are too lenient")
            return 2
        target, reps, system = oracle, 1, "oracle (dry run)"
    else:
        from target import run as real_run

        def target(case_input: dict[str, Any], budget: dict[str, int], case: dict[str, Any]) -> dict[str, Any]:
            return real_run(case_input, budget)

        reps, system = args.reps, "evals/target.py"

    rows = run_suite(target, cases, reps, budget)
    if all(r["status"] == "error" for r in rows):
        print("harness broken: every attempt errored:", rows[0].get("error"))
        return 2
    scores = score(rows)
    problems = verdicts(scores, criteria, baseline, args.tolerance)
    if args.dry_run:
        broken = sorted({r["case_id"] for r in rows if r["status"] != "pass"})
        if broken:
            problems.insert(0, f"oracle failed {broken}: the reference does not pass its own grader (a broken case)")

    now = dt.datetime.now()
    config = {
        "date": now.strftime("%Y-%m-%d %H:%M"),
        "sha": git_sha(),
        "system": system,
        "cases": len(cases),
        "reps": reps,
        "budget": f"{args.max_turns} turns, {args.max_tokens} tokens, {args.timeout}s per attempt",
        "tolerance": args.tolerance,
    }
    out = ROOT / "reports" / f"{now:%Y-%m-%d-%H%M%S}-{config['sha']}"
    write_report(out, config, scores, baseline, criteria, problems, rows)

    for name, s in sorted(scores.items()):
        print(f"{name}: {s['pass_rate']} (95% CI {s['ci95'][0]}–{s['ci95'][1]}), errors {s['error']}")
    print(f"report: {out / 'report.md'}")
    for p in problems:
        print("FAIL", p)

    if args.update_baseline and not args.dry_run:
        if problems:
            print("baseline not updated: the run did not pass")
            return 1
        baseline_path.write_text(json.dumps({k: {"pass_rate": v["pass_rate"]} for k, v in scores.items()}, indent=2) + "\n")
        print(f"baseline updated: {baseline_path}; commit it on its own, with the reason")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
