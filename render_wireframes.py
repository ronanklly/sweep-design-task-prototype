#!/usr/bin/env python3
"""
Renders design-task/prototype/storyboard-wireframes.html from the data in
design-task/prototype/data/*.json — a build-time step, not a runtime one.
The shipped file is plain static HTML/CSS (+ native <details>/radio-tab
tricks and CSS-only hover tooltips, no JS needed) so it still opens with a
double-click, offline, no server. Re-run this any time the data or the
copy changes.

Run: python3 render_wireframes.py
"""
import json
from pathlib import Path

HERE = Path(__file__).parent
# TODO(Ronan): point this at the real repo once it is pushed (decisions-log.md
# still has repo visibility as an open question) -- the dock's repo icon links here.
REPO_URL = "https://github.com/REPLACE-ME/sweep-design-task"

# Presentation header (subtle top bar) -- update PRESENTATION_DATE/TITLE if the
# session moves or the framing changes.
PRESENTER_NAME = "Ronan Kelly"
PRESENTATION_DATE = "Thu 17 Sep"
PRESENTATION_TITLE = "From Spreadsheets to Sustained Accountability"
DATA = HERE / "data"
OUT_FILE = HERE / "storyboard-wireframes.html"

initiatives_doc = json.loads((DATA / "initiatives.json").read_text())
initiatives = initiatives_doc["initiatives"]
LEAD = initiatives_doc["lead"]
trajectory = json.loads((DATA / "trajectory.json").read_text())
for_you_items = json.loads((DATA / "for-you-items.json").read_text())
reports_doc = json.loads((DATA / "reports.json").read_text())
reports = reports_doc["reports"]
activity_rows = json.loads((DATA / "activity-data.json").read_text())["rows"]
activity_log = json.loads((DATA / "activity-log.json").read_text())
goals = json.loads((DATA / "goals.json").read_text())

STATUS_LABEL = {"up_to_date": "Up to date", "pending_review": "Pending review", "awaiting_data": "Awaiting data"}
STATUS_RAMP = {"up_to_date": "grass", "pending_review": "crop", "awaiting_data": "fire"}
GOAL_STATUS_RAMP = {"on_track": "grass", "at_risk": "crop", "stalled": "fire"}
GOAL_STATUS_LABEL = {"on_track": "On track", "at_risk": "At risk", "stalled": "Stalled"}
# All-initiatives grid sort: awaiting data first (nothing back yet, needs attention), then
# pending review (in the lead's For You queue), then up to date.
DATA_STATUS_SORT = {"awaiting_data": 0, "pending_review": 1, "up_to_date": 2}

SCOPE_ICON = {
    "Scope 1": ("flame", "#b81f00"),
    "Scope 2": ("bolt", "#283fff"),
    "Scope 3": ("network", "#6e6e6e"),
}

ICONS = {
    "bolt": '<path d="M13 2 4 14h6l-1 8 9-12h-6l1-8Z"/>',
    "flame": '<path d="M12 2c1 3-1 4-2 6-1.5 2.5 0 4 1 4.5-2-1-3-3-2-5-2 2-3 5-1 8 1.3 1.7 3.6 2.5 6 2 2.6-.6 4-2.8 4-5.3 0-3-2-5-3-6.5.3 1.7-.4 2.6-1 3C15 6 13 4 12 2Z"/>',
    "network": '<circle cx="6" cy="6" r="2.2"/><circle cx="18" cy="6" r="2.2"/><circle cx="12" cy="18" r="2.2"/><path d="M7.7 7.2 10.5 16M16.3 7.2 13.5 16M8.2 6h7.6" stroke="currentColor" stroke-width="1.4" fill="none"/>',
}


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


def pct_html(pct):
    sign = "+" if pct > 0 else ""
    cls = "delta-bad" if pct > 0 else "delta-good"
    return f'<span class="{cls}">{sign}{pct:g}%</span>'


def initials(name):
    parts = name.split()
    return (parts[0][0] + parts[-1][0]).upper()


def fmt(n):
    return f"{n:,}" if n is not None else "—"


def fmt_delta(n):
    if n is None:
        return "—"
    return f"+{n:,}" if n > 0 else f"{n:,}"


# ---------------------------------------------------------------------------
# Effort / emotional-journey helpers (beat 2 + the reframe, beat 3)
# ---------------------------------------------------------------------------

EMOTION_SCALE = [
    ("exasperated", "😤", "Exasperated"),
    ("drained", "😩", "Drained"),
    ("frustrated", "😕", "Frustrated"),
    ("neutral", "😐", "Neutral"),
    ("reassured", "🙂", "Reassured"),
    ("delighted", "😊", "Delighted"),
]
EMOTION_RANK = {key: i for i, (key, _, _) in enumerate(EMOTION_SCALE)}


def emotion_parts(key):
    return EMOTION_SCALE[EMOTION_RANK[key]][1:]


def emotion_chip(key):
    emoji, label = emotion_parts(key)
    return f'<span class="emo-chip"><span class="emo-emoji">{emoji}</span>{esc(label)}</span>'


def effort_dots(score, max_score=5):
    dots = "".join(
        f'<span class="ef-dot{" on" if i < score else ""}"></span>' for i in range(max_score)
    )
    return f'<span class="effort" title="Effort — assumed and relative, {score}/{max_score}">{dots}</span>'


def stage_shift_html(old_effort, old_emotion, new_effort, new_emotion):
    return (
        '<div class="stage-shift">'
        f'<span class="shift-old">{emotion_chip(old_emotion)} · {effort_dots(old_effort)}</span>'
        '<span class="shift-arrow" aria-hidden="true">→</span>'
        f'<span class="shift-new">{emotion_chip(new_emotion)} · {effort_dots(new_effort)}</span>'
        '</div>'
    )


def emotion_journey_svg(points, w=900, h=170):
    """points: list of (step_num, emotion_key, effort). Plots the emotional
    read at each step (y position on the exasperation-to-delight scale,
    labelled by emoji) with dot size carrying the effort score — one
    picture for both dimensions, across every step."""
    n = len(points)
    PAD_L, PAD_R, PAD_T, PAD_B = 26, 26, 32, 30
    top_rank = len(EMOTION_SCALE) - 1

    def x_at(i):
        return PAD_L + (w - PAD_L - PAD_R) * i / (n - 1)

    def y_at(rank):
        return PAD_T + (h - PAD_T - PAD_B) * (1 - rank / top_rank)

    coords = []
    for i, (num, key, effort) in enumerate(points):
        coords.append((x_at(i), y_at(EMOTION_RANK[key]), key, effort, num))

    path_d = "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y, *_ in coords)
    boundary_x = (coords[3][0] + coords[4][0]) / 2

    dots = "".join(
        f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{4 + effort * 1.5:.1f}" class="emo-dot"/>'
        for x, y, key, effort, num in coords
    )
    emojis = "".join(
        f'<text x="{x:.1f}" y="{y - 10 - effort * 1.5:.1f}" text-anchor="middle" class="emo-journey-emoji">{emotion_parts(key)[0]}</text>'
        for x, y, key, effort, num in coords
    )
    nums = "".join(
        f'<text x="{x:.1f}" y="{h - 6}" text-anchor="middle" class="axis-label">{num}</text>'
        for x, y, key, effort, num in coords
    )

    return f'''
    <svg viewBox="0 0 {w} {h}" class="chart emo-journey" role="img" aria-label="Effort and emotional read across the seven steps">
      <text x="{PAD_L}" y="16" class="emo-axis-top">😊 Delight</text>
      <text x="{PAD_L}" y="{h - PAD_B + 24}" class="emo-axis-bottom">😤 Exasperation</text>
      <line x1="{boundary_x:.1f}" y1="{PAD_T - 10}" x2="{boundary_x:.1f}" y2="{h - PAD_B + 10}" class="emo-boundary"/>
      <path d="{path_d}" class="emo-journey-line"/>
      {dots}
      {emojis}
      {nums}
    </svg>
    <p class="caption muted" style="margin-top:6px">Dot size = assumed relative effort · the dashed line marks where the cycle starts repeating, every month, forever.</p>'''



# ---------------------------------------------------------------------------
# Reusable dual-line chart, CSS-only hover tooltips (no JS)
# ---------------------------------------------------------------------------

_chart_seq = [0]


def dual_line_chart(monthly, unit="tCO2e", w=900, h=260, hero_tag=None):
    """monthly: list of {month,label,target,actual,delta}. actual is None
    for future months. Renders target (dashed, all 12) + actual (solid,
    through the last non-null month) + a shaded delta band + a per-month
    CSS-hover tooltip (target / actual / delta)."""
    _chart_seq[0] += 1
    cid = f"c{_chart_seq[0]}"
    PAD_L, PAD_R, PAD_T, PAD_B = 44, 20, hero_tag and 56 or 20, 30
    n = len(monthly)

    all_targets = [m["target"] for m in monthly]
    all_actuals = [m["actual"] for m in monthly if m["actual"] is not None]
    vmin = min(all_targets + all_actuals) * 0.93
    vmax = max(all_targets + all_actuals) * 1.06

    def x_at(idx):
        return PAD_L + (w - PAD_L - PAD_R) * idx / (n - 1)

    def y_at(v):
        return PAD_T + (h - PAD_T - PAD_B) * (1 - (v - vmin) / (vmax - vmin))

    target_pts = [(x_at(i), y_at(m["target"])) for i, m in enumerate(monthly)]
    actual_idx = [i for i, m in enumerate(monthly) if m["actual"] is not None]
    actual_pts = [(x_at(i), y_at(monthly[i]["actual"])) for i in actual_idx]

    def path(pts):
        return "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in pts)

    band = ""
    if actual_pts:
        top = [(x_at(i), y_at(monthly[i]["actual"])) for i in actual_idx]
        bot = list(reversed([(x_at(i), y_at(monthly[i]["target"])) for i in actual_idx]))
        band_pts = top + bot
        band = f'<path d="{path(band_pts)} Z" class="chart-band"/>'

    axis_labels = "".join(
        f'<text x="{x_at(i):.1f}" y="{h-8}" class="axis-label" text-anchor="middle">{m["label"]}</text>'
        for i, m in enumerate(monthly)
    )

    barw = (w - PAD_L - PAD_R) / n

    tag = ""
    if hero_tag:
        last = monthly[actual_idx[-1]]
        gap_pct = round(last["delta"] / last["target"] * 100, 1)
        tag = f'''
        <g class="chart-hero-tag">
          <text x="{PAD_L}" y="20" class="chart-hero-value">{fmt(last["actual"])} <tspan class="chart-hero-unit">{esc(unit)}</tspan></text>
          <text x="{PAD_L}" y="38" class="chart-hero-sub">{esc(hero_tag)} · <tspan class="delta-bad">+{gap_pct}% vs target</tspan></text>
        </g>'''

    points = []
    for i, m in enumerate(monthly):
        x = x_at(i)
        yt = y_at(m["target"])
        has_actual = m["actual"] is not None
        ya = y_at(m["actual"]) if has_actual else None

        tt_lines = f'<div class="tt-month">{esc(m["label"])}</div>'
        tt_lines += f'<div class="tt-row"><span>Target</span><b>{fmt(m["target"])}</b></div>'
        if has_actual:
            tt_lines += f'<div class="tt-row"><span>Actual</span><b>{fmt(m["actual"])}</b></div>'
            delta_cls = "delta-bad" if m["delta"] > 0 else "delta-good"
            tt_lines += f'<div class="tt-row"><span>Delta</span><b class="{delta_cls}">{fmt_delta(m["delta"])}</b></div>'
        else:
            tt_lines += '<div class="tt-row"><span class="muted">No data yet</span></div>'

        tt_w, tt_h = 128, (70 if has_actual else 50)
        tx = min(max(x - tt_w / 2, PAD_L), w - PAD_R - tt_w)
        ty = min(yt, ya) - tt_h - 14 if has_actual else yt - tt_h - 14
        ty = max(ty, 4)

        dots = f'<circle cx="{x:.1f}" cy="{yt:.1f}" r="3.2" class="dot dot--target"/>'
        if has_actual:
            dots += f'<circle cx="{x:.1f}" cy="{ya:.1f}" r="3.6" class="dot dot--actual"/>'

        points.append(f'''
        <g class="pt">
          <rect class="hit" x="{x-barw/2:.1f}" y="0" width="{barw:.1f}" height="{h}"/>
          <line class="guide" x1="{x:.1f}" y1="{PAD_T}" x2="{x:.1f}" y2="{h-PAD_B}"/>
          {dots}
          <foreignObject class="tooltip" x="{tx:.1f}" y="{ty:.1f}" width="{tt_w}" height="{tt_h}">
            <div xmlns="http://www.w3.org/1999/xhtml" class="tt-box">{tt_lines}</div>
          </foreignObject>
        </g>''')

    return f'''
    <svg viewBox="0 0 {w} {h}" class="chart" id="{cid}" role="img" aria-label="Target versus actual, month by month">
      <line x1="{PAD_L}" y1="{PAD_T}" x2="{PAD_L}" y2="{h-PAD_B}" class="axis-line"/>
      <line x1="{PAD_L}" y1="{h-PAD_B}" x2="{w-PAD_R}" y2="{h-PAD_B}" class="axis-line"/>
      {tag}
      {band}
      <path d="{path(target_pts)}" class="line line--target"/>
      <path d="{path(actual_pts)}" class="line line--actual"/>
      {axis_labels}
      {''.join(points)}
    </svg>
    <div class="chart-legend">
      <span class="legend-item"><span class="legend-swatch legend-swatch--target"></span>Target</span>
      <span class="legend-item"><span class="legend-swatch legend-swatch--actual"></span>Actual</span>
      <span class="legend-item"><span class="legend-swatch legend-swatch--band"></span>Delta</span>
      <span class="legend-hint muted">Hover a month for the numbers</span>
    </div>'''


def tile_html(i):
    icon_key, _ = SCOPE_ICON[i["scope"]]
    ramp = STATUS_RAMP[i["dataStatus"]]
    label = STATUS_LABEL[i["dataStatus"]]
    href = f'#init-{i["id"]}' if i["id"] == "offgrid-solar" else "#state-f"
    blocked_html = ""
    if i.get("blocked"):
        blocked_html = f'''<span class="blocker-flag">
              <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 9v4M12 17h.01M10.3 3.86 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.86a2 2 0 0 0-3.4 0Z"/></svg>
              Blocked — {esc(i["blockerShort"])}</span>'''
    return f'''
      <a class="tile" href="{href}">
        <div class="tile-art tile-art--{icon_key}">
          <svg viewBox="0 0 24 24" width="22" height="22" fill="currentColor">{ICONS[icon_key]}</svg>
          <span class="tile-scope">{esc(i["scope"].replace("Scope ", "S"))}</span>
        </div>
        <div class="tile-body">
          <div class="tile-top">
            <h4>{esc(i["shortName"])}</h4>
            {pct_html(i["percentVsTarget"])}
          </div>
          <p class="tile-owner">{esc(i["owner"]["name"])} · {esc(i["owner"]["department"])}</p>
          <span class="pill pill--{ramp}">{label}</span>
          {blocked_html}
        </div>
      </a>'''


def for_you_card_html(item, init):
    owner_first = item["owner"]["name"].split()[0]
    msgs = "".join(
        f'''<div class="msg{' msg--owner' if m["from_"] != "Sweepy" else ''}">
              <div class="msg-meta"><strong>{esc(m["from_"])}</strong> via {esc(m["sentVia"])} · {m["timestamp"][:10]}</div>
              <p>{esc(m["text"])}</p>
            </div>'''
        for m in item["messages"]
    )

    if item["cardType"] == "signoff":
        summary_pill = f'<span class="pill pill--{STATUS_RAMP["pending_review"]}">{STATUS_LABEL["pending_review"]}</span>'
        sub = item["dataSubmission"]
        attachment_html = f'''
          <div class="data-attachment">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 3v5h5"/><path d="M6 3h8l5 5v13H6z"/><path d="M9 13h6M9 17h6"/></svg>
            <div>
              <strong>{esc(sub["filename"])}</strong><span class="muted caption"> · {esc(sub["type"].capitalize())}</span>
              <p class="caption muted" style="margin:2px 0 0">{esc(sub["note"])}</p>
            </div>
          </div>'''
        check_html = f'''
          <div class="ok-note">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 6 9 17l-5-5"/></svg>
            <p><b>Sweepy's checked it</b> — {esc(item["qualityCheck"]["text"])} Take a look yourself and sign off when you're ready.</p>
          </div>'''
        nuance = item.get("nuance")
        nuance_html = ""
        if nuance:
            nuance_html = f'''
          <div class="nuance-note">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M12 8v5M12 16h.01"/></svg>
            <p><b>Worth knowing:</b> {esc(nuance["text"])}</p>
          </div>'''
        body_extra = attachment_html + check_html + nuance_html
        footer = '<span class="muted caption">Ready for your sign-off.</span>'
        action_btn = '<button class="btn btn--primary btn--sm">Confirm</button>'
    else:
        summary_pill = '<span class="pill pill--fire">Blocked</span>'
        body_extra = f'''
          <div class="flag-note flag-note--sm">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 9v4M12 17h.01M10.3 3.86 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.86a2 2 0 0 0-3.4 0Z"/></svg>
            <div>
              <p><b>{esc(owner_first)} says this is blocked</b> — there's nothing to review yet.</p>
              <p class="caption muted" style="margin-top:4px">{esc(item["blockerSummary"])}</p>
            </div>
          </div>'''
        footer = '<span class="muted caption">No data to sign off — just so you know.</span>'
        action_btn = '<button class="btn btn--sm">Acknowledge</button>'

    return f'''
      <details class="foryou-row">
        <summary>
          <span class="avatar">{esc(initials(item["owner"]["name"]))}</span>
          <span class="foryou-row-main">
            <strong>{esc(item["owner"]["name"])}</strong>
            <span class="muted"> · {esc(init["shortName"])}</span>
          </span>
          {summary_pill}
        </summary>
        <div class="thread">
          {msgs}
          {body_extra}
          <div class="thread-footer">
            {footer}
            <span style="margin-left:auto;display:flex;gap:8px">
              {action_btn}
              <button class="btn btn--ghost" disabled title="Not available in this preview">Take control</button>
            </span>
          </div>
        </div>
      </details>'''


def draft_source_lines():
    return [
        "site power draw way up at the busier towers again this qtr...",
        "priya flagged the cooling retrofit budget, need renewable PPA numbers",
        "fleet — still 40% diesel vans, leases turn over through 2027",
        "packaging + device takeback keep coming up in every interview",
    ]


def stat(label, value):
    return f'<div class="stat"><span class="stat-value">{value}</span><span class="stat-label">{esc(label)}</span></div>'


def beat_nav(prev_id, prev_label, next_id, next_label, dot_index, dot_total=3):
    dots = "".join(f'<span class="bn-dot{" bn-dot--on" if i == dot_index else ""}"></span>' for i in range(dot_total))
    prev = f'<a href="#{prev_id}" class="bn-btn">← {esc(prev_label)}</a>' if prev_id else '<span class="bn-btn bn-btn--spacer"></span>'
    nxt = f'<a href="#{next_id}" class="bn-btn bn-btn--primary">{esc(next_label)} →</a>' if next_id else '<span class="bn-btn bn-btn--spacer"></span>'
    return f'<div class="beat-nav">{prev}<span class="bn-dots">{dots}</span>{nxt}</div>'


# ---------------------------------------------------------------------------
# Sweepy tab content — For You / Activity / Goals / Chat
# ---------------------------------------------------------------------------

items_by_init = {t["initiativeId"]: t for t in for_you_items}
signoff_inits = [i for i in initiatives if i["dataStatus"] == "pending_review"]
blocked_inits = [i for i in initiatives if i.get("blocked")]
for_you_order = signoff_inits + blocked_inits
for_you_cards = "".join(for_you_card_html(items_by_init[i["id"]], i) for i in for_you_order)
for_you_msg = (
    f"Sweepy's prepared {len(for_you_order)} thing{'s' if len(for_you_order) != 1 else ''} for you this month — "
    f"{len(signoff_inits)} ready to sign off, {len(blocked_inits)} you should just know about."
)

activity_feed = "".join(f'''
      <div class="feed-row">
        <span class="feed-dot"></span>
        <div>
          <p class="feed-text">{esc(a["text"])}</p>
          <span class="feed-ts caption muted">{a["ts"].replace("T", " · ")}</span>
        </div>
      </div>''' for a in activity_log)

goals_list = "".join(f'''
      <div class="goal-row">
        <span class="goal-mark">S</span>
        <p>{esc(g)}</p>
      </div>''' for g in goals)

chat_thread = [
    (LEAD["name"], "Can you double-check the off-grid diesel numbers before I sign off the report? Daniel's status still says on track."),
    ("Sweepy", "Already flagged it on his initiative page — diesel volumes haven't moved in two months despite the confirmed status. I haven't changed what he logged, just surfaced the discrepancy."),
    (LEAD["name"], "Good, leave it as a flag for now. I'll follow up with him directly this week."),
    ("Sweepy", "Noted — I'll hold off on a third automated nudge and let you take it from here."),
]
chat_html = "".join(f'''
      <div class="chat-msg {'chat-msg--me' if who != 'Sweepy' else ''}">
        <span class="avatar avatar--chat">{esc(initials(who) if who != 'Sweepy' else 'S')}</span>
        <div class="chat-bubble"><p>{esc(text)}</p></div>
      </div>''' for who, text in chat_thread)


# ---------------------------------------------------------------------------
# Reports page (State G) — timeline / version history, radio-driven
# ---------------------------------------------------------------------------

def trajectory_through(month):
    """A copy of the trajectory truncated to what would actually have been
    known as of a given report month -- so each report's chart shows only
    the line as it stood at the time, and flicking through the reports
    shows it grow, month by month, rather than always showing the full
    current-day picture."""
    return [
        dict(m, actual=(m["actual"] if m["month"] <= month else None),
                delta=(m["delta"] if m["month"] <= month else None))
        for m in trajectory["monthly"]
    ]


def report_panel(r):
    banner = ""
    if r["needsReview"]:
        gen_date = r["generatedAt"][:10]
        banner = f'''
        <div class="review-banner">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M12 7v6l4 2"/></svg>
          <span>Generated by Sweepy on {gen_date} — please review and finalise.</span>
          <button class="btn btn--primary btn--sm" style="margin-left:auto">Review &amp; finalise</button>
        </div>'''
    else:
        badge = f'<span class="pill pill--grass" style="margin-top:0">Reviewed by {esc(r["reviewedBy"])} · {r["reviewedAt"]}</span>'
        banner = f'<div class="reviewed-row">{badge}</div>'

    stats = (stat("On track", r["stats"]["onTrack"]) + stat("At risk", r["stats"]["atRisk"]) +
              stat("Stalled", r["stats"]["stalled"]) + stat("Awaiting data", r["stats"]["dataOverdue"]))

    extra = ""
    if "highlights" in r:
        hi = "".join(f'<li><strong>{esc(h["shortName"])}</strong> <span class="muted">— {esc(h["note"])}</span></li>' for h in r["highlights"])
        ga = "".join(f'<li><strong>{esc(g["shortName"])}</strong> <span class="muted">— {esc(g["note"])}</span></li>' for g in r["gaps"])
        extra = f'''
        <div class="report-grid">
          <div class="report-col">
            <h4 class="text-heading">Highlights</h4>
            <ul class="report-list report-list--good">{hi}</ul>
          </div>
          <div class="report-col">
            <h4 class="text-heading">Gaps &amp; flags</h4>
            <ul class="report-list report-list--bad">{ga}</ul>
          </div>
        </div>'''

    return f'''
    <div class="report-panel rp-{r["id"]}">
      {banner}
      <div class="report-head-row">
        <div>
          <p class="eyebrow" style="margin-top:22px">{esc(r["label"])} · generated by {esc(r["generatedBy"])}</p>
          <h2 class="text-title" style="margin-top:6px">{esc(r["headline"])}</h2>
        </div>
        <div class="report-actions">
          <button class="btn btn--sm" type="button" title="Not wired up in this preview">Download PDF</button>
          <button class="btn btn--primary btn--sm" type="button" title="Not wired up in this preview">Send to leadership</button>
        </div>
      </div>
      <p class="text-body muted" style="margin-top:8px;max-width:640px">{esc(r["summary"])}</p>
      <div class="report-chart-card">
        {dual_line_chart(trajectory_through(r["month"]), unit=trajectory["unit"], hero_tag=f'All initiatives, {r["label"]}')}
      </div>
      <div class="stat-row" style="margin-top:20px">{stats}</div>
      {extra}
    </div>'''


report_radios = "".join(
    f'<input type="radio" name="report" id="rep-{r["id"]}"{" checked" if i == 0 else ""}>'
    for i, r in enumerate(reports)
)
report_timeline = "".join(f'''
      <label for="rep-{r["id"]}" class="timeline-item">
        <span class="timeline-dot"></span>
        <span class="timeline-body">
          <strong>{esc(r["label"])}</strong>
          <span class="caption muted">{"Needs review" if r["needsReview"] else f'Reviewed {r["reviewedAt"]}'}</span>
        </span>
      </label>''' for r in reports)
report_panels = "".join(report_panel(r) for r in reports)
report_visibility_css = "\n".join(
    f'#rep-{r["id"]}:checked ~ .report-body .rp-{r["id"]}{{display:block}}' for r in reports
)


# ---------------------------------------------------------------------------
# Initiative detail page (State F) — offgrid-solar
# ---------------------------------------------------------------------------

init_page = next(i for i in initiatives if i["id"] == "offgrid-solar")
init_rows_all = [r for r in activity_rows if r["initiativeId"] == "offgrid-solar"]
latest_period = max(r["reportingPeriod"] for r in init_rows_all)
init_rows = sorted([r for r in init_rows_all if r["reportingPeriod"] == latest_period], key=lambda r: r["siteId"])

table_rows = "".join(f'''
      <tr>
        <td>{esc(r["siteId"])}</td>
        <td>{esc(r["activityType"])}</td>
        <td>{r["activityData"]:,.0f} {esc(r["activityUnit"])}</td>
        <td>{r["emissionFactor"]} {esc(r["emissionFactorUnit"])}</td>
        <td>{r["emissionsTco2e"]:,.1f}</td>
        <td><span class="pill pill--{"grass" if r["dataQuality"]=="Verified" else "crop"}" style="margin-top:0">{esc(r["dataQuality"])}</span></td>
      </tr>''' for r in init_rows)


# ---------------------------------------------------------------------------
# Preamble content (beats 1–7) — unchanged structure from the previous pass
# ---------------------------------------------------------------------------

step_rows = [
    # short label, full description, assumed relative effort (1-5), emotional read (EMOTION_SCALE key)
    ("Draft actions from interviews", "Lead drafts candidate actions in a spreadsheet from stakeholder interviews", 3, "neutral"),
    ("Circulate for review", "Lead emails the spreadsheet to 5–6 stakeholders for review and comment", 2, "frustrated"),
    ("Consolidate & finalise list", "Lead consolidates feedback and finalises ~15 actions", 3, "frustrated"),
    ("Assign owners", "Lead assigns owners by emailing each person individually", 2, "neutral"),
    ("Owners update monthly", "Each owner updates progress monthly on a central spreadsheet", 2, "drained"),
    ("Chase silent owners", "Lead manually chases the 4–5 owners who haven't reported", 5, "exasperated"),
    ("Compile leadership summary", "Lead compiles a summary for leadership review, often from memory", 4, "drained"),
]


def step_row_html(n, s, f, effort, emotion):
    return (
        f'<div class="step-row"><span class="num">{n}</span><div class="step-main"><div>{esc(s)}</div>'
        f'<div class="full">{esc(f)}</div></div>'
        f'<div class="step-meta">{effort_dots(effort)}{emotion_chip(emotion)}</div></div>'
    )


episodic_rows = "".join(
    step_row_html(n, s, f, effort, emotion)
    for n, (s, f, effort, emotion) in enumerate(step_rows[:4], 1)
)
recurring_rows = "".join(
    step_row_html(n, s, f, effort, emotion)
    for n, (s, f, effort, emotion) in enumerate(step_rows[4:], 5)
)
emotion_journey = emotion_journey_svg(
    [(n, emotion, effort) for n, (_, _, effort, emotion) in enumerate(step_rows, 1)]
)

initiatives_for_grid = sorted(initiatives, key=lambda i: DATA_STATUS_SORT[i["dataStatus"]])
tiles = "".join(tile_html(i) for i in initiatives_for_grid)

draft_notes = "".join('<div class="notes-line"></div>' for _ in draft_source_lines())
draft_checklist = "".join(
    f'<div class="check-item"><span class="box {"done" if idx < 2 else ""}"></span>{esc(n)}</div>'
    for idx, n in enumerate([i["shortName"] for i in initiatives[:4]])
)

align_rows = "".join(f'''
  <div class="stakeholder-row">
    <span class="avatar-sm">{esc(initials(n))}</span> {esc(n)}
    <span style="margin-left:auto">{tag}</span>
  </div>''' for n, tag in [
    ("Priya Nair", '<span class="pill pill--grass" style="margin-top:0">Responded</span>'),
    ("Marcus Webb", '<span class="pill pill--grass" style="margin-top:0">Responded</span>'),
    ("Ben Fitzgerald", '<span class="pill pill--crop" style="margin-top:0">Flagged</span>'),
    ("Nadia Petrov", '<span class="pill pill--crop" style="margin-top:0">Awaiting</span>'),
])

assign_owner = next(i for i in initiatives if i["id"] == "offgrid-solar")
sustain_owner = next((i for i in initiatives if i["dataStatus"] == "pending_review"), initiatives[0])

latest_report = reports[0]


# ---------------------------------------------------------------------------
# Beat 3 — the reframe, merged with the old beats 4-6 and 7: all four stages,
# how the seven steps map onto them, what Sweepy actually accelerates, and
# the effort/emotion shift each one buys.
# ---------------------------------------------------------------------------

draft_frag_html = (
    f'<div class="frag draft-frag"><div class="notes-panel">{draft_notes}</div>'
    f'<div class="checklist">{draft_checklist}</div></div>'
)
align_frag_html = (
    f'<div class="frag">{align_rows}'
    f'<button class="btn btn--primary btn--sm" style="margin-top:8px;width:100%">Finalise ~15 actions</button></div>'
)
assign_frag_html = f'''<div class="frag"><div class="assign-card">
    <div class="text-dense" style="font-weight:700">{esc(assign_owner["name"])}</div>
    <div class="suggest-chip">Suggested — {esc(assign_owner["owner"]["name"])}, owns 2 similar sites</div>
    <button class="btn btn--sm" style="margin-top:10px;width:100%">Edit &amp; send</button>
  </div></div>'''
sustain_frag_html = f'''<div class="frag sustain-frag">
    <div class="checkin-row"><span class="avatar-sm">{esc(initials(sustain_owner["owner"]["name"]))}</span> {esc(sustain_owner["owner"]["name"])}
      <span class="pill pill--crop" style="margin-top:0;margin-left:auto">Pending review</span></div>
    <div class="checkin-bubble">
      <p class="caption muted">Sweepy, via Teams · 3 days ago</p>
      <p>"Quick check on '{esc(sustain_owner["shortName"])}' — how's this month looking?"</p>
    </div>
    <div class="checkin-bubble checkin-bubble--reply">
      <p class="caption muted">{esc(sustain_owner["owner"]["name"].split()[0])} replied, with this month's data attached</p>
      <p>"Sorted now — attaching this month's site numbers."</p>
    </div>
    <div class="sweepy-extract">
      <span class="suggest-chip">Sweepy checked it — looks consistent, ready for your sign-off</span>
      <button class="btn btn--primary btn--sm" style="margin-top:8px;width:100%">Confirm</button>
    </div>
  </div>'''

REFRAME_STAGES = [
    dict(
        key="draft", title="Draft", steps=[1],
        one_liner="Turns a lead's raw interview notes into a structured first draft, ready to edit, not send.",
        paragraph="Sweepy turns the lead's raw interview notes into a structured first-draft action list; the lead edits before it goes anywhere.",
        frag_html=draft_frag_html,
        accelerants=[
            "Turns unstructured interview notes into a candidate action list in minutes, not a spreadsheet built by hand.",
            "Suggests a scope and GHG category per action, drawn from the notes' own language.",
            "Never publishes the draft itself — it's a starting point the lead edits before anyone else sees it.",
        ],
        old_effort=3, old_emotion="neutral", new_effort=2, new_emotion="reassured",
    ),
    dict(
        key="align", title="Align", steps=[2, 3],
        one_liner="Replaces the emailed spreadsheet with a structured, Survey-style ask — and consolidates, but never decides.",
        paragraph="A structured, Survey-style request replaces the emailed spreadsheet; Sweepy consolidates responses and flags disagreement; the lead makes the final call.",
        frag_html=align_frag_html,
        accelerants=[
            "Sends one structured request per stakeholder, instead of a spreadsheet and a round of reply-all email.",
            "Consolidates every response into a single list automatically, instead of the lead copying from five inboxes.",
            "Flags where stakeholders actually disagree, rather than quietly averaging or picking one for them.",
        ],
        old_effort=3, old_emotion="frustrated", new_effort=2, new_emotion="reassured",
    ),
    dict(
        key="assign", title="Assign", steps=[4],
        one_liner="Suggests the best-placed owner for each initiative from who already owns similar work — the lead can always override.",
        paragraph="Sweepy suggests the best-placed owner per initiative and drafts the ask; the lead can override before it sends.",
        frag_html=assign_frag_html,
        accelerants=[
            "Suggests an owner from existing site and role data, not a cold guess.",
            "Drafts the individual ask to each owner, instead of the lead writing fifteen emails by hand.",
            "Leaves the send decision with the lead — a suggestion, never an assignment.",
        ],
        old_effort=2, old_emotion="neutral", new_effort=1, new_emotion="delighted",
    ),
    dict(
        key="sustain", title="Sustain", steps=[5, 6, 7],
        one_liner="Chases, interprets and drafts every month — but never saves a status the owner hasn't confirmed.",
        paragraph="A plain-language check-in goes out wherever the owner already works — no login, no new tool. Sweepy reads the reply, proposes a structured status, and shows the owner exactly what it understood before anything is saved.",
        frag_html=sustain_frag_html,
        accelerants=[
            "Sends the monthly check-in and chases silence automatically, so the lead never has to.",
            "Turns a free-text reply into a structured status, blocker and next step.",
            "Flags a likely discrepancy (e.g. \u201Con track\u201D with no measurable movement) — but never changes a confirmed status itself.",
            "Drafts the leadership summary from confirmed, sourced data only, with anything uncertain left flagged, not smoothed over.",
        ],
        old_effort=5, old_emotion="exasperated", new_effort=2, new_emotion="delighted",
        cta=True,
    ),
]


def accelerants_html(items):
    lis = "".join(f"<li>{i}</li>" for i in items)
    return f'<p class="accel-label caption muted" style="margin-top:16px">Sweepy accelerates this by</p><ul class="accelerate-list">{lis}</ul>'


def steps_label_for(steps):
    if len(steps) == 1:
        return f"from step {steps[0]}"
    return f"from steps {steps[0]}\u2013{steps[-1]}"


def stage_card_html(stage):
    primary = stage.get("cta", False)
    card_cls = "hero-card hero-card--sustain" if primary else "hero-card"
    card_style = ' style="border-color:var(--primary);background:var(--primary-tint)"' if primary else ""
    title_style = ' style="color:var(--primary)"' if primary else ""
    cta_html = ""
    if primary:
        cta_html = '''<a class="prototype-cta" href="#prototype-reveal">
          <span class="prototype-cta-badge">Prototyped at high fidelity</span>
          <strong>Open the clickable prototype &rarr;</strong>
          <span class="caption" style="opacity:.85;display:block;margin-top:2px">The real, interactive Act view — see it below.</span>
        </a>'''
    return f'''
      <div class="{card_cls}"{card_style}>
        <span class="tag">Wireframe</span>
        <h4{title_style}>{esc(stage["title"])}</h4>
        <p class="maps-from muted caption">{steps_label_for(stage["steps"])}{" — prototyped" if primary else ""}</p>
        <p class="stage-oneliner">{esc(stage["one_liner"])}</p>
        {stage["frag_html"]}
        <p class="frag-caption caption">{stage["paragraph"]}</p>
        {accelerants_html(stage["accelerants"])}
        {stage_shift_html(stage["old_effort"], stage["old_emotion"], stage["new_effort"], stage["new_emotion"])}
        {cta_html}
      </div>'''


stage_cards = "".join(stage_card_html(s) for s in REFRAME_STAGES)

STEP_SHORT = [s[0] for s in step_rows]
bridge_chips = "".join(
    f'<div class="bridge-chip"><span class="bridge-chip-num">{n}</span><span class="bridge-chip-label">{esc(STEP_SHORT[n-1])}</span></div>'
    for n in range(1, 8)
)
bridge_stage_labels = "".join(
    f'<div class="bridge-stage{" bridge-stage--primary" if s.get("cta") else ""}" style="grid-column:{min(s["steps"])} / span {len(s["steps"])}">{esc(s["title"])}</div>'
    for s in REFRAME_STAGES
)


CSS = '''
:root{
  --primary:#283fff; --primary-tint:#eef0ff;
  --black:#000; --text-subdued:#6e6e6e; --disabled:#bdbdbd;
  --border:#e0e0e0; --surface-subdued:#f2f2f2; --white:#fff;
  --grass-500:#008113; --grass-400:#1ac734; --grass-100:#ddf3d8;
  --crop-500:#9a6500;  --crop-400:#ebb900;  --crop-100:#fff4d7;
  --fire-500:#b81f00;  --fire-400:#ff4d2a;  --fire-100:#fce6e2;
  --glacier:#1fc0ff; --coral:#af32b8;
  --font:'Inter',-apple-system,BlinkMacSystemFont,'Helvetica Neue',Arial,sans-serif;
  --shadow-btn:0 1px 2px rgba(0,0,0,.06);
  --shadow-pop:0 16px 40px rgba(0,0,0,.10), 0 2px 8px rgba(0,0,0,.05);
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;font-family:var(--font);color:var(--black);background:var(--white);
  -webkit-font-smoothing:antialiased}
.wrap{max-width:1120px;margin:0 auto;padding:0 32px}

/* Standard page chrome: a subtle presenter header, and the sign-off footer.
   The mocked browser chrome below is reserved for the prototype only. */
.top-bar{border-bottom:1px solid var(--border);padding:14px 0}
.top-bar-inner{display:flex;align-items:baseline;justify-content:space-between;gap:16px}
.top-bar-title{font-size:12.5px;font-weight:700;color:var(--black)}
.top-bar-meta{font-size:12.5px;color:var(--text-subdued);white-space:nowrap}
@media (max-width:600px){
  .top-bar-inner{flex-direction:column;align-items:flex-start;gap:2px}
}
.sign-off{padding:24px 0 56px;color:var(--text-subdued);font-size:13px;line-height:20px}
.sign-off p{margin:0}
h1,h2,h3,h4{margin:0;font-weight:700}
p{margin:0}
.text-display{font-size:32px;line-height:40px;font-weight:700}
.text-title{font-size:24px;line-height:32px;font-weight:700}
.text-heading{font-size:18px;line-height:28px;font-weight:700}
.text-body{font-size:16px;line-height:24px}
.text-dense{font-size:14px;line-height:20px}
.caption{font-size:12px;line-height:18px}
.muted{color:var(--text-subdued)}
.eyebrow{font-size:12px;line-height:18px;letter-spacing:.04em;text-transform:uppercase;
  color:var(--text-subdued);font-weight:700}

/* ==== persistent mock browser chrome + dock ==== */
.browser-window{max-width:1240px;margin:28px auto 120px;background:var(--white);
  border-radius:16px;overflow:hidden;box-shadow:var(--shadow-pop);border:1px solid #c7cad1}
.browser-chrome{position:sticky;top:0;z-index:80;display:flex;align-items:center;gap:16px;
  padding:11px 16px;background:#ececee;border-bottom:1px solid #d5d7db}
.traffic{display:flex;gap:7px}
.traffic .dot{width:11px;height:11px;border-radius:999px;display:inline-block}
.dot-r{background:#ff5f56}.dot-y{background:#ffbd2e}.dot-g{background:#27c93f}
.browser-nav-btns{display:flex;gap:4px}
.nb{width:26px;height:26px;border-radius:999px;border:none;background:transparent;color:#8a8d93;
  font-size:15px;cursor:pointer;display:flex;align-items:center;justify-content:center}
.nb:hover{background:#dfe1e5}
.address-bar{flex:1;max-width:420px;margin:0 auto;background:var(--white);border:1px solid #d5d7db;
  border-radius:999px;padding:6px 14px;font-size:12.5px;color:var(--text-subdued);
  display:flex;align-items:center;gap:7px}
.address-bar svg{flex:none;opacity:.6}
.browser-spacer{width:64px}
.browser-body{background:#fafafa}

.dock{position:fixed;left:50%;bottom:14px;transform:translateX(-50%);z-index:90;
  display:flex;align-items:flex-end;gap:10px;padding:9px 14px;border-radius:20px;
  background:rgba(255,255,255,.7);backdrop-filter:blur(14px) saturate(1.6);
  border:1px solid rgba(255,255,255,.5);box-shadow:0 12px 30px rgba(0,0,0,.18)}
.dock-icon{width:40px;height:40px;border-radius:11px;background:linear-gradient(160deg,#fff,#e2e4e8);
  box-shadow:0 2px 4px rgba(0,0,0,.12), inset 0 1px 0 rgba(255,255,255,.6);
  display:flex;align-items:center;justify-content:center;color:var(--text-subdued);font-size:16px;
  text-decoration:none;transition:transform 160ms cubic-bezier(.23,1,.32,1)}
.dock-icon:hover{transform:translateY(-6px)}
.dock-icon:active{transform:translateY(-2px) scale(.96)}
.dock-icon--brand{background:var(--primary);color:#fff;font-weight:700}

header.page{padding:56px 0 28px;border-bottom:1px solid var(--border)}
header.page h1{font-size:28px}
header.page p{margin-top:8px;color:var(--text-subdued);max-width:640px}

section.beat{padding:64px 0 40px;border-bottom:1px solid var(--border)}
section.beat:last-of-type{border-bottom:none}
.beat-kicker{display:flex;align-items:baseline;gap:10px;margin-bottom:20px}
.beat-num{display:inline-flex;align-items:center;justify-content:center;min-width:26px;height:26px;
  padding:0 9px;white-space:nowrap;border-radius:999px;background:var(--black);color:var(--white);
  font-size:12px;font-weight:700}
.say{margin-top:18px;padding:14px 16px;border-left:2px solid var(--primary);background:var(--primary-tint);
  border-radius:0 8px 8px 0;color:#1a1a1a}
.say b{color:var(--primary)}

/* beat prev/next nav */
.beat-nav{display:flex;align-items:center;justify-content:space-between;gap:14px;margin-top:40px}
.bn-btn{font-family:var(--font);font-size:13px;font-weight:700;color:var(--text-subdued);
  text-decoration:none;padding:9px 16px;border-radius:999px;border:1px solid var(--border);background:var(--white)}
.bn-btn:hover{border-color:var(--primary);color:var(--primary)}
.bn-btn--primary{background:var(--primary);border-color:var(--primary);color:#fff}
.bn-btn--primary:hover{color:#fff;opacity:.9}
.bn-btn--spacer{visibility:hidden}
.bn-dots{display:flex;gap:6px}
.bn-dot{width:6px;height:6px;border-radius:999px;background:var(--border)}
.bn-dot--on{background:var(--primary);width:16px;border-radius:999px}

/* Beat 1 */
.intro-statement{font-size:34px;line-height:1.25;font-weight:700;max-width:720px;margin:24px 0}

/* Beat 2 — seven steps */
.steps{display:grid;grid-template-columns:140px 1fr;gap:18px;margin-top:24px}
.cadence{padding:18px 16px;border-radius:12px;background:var(--surface-subdued)}
.cadence h5{font-size:13px;font-weight:700;margin:0}
.step-list{display:flex;flex-direction:column;gap:10px}
.step-row{display:flex;align-items:center;gap:12px;padding:12px 14px;border:1px solid var(--border);
  border-radius:10px;background:var(--white)}
.step-row .num{width:22px;height:22px;border-radius:999px;background:var(--surface-subdued);
  display:inline-flex;align-items:center;justify-content:center;font-size:12px;font-weight:700;flex:none}
.step-row .full{color:var(--text-subdued);font-size:13px}

/* Beat 2 — effort + emotional journey */
.journey-card{margin-top:28px;border:1px solid var(--border);border-radius:14px;padding:18px 20px;background:var(--white)}
.effort{display:inline-flex;gap:3px;align-items:center;vertical-align:middle}
.ef-dot{width:7px;height:7px;border-radius:999px;background:var(--border);display:inline-block}
.ef-dot.on{background:var(--primary)}
.emo-chip{display:inline-flex;align-items:center;gap:5px;font-size:12px;color:var(--text-subdued);font-weight:600;white-space:nowrap}
.emo-emoji{font-size:15px;line-height:1}
.step-row{flex-wrap:wrap}
.step-main{flex:1;min-width:200px}
.step-meta{display:flex;align-items:center;gap:10px;margin-left:auto;flex:none}
.emo-journey{overflow:visible}
.emo-journey-line{fill:none;stroke:var(--primary);stroke-width:2.5}
.emo-dot{fill:var(--white);stroke:var(--primary);stroke-width:2}
.emo-journey-emoji{font-size:16px}
.emo-boundary{stroke:var(--border);stroke-width:1;stroke-dasharray:3 4}
.emo-axis-top,.emo-axis-bottom{font-size:11px;fill:var(--text-subdued);font-family:var(--font)}

/* Beat 3 — the reframe, accelerated: bridge + stage cards */
.bridge{margin-top:24px}
.bridge-steps,.bridge-stages{display:grid;grid-template-columns:repeat(7,1fr);gap:8px}
.bridge-chip{border:1px solid var(--border);border-radius:10px;background:var(--white);
  padding:8px 8px;text-align:center;display:flex;flex-direction:column;gap:4px;min-height:54px;justify-content:center}
.bridge-chip-num{width:18px;height:18px;border-radius:999px;background:var(--surface-subdued);
  font-size:10.5px;font-weight:700;display:inline-flex;align-items:center;justify-content:center;margin:0 auto}
.bridge-chip-label{font-size:10.5px;line-height:13px;color:var(--text-subdued)}
.bridge-stages{margin-top:8px}
.bridge-stage{border-radius:10px;padding:10px 8px;text-align:center;font-size:13px;font-weight:700;
  background:var(--surface-subdued);color:var(--text-subdued);position:relative}
.bridge-stage::before{content:"";position:absolute;top:-8px;left:50%;transform:translateX(-50%);
  width:1px;height:8px;background:var(--border)}
.bridge-stage--primary{background:var(--primary-tint);color:var(--primary)}

.principle-banner{margin-top:24px;padding:14px 18px;border-radius:12px;background:var(--black);
  color:#fff;text-align:center;font-size:14.5px}
.principle-banner strong{color:#fff}

.maps-from{margin-top:12px;color:var(--text-subdued)}
.stage-oneliner{margin-top:8px;font-size:14.5px;line-height:21px;font-weight:600}
.accelerate-list{list-style:none;margin:8px 0 0;padding:0;display:flex;flex-direction:column;gap:6px}
.accelerate-list li{font-size:12.5px;line-height:18px;padding-left:18px;position:relative;color:#1a1a1a}
.accelerate-list li::before{content:"⚡";position:absolute;left:0;top:-1px;font-size:10px;color:var(--primary)}
.accel-label{text-transform:uppercase;letter-spacing:.03em;font-weight:700}
.stage-shift{display:flex;align-items:center;gap:8px;margin-top:16px;padding-top:14px;
  border-top:1px dashed var(--border);flex-wrap:wrap}
.shift-old{opacity:.65}
.shift-new{font-weight:700}
.shift-arrow{color:var(--text-subdued)}

.prototype-cta{display:block;margin-top:16px;padding:16px 18px;border-radius:14px;background:var(--primary);
  color:#fff;text-decoration:none;box-shadow:var(--shadow-pop);transition:transform 160ms cubic-bezier(.23,1,.32,1)}
.prototype-cta:hover{transform:translateY(-2px)}
.prototype-cta strong{display:block;font-size:15px;margin-top:2px}
.prototype-cta-badge{display:inline-block;background:rgba(255,255,255,.18);padding:3px 9px;
  border-radius:999px;font-size:10.5px;font-weight:700;text-transform:uppercase;letter-spacing:.03em}

.sustain-frag .checkin-row{display:flex;align-items:center;gap:8px;font-size:12px;font-weight:700}
.checkin-bubble{margin-top:8px;background:var(--white);border:1px solid var(--border);border-radius:8px;padding:8px 10px}
.checkin-bubble p{font-size:12px;line-height:17px;margin-top:3px}
.checkin-bubble--reply{background:var(--primary-tint);border-color:transparent}
.sweepy-extract{margin-top:8px}

/* Beats 4-6 hero cards, now 4-up (Draft / Align / Assign / Sustain) */
.hero-cards{display:grid;grid-template-columns:repeat(4,1fr);gap:20px;margin-top:28px}
.hero-card{border:1px solid var(--border);border-radius:16px;padding:20px;background:var(--white);
  box-shadow:var(--shadow-btn)}
.hero-card .tag{display:inline-block;padding:3px 9px;border-radius:999px;background:var(--surface-subdued);
  font-size:11px;font-weight:700;letter-spacing:.02em;text-transform:uppercase;color:var(--text-subdued)}
.hero-card h4{margin-top:10px;font-size:18px}
.frag{margin-top:14px;border:1px solid var(--border);border-radius:10px;padding:12px;background:var(--surface-subdued)}
.frag-caption{margin-top:12px;color:var(--text-subdued)}

.draft-frag{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.notes-panel{background:var(--white);border-radius:8px;padding:10px;border:1px dashed var(--border)}
.notes-line{height:8px;border-radius:4px;background:var(--border);margin:8px 0}
.notes-line:nth-child(1){width:92%}.notes-line:nth-child(2){width:78%}
.notes-line:nth-child(3){width:85%}.notes-line:nth-child(4){width:64%}
.checklist{background:var(--white);border-radius:8px;padding:10px;border:1px solid var(--border)}
.check-item{display:flex;align-items:center;gap:8px;padding:5px 0;font-size:12px}
.check-item .box{width:14px;height:14px;border-radius:4px;border:1.5px solid var(--primary);flex:none}
.check-item .box.done{background:var(--primary)}

.stakeholder-row{display:flex;align-items:center;gap:8px;background:var(--white);border:1px solid var(--border);
  border-radius:8px;padding:7px 10px;margin-bottom:6px;font-size:12px}
.avatar-sm{width:20px;height:20px;border-radius:999px;background:var(--primary);color:#fff;font-size:9px;
  font-weight:700;display:inline-flex;align-items:center;justify-content:center;flex:none}

.assign-card{background:var(--white);border:1px solid var(--border);border-radius:8px;padding:12px}
.suggest-chip{display:inline-flex;align-items:center;gap:6px;background:var(--primary-tint);color:var(--primary);
  border-radius:999px;padding:4px 10px;font-size:11px;font-weight:700;margin-top:8px}

.btn{font-family:var(--font);font-size:14px;font-weight:500;border-radius:10px;padding:9px 16px;
  border:1px solid var(--border);background:var(--white);box-shadow:var(--shadow-btn);cursor:pointer;
  transition:filter .1s, background .1s}
.btn:hover{filter:brightness(.97)}
.btn--primary{background:var(--primary);border-color:var(--primary);color:#fff}
.btn--primary:hover{filter:brightness(1.1)}
.btn--ghost{background:var(--surface-subdued);color:var(--disabled);cursor:not-allowed}
.btn--sm{padding:6px 12px;font-size:12px;border-radius:8px}

/* The prototype reveal — fade + slight z-axis rotation in, on scroll-into-view */
.prototype-reveal{opacity:0;transform:perspective(1600px) rotateZ(-2.5deg) scale(.94);
  transform-origin:50% 20%;filter:blur(2px);
  transition:opacity .65s cubic-bezier(.23,1,.32,1), transform .65s cubic-bezier(.23,1,.32,1), filter .65s ease}
.prototype-reveal.is-visible{opacity:1;transform:none;filter:none}
@media (prefers-reduced-motion: reduce){
  .prototype-reveal{opacity:0;transform:none;filter:none;transition:opacity .4s ease}
  .prototype-reveal.is-visible{opacity:1}
}

/* ==== Act view ==== */
.act-frame{border-radius:0;overflow:visible;background:var(--white)}
.act-body{display:grid;grid-template-columns:64px 1fr 300px;min-height:640px}
.act-rail{background:var(--surface-subdued);border-right:1px solid var(--border);
  display:flex;flex-direction:column;align-items:center;gap:14px;padding:18px 0}
.act-rail .r{width:32px;height:32px;border-radius:10px;background:var(--white);border:1px solid var(--border)}
.act-rail .r.active{background:var(--primary)}
.act-main{padding:28px 28px 8px}
.act-main h2{font-size:28px}
.act-chart-card{margin-top:18px;border:1px solid var(--border);border-radius:14px;padding:18px 18px 10px}

/* chart component (shared: Act hero, Reports, Initiative page) */
.chart{width:100%;height:auto;display:block;overflow:visible}
.axis-line{stroke:var(--border);stroke-width:1}
.axis-label{font-size:11px;fill:var(--text-subdued);font-family:var(--font)}
.line{fill:none;stroke-width:2.5}
.line--actual{stroke:var(--primary)}
.line--target{stroke:var(--disabled);stroke-dasharray:4 5}
.chart-band{fill:var(--fire-400);fill-opacity:.12}
.dot{stroke:var(--white);stroke-width:1.5}
.dot--actual{fill:var(--primary)}
.dot--target{fill:var(--disabled)}
.chart-hero-value{font-size:20px;font-weight:700;font-family:var(--font);fill:var(--black)}
.chart-hero-unit{font-size:12px;font-weight:500;fill:var(--text-subdued)}
.chart-hero-sub{font-size:12px;font-family:var(--font);fill:var(--text-subdued)}
.pt .hit{fill:transparent;cursor:pointer}
.pt .guide{stroke:var(--border);stroke-width:1;opacity:0}
.pt .tooltip{opacity:0;pointer-events:none;transition:opacity .12s}
.pt:hover .guide{opacity:1}
.pt:hover .tooltip{opacity:1}
.tt-box{background:var(--black);color:#fff;border-radius:10px;padding:9px 11px;font-family:var(--font);
  box-shadow:var(--shadow-pop)}
.tt-month{font-size:11px;font-weight:700;margin-bottom:4px;color:#fff}
.tt-row{display:flex;justify-content:space-between;gap:14px;font-size:11px;color:#c9cad0}
.tt-row b{color:#fff;font-weight:700}
.chart-legend{display:flex;align-items:center;gap:16px;margin-top:6px;padding:0 4px 4px}
.legend-item{display:flex;align-items:center;gap:6px;font-size:11.5px;color:var(--text-subdued)}
.legend-swatch{width:14px;height:3px;border-radius:2px;display:inline-block}
.legend-swatch--target{background:var(--disabled)}
.legend-swatch--actual{background:var(--primary)}
.legend-swatch--band{background:var(--fire-400);opacity:.35}
.legend-hint{margin-left:auto;font-style:italic}

.reports-card{margin-top:16px;border:1px solid var(--border);border-radius:14px;padding:16px 18px}
.reports-card:hover{border-color:var(--primary)}
.reports-card .left{display:flex;align-items:center;gap:12px}
.reports-icon{width:40px;height:40px;border-radius:10px;background:var(--primary-tint);color:var(--primary);
  display:flex;align-items:center;justify-content:center}
.badge-new{background:var(--primary-tint);color:var(--primary);font-size:11px;font-weight:700;
  padding:4px 10px;border-radius:999px}
.reports-teaser{color:var(--text-subdued);margin-top:2px;max-width:440px}

.stat-row{display:flex;gap:28px}
.stat{display:flex;flex-direction:column}
.stat-value{font-size:22px;font-weight:700}
.stat-label{font-size:11px;color:var(--text-subdued);margin-top:2px}

.act-main-head{display:flex;align-items:center;justify-content:space-between;margin-top:30px}
.act-main-actions{display:flex;align-items:center;gap:10px}
.sort-pill{display:inline-flex;align-items:center;gap:6px;font-size:12px;color:var(--text-subdued);
  border:1px solid var(--border);border-radius:8px;padding:6px 10px;background:var(--white)}
.tile-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:16px;padding-bottom:24px}
.tile{border:1px solid var(--border);border-radius:14px;overflow:hidden;background:var(--white);
  text-decoration:none;color:inherit;display:block;transition:box-shadow .12s, border-color .12s}
.tile:hover{border-color:var(--primary);box-shadow:var(--shadow-btn)}
.tile-art{position:relative;height:64px;background:var(--surface-subdued);display:flex;
  align-items:center;justify-content:center;color:var(--text-subdued)}
.tile-art--bolt{color:var(--primary)}
.tile-art--flame{color:var(--fire-500)}
.tile-scope{position:absolute;top:8px;right:8px;font-size:10px;font-weight:700;color:var(--text-subdued);
  background:rgba(255,255,255,.85);padding:2px 6px;border-radius:6px}
.tile-body{padding:12px 14px 14px}
.tile-top{display:flex;align-items:center;justify-content:space-between;gap:8px}
.tile-top h4{font-size:13.5px}
.tile-owner{font-size:11px;color:var(--text-subdued);margin-top:3px}
.delta-bad{color:var(--fire-500);font-size:12.5px;font-weight:700}
.delta-good{color:var(--grass-500);font-size:12.5px;font-weight:700}
.pill{display:inline-flex;align-items:center;gap:5px;font-size:10.5px;font-weight:700;padding:3px 8px;
  border-radius:999px;margin-top:9px}
.pill::before{content:"";width:6px;height:6px;border-radius:999px}
.pill--grass{background:var(--grass-100);color:var(--grass-500)}
.pill--grass::before{background:var(--grass-500)}
.pill--crop{background:var(--crop-100);color:var(--crop-500)}
.pill--crop::before{background:var(--crop-500)}
.pill--fire{background:var(--fire-100);color:var(--fire-500)}
.pill--fire::before{background:var(--fire-500)}

.sweepy-panel{border-left:1px solid var(--border);padding:22px 20px;display:flex;flex-direction:column}
.sweepy-head{display:flex;align-items:center;gap:10px}
.sweepy-avatar{width:34px;height:34px;border-radius:999px;background:var(--primary);color:#fff;
  display:flex;align-items:center;justify-content:center;font-weight:700;font-size:13px}
.tabs{display:flex;gap:16px;margin-top:16px;border-bottom:1px solid var(--border)}
.tabs input{display:none}
.tabs label{font-size:12.5px;color:var(--text-subdued);padding-bottom:9px;cursor:pointer;
  border-bottom:2px solid transparent}
#tab-for-you:checked ~ .tabs label[for=tab-for-you],
#tab-activity:checked ~ .tabs label[for=tab-activity],
#tab-goals:checked ~ .tabs label[for=tab-goals],
#tab-chat:checked ~ .tabs label[for=tab-chat]{color:var(--black);border-bottom-color:var(--primary);font-weight:700}
.tab-panel{display:none;padding-top:16px}
#tab-for-you:checked ~ .tab-content .panel-for-you,
#tab-activity:checked ~ .tab-content .panel-activity,
#tab-goals:checked ~ .tab-content .panel-goals,
#tab-chat:checked ~ .tab-content .panel-chat{display:block}

.foryou-msg{font-size:13px;line-height:20px;color:#1a1a1a}
.foryou-row{margin-top:14px;border:1px solid var(--border);border-radius:10px;overflow:hidden}
.foryou-row summary{list-style:none;display:flex;align-items:center;gap:8px;padding:9px 10px;cursor:pointer}
.foryou-row summary::-webkit-details-marker{display:none}
.avatar{width:22px;height:22px;border-radius:999px;background:var(--surface-subdued);font-size:9px;
  font-weight:700;display:inline-flex;align-items:center;justify-content:center;flex:none}
.foryou-row-main{flex:1;font-size:12px}
.thread{padding:0 10px 10px;border-top:1px solid var(--border)}
.msg{padding:9px 0;border-bottom:1px dashed var(--border)}
.msg-meta{font-size:10.5px;color:var(--text-subdued)}
.msg p{font-size:12px;margin-top:3px}
.msg--owner{border-left:2px solid var(--primary);padding-left:8px}
.thread-footer{display:flex;align-items:center;justify-content:space-between;padding-top:9px;flex-wrap:wrap;gap:8px}

.data-attachment{margin-top:10px;display:flex;gap:9px;align-items:flex-start;padding:9px 10px;
  border:1px solid var(--border);border-radius:9px;background:var(--surface-subdued)}
.data-attachment svg{flex:none;margin-top:2px;color:var(--text-subdued)}
.data-attachment strong{font-size:12px}

.ok-note{margin-top:10px;display:flex;gap:9px;align-items:flex-start;padding:9px 10px;
  border:1px solid #bfe3c8;border-radius:9px;background:var(--grass-100)}
.ok-note svg{flex:none;margin-top:2px;color:var(--grass-500)}
.ok-note p{font-size:12px;line-height:18px;margin:0;color:#0f4d24}
.ok-note b{color:var(--grass-500)}

.nuance-note{margin-top:10px;display:flex;gap:9px;align-items:flex-start;padding:9px 10px;
  border:1px dashed var(--border);border-radius:9px}
.nuance-note svg{flex:none;margin-top:2px;color:var(--text-subdued)}
.nuance-note p{font-size:12px;line-height:18px;margin:0;color:var(--text-subdued)}
.nuance-note b{color:var(--black)}

.blocker-flag{display:inline-flex;align-items:center;gap:5px;font-size:10.5px;font-weight:700;
  color:var(--fire-500);margin-top:8px}
.blocker-flag svg{flex:none}

.report-ready-card{display:none;align-items:center;gap:10px;margin-top:14px;padding:11px 12px;
  border:1px solid var(--primary);background:var(--primary-tint);border-radius:10px}
.report-ready-card strong{font-size:12.5px}
.report-ready-icon{width:30px;height:30px;border-radius:8px;background:var(--white);color:var(--primary);
  display:flex;align-items:center;justify-content:center;flex:none}

.preview-checkbox{display:none}
.preview-toggle{display:inline-block;margin-top:8px;font-size:12px;color:var(--text-subdued);
  cursor:pointer;text-decoration:underline;text-underline-offset:2px}
.reports-normal{display:flex;align-items:center;justify-content:space-between;text-decoration:none;color:inherit}
.reports-loading{display:none;align-items:center;gap:12px}
.spinner{width:16px;height:16px;border-radius:50%;flex:none;
  border:2px solid var(--border);border-top-color:var(--primary);animation:spin .8s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
#preview-cleared:checked ~ .act-main .reports-card .reports-normal{display:none}
#preview-cleared:checked ~ .act-main .reports-card .reports-loading{display:flex}
#preview-cleared:checked ~ .sweepy-panel .report-ready-card{display:flex}

.feed-row{display:flex;gap:10px;padding:11px 0;border-bottom:1px dashed var(--border)}
.feed-row:last-child{border-bottom:none}
.feed-dot{width:7px;height:7px;border-radius:999px;background:var(--primary);margin-top:6px;flex:none}
.feed-text{font-size:12.5px;line-height:18px}
.feed-ts{display:block;margin-top:3px}

.goal-row{display:flex;gap:10px;align-items:flex-start;padding:10px 0;border-bottom:1px solid var(--border)}
.goal-row:last-child{border-bottom:none}
.goal-mark{width:20px;height:20px;border-radius:999px;background:var(--primary-tint);color:var(--primary);
  font-size:10px;font-weight:700;display:flex;align-items:center;justify-content:center;flex:none;margin-top:1px}
.goal-row p{font-size:12.5px;line-height:18px}

.chat-msg{display:flex;gap:8px;margin-top:12px;align-items:flex-start}
.chat-msg--me{flex-direction:row-reverse}
.avatar--chat{background:var(--primary);color:#fff}
.chat-msg--me .avatar--chat{background:var(--surface-subdued);color:var(--text-subdued)}
.chat-bubble{background:var(--surface-subdued);border-radius:12px;padding:9px 12px;max-width:78%}
.chat-msg--me .chat-bubble{background:var(--primary-tint)}
.chat-bubble p{font-size:12.5px;line-height:18px}

.static-note{border:1px dashed var(--border);border-radius:10px;padding:14px;color:var(--text-subdued);font-size:12.5px}
.compose{margin-top:auto;padding-top:16px}
.compose-box{border:1px solid var(--border);border-radius:10px;padding:10px;color:var(--disabled);font-size:12.5px}

/* ==== full pages: Initiative detail (State F) / Reports (State G) ==== */
.page-shell{padding:40px 0 8px}
.page-crumb{font-size:12px;color:var(--text-subdued);display:flex;align-items:center;gap:6px}
.page-crumb a{color:var(--text-subdued);text-decoration:none}
.page-crumb a:hover{color:var(--primary)}
.page-header{display:flex;align-items:flex-start;justify-content:space-between;gap:20px;margin-top:14px}
.page-header h1{font-size:30px}
.page-header .owner-row{display:flex;align-items:center;gap:8px;margin-top:8px;color:var(--text-subdued);font-size:13px}
.page-tags{display:flex;gap:8px;margin-top:10px}
.page-tag{font-size:11px;font-weight:700;padding:4px 10px;border-radius:999px;background:var(--surface-subdued);color:var(--text-subdued)}

.page-overview{margin-top:26px;max-width:760px}
.page-overview h3{font-size:13px;text-transform:uppercase;letter-spacing:.04em;color:var(--text-subdued)}
.page-overview p{margin-top:10px;font-size:15.5px;line-height:25px}

.flag-note{margin-top:18px;max-width:760px;display:flex;gap:10px;align-items:flex-start;
  background:var(--crop-100);border:1px solid #f0dca0;border-radius:12px;padding:14px 16px}
.flag-note svg{flex:none;margin-top:2px;color:var(--crop-500)}
.flag-note p{font-size:13.5px;line-height:20px;color:#5c4400}
.flag-note b{color:var(--crop-500)}
.flag-note--sm{padding:10px 12px;margin-top:10px;max-width:none}
.flag-note--sm p{font-size:12px;line-height:18px;margin:0}
.extraction-fields{margin-top:8px;display:grid;grid-template-columns:64px 1fr;gap:5px 10px;font-size:12px}
.extraction-fields dt{color:var(--text-subdued);font-weight:700;margin:0}
.extraction-fields dd{margin:0;line-height:16px}

.live-data-head{display:flex;align-items:center;gap:8px;margin-top:38px}
.live-dot{width:7px;height:7px;border-radius:999px;background:var(--grass-500);
  box-shadow:0 0 0 3px var(--grass-100)}
.page-chart-card{margin-top:16px;border:1px solid var(--border);border-radius:16px;padding:22px 22px 12px;background:var(--white)}

.data-table{width:100%;border-collapse:collapse;margin-top:16px;font-size:12.5px}
.data-table th{text-align:left;color:var(--text-subdued);font-weight:700;font-size:11px;
  text-transform:uppercase;letter-spacing:.03em;padding:8px 10px;border-bottom:1px solid var(--border)}
.data-table td{padding:10px 10px;border-bottom:1px solid var(--border)}
.data-table tr:last-child td{border-bottom:none}
.table-card{margin-top:14px;border:1px solid var(--border);border-radius:14px;padding:6px 14px 8px;background:var(--white);overflow-x:auto}

/* Reports page */
.report-layout{display:grid;grid-template-columns:220px 1fr;gap:32px;margin-top:26px;align-items:start}
.report-timeline{display:flex;flex-direction:column;gap:2px;position:sticky;top:78px}
.report-timeline::before{content:"";display:none}
.timeline-item{display:flex;gap:10px;padding:10px 8px;border-radius:10px;cursor:pointer;position:relative}
.timeline-item:hover{background:var(--surface-subdued)}
.timeline-dot{width:9px;height:9px;border-radius:999px;background:var(--border);margin-top:4px;flex:none}
.timeline-body{display:flex;flex-direction:column;font-size:13px;gap:2px}
input[type=radio][name=report]{display:none}
#rep-2026-09:checked ~ .report-timeline label[for=rep-2026-09] .timeline-dot,
#rep-2026-08:checked ~ .report-timeline label[for=rep-2026-08] .timeline-dot,
#rep-2026-07:checked ~ .report-timeline label[for=rep-2026-07] .timeline-dot,
#rep-2026-06:checked ~ .report-timeline label[for=rep-2026-06] .timeline-dot,
#rep-2026-05:checked ~ .report-timeline label[for=rep-2026-05] .timeline-dot,
#rep-2026-04:checked ~ .report-timeline label[for=rep-2026-04] .timeline-dot{background:var(--primary);
  box-shadow:0 0 0 3px var(--primary-tint)}
#rep-2026-09:checked ~ .report-timeline label[for=rep-2026-09],
#rep-2026-08:checked ~ .report-timeline label[for=rep-2026-08],
#rep-2026-07:checked ~ .report-timeline label[for=rep-2026-07],
#rep-2026-06:checked ~ .report-timeline label[for=rep-2026-06],
#rep-2026-05:checked ~ .report-timeline label[for=rep-2026-05],
#rep-2026-04:checked ~ .report-timeline label[for=rep-2026-04]{background:var(--surface-subdued)}
.report-body{min-width:0}
.report-panel{display:none}
REPORT_VISIBILITY_PLACEHOLDER
.review-banner{display:flex;align-items:center;gap:10px;background:var(--primary-tint);color:var(--primary);
  border-radius:12px;padding:13px 16px;font-size:13.5px;font-weight:600}
.reviewed-row{margin-top:4px}
.report-head-row{display:flex;align-items:flex-start;justify-content:space-between;gap:20px;flex-wrap:wrap}
.report-actions{display:flex;gap:8px;margin-top:22px;flex:none}
.report-chart-card{margin-top:18px;border:1px solid var(--border);border-radius:16px;padding:22px 22px 12px;background:var(--white)}
.report-grid{display:grid;grid-template-columns:1fr 1fr;gap:24px;margin-top:26px}
.report-list{list-style:none;margin:10px 0 0;padding:0;display:flex;flex-direction:column;gap:10px}
.report-list li{font-size:13px;line-height:19px;padding-left:16px;position:relative}
.report-list--good li::before{content:"";position:absolute;left:0;top:6px;width:6px;height:6px;border-radius:999px;background:var(--grass-500)}
.report-list--bad li::before{content:"";position:absolute;left:0;top:6px;width:6px;height:6px;border-radius:999px;background:var(--fire-500)}

footer.page{padding:48px 0 64px;color:var(--text-subdued)}
footer.page a{color:var(--primary)}

@media (max-width: 960px){
  .steps{grid-template-columns:1fr}
  .hero-cards{grid-template-columns:1fr}
  .bridge-steps,.bridge-stages{grid-template-columns:repeat(7,84px)}
  .bridge{overflow-x:auto}
  .bridge-stage::before{display:none}
  .step-meta{margin-left:0}
  .act-body{grid-template-columns:1fr}
  .act-rail{flex-direction:row;justify-content:center}
  .sweepy-panel{border-left:none;border-top:1px solid var(--border)}
  .tile-grid{grid-template-columns:repeat(2,1fr)}
  .report-layout{grid-template-columns:1fr}
  .report-timeline{position:static;flex-direction:row;overflow-x:auto}
  .report-grid{grid-template-columns:1fr}
}
'''

CSS = CSS.replace("REPORT_VISIBILITY_PLACEHOLDER", report_visibility_css)


HTML = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Sustain — storyboard &amp; wireframes</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>

<header class="top-bar">
  <div class="wrap top-bar-inner">
    <span class="top-bar-title">{PRESENTATION_TITLE}</span>
    <span class="top-bar-meta">{PRESENTER_NAME} · {PRESENTATION_DATE}</span>
  </div>
</header>

<div class="wrap">

  <header class="page" id="beat-1">
    <span class="eyebrow">Sweep — design task · content &amp; structure pass, not final visual design</span>
    <h1 class="text-display" style="margin-top:8px">Storyboard — wireframe sequence</h1>
    <p class="text-body">A written run-through, beat by beat, carrying real content from
      <code>data/*.json</code> instead of placeholder text, styled with Sweep's own tokens — so we can
      riff on structure and copy before Ronan takes the key screens into Figma for final visual design.</p>
  </header>

  <section class="beat">
    <div class="beat-kicker"><span class="beat-num">1</span><span class="eyebrow">Open</span></div>
    <p class="intro-statement">A handful of people, across departments, trying to agree on actions and
      keep them honest, currently held together by spreadsheets and email.</p>
    <div class="say">"Sweep's brief was: simplify this flow, and find where AI actually accelerates it —
      <b>not for its own sake.</b> Here's how I got from their seven steps to what we built."</div>
    {beat_nav(None, "", "beat-2", "The original flow", 0)}
  </section>

  <section class="beat" id="beat-2">
    <div class="beat-kicker"><span class="beat-num">2</span><span class="eyebrow">The original flow, and where it actually hurts</span></div>
    <div class="steps">
      <div class="cadence"><h5>Once per cycle</h5><p class="caption muted" style="margin-top:4px">Steps 1–4</p></div>
      <div class="step-list">{episodic_rows}</div>
      <div class="cadence"><h5>Every month, forever</h5><p class="caption muted" style="margin-top:4px">Steps 5–7</p></div>
      <div class="step-list">{recurring_rows}</div>
    </div>
    <div class="journey-card">
      <p class="eyebrow" style="margin-bottom:6px">Effort &amp; emotional read, step by step — assumed and relative, not measured</p>
      {emotion_journey}
    </div>
    <div class="say">"Steps one through four happen once a cycle — slow, but they don't compound.
      Steps five through seven happen every month, forever, and they're the ones the brief itself
      describes with real frustration — <i>'manually chase,' 'reconstructing from memory.'</i> The
      grind shows up directly in the effort and the emotion, not just in the copy."</div>
    {beat_nav("beat-1", "Open", "beat-3", "The reframe, accelerated", 1)}
  </section>

  <section class="beat" id="beat-3">
    <div class="beat-kicker"><span class="beat-num">3</span><span class="eyebrow">The reframe — seven steps become four stages, accelerated by Sweepy</span></div>

    <div class="bridge">
      <div class="bridge-steps">{bridge_chips}</div>
      <div class="bridge-stages">{bridge_stage_labels}</div>
    </div>

    <div class="principle-banner">
      <strong>The rule that runs through all four:</strong> Sweepy expedites and suggests — the human always decides.
    </div>

    <div class="hero-cards">{stage_cards}</div>

    <div class="say">"Draft, Align and Assign are described, not built — Sustain is the one that compounds
      every month instead of once, and it's the cleanest place to show the trust boundary that matters
      most: Sweepy interprets what an owner said, but never invents or upgrades it on their behalf.
      That's where the build went — and where the effort and the emotion actually turn around."</div>
    {beat_nav("beat-2", "The original flow", "prototype-reveal", "Open the prototype", 2)}
  </section>

</div><!-- /.wrap (preamble) -->

<div class="browser-window prototype-reveal" id="prototype-reveal">
  <div class="browser-chrome">
    <div class="traffic"><span class="dot dot-r"></span><span class="dot dot-y"></span><span class="dot dot-g"></span></div>
    <div class="browser-nav-btns">
      <button class="nb" title="Back">‹</button>
      <button class="nb" title="Forward">›</button>
      <button class="nb" title="Reload">⟳</button>
    </div>
    <div class="address-bar">
      <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="5" y="11" width="14" height="9" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/></svg>
      app.sweep.net
    </div>
    <div class="browser-spacer"></div>
  </div>

  <div class="browser-body">
  <div class="wrap">

  <section id="state-e" style="padding:56px 0 0">
    <div class="beat-kicker"><span class="beat-num">State E</span><span class="eyebrow">The Act view — opens directly here, no preamble chat</span></div>
    <p class="muted">The high-fidelity frame the brief is actually asking for. Now carrying real content
      from <code>{esc(trajectory["company"])}</code>'s dataset, with a working hover chart and live links
      into the Reports and Initiative pages below.</p>
  </section>

  <section class="act-frame">
      <div class="act-body">
        <input type="checkbox" id="preview-cleared" class="preview-checkbox">
        <div class="act-rail">
          <div class="r"></div><div class="r active"></div><div class="r"></div><div class="r"></div>
        </div>

        <div class="act-main">
          <h2>Act</h2>
          <div class="act-chart-card">
            {dual_line_chart(trajectory["monthly"], unit=trajectory["unit"], hero_tag="All initiatives, Sep 2026")}
          </div>

          <div class="reports-card">
            <a class="reports-normal" href="#state-g">
              <div class="left">
                <div class="reports-icon">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
                    <path d="M6 3h9l5 5v13H6z"/><path d="M14 3v6h6"/></svg>
                </div>
                <div>
                  <div style="display:flex;align-items:center;gap:8px">
                    <strong>Reports</strong><span class="badge-new">New report available</span>
                  </div>
                  <p class="reports-teaser">{esc(latest_report["label"])} — please review and finalise</p>
                </div>
              </div>
              <span aria-hidden="true">→</span>
            </a>
            <div class="reports-loading">
              <span class="spinner"></span>
              <div>
                <strong>Sweepy's making your report…</strong>
                <p class="reports-teaser" style="margin-top:2px">Pulling together this month's confirmed data.</p>
              </div>
            </div>
          </div>
          <label for="preview-cleared" class="preview-toggle">↻ Preview: once you clear For You</label>

          <div class="act-main-head">
            <h3 class="text-heading">All initiatives</h3>
            <div class="act-main-actions">
              <span class="sort-pill">Sort by: status
                <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="m6 9 6 6 6-6"/></svg>
              </span>
              <button class="btn btn--sm">+ Add new</button>
            </div>
          </div>
          <div class="tile-grid">{tiles}</div>
        </div>

        <div class="sweepy-panel">
          <div class="sweepy-head">
            <span class="sweepy-avatar">S</span><strong>Sweepy</strong>
          </div>

          <input type="radio" name="tabs" id="tab-for-you" checked>
          <input type="radio" name="tabs" id="tab-activity">
          <input type="radio" name="tabs" id="tab-goals">
          <input type="radio" name="tabs" id="tab-chat">
          <div class="tabs">
            <label for="tab-for-you">For You</label>
            <label for="tab-activity">Activity</label>
            <label for="tab-goals">Goals</label>
            <label for="tab-chat">Chat</label>
          </div>

          <div class="tab-content">
            <div class="tab-panel panel-for-you">
              <p class="foryou-msg">{for_you_msg}</p>
              {for_you_cards}
              <div class="report-ready-card">
                <span class="report-ready-icon">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M6 3h9l5 5v13H6z"/><path d="M14 3v6h6"/></svg>
                </span>
                <div>
                  <strong>This month's report is ready</strong>
                  <p class="caption muted" style="margin-top:2px">Generated the moment you cleared the last item above.</p>
                </div>
                <a class="btn btn--sm" style="margin-left:auto" href="#state-g">View</a>
              </div>
            </div>
            <div class="tab-panel panel-activity">
              {activity_feed}
            </div>
            <div class="tab-panel panel-goals">
              {goals_list}
            </div>
            <div class="tab-panel panel-chat">
              {chat_html}
            </div>
          </div>

          <div class="compose">
            <div class="compose-box">Write a message…</div>
          </div>
        </div>
      </div>
  </section>

  <section class="page-shell" id="init-offgrid-solar">
    <div class="page-crumb"><a href="#state-e">Act</a> &nbsp;/&nbsp; Initiative</div>
    <div class="page-header">
      <div>
        <h1>{esc(init_page["name"])}</h1>
        <div class="owner-row">
          <span class="avatar-sm">{esc(initials(init_page["owner"]["name"]))}</span>
          {esc(init_page["owner"]["name"])} · {esc(init_page["owner"]["role"])}
          <span class="pill pill--{GOAL_STATUS_RAMP[init_page["status"]]}" style="margin-top:0">{GOAL_STATUS_LABEL[init_page["status"]]}</span>
        </div>
        <div class="page-tags">
          <span class="page-tag">{esc(init_page["scope"])}</span>
          <span class="page-tag">{esc(init_page["ghgCategory"])}</span>
          <span class="page-tag">Target {init_page["targetYear"]}</span>
        </div>
      </div>
      <button class="btn btn--sm">Edit initiative</button>
    </div>

    <div class="page-overview">
      <h3>Overview</h3>
      <p>{esc(init_page["overview"])}</p>
    </div>

    <div class="flag-note">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 9v4M12 17h.01M10.3 3.86 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.86a2 2 0 0 0-3.4 0Z"/></svg>
      <p><b>Sweepy flagged:</b> {esc(init_page["currentNote"])}</p>
    </div>

    <div class="live-data-head">
      <span class="live-dot"></span>
      <h3 class="text-heading">Live data</h3>
      <span class="caption muted">as of {init_page["lastCheckIn"] or "last confirmed check-in"}</span>
    </div>

    <div class="page-chart-card">
      {dual_line_chart(init_page["monthly"], unit=init_page["unit"], hero_tag="Current, Sep 2026")}
    </div>

    <div class="stat-row" style="margin-top:20px">
      {stat("Baseline", f'{init_page["baseline"]:,}')}
      {stat("Current", f'{init_page["current"]:,}')}
      {stat("Target " + str(init_page["targetYear"]), f'{init_page["target"]:,}')}
    </div>

    <h3 class="text-heading" style="margin-top:32px">Activity data — {latest_period}</h3>
    <p class="caption muted" style="margin-top:4px">Per-site rows for the most recent reporting period, exactly as an owner or Sweepy would see them.</p>
    <div class="table-card">
      <table class="data-table">
        <thead><tr><th>Site</th><th>Activity</th><th>Activity data</th><th>Emission factor</th><th>tCO2e</th><th>Quality</th></tr></thead>
        <tbody>{table_rows}</tbody>
      </table>
    </div>
  </section>

  <section class="page-shell" id="state-g" style="padding-bottom:20px">
    <div class="page-crumb"><a href="#state-e">Act</a> &nbsp;/&nbsp; Reports</div>
    <div class="page-header">
      <div>
        <h1>Reports</h1>
        <p class="muted" style="margin-top:8px;max-width:560px">A timeline of monthly leadership reports,
          generated by Sweepy from confirmed initiative data only. The most recent opens by default.</p>
      </div>
    </div>

    <div class="report-layout">
      {report_radios}
      <div class="report-timeline">{report_timeline}</div>
      <div class="report-body">{report_panels}</div>
    </div>
  </section>

  </div>
  </div>
</div><!-- /#prototype-reveal -->

<div class="wrap">
  <footer class="page">
    <p>Content pass, generated from <code>data/*.json</code> via <code>render_wireframes.py</code> —
      re-run after editing the data or the copy in this file's source. Reasoning trail in
      <code>decisions-log.md</code>; full beat script in <code>storyboard.md</code>.</p>
  </footer>

  <footer class="sign-off">
    <p>Thanks for reading. — {PRESENTER_NAME}<br>
      <!-- TODO(Ronan): add contact details here (email / phone / LinkedIn) -->
      [ contact details ]</p>
  </footer>
</div>

<div class="dock">
  <a class="dock-icon dock-icon--brand" href="#prototype-reveal" title="Open the prototype" aria-label="Open the prototype">S</a>
  <a class="dock-icon" href="{REPO_URL}" target="_blank" rel="noopener noreferrer" title="View the repo" aria-label="View the repo">
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 6 3 12l6 6M15 6l6 6-6 6"/></svg>
  </a>
</div>

<script>
(function(){{
  var el = document.getElementById('prototype-reveal');
  if(!el) return;
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  if(reduce || !('IntersectionObserver' in window)){{ el.classList.add('is-visible'); return; }}
  // Watch a short sentinel near the top of the frame (its own chrome bar), not the
  // whole multi-screen-tall container: on narrow viewports the container's height can
  // exceed the viewport by several times over, so an area-based threshold against the
  // full element can never be satisfied and the reveal would never fire.
  var sentinel = el.querySelector('.browser-chrome') || el;
  var obs = new IntersectionObserver(function(entries){{
    entries.forEach(function(entry){{
      if(entry.isIntersecting){{ el.classList.add('is-visible'); obs.unobserve(entry.target); }}
    }});
  }}, {{threshold: .2}});
  obs.observe(sentinel);
}})();
</script>

</body>
</html>
'''

OUT_FILE.write_text(HTML)
print(f"Wrote {OUT_FILE} ({len(HTML):,} bytes)")
