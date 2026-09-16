# Visual language — the design system for this task

The visual language for this prototype is defined by the high-fidelity design files I created for this task in Figma, and the build reads directly from them via the Figma MCP tools (design tokens + a structural read of the screens) rather than from a written approximation. It's deliberately Sweep-adjacent — evoking a genuine, on-brand feel — without cloning proprietary product screens: aspirational, not a literal skin.

**Source:** the high-fidelity Act view design files for this task, read via `get_variable_defs`, `get_design_context` and `get_screenshot`.

## Colour

- **Typeface:** Maison Neue (Book / Medium / Bold). Licensed to Sweep — the site/prototype uses a close web-safe pairing (Inter), not the actual font file.
- **Primary action:** `#283fff` — a confident blue, used for primary buttons, selected state, and links. One accent colour, used deliberately.
- **Neutrals:** black `#000`, text-subdued `#6e6e6e`, disabled `#bdbdbd`, border `#e0e0e0`, surface-subdued/background `#f2f2f2`, white `#fff`.
- **Semantic status ramp — the load-bearing colour system for this brief:**
  | Meaning | 500 | 400 | 100 |
  |---|---|---|---|
  | Success / on track | `#008113` (grass) | `#1ac734` | `#ddf3d8` |
  | Caution / at risk | `#9a6500` (crop) | `#ebb900` | `#fff4d7` |
  | Danger / stalled | `#b81f00` (fire) | `#ff4d2a` | `#fce6e2` |

  A three-step grass/crop/fire ramp maps one-to-one onto **on track / at risk / stalled** — exactly the status vocabulary the prototype needs, chosen to read as Sweep-adjacent rather than invented from scratch.
- **Secondary accents** (used sparingly, not for status): glacier `#1fc0ff`, coral `#af32b8` / `#732178`.

## Type scale

Display 32/40 bold · Title 24/32 bold · Heading (strong) 18/28 bold · Body 16/24 (book / bold) · Body dense 14/20 book · Caption 12/18 (book / bold) · Button 16/24 medium (14/20 dense).

## Elevation

Restrained throughout — nothing skeuomorphic. Buttons carry a 1px hairline shadow (4% black). Popovers and modals use soft, diffuse, multi-layer shadows (large radius, very low opacity) rather than hard drop shadows. Selected states use an inset shadow, not a glow or heavy border. The interface reads calm and data-serious, not decorative.

## Component vocabulary

The component set the design defines:

- **Buttons:** primary / secondary / default, icon buttons, split buttons, toggle buttons, radio-card buttons
- **Status:** a `Tag` component, an "annotation badge"
- **Containers:** card elements + card header, a "folder card"
- **Data:** tables, a segmented linear progress indicator, stat blocks (complete/incomplete counts with trend arrows and a "vs. prev year" caption)
- **Navigation:** a left nav module with sub-nav and tabs
- **Inputs:** dropdown, checkbox, toggle
- **Feedback:** banner

The design places an **Initiatives** surface alongside the strategy/scenario area — the natural home for the initiative concept this task extends Act with.

## High-fidelity screens

The in-app Act view was designed as high-fidelity screens in the design files above, and the build is implemented directly against those Figma frames via the Figma MCP (`get_design_context` / `get_screenshot` / `get_variable_defs`) rather than from a written approximation. That keeps the built screen honest to the design — tokens, type sizes, spacing and component structure resolve against the actual file, and anything the code simplifies gets checked back against it. The initiatives grid, the target-vs-actual chart, and the For You sign-off queue all originate there.

## How to use this

- Borrow the design's component grammar — tags for status, cards for grouped content, a segmented indicator for completion, split/icon buttons for compact actions.
- One confident accent colour against mostly neutral surfaces; semantic colour (grass/crop/fire) used only for actual status meaning, never decoratively.
- Generous whitespace, restrained shadows, calm rather than busy.
- Where the concept needs a surface the main screens don't cover — the owner-facing, outside-the-app check-in — extend the same tokens, type, and shadow language rather than inventing a separate visual system for it. It should feel like the same product's hand.
- Deliberately aspirational, not a skin: the prototype should feel like it could plausibly sit inside Sweep.
