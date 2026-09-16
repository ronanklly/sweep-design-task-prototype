# North Star — how we work on this, together

## Why this exists

Everything here is built for a live evaluation. Sweep is comparing candidates on process and judgment, not polish — how I think and prototype *with AI* as much as what the prototype ends up doing. So the repo itself, not only the final prototype, is part of the deliverable. This is the standing brief every piece of work here is checked against, so the narrative stays consistent across however many sessions it takes.

## The narrative to hold

Before anything is called finished, it should clearly answer:

1. **How does this person think?** Structured, not scattershot — ambiguity reduced to a few clearly named, defended decisions rather than hedging across every option.
2. **What's the level of maturity?** Senior thinking separates leverage from busywork, knows what *not* to build, anticipates second-order consequences, and doesn't over-invest past the brief's own 4-hour scope ("not AI for its own sake").
3. **Where does prior Sweep experience show up?** As demonstrated domain fluency — knowing the real primitives (Surveys, Act's quantitative tracking), extending what already exists rather than reinventing it, and reading the gap between the sustainability-literate ESG lead and the much-less-literate stakeholder — never as name-dropping.
4. **Is it strategic, not just usable?** Every decision traces back to a business reason for Sweep — time-to-value, reducing the lead's manual toil, staying consistent with Sweep's own shipped AI principles so it reads as shippable inside their product — not only a user-experience one.
5. **Does the AI judgment hold?** "AI is an enabler, not the product." Every AI-touching call is checked against Sweep's principles — traceable, controllable, auditable, human-in-the-loop, opt-out — and if a moment doesn't actually need AI, it's left out. That restraint is itself the evidence of judgment.

## The standard the repo is held to

- **Clean, minimal structure** — no dead files, no duplicate exploratory drafts left lying around.
- **A visible reasoning trail** — meaningful calls logged in `design-task/md/decisions-log.md` at the point they're made: what was decided, the alternative, and why, so someone skimming can reconstruct the thinking.
- **Evidence of directing AI deliberately** — the repo should read like a designer directing a capable tool with a clear point of view, not the tool free-wheeling and the good bits picked out after.
- **Grounded in what's real wherever checkable** — Sweep's actual Figma design system and shipped Sweepy AI principles over a plausible-sounding but generic invention.
