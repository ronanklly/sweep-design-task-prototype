# Build brief — the single-page deliverable

The whole presentation is one continuous scrolling page: a short strategic narrative (the pain in the original flow, then the reframe into four stages) that leads directly into the high-fidelity Act view prototype, mounted inside a mock browser chrome. This brief is the spec the page was built from end to end — the preamble sections and the high-fidelity prototype together, as one build, not two.

**Figma sources (inspect these directly while building via the Figma MCP — `get_design_context` / `get_screenshot` / `get_metadata` / `get_variable_defs`):**

- Preamble + page shell — Page 2, Section 1: https://www.figma.com/design/0gxNwR6hoK0tJrP5RpzF9I/Untitled?node-id=2-10829
- High-fidelity Act view — node `64:24885`, "High fidelity page": https://www.figma.com/design/0gxNwR6hoK0tJrP5RpzF9I/Untitled?node-id=64-24885

Both frames were designed by Ronan for this task and are read into the build via the Figma MCP. This brief is a thorough written account of them, but it's a *description*, not a substitute for the source: exact spacing, type sizes, colours, icon shapes — anything this brief simplifies — should be resolved against the live frames, not guessed. The goal is for the built page to sit as close to the real design as plain HTML/CSS can get.

## What this brief covers

One page, top to bottom:

- The sticky header.
- The full-viewport hero.
- The "Analysis of the original flow" section (7-step breakdown + effort/emotion chart).
- The "Reframing into 4 stages" section (Drafting / Aligning / Assigning / Sustaining cards).
- The **high-fidelity Act view prototype**, mounted inside a mock browser chrome — the single frame the brief's "highest-leverage moment" refers to.
- The scroll-reveal that brings the browser chrome in, and the sticky-header behaviour.

The page ends on the prototype fully in view — there is nothing below it.

## Tech constraints

- Plain HTML/CSS/vanilla JS. No framework, no build step — this needs to survive being opened cold in a demo room and hosted on GitHub Pages.
- JS covers: sticky-header behaviour, the scroll-reveal animation, smooth-scroll for the header's play icon, and the Act view's own interactivity.
- The Act view fetches the real `data/` JSON at runtime and derives everything from it through a single `render()` — no baked-in content. (Because of the runtime `fetch`, the page must be served over http, not opened from `file://`.)
- Figma frames are fixed 1440px-wide desktop designs — there is no mobile frame. Build responsively off 1440 as the reference breakpoint; use judgment for tablet/mobile collapse.
- Visual tokens (colour, neutrals, the grass/crop/fire semantic ramp) come from `visual-language.md`. The high-fidelity Act view frame is authored in **Inter** specifically, so this screen uses Inter directly at the exact px sizes given below.

## Page structure (top to bottom)

The whole thing lives inside one 1440px-wide flow, sections stacked with no gaps between the hero and the sections that follow it (each section carries its own internal padding: **120px left/right, 120px top, 60/120px bottom** — apply the same rhythm across sections unless a section's content clearly calls for something else).

### 0. Sticky header (persists across the whole page)

Fixed/sticky at all times, 1440×67, white background, `space-between` layout, 24px horizontal / 16px vertical padding:

- Left: title text, **"From spreadsheets to sustained accountability"** (bold/dark).
- Next to it: **"Ronan Kelly · September 2026"** (gray, smaller — presenter/date byline).
- Right: two icon buttons, in this order:
  1. **Play** (▶) — a blue-outlined rounded-square button, blue triangle icon. **Active/current state by default.**
  2. **Code** (`</>`) — plain icon, no background, gray/neutral (inactive state).

**Icon behavior:**
- **Play** returns to the top of the presentation — smooth-scroll to Beat 1, re-starting the narrated walkthrough (this page *is* the presentation; there's no separate slide-mode file).
- **Code** opens the Repo page (`repo.html`).
- Do **not** implement scrollspy / auto-swap of the active icon based on scroll position — the blue "active" state is just play's default look, not a tracked state.

### 1. Hero (full viewport height on load)

**Annotation, verbatim:** *"The opening headline should take up the full browser height on page load. The next section should only be visible on scroll."*

- Height: hero content area = 100vh, with the header a fixed bar on top of that (additive, not overlapping).
- White background.
- Eyebrow label (small, gray, uppercase-tracking style consistent with the rest of the deck's eyebrow labels).
- H1 (large, bold) stating the deliverable's thesis, with key phrases italicised.
- Nothing else in the hero — a clean, single-statement opening. The next section must not be peekable/visible until the user actually scrolls (don't let flex/grid overflow leak the next section's top edge into view on load).

### 2. "Analysis of the original flow and where it hurts"

Section heading, then a two-column layout: a left **stage swimlane** and a right **numbered step list**, followed by a **compounding-impact chart**.

**Stage swimlane (left column, narrow):**
Two stacked colored blocks spanning the height of the rows they group:
- A dark/near-black block labeled **"Once per cycle"**, spanning steps 1–4. Inside it, three sub-labels in lighter gray card panels, each spanning its own step range: **"Drafting"** (step 1), **"Aligning"** (steps 2–3), **"Assigning"** (step 4).
- A red block labeled **"Every month, indefinitely"**, spanning steps 5–7. Inside it, one sub-label in a light pink/tinted panel: **"Sustaining"** (steps 5–7). The red block and its tint are `visual-language.md`'s fire-500 / fire-100 (`#b81f00` / `#fce6e2`) — Sweep's own "this is the pain" signal.

**Numbered step list (right column, 7 rows):**
Each row: number chip, bold title, gray one-line description, and a right-aligned "Effort" label with 5 dots (filled dots colored by magnitude, unfilled gray). Exact copy and effort reads:

| # | Title | Description | Effort (dots, colored) |
|---|---|---|---|
| 1 | Draft actions from interviews | Lead drafts candidate actions in a spreadsheet from stakeholder interviews | 3/5, amber |
| 2 | Circulate for review | Lead emails the spreadsheet to 5–6 stakeholders for review and comment | 2/5, green |
| 3 | Consolidate & finalise list | Lead consolidates feedback and finalises ~15 actions | 3/5, amber |
| 4 | Assign owners | Lead assigns owners by emailing each person individually | 2/5, green |
| 5 | Owners update monthly | Each owner updates progress monthly on a central spreadsheet | 2/5, green |
| 6 | Chase silent owners | Lead manually chases the 4–5 owners who haven't reported | 5/5, red (max) |
| 7 | Compile leadership summary | Lead compiles a summary for leadership review, often from memory | 4/5, orange |

**Compounding-impact chart** ("The impact of steps 5-7 compounding"):
An emoji-anchored line/dot chart. Y axis: "Delight 😀" (top) to "Exasperation 😫" (bottom). X axis: steps 1–7. Background is split into two zones matching the swimlane: a plain zone for "Once per cycle" (steps 1–4) and a light pink-tinted zone for "Every month, indefinitely" (steps 5–7). The line dips gently across 1–4, then drops hard across 5–7 (step 6 is the visual low point), with a curved red dashed arrow looping from step 5 up over the dip to step 7 — implying the monthly repeat/compounding cycle. Dot size doubles as the effort score, matching the step list's dots. Caption underneath, small gray text: **"Effort is and emotional experience are assumed and illustrative only"** — copy this exactly as written, apparent typo and all.

### 3. "Reframing into 4 stages, accelerated by Sweepy"

Section heading, then four equal-width cards in one row (Drafting, Aligning, Assigning, Sustaining). Each card:

- Eyebrow tag: **"Wireframe"** (gray) for the first three, **"Prototyped"** (blue) for Sustaining only.
- Title (bold, larger — blue for Sustaining, dark for the other three).
- One-sentence description.
- Small gray caption: **"How Sweepy accelerates [drafting initiatives / aligning stakeholders / assigning ownership / progress]"**.
- A short icon list (emoji/icon + one line each) — Sweepy's specific contributions for that stage.
- An embedded UI fragment (the first three only — Sustaining has no fragment). **Use the exported images, don't rebuild these in code.** Files: `design-task/prototype/assets/reframe-drafting-fragment.png`, `reframe-aligning-fragment.png`, `reframe-assigning-fragment.png`.
- Sustaining only: a filled blue **"View the prototype"** button at the bottom, and a blue border around the whole card (visually heroed).

Exact copy per card:

**Drafting** — "Sweepy turns the raw interview notes into a structured first-draft action list for the lead to review." / "How Sweepy accelerates drafting initiatives" / 🎤 Turns unstructured interview notes into a candidate action list / 💡 Suggests a scope and GHG category per action.

**Aligning** — "Sweepy requests and consolidates responses, flagging disagreements and making the lead's final call easier." / "How Sweepy accelerates aligning stakeholders" / 🗂️ Consolidates every response into a single list automatically / 🚩 Flags where stakeholders agree and disagree.

**Assigning** — "Sweepy suggests the best-placed owner per initiative and drafts the ask; the lead can override at any time." / "How Sweepy accelerates assigning ownership" / 🧑 Suggests an owner from existing site and role data / 📣 Drafts the individual ask to each owner.

**Sustaining** (heroed, blue border, "Prototyped" tag) — "Sweepy collects, chases and checks the data, then drafts the report; the lead signs everything off." / "How Sweepy accelerates progress" / 📨 Sends the monthly check-in and chases silence automatically / 💬 Turns a free-text reply into a structured status, next step or blocker / 🚩 Flags likely discrepancies / 📄 Drafts the leadership summary for the lead to review / **[View the prototype]** button.

### 4. The browser chrome

Directly below the reframe section: a minimal mac-style browser-chrome frame that wraps the high-fidelity prototype — three traffic-light dots (red/amber/green, non-functional), a sidebar-toggle icon, and back/forward chevrons. The container is sized to hold the full 1440-wide Act view within one viewport, and it's the element that animates in on scroll/click (see Reveal animation). Everything in section 5 mounts inside its body.

### 5. The high-fidelity Act view prototype

The real product surface, built into the chrome above. It fetches the real JSON (`initiatives.json`, `reports.json`, `for-you-items.json`, `activity-log.json`, `trajectory.json`) at runtime and drives one in-memory state object through a single `render()`. Layout: a slim left nav rail, the main Act column (chart → monthly-reports tile → initiatives grid), and Sweepy's agent panel on the right.

**Chart — "Total carbon reduction · YTD".** Two lines — **Actual** (black) and **Target** (blue `#283fff`) — with a red/pink fill rendered only where Actual sits above Target. Fixed y-axis gridlines at **3k / 6k / 9k / 12k / 15k**; x-axis **Feb–Nov**, the current month (Jun in the reference state) at full opacity, the rest at 50%. Point markers at each vertex, and a real per-month hover interaction: a vertical guideline down to a dot on each line, plus a floating card showing both series in tCO2e. Stat block above the chart: **"147,307 tCO2e"** (18/28 bold), then on one row "15 initiatives" (14 regular) + "**+4.9% vs. target**" — the deviation coloured by polarity (`#ff383c` when positive/worse, `#0f7200` when negative/better). The chart's small-number scale is a separate aggregate from that headline total.

**Monthly Reports tile** (below the chart, in the same bordered wrapper): a four-state row — **Default** ("Awaiting data"), **Hover**, **In progress** ("Sweepy's making your report…", once the For You queue is cleared, ~2s), and **Ready** (blue border on the card + a solid-blue "Report ready" pill). Lucide `globe` icon tile on the left; "View all reports" on the right.

**Initiatives grid ("All actions"):** a 3×5 grid of 283×290 cards — photo, scope chip (each card's **real** scope from the data, top-right), status row (7px dot + label, coloured **Ready for review `#0016d0` / Blocked `#dc6800` / Up to date `#0f7200`**), title (18/23 bold), owner · team (14 regular `#858585`), and a change-vs-YTD line coloured by polarity, independent of the status colour above it. The grid is **sorted by status** — the three actions surfaced in the For You panel lead (Ready for review first, then the two Blocked in the panel's own order), with everything Up to date following; the **Sort control reads "Sort: Status."** Filter and "Add new +" are styled but inert.

**Agent panel (Sweepy)** on the right: an 83px Sweepy mark, then a four-tab pill bar — **For You, Activity, Goals, Chat** — using the Tabler set (`notification` / `activity` / `target` / `message-circle`). The Monthly Reports globe is Lucide (`globe`) — deliberately two different icon families, not unified. Only **For You** is wired; Activity, Goals and Chat are present with real content but static.

**For You — the decision queue.** "The following actions need your attention." Each row opens (pages, doesn't route) to a full drill-in that plays back the whole trail — Sweepy's check-in, the owner's reply, the data they sent back, and Sweepy's own quality-check note. A **Ready** item (Daniel Osiel) carries a filled-blue **Submit data** button that flips the initiative to Up to date and clears the card; a **Blocked** item (Yuki Tanaka, Sam Okafor) carries an outline **Acknowledge** button that clears the card but leaves it Blocked. The back chevron always returns to the list. Once the queue is empty, the report tile moves Default → In progress → Ready and a "report is ready" row appears in For You at the same moment.

**Statuses** are exactly three anywhere in the UI — Ready for review, Blocked, Up to date — derived from the data: `blocked` → Blocked; else `dataStatus === "pending_review"` → Ready for review; else → Up to date.

**Typography** is Inter throughout this screen, at the frame's exact sizes: chart title 20/32, total stat 18/28, initiative card titles 18/23, For You row titles 16/28, meta/owner/chip 14/20.

**Deliberately inert:** the initiative-detail and report pages (wireframe stubs), the nav rail's placeholder tiles, "Add new +", the Configure control, and the message input. The Act view is the one frame taken to full fidelity — that restraint is the point, not a gap.

## Reveal animation

**Annotation, verbatim:** *"Pressing view the prototype auto scrolls the page and the browser animates in — subtle fade and easing with slight x axis rotation from -2 to 0 degrees. Browser also appears in on scroll, with the same animation effect."*

- Trigger 1: clicking Sustaining's "View the prototype" button → smooth-scroll down to the browser-chrome container.
- Trigger 2: the container scrolling into view naturally — use an IntersectionObserver on a **short element near the top of the chrome** (the chrome bar), not the whole tall container, so it fires reliably regardless of the container's height.
- Effect (both triggers): fade in + ease, combined with an X-axis rotation from **-2° to 0°** (a slight "tilting up into place" feel, not a 3D flip).
- Plays once on first arrival; do not replay on subsequent scrolls.
- Respect `prefers-reduced-motion`: skip the animation entirely if set.

## Grounding and copy fidelity

- Both Figma frames were designed by Ronan for this task and read live via the Figma MCP; where the code simplifies a detail, it's checked back against the frame rather than guessed.
- Real names and content come from the JSON data layer, not Figma's placeholder duplication (the design's example rows repeat a few names/images; the build pulls the real seed data). "Daniel Osiel" is spelled with the "l" everywhere it appears.
- Build copy exactly as designed — including spots that read like mistakes (the chart caption's "Effort is and emotional experience are…" and Sustaining's "How Sweepy accelerates progress"). Flag anything that looks wrong rather than silently correcting it.

## How the prototype came together (decisions)

- **Everything derives from one data layer.** The Act view, the reports timeline and the per-initiative history all read the same JSON, so the supporting surfaces could be generated from it at little extra cost, extending the Sustain narrative beyond the hero frame without extra hand-building (see `decisions-log.md`).
- **Real seed data wins over literal Figma placeholder.** Where the design showed duplicated placeholder content (a repeated scope chip, repeated example names), the build uses each initiative's real scope and owner from the data instead.
- **Allude, don't build.** Configure, the message input, "Add new +", and the detail/report pages are present but inert — the trust discipline is carried by the For You sign-off loop, not by building out every surface.

## Assets exported for this build

Exported from the live Figma file into `design-task/prototype/assets/`: `reframe-drafting-fragment.png`, `reframe-aligning-fragment.png`, `reframe-assigning-fragment.png` (the three reframe-card UI fragments). Initiative photography lives in `assets/initiatives/`, referenced by a single `image` field per initiative in `initiatives.json`.

## Acceptance checklist

**Shell + preamble**
- [ ] Opened both live Figma frames directly (links at the top) and checked spacing, type, colour and icon details against them — not just this document's prose.
- [ ] Sticky header present at all scroll positions, correct copy, play icon defaults to active/blue; play smooth-scrolls to top; code icon opens the Repo page.
- [ ] Hero is a full viewport tall on load; no part of the next section is visible without scrolling.
- [ ] Analysis section: swimlane grouping, all 7 rows with correct copy/effort dots, chart with correct emoji anchors and pink recurring-zone tint.
- [ ] Reframe section: four cards, copy verbatim, three real exported fragment images (not rebuilt in HTML/CSS), Sustaining heroed with a working "View the prototype" button.
- [ ] Browser chrome present and correctly styled, sized to hold the 1440-wide Act view; reveal animation (fade + -2°→0°) fires once on both button-click and natural scroll-in, skipped under `prefers-reduced-motion`.
- [ ] Page ends on the prototype fully in view — nothing scrollable below it.

**High-fidelity Act view**
- [ ] Renders from the real `data/` JSON at runtime through a single `render()`.
- [ ] Chart is a real two-line (Actual/Target) chart with a red fill only where Actual > Target; x-axis Feb–Nov; y-axis gridlines exactly 3k/6k/9k/12k/15k; per-month hover tooltip with guideline + two dots + floating card.
- [ ] "+X%/-X% vs. target" (top stat and every card) coloured `#ff383c` positive / `#0f7200` negative.
- [ ] Initiative statuses render in the three states with the exact hexes; grid is sorted by status and the Sort control reads "Sort: Status."
- [ ] Tab bar icons are Tabler; the report globe is Lucide — two different families, not unified.
- [ ] Typography is Inter at the exact px/line-heights above.
- [ ] "Daniel Osiel" spelled correctly everywhere.
- [ ] Monthly Reports tile implements all 4 states; the report-ready row appears in For You the moment the queue clears.
- [ ] For You is a single paginated surface (list ↔ detail); back chevron always returns to the list; Submit data (filled) vs. Acknowledge (outline) are distinct; both clear the card, only Submit changes status.
- [ ] Whole page is plain HTML/CSS/vanilla JS, no build step, served over http.
