# Process: how I'd simplify this flow

## Where the current flow actually breaks

The seven-step manual flow has two different kinds of pain in it, and they don't deserve the same response.

**Episodic pain (steps 1–4):** drafting the first action list, circulating it for comment, consolidating feedback, assigning owners. This happens once per planning cycle. Slow and effortful, but it doesn't compound — the lead feels it once, then moves on.

**Recurring pain (steps 5–7):** owners updating progress monthly, the lead manually chasing the 4–5 who go quiet, then reconstructing a leadership summary from memory and old emails. This happens every month, for the life of the program, and it's the only part of the flow the brief itself describes with real frustration ("manually chase," "reconstructing... from memory").

That distinction is the whole basis for where effort goes below: light assistance for the episodic half, real investment in the one part that compounds.

## The principle: AI expedites, clarifies, and suggests — the human always decides

One rule, applied consistently across every stage, rather than a different ad hoc justification at each step. It also isn't invented from nothing — it's how Sweepy already works ("every action keeps the human in the loop... review, approve, and control all recommendations"), applied to a part of the product that doesn't have it yet: a first-class initiative, with an owner and a status, that today only exists in spreadsheets.

## The redesigned flow: four stages instead of seven steps

**1. Draft** — Interviews stay human (irreducibly so). Sweepy turns the lead's raw notes into a structured first-draft list, faster than typing it into a spreadsheet by hand. The lead edits before it goes anywhere.

**2. Align** — Stakeholder input is gathered through a structured, Sweep-style request (closer to how Surveys already work) rather than an email with a spreadsheet attached. Sweepy consolidates the responses and flags where stakeholders disagree or an action still lacks a clear owner. The lead makes the final call on the ~15-item list.

**3. Assign** — Once the list is set, Sweepy suggests the best-placed owner per initiative and drafts the personalised ask. The lead can override any suggestion and edits the message before it sends. Ownership is a judgment call about capacity and relationships — Sweepy accelerates it, it doesn't make it.

**4. Sustain — the stage we're prototyping.** Replaces steps 5–7 entirely. Instead of a spreadsheet cell nobody updates, each owner gets a plain-language check-in; they reply in their own words; Sweepy extracts a structured status (on track / at risk / stalled, blocker, next step) and shows the owner what it understood before anything saves. The ESG lead's Act view rolls these up next to the existing target-vs-actual charts — anyone who hasn't responded stays visibly stale, never quietly inferred — and Sweepy can draft the leadership-review summary from confirmed data only.

## Mapping: the brief's 7 steps → our 4 stages

A single reference table so the logic above can be checked against the original brief at any point, rather than taken on faith.

| # | Brief's original step | Our stage | What changes |
|---|---|---|---|
| 1 | Lead drafts candidate actions in a spreadsheet from stakeholder interviews | **1. Draft** | Interviews stay human; Sweepy structures the notes into a first-draft list; lead edits |
| 2 | Lead emails the spreadsheet to 5–6 stakeholders for review and comment | **2. Align** | Email-a-spreadsheet replaced by a structured, Survey-style request |
| 3 | Lead consolidates feedback and finalises ~15 actions | **2. Align** | Sweepy consolidates responses and flags disagreement; lead makes the final call |
| 4 | Lead assigns owners by emailing each person individually | **3. Assign** | Sweepy suggests the best-placed owner and drafts the ask; lead can override and edits before sending |
| 5 | Each owner updates progress monthly on a central spreadsheet | **4. Sustain** *(prototyped)* | Spreadsheet cell replaced by a plain-language check-in the owner replies to in their own words |
| 6 | Lead manually chases the 4–5 owners who haven't reported | **4. Sustain** *(prototyped)* | No chasing needed — anyone who hasn't responded is visibly stale in the Act view automatically |
| 7 | Lead compiles a summary for leadership review, often from memory | **4. Sustain** *(prototyped)* | Sweepy drafts the summary directly from confirmed, sourced status — nothing reconstructed from memory |

The table makes the shape of the redesign visible at a glance: steps 2–3 collapse into one aligned stage, and steps 5–7 — the three steps that were actually broken — collapse into a single continuous loop, which is exactly where the prototype investment goes.

## Why Stage 4 is the one we built, not the others

It's the only stage that's recurring rather than one-off, so the time saved compounds every month instead of once per cycle. It's the stage the brief itself names as painful, not just slow. And it's the cleanest place to demonstrate the trust boundary that matters most here: Sweepy interprets what an owner said, but it never invents or upgrades their status on their behalf — exactly the discipline Sweep already holds itself to, and exactly the discipline that matters most once a number this personal (a program's real status, going in front of leadership) is on the line.

## What's deliberately out of scope for this pass

Given the 4-hour budget, these are conscious omissions, not oversights:

- Stages 1–3 are described and reasoned through above, not built — the leverage is in Stage 4.
- The prototype simulates the check-in channel (what would be email, Slack, or similar in production) rather than integrating a real messaging system.
- Single program, ~15 initiatives — no portfolio-level view across multiple concurrent programs.
- No admin/configuration surface (setting up targets, inviting stakeholders) — assumed to already exist elsewhere in Sweep.

## Guardrails carried into the prototype

- Sweepy never invents or upgrades a status — everything traces back to the owner's own words.
- Anything unconfirmed stays visibly stale. It's never smoothed over into a false "on track."
- The owner always sees and can correct what Sweepy understood before it's saved — nothing is recorded without their confirmation.
- The leadership summary only ever draws from confirmed, sourced data, with gaps flagged rather than filled in.

## What's next

The Stage 4 prototype (`design-task/prototype/`) and the walkthrough. Beyond the hero Act view, the prototype also carries a reports timeline and a per-initiative history — generated from the same underlying data layer at little extra cost, and worth the space because they show the one thing a single snapshot can't: the monthly cadence where a status story compounds over time. See `decisions-log.pdf` for the reasoning trail behind every call above.
