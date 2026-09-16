# Decisions log

A record of the judgment calls on this task and where the direction came from. Almost all of them were Ronan's — made in conversation, often thinking out loud, and often redirecting me when I drifted or over-reached. I wrote each one down at the point it was made, with the alternative that was on the table and the reasoning, so the thinking is recoverable without having been in the room. The brief values process over polish; this is that process.

---

## 2026-09-11 — Strategy and concept

### Leverage moment: the recurring monthly loop, not the one-off setup

The first thing Ronan did was refuse to treat all seven steps of the flow as equal. He split them: steps 1–4 (drafting the action list, circulating it, consolidating, assigning owners) are episodic — slow, but they happen once a cycle and don't compound. Steps 5–7 (owners updating monthly, the lead chasing the quiet ones, reconstructing a leadership summary) recur every month for the life of the programme, and they're the only part the brief describes with real frustration — "manually chase," "reconstructing… from memory." Ronan's call was to prototype that recurring loop and give the episodic half only light assistance. I'd floated the interview-notes-to-draft-list step as an alternative demo; he rejected it as one-off synthesis with lower recurring leverage. The rule he set — investment goes where the pain compounds — governed everything after.

### Reframe: extend Sweep's own primitives, not bolt on a chatbot

This is where Ronan's history at Sweep did the most work. He knew first-hand that there's no first-class "initiative" object with an owner and a qualitative status — those actions live in spreadsheets and email, which is exactly the brief's pain. So instead of "add an AI agent," he framed the concept as connective tissue between two things Sweep already does well: outward, no-login data-collection reach-outs (Surveys) and Act's quantitative target-tracking. His argument was that "extend two things that already work" is a stronger and more shippable story than inventing a new mechanism, and reads as something Sweep would actually build. I took that framing as the spine of the whole concept.

### Two-sided, not one screen

Ronan was emphatic on this one, and it came straight from his knowledge of who actually uses the product: the ops/finance/HR owners the brief describes essentially never log into Sweep — only the sustainability-literate ESG leads do. He insisted the prototype had to have two surfaces: a plain-language, low-jargon check-in for the owner that lives *outside* the app (no login), and the high-fidelity in-app Act view for the lead. I had drifted toward a single in-app solution; Ronan pulled it back, on the grounds that designing in-app-only would misread the real audience entirely. The owner-facing side also had to show the owner what Sweepy understood before anything saved — mirroring Sweep's own "review, approve, and control" principle.

### The initiatives rollup is *the* one high-fidelity frame

Fairly early on, Ronan wanted a crisp answer to a question he expected to be asked directly: what, exactly, are you prototyping at high fidelity? Not a diffuse "the whole Sustain experience." His call was that the initiatives rollup in the Act view is explicitly the single frame that answers the brief's "prototype the highest-leverage moment," and everything else — the reframe narrative, the owner-facing check-in, the report and the initiative detail — exists to set it up or extend it, never to share equal billing. He framed it as much about honesty as focus: it keeps the build effort weighted toward the one screen that carries the most, and it gives a defensible one-sentence answer if an interviewer asks what was actually built.

### One AI principle everywhere: Sweepy suggests and expedites; the human decides

I'd initially wanted to keep owner-assignment (step 4) fully manual — the theory being that ownership is a political/capacity judgment AI shouldn't touch. Ronan overruled that. He argued a single consistent rule applied across every stage — Sweepy drafts, consolidates and suggests; the lead edits, overrides or confirms before anything saves or sends — is more sophisticated than an ad-hoc "AI helps here, not there" split, and that it matches Sweepy's own stated principle almost word-for-word ("review, approve, and control all recommendations"). His point that stuck with me: restraint shouldn't show up as withholding AI from a step, but in *how much build investment* each step earns — the front half stays light-touch, and the real build goes into the one loop that compounds monthly.

### Package as one hosted microsite, prototype-first

Ronan decided early that the deliverable shouldn't be a folder of files someone has to open cold, or a slide deck with the prototype linked off to one side. His steer was a single hosted page opened from one link, with the interactive prototype as the primary surface and the reasoning trail (the Repo page) in support — explicitly *not* three co-equal tabs. His reasoning tied back to the brief: it asks for one prototype of the highest-leverage moment with everything else in support, so the structure itself should say the same thing rather than contradict it with equal weighting.

### Visual language: Sweep-adjacent by design, not a literal skin

Ronan designed the high-fidelity screens for this task in Figma and defined their design tokens and component patterns there, and had me build directly from that source via the Figma MCP. He was deliberate that this evoke Sweep's visual language without reproducing proprietary product screens — cloning an internal file pixel-for-pixel would be an IP overstep and would read as replication rather than design judgment, which is the thing being evaluated. Two choices of his carry the concept visually: a grass/crop/fire semantic ramp that maps one-to-one onto on-track / at-risk / stalled, and an Initiatives surface placed alongside the strategy/scenario area — the natural home for what he's extending Act with.

### Sweepy flags, but never overrides a confirmed status

When we talked through the "chase and validate" half of the loop, Ronan didn't want it left entirely on the lead's own vigilance — that's the manual burden the brief is trying to remove. His decision: Sweepy can proactively flag a possible discrepancy (e.g. "on track" with no measurable movement), but only ever as a visibly separate annotation next to the confirmed status, never a change to it — a human decides what happens next. He framed it as the same "review, approve, control" discipline already applied to extraction, extended to challenge, so it stays one consistent rule rather than a new exception.

### Configure stays as chrome, not a built screen

Ronan explicitly did not want to build a settings surface. A Configure control sits in the Act view alluding to cadence and business rules being configurable, but he called it: a config screen demonstrates product completeness more than it demonstrates the trust discipline that's the actual point here, and the brief warns against over-investing past what the judgment needs to show. Alluding to the capability keeps the signal without the cost. He used the same move — allude, don't build — in a few other places, and was consistent about it being a deliberate restraint, not a gap.

---

## 2026-09-13 — Shape of the prototype

### Sustain opens straight into the Act view — one continuous surface

We'd originally planned a staged low-fidelity-to-high-fidelity transition — the owner-facing chat first, then a "wow" reveal into the Act view. Ronan cut it. His reasoning: the ESG lead never watches the DM exchange happen — they see its outcome, surfaced by Sweepy, inside the tool they already live in. So the prototype should open directly on the high-fidelity Act view, and tell the owner's check-in and reply in place, as history, inside the panel. He was clear that one hero surface carrying the whole story is a leaner, more honest demonstration than narrating it first and showing the "real" screen after — and that it matches how the thing would actually ship.

### "For You" is Sweepy's decision queue

Ronan reframed the lead's panel as a For You queue — the things Sweepy has prepared for the lead's decision, never a decision it has made itself. He was precise about the mechanics: each sign-off card plays back the full trail (the check-in, the owner's reply, the data they sent back, Sweepy's own quality-check note) with a single human Confirm that updates the initiative. He also drew a distinction I'd collapsed — a genuine blocker an owner reports should be an acknowledge-only FYI, not a sign-off, because there's nothing to approve when the work itself is stuck, and dressing it up as a sign-off would be dishonest. His governing line: the only thing that ever changes a confirmed status is a human clicking Confirm.

### Show the owner's reply and Sweepy's extraction, don't just describe them

Ronan pointed out that the most novel part of the whole concept — an owner replying in plain language, Sweepy extracting a structured status, the owner confirming before anything saves — had until then only ever been narrated in prose, never actually shown on screen. So he had the overdue threads carry the owner's real reply, followed by a "here's what Sweepy understood" card (status, blocker, next step). He deliberately varied the three outcomes rather than repeating one template: Daniel Osiel's resolves cleanly (a planning-consent delay that's cleared), while Yuki Tanaka's and Sam Okafor's stay blocked by external, third-party causes with no date yet. None of them reads as confirmed — both the card and the thread say it's Sweepy's read, not yet saved — so the "nothing is recorded without a human confirming it" principle gets demonstrated in the one place the storyboard had only described it.

### Reports is a dedicated view, generated only from confirmed data

Ronan wanted the leadership summary to be its own page — a timeline of monthly reports, most recent first — drafted by Sweepy from confirmed, sourced status only, with gaps flagged rather than smoothed over.

### Allude to refining the report by conversation — don't script it

On whether to show the report being refined in a back-and-forth, Ronan's call was to allude, not build. The report renders as a real, chart-supported document; the possibility of refining it by conversation is present only as a "write a message…" input pinned to the panel — there, but not demonstrated. He weighed a scripted multi-turn exchange and rejected it: it risks reading as a script the moment anyone scrutinises it, and live generation would be real build risk spent on something that isn't the highest-leverage moment. It's the same allude-don't-build restraint he applied to Configure — the well-written report does the work, and the input box implies the rest.

### Build the data layer once, get the supporting surfaces almost for free

This was a deliberate leverage call from Ronan, and one he was explicit about wanting on the record. Because the whole prototype derives from a single mock data layer — the fifteen initiatives, the monthly target-vs-actual figures, the six leadership reports, all as JSON that acts as the single source of truth — the supporting screens didn't need hand-building. Ronan had me spin them straight out of that same data as wireframes: the Reports timeline (six months, each with its own stats and gaps) and the per-initiative detail page with its own history. The point he made was that this cost him essentially none of his own time — the dataset already existed, and generating the extra surfaces from it was cheap for me to do — but the pages are not filler. They carry a real part of the Sustain argument that a single Act-view snapshot can't: that this is a monthly cadence where a story compounds over time. It's a conscious use of the collaboration — invest once in a real dataset, let the surfaces that extend the narrative come almost for free, and keep Ronan's own time on the decisions that actually needed his judgment.

---

## 2026-09-15 — High fidelity

### Repo presented as a curated, live file browser

For the Repo page, Ronan chose curation over a literal 1:1 mirror of the folder tree — a raw mirror would only surface working debris (`_to_delete/` folders, superseded drafts) with no reasoning value, and undercut the restraint the rest of the deliverable practises. His other requirement was that it fetch each real file live at runtime from the same repo rather than hold a baked-in copy, so the page can never quietly drift from the source. He liked that this was also a concrete, checkable technical decision to point to if an engineer asked how the page was actually built.

### Act view built at high fidelity from the real dataset

The Act view is built into the browser-chrome container, fetching the real JSON at runtime and deriving everything from data through a single render. It's implemented directly against the high-fidelity screens Ronan designed in Figma, read via the Figma MCP: the initiatives grid with each card's real scope, the target-vs-actual chart with a live hover tooltip, and the For You queue with working Submit and Acknowledge actions. Where the build and the design briefly diverged on genuinely-placeholder content, Ronan's rule was that the real seed data wins over literal Figma fidelity. He also directed that the initiative-detail and report pages stay inert stubs — the Act view is the single frame the brief's "highest-leverage moment" refers to, and that's where the fidelity belongs, not spread thin across screens the brief didn't ask for.
