# Microsite structure — the deliverable as one artifact

How the process, reasoning and prototype come together as a single hosted site opened from one link, rather than a folder of separate files handed over cold.

## What it has to do

- Open to one link, live, inside a demo that stays well under 30 minutes.
- Make the interactive prototype the thing being looked at for most of that time.
- Keep the reasoning trail one click away without letting it compete for attention.
- Read as a considered, restrained product artifact in its own right, not a portfolio wrapper with unnecessary chrome.

## Page structure — two destinations

| Page | Weight | Content |
|---|---|---|
| **Main page** (`index.html`) | Primary | One continuous scroll: a short analysis of where the manual flow hurts, the reframe from seven steps into four stages, then — inside a mock browser chrome — the high-fidelity Act view prototype. The narrative leads straight into the live prototype rather than sitting on a separate tab, so the "single highest-leverage moment" is the thing being looked at, not one destination among equals. |
| **Repo** (`repo.html`) | Secondary | The transparency layer: a curated file browser over the real working files — North Star, this site plan, the process one-pager, the decisions log, the visual-language grounding, the data layer, and the build brief the prototype was built from — fetched live from the repo so it can't drift from the source. |

## Navigation

A slim link between the two — no sidebar taking permanent width, no logo lockup, no hero "welcome to my technical exercise" framing. The nav all but disappears once someone's looking at the prototype.

## Visual direction

Governed by `visual-language.md`: neutral surfaces, one confident accent colour, an Inter / Maison-Neue-adjacent type scale (Maison Neue itself is a licensed Sweep asset, not shipped here), restrained shadows, and semantic grass/crop/fire used only where it actually means on-track / at-risk / stalled. The Act view is grounded directly in the high-fidelity screens I designed in Figma, read into the build via the Figma MCP — aspirational and Sweep-adjacent, deliberately not a literal Sweep skin.

## Build approach

Plain HTML/CSS — no client framework, no build step that could trip up in the interview room. JS is limited to nav state, the prototype's own interactivity, and fetching the real `data/` and repo files at runtime. Because every screen derives from that one `data/` layer, the supporting surfaces — the reports timeline, the per-initiative history — could be generated straight from the same data as wireframes at almost no extra cost, extending the Sustain narrative beyond the single hero frame without extra hand-building. The `.md` files in each folder's `md/` subfolder stay the single source of truth; the PDF pack (`tools/pdf/`) is generated from them as an offline fallback, never the other way round. Hosted on GitHub Pages from this repo.
