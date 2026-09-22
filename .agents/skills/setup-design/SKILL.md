---
name: setup-design
description: "Fill this project's DESIGN.md through a short Q&A instead of hand-editing {{TOKEN}}s — read before running /setup-design"
---

# Setup Design

Fill `DESIGN.md` through conversation. Its own header already states the
rule this skill exists to enforce: a value put in the template "becomes the
default of every project, and a default shared by every project is what
slop is." Never pick a reference, color, or number for the human — ask.

## Steps

1. Read the current `DESIGN.md`. Skip any section that already holds a
   real value, not a `{{TOKEN}}`.
2. Ask in batches, in this order — never every field at once:
   - **Overview**: Reference (a concrete object, place, or tradition —
     reject an adjective like "modern" or "clean" and ask for the specific
     thing it resembles instead), Audience, Primary job, Density + why, the
     one bold thing.
   - **Colors**: what the primary color means, whether dark mode ships (if
     no, drop every `-dark` token and component from the front matter).
   - **Typography**: display/text family and why each fits the Reference,
     weight count, line length if it differs from the 70ch default.
   - **Layout / Shapes / Elevation**: grid (columns, max width, gutter),
     radius hierarchy, the one elevation method (tonal layers, hairline
     border, or shadow).
   - **Components**: a real file or page that best shows the system — point
     at an actual path, since agents copy nearby code more than they read
     this file — and which component library, if any.
   - **Motion & Copy**: feedback/transition timing, voice, and any
     project-specific do's/don'ts.
3. Exact hex codes and px values: ask for them directly. No exact value yet
   → leave the token. Do not choose a color or spacing step for the human —
   that is the exact failure this file's header warns about.
4. Write a token and its prose explanation together — they travel as a
   pair, not as a bare front-matter value with no reasoning behind it.
5. Once every section you covered is resolved, delete the file's template
   guidance comment; leave it if `{{TOKEN}}`s remain.
6. Tell the human to run `npx @google/design.md lint DESIGN.md` once done —
   it catches broken token references and contrast failures this skill
   does not check itself.
