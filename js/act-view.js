/* ============================================================
   ACT VIEW — high-fidelity prototype (vanilla JS, no build step)
   Fetches the real repo JSON at runtime, derives the 3-state
   uiStatus, and drives one in-memory state object through a
   single render(). See design-task/md/act-view-plan.md.
============================================================ */
(function () {
  'use strict';

  var DATA = 'data/';
  var MONTHS = ['January','February','March','April','May','June','July',
                'August','September','October','November','December'];

  /* ---------- inline icons ---------- */
  var I = {
    sweepy:
      '<svg width="52" height="52" viewBox="0 0 52 52" fill="none">' +
      '<path d="M26 9 C20 22 13 33 8 40 C15 43 37 43 44 40 C39 33 32 22 26 9 Z" fill="#283fff"/>' +
      '<path d="M20 33 q6 6 12 0" stroke="#fff" stroke-width="2.4" fill="none" stroke-linecap="round"/>' +
      '</svg>',
    // For You tab — tabler/notification (bell)
    foryou:
      '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M10 5a2 2 0 1 1 4 0a7 7 0 0 1 4 6v3a4 4 0 0 0 2 3h-16a4 4 0 0 0 2 -3v-3a7 7 0 0 1 4 -6"/><path d="M9 17v1a3 3 0 0 0 6 0v-1"/></svg>',
    // Activity tab — tabler/activity
    activity:
      '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12h4l3 8l4 -16l3 8h4"/></svg>',
    // Goals tab — tabler/target
    goals:
      '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/></svg>',
    // Chat tab — tabler/message-circle
    chat:
      '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M3 20l1.3 -3.9a9 8 0 1 1 3.4 2.9l-4.7 1"/></svg>',
    // Monthly Reports tile — lucide/globe (a different family from the Tabler tabs)
    globe:
      '<svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/></svg>',
    globeBig:
      '<svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/></svg>',
    globeCard:
      '<svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/></svg>',
    // Report tile hover affordance — right arrow, 2px weight
    reportArrow:
      '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
    file:
      '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"><path d="M6 2h8l4 4v16H6Z"/><path d="M14 2v4h4"/><path d="M9 13h6M9 16h6M9 10h3"/></svg>',
    check:
      '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#0f7200" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M8 12l2.5 2.5L16 9"/></svg>',
    info:
      '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 8h.01"/></svg>',
    barrier:
      '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#DC6800" stroke-width="1.8" stroke-linejoin="round"><rect x="3" y="8" width="18" height="8" rx="1"/><path d="M6 8 3 16M12 8 9 16M18 8l-3 8M4 16v4M20 16v4"/></svg>',
    back:
      '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 5l-7 7 7 7"/></svg>',
    plus:
      '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M12 5v14M5 12h14"/></svg>',
    goalReport:
      '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"><rect x="5" y="4" width="14" height="17" rx="2"/><path d="M9 4V3h6v1"/><circle cx="16.5" cy="8.5" r="3" fill="#fff"/><path d="M16.5 7v1.5l1 .8" stroke-width="1.3"/></svg>',
    goalChase:
      '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"><path d="M3 11a6 6 0 0 1 12 0v7H5a2 2 0 0 1-2-2Z"/><path d="M9 18V9"/><path d="M15 6h5v4h-5z" fill="#fff"/><path d="M15 6V4"/></svg>',
    goalFind:
      '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"><ellipse cx="10" cy="5.5" rx="7" ry="2.5"/><path d="M3 5.5v6c0 1.4 3.1 2.5 7 2.5"/><path d="M3 11.5v5c0 1.4 3.1 2.5 7 2.5"/><circle cx="17" cy="15" r="3.4"/><path d="M19.5 17.5 22 20"/></svg>',
    navGrid:
      '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/></svg>',
    navChart:
      '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M4 20V4M4 20h16"/><path d="M8 16l4-5 3 3 4-6"/></svg>',
    navList:
      '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"><path d="M8 6h13M8 12h13M8 18h13M3.5 6h.01M3.5 12h.01M3.5 18h.01"/></svg>',
    navGear:
      '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M5 5l2 2M17 17l2 2M19 5l-2 2M7 17l-2 2"/></svg>',
    filter:
      '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/></svg>',
    sort:
      '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 6h18M7 12h10M11 18h2"/></svg>',
    fileSpreadsheet:
      '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round" stroke-linecap="round">' +
      '<path d="M6 2h8l4 4v16H6Z"/><path d="M14 2v4h4"/>' +
      '<rect x="8" y="11" width="8" height="7" rx="0.5"/>' +
      '<line x1="11.5" y1="11" x2="11.5" y2="18"/>' +
      '<line x1="8" y1="14.5" x2="16" y2="14.5"/>' +
      '</svg>'
  };

  /* ---------- state ---------- */
  var db = {};                 // loaded json
  var initById = {};           // initiative lookup (mutable uiStatus)
  var state = {
    activeTab: 'foryou',
    fyPage: 'list',            // 'list' | initiativeId
    fyItems: [],               // remaining For You items (objects)
    report: 'awaiting',        // 'awaiting' | 'inprogress' | 'ready'
    wire: null                 // null | {type:'initiative'|'report', title}
  };
  var root;
  var reportTimer = null;      // pending "report generating → ready" timeout
  var wireTypingTimer = null;  // pending 1s delay before wire-panel message types in
  var sliding = false;         // prevents double-navigation during slide animation

  /* ---------- helpers ---------- */
  function el(html) { var t = document.createElement('template'); t.innerHTML = html.trim(); return t.content.firstChild; }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;' }[c]; }); }
  function skelLines(widths) {
    var d = el('<div style="display:flex;flex-direction:column;gap:8px"></div>');
    widths.forEach(function(w) { d.appendChild(el('<div class="av-skel" style="width:' + w + '%"></div>')); });
    return d;
  }
  function firstName(n) { return String(n).split(' ')[0]; }
  function fmtDate(ts) { return String(ts).slice(0, 10); }

  // derive the brief's 3-state status from the two-axis data model
  function uiStatus(init) {
    if (init.blocked === true) return 'blocked';
    if (init.dataStatus === 'pending_review') return 'ready';
    return 'uptodate'; // up_to_date OR awaiting_data (collapsed, per plan §2 / review)
  }
  function statusMeta(s) {
    if (s === 'ready') return { cls: 'st-ready', label: 'Ready for review' };
    if (s === 'blocked') return { cls: 'st-blocked', label: 'Blocked' };
    return { cls: 'st-uptodate', label: 'Up to date' };
  }
  function statusPill(s) {
    var m = statusMeta(s);
    return '<span class="av-status ' + m.cls + '"><span class="dot"></span>' + m.label + '</span>';
  }

  // ONE source of truth for "the current report" — never by array position
  function currentReport() {
    var rs = db.reports.reports;
    return rs.filter(function (r) { return r.needsReview === true; })[0] ||
           rs.filter(function (r) { return r.id === '2026-09'; })[0] || rs[0];
  }

  /* ============================================================
     CHART
  ============================================================ */
  function buildChart() {
    // Honest, data-grounded rebuild (see md/act-view-chart-brief.md): plots the
    // REAL numbers from trajectory.json — target (all 12 months), actual (Jan–Sep),
    // forecast (Oct–Dec), and the per-month delta (actual/forecast vs target) — on
    // a y-axis derived from the data at render time, with one continuous red overage
    // fill and curved (Catmull-Rom) trend lines. The SVG is RE-RENDERED to the
    // container's real pixel width (see draw()/ResizeObserver below) rather than
    // scaled with preserveAspectRatio="none", so dots stay perfect circles and text
    // never stretches when the window is resized.
    var all = db.trajectory.monthly;                 // all 12 months, Jan→Dec
    // upper edge of the red zone = whatever's real this month (actual, else forecast)
    all.forEach(function (d) { d._upper = (d.actual != null) ? d.actual : d.forecast; });
    // "current month" = last month with a real actual (Sep here) — drives the
    // x-axis highlight AND the "Now" boundary, computed once and shared.
    var curIdx = 0;
    all.forEach(function (d, i) { if (d.actual != null) curIdx = i; });
    var cur = all[curIdx];

    // ---- stat block — CUMULATIVE actual across every month with real data, and
    // that same running total compared against the cumulative target (the honest
    // headline: total emitted so far vs. where the plan said we'd be).
    var sumActual = 0, sumTarget = 0;
    all.forEach(function (d) { if (d.actual != null) { sumActual += d.actual; sumTarget += d.target; } });
    var vs = ((sumActual - sumTarget) / sumTarget) * 100;
    var vsCls = vs >= 0 ? 'pol-pos' : 'pol-neg';
    var vsTxt = (vs >= 0 ? '+' : '') + vs.toFixed(1) + '% vs. target';
    var stats =
      '<div class="av-chart-stats">' +
      '<div class="av-stat-total">' + Math.round(sumActual).toLocaleString() + ' tCO2e</div>' +
      '<div class="av-stat-sub"><span class="av-stat-count">' + db.initiatives.initiatives.length + ' initiatives</span>' +
      '<span class="av-stat-vs ' + vsCls + '">' + vsTxt + '</span></div></div>';

    // ---- legend (top-right, quiet) — line-swatches matching each stroke style,
    // so the Forecast key is visibly dashed and the Gap key is a vertical tick.
    // swatches mirror the plotted series exactly: 1px strokes, matching dash/opacity,
    // and the same white-filled dot with a series-coloured 1px outline.
    var legend =
      '<div class="av-legend">' +
      '<span class="av-lg"><svg width="20" height="8"><line x1="1" y1="4" x2="19" y2="4" stroke="#283fff" stroke-width="1"/><circle cx="10" cy="4" r="2.4" fill="#fff" stroke="#283fff" stroke-width="1"/></svg>Target</span>' +
      '<span class="av-lg"><svg width="20" height="8"><line x1="1" y1="4" x2="19" y2="4" stroke="#16181d" stroke-width="1"/><circle cx="10" cy="4" r="2.4" fill="#fff" stroke="#16181d" stroke-width="1"/></svg>Actual</span>' +
      '<span class="av-lg"><svg width="20" height="8"><line x1="1" y1="4" x2="19" y2="4" stroke="#16181d" stroke-width="1" stroke-dasharray="4 4" opacity="0.55"/><circle cx="10" cy="4" r="2.4" fill="#fff" stroke="#16181d" stroke-width="1" opacity="0.7"/></svg>Forecast</span>' +
      '<span class="av-lg"><svg width="20" height="8"><line x1="10" y1="1" x2="10" y2="7" stroke="#ff383c" stroke-width="1.5" opacity="0.5"/></svg>Gap vs. target</span>' +
      '</div>';

    var card = el(
      '<div class="av-chart-card"><div class="av-chart-wrap">' + stats + legend +
      '<svg class="av-chart-svg"></svg><div class="av-tooltip" id="av-tt"></div></div></div>'
    );
    var wrap = card.querySelector('.av-chart-wrap');
    var svgEl = card.querySelector('.av-chart-svg');
    var tt = card.querySelector('#av-tt');

    var VBH = 260;               // fixed pixel height; width tracks the container
    var geom = null;             // {X, Y, x0, x1, y0, y1} — shared with the hover code

    // ---- Catmull-Rom → cubic-Bézier smoothing. pts = [[x,y],...].
    function segs(pts) {
      var s = '';
      for (var i = 0; i < pts.length - 1; i++) {
        var p0 = pts[i - 1] || pts[i], p1 = pts[i], p2 = pts[i + 1], p3 = pts[i + 2] || p2;
        var c1x = p1[0] + (p2[0] - p0[0]) / 6, c1y = p1[1] + (p2[1] - p0[1]) / 6;
        var c2x = p2[0] - (p3[0] - p1[0]) / 6, c2y = p2[1] - (p3[1] - p1[1]) / 6;
        s += 'C' + c1x + ',' + c1y + ' ' + c2x + ',' + c2y + ' ' + p2[0] + ',' + p2[1] + ' ';
      }
      return s;
    }
    function curve(pts) { return 'M' + pts[0][0] + ',' + pts[0][1] + ' ' + segs(pts); }

    // Render the whole plot for a given pixel width. Called once on mount and again
    // on every width change — viewBox width == pixel width, so scaling is always 1:1.
    function draw(VBW) {
      // Below ~520px the 4-item legend can't share the top row with the stat block,
      // so we drop it onto its own wrapped row beneath the headline (see the
      // .av-chart-narrow rules in CSS) and grow the top margin to clear it. This is
      // container-width driven, not viewport-driven, so it also fixes the squeezed
      // two-column case where a media query would never fire.
      var narrow = VBW < 520;
      wrap.classList.toggle('av-chart-narrow', narrow);
      // mT clears the top-left stat overlay (~39px tall) AND leaves a 30px stat→chart
      // gap above the plot (see .av-chart-stats CSS). mL clears the y-axis labels.
      var mL = 46, mR = 16, mT = narrow ? 96 : 69, mB = 26;
      var x0 = mL, x1 = VBW - mR, y0 = mT, y1 = VBH - mB;
      var step = (x1 - x0) / (all.length - 1);
      function X(i) { return x0 + i * step; }

      // ---- y-axis: 5 "nice" gridlines derived from the real min/max, with
      // headroom on both ends. NOT forced to zero (trend chart — the story is the
      // shape and the gap, not distance from an origin).
      var vals = [];
      all.forEach(function (d) {
        vals.push(d.target);
        if (d.actual != null) vals.push(d.actual);
        if (d.forecast != null) vals.push(d.forecast);
      });
      var dMin = Math.min.apply(null, vals), dMax = Math.max.apply(null, vals);
      var raw = (dMax - dMin) / 3;
      var mag = Math.pow(10, Math.floor(Math.log10(raw)));
      var norm = raw / mag;
      var nice = norm <= 1 ? 1 : norm <= 1.5 ? 1.5 : norm <= 2 ? 2 : norm <= 2.5 ? 2.5 : norm <= 5 ? 5 : 10;
      var gStep = nice * mag;
      var gMin = Math.floor(dMin / gStep) * gStep;
      var gMax = gMin + gStep * 4;
      while (gMax < dMax) { gMax += gStep; }          // safety net (shouldn't trigger)
      function Y(v) { return y1 - (v - gMin) / (gMax - gMin) * (y1 - y0); }

      // ---- gridlines + right-aligned labels, top→bottom, same visual rhythm
      var g = '';
      for (var gv = gMax; gv >= gMin - 1; gv -= gStep) {
        var gy = Y(gv);
        g += '<line class="av-grid-line" x1="' + x0 + '" y1="' + gy + '" x2="' + x1 + '" y2="' + gy + '"/>';
        var lbl = gv >= 1000 ? (Math.round(gv / 100) / 10) + 'k' : String(gv);
        g += '<text class="av-grid-label" x="' + (x0 - 8) + '" y="' + (gy + 3) + '" text-anchor="end">' + lbl + '</text>';
      }

      // ---- x labels — current month (Sep) highlighted, the rest quiet
      var xl = '';
      all.forEach(function (d, i) {
        var hiCls = i === curIdx ? ' is-hi' : '';
        xl += '<text class="av-x-label' + hiCls + '" x="' + X(i) + '" y="' + (y1 + 16) + '">' + d.label + '</text>';
      });

      // point sets
      var targetPts = all.map(function (d, i) { return [X(i), Y(d.target)]; });
      var upperPts  = all.map(function (d, i) { return [X(i), Y(d._upper)]; });
      var actualPts = [], forePts = [];
      all.forEach(function (d, i) { if (d.actual != null) actualPts.push([X(i), Y(d.actual)]); });
      // forecast path PREPENDS the current-month actual point so the dashed line
      // continues seamlessly from where the solid actual line ends (no gap/jump).
      forePts.push([X(curIdx), Y(cur.actual)]);
      all.forEach(function (d, i) { if (d.forecast != null) forePts.push([X(i), Y(d.forecast)]); });

      // ---- red zone: ONE continuous shape, actual-vs-target (Jan–Sep) then
      // forecast-vs-target (Oct–Dec), upper edge = smoothed _upper curve, lower
      // edge = smoothed target curve walked back.
      var down = targetPts.slice().reverse();
      var area = curve(upperPts) + 'L' + down[0][0] + ',' + down[0][1] + ' ' + segs(down) + 'Z';

      var yTop = Math.min.apply(null, upperPts.map(function (p) { return p[1]; }));
      var yBot = Math.max.apply(null, targetPts.map(function (p) { return p[1]; }));

      // ---- delta: a vertical connector at each month from the target point up to
      // the actual/forecast point — the literal per-month gap, plotted as a series.
      var dl = '';
      all.forEach(function (d, i) {
        if (d._upper == null) return;                 // no actual/forecast → no gap to draw
        var yt = Y(d.target), yu = Y(d._upper);
        if (Math.abs(yt - yu) < 0.5) return;
        dl += '<line class="av-delta-line" x1="' + X(i) + '" y1="' + yt + '" x2="' + X(i) + '" y2="' + yu + '"/>';
      });

      // ---- markers
      var mk = '';
      targetPts.forEach(function (p) { mk += '<circle class="av-pt av-pt-target" cx="' + p[0] + '" cy="' + p[1] + '" r="4"/>'; });
      actualPts.forEach(function (p) { mk += '<circle class="av-pt av-pt-actual" cx="' + p[0] + '" cy="' + p[1] + '" r="4"/>'; });
      // hollow forecast markers — skip index 0 (that's the shared Sep actual dot)
      forePts.slice(1).forEach(function (p) { mk += '<circle class="av-pt-forecast" cx="' + p[0] + '" cy="' + p[1] + '" r="4"/>'; });

      // ---- "Now" boundary — quiet dashed vertical at the actual/forecast handoff
      var nowX = X(curIdx);
      var nowMarker =
        '<line class="av-now-line" x1="' + nowX + '" y1="' + y0 + '" x2="' + nowX + '" y2="' + y1 + '"/>' +
        '<text class="av-now-label" x="' + (nowX + 4) + '" y="' + (y0 + 9) + '">Now</text>';

      var defs =
        '<defs><linearGradient id="av-overage-grad" gradientUnits="userSpaceOnUse" x1="0" y1="' + yTop + '" x2="0" y2="' + yBot + '">' +
        '<stop offset="0" stop-color="#ff383c" stop-opacity="0.20"/>' +
        '<stop offset="0.75" stop-color="#ff383c" stop-opacity="0.05"/>' +
        '<stop offset="1" stop-color="#ff383c" stop-opacity="0"/>' +
        '</linearGradient></defs>';

      svgEl.setAttribute('viewBox', '0 0 ' + VBW + ' ' + VBH);
      svgEl.innerHTML =
        defs + g + nowMarker +
        '<path class="av-overage" d="' + area + '"/>' + dl +
        '<path class="av-line-target" d="' + curve(targetPts) + '"/>' +
        '<path class="av-line-forecast" d="' + curve(forePts) + '"/>' +
        '<path class="av-line-actual" d="' + curve(actualPts) + '"/>' +
        mk +
        '<line class="av-hover-guide" id="av-guide" x1="0" y1="' + y0 + '" x2="0" y2="' + y1 + '" style="opacity:0"/>' +
        '<circle class="av-hover-dot" id="av-dot-t" r="4" fill="#283fff" style="opacity:0"/>' +
        '<circle class="av-hover-dot" id="av-dot-a" r="4" fill="#16181d" style="opacity:0"/>' +
        '<rect id="av-hit" x="' + x0 + '" y="' + y0 + '" width="' + (x1 - x0) + '" height="' + (y1 - y0) + '" fill="transparent" style="cursor:crosshair"/>' +
        xl;

      geom = { X: X, Y: Y, x0: x0, x1: x1, y0: y0, y1: y1 };
      bindHover();
    }

    // ---- hover (rAF-throttled; attribute updates only). Re-bound after each draw()
    // because innerHTML replaces the hit-rect/guide/dots. Coordinates are pixels
    // (viewBox == pixel size), so the tooltip maps svg units → wrap offset 1:1.
    function bindHover() {
      var hit = svgEl.querySelector('#av-hit');
      var guide = svgEl.querySelector('#av-guide');
      var dotT = svgEl.querySelector('#av-dot-t');
      var dotA = svgEl.querySelector('#av-dot-a');
      var raf = null, lastEvt = null;

      function apply() {
        var e = lastEvt, gm = geom;
        var r = hit.getBoundingClientRect();
        var frac = (e.clientX - r.left) / r.width;
        var i = Math.max(0, Math.min(all.length - 1, Math.round(frac * (all.length - 1))));
        var d = all[i];
        var gx = gm.X(i), uy = gm.Y(d._upper);
        var isFore = d.actual == null;                // Oct–Dec are forecast slots
        guide.setAttribute('x1', gx); guide.setAttribute('x2', gx); guide.style.opacity = 1;
        dotT.setAttribute('cx', gx); dotT.setAttribute('cy', gm.Y(d.target)); dotT.style.opacity = 1;
        // the upper dot borrows the forecast (hollow) or actual (filled ink) look
        dotA.setAttribute('cx', gx); dotA.setAttribute('cy', uy);
        dotA.setAttribute('fill', isFore ? '#fff' : '#16181d');
        dotA.setAttribute('stroke', isFore ? '#16181d' : '#fff');
        dotA.style.opacity = 1;

        var delta = d._upper - d.target;
        tt.innerHTML =
          '<div class="av-tt-month">' + d.label + '</div>' +
          '<div class="av-tt-row"><span class="dot" style="background:#16181d' + (isFore ? ';outline:1px solid #16181d;background:#fff' : '') + '"></span>' +
          '<span class="lbl">' + (isFore ? 'Forecast' : 'Actual') + '</span>' +
          '<span class="val">' + d._upper.toLocaleString() + ' tCO2e</span></div>' +
          '<div class="av-tt-row"><span class="dot" style="background:#283fff"></span><span class="lbl">Target</span>' +
          '<span class="val">' + d.target.toLocaleString() + ' tCO2e</span></div>' +
          '<div class="av-tt-row"><span class="dot" style="background:#ff383c"></span><span class="lbl">Gap</span>' +
          '<span class="val">' + (delta >= 0 ? '+' : '') + delta.toLocaleString() + ' tCO2e</span></div>';
        // gx / min(...) are already pixels in the svg's own box == wrap's box
        tt.style.left = gx + 'px';
        tt.style.top = Math.min(gm.Y(d.target), uy) + 'px';
        tt.classList.add('is-on');
      }
      hit.addEventListener('mousemove', function (e) {
        lastEvt = e;
        if (raf) return;
        raf = requestAnimationFrame(function () { raf = null; apply(); });
      });
      hit.addEventListener('mouseleave', function () {
        if (raf) { cancelAnimationFrame(raf); raf = null; }
        tt.classList.remove('is-on'); guide.style.opacity = 0; dotT.style.opacity = 0; dotA.style.opacity = 0;
      });
    }

    // Track the container's real width and redraw on change. viewBox width is set
    // to that pixel width so 1 user unit == 1px — circles stay round, glyphs keep
    // their aspect. rAF fallback covers the first paint (and browsers without RO).
    var lastW = 0;
    function sync(w) { w = Math.round(w); if (w > 0 && w !== lastW) { lastW = w; draw(w); } }
    if (typeof ResizeObserver !== 'undefined') {
      new ResizeObserver(function (entries) {
        sync(entries[entries.length - 1].contentRect.width);
      }).observe(wrap);
    }
    requestAnimationFrame(function () { sync(wrap.getBoundingClientRect().width); });

    return card;
  }

  /* ============================================================
     INITIATIVE CHART (same visual style as main chart, no forecast)
  ============================================================ */
  function buildInitiativeChart(init) {
    var all = init.monthly.slice();
    var curIdx = 0;
    all.forEach(function(d, i) { if (d.actual != null) curIdx = i; });

    var pctVal = init.percentVsTarget;
    var pctStr = (pctVal >= 0 ? '+' : '') + pctVal + '% vs. target';
    var vsCls = pctVal >= 0 ? 'pol-pos' : 'pol-neg';
    var stats =
      '<div class="av-chart-stats">' +
      '<div class="av-stat-total">' + init.current.toLocaleString() + ' tCO2e</div>' +
      '<div class="av-stat-sub"><span class="av-stat-count">Sep 2026</span>' +
      '<span class="av-stat-vs ' + vsCls + '">' + pctStr + '</span></div></div>';

    var legend =
      '<div class="av-legend">' +
      '<span class="av-lg"><svg width="20" height="8"><line x1="1" y1="4" x2="19" y2="4" stroke="#283fff" stroke-width="1"/><circle cx="10" cy="4" r="2.4" fill="#fff" stroke="#283fff" stroke-width="1"/></svg>Target</span>' +
      '<span class="av-lg"><svg width="20" height="8"><line x1="1" y1="4" x2="19" y2="4" stroke="#16181d" stroke-width="1"/><circle cx="10" cy="4" r="2.4" fill="#fff" stroke="#16181d" stroke-width="1"/></svg>Actual</span>' +
      '<span class="av-lg"><svg width="20" height="8"><line x1="10" y1="1" x2="10" y2="7" stroke="#ff383c" stroke-width="1.5" opacity="0.5"/></svg>Gap vs. target</span>' +
      '</div>';

    var card = el(
      '<div class="av-chart-card"><div class="av-chart-wrap">' + stats + legend +
      '<svg class="av-chart-svg"></svg><div class="av-tooltip" id="av-tt-init"></div></div></div>'
    );
    var wrap = card.querySelector('.av-chart-wrap');
    var svgEl = card.querySelector('.av-chart-svg');
    var tt = card.querySelector('#av-tt-init');
    var VBH = 260;
    var geom = null;

    function segs(pts) {
      var s = '';
      for (var i = 0; i < pts.length - 1; i++) {
        var p0 = pts[i - 1] || pts[i], p1 = pts[i], p2 = pts[i + 1], p3 = pts[i + 2] || p2;
        var c1x = p1[0] + (p2[0] - p0[0]) / 6, c1y = p1[1] + (p2[1] - p0[1]) / 6;
        var c2x = p2[0] - (p3[0] - p1[0]) / 6, c2y = p2[1] - (p3[1] - p1[1]) / 6;
        s += 'C' + c1x + ',' + c1y + ' ' + c2x + ',' + c2y + ' ' + p2[0] + ',' + p2[1] + ' ';
      }
      return s;
    }
    function curve(pts) { return 'M' + pts[0][0] + ',' + pts[0][1] + ' ' + segs(pts); }

    function draw(VBW) {
      // Same container-aware collapse as the main chart — the 3-item legend drops
      // beneath the headline and the top margin grows to clear it (see CSS).
      var narrow = VBW < 460;
      wrap.classList.toggle('av-chart-narrow', narrow);
      var mL = 46, mR = 16, mT = narrow ? 96 : 69, mB = 26;
      var x0 = mL, x1 = VBW - mR, y0 = mT, y1 = VBH - mB;
      var step = (x1 - x0) / (all.length - 1);
      function X(i) { return x0 + i * step; }

      var vals = [];
      all.forEach(function(d) { vals.push(d.target); if (d.actual != null) vals.push(d.actual); });
      var dMin = Math.min.apply(null, vals), dMax = Math.max.apply(null, vals);
      var raw = (dMax - dMin) / 3;
      var mag = Math.pow(10, Math.floor(Math.log10(raw)));
      var norm = raw / mag;
      var nice = norm <= 1 ? 1 : norm <= 1.5 ? 1.5 : norm <= 2 ? 2 : norm <= 2.5 ? 2.5 : norm <= 5 ? 5 : 10;
      var gStep = nice * mag;
      var gMin = Math.floor(dMin / gStep) * gStep;
      var gMax = gMin + gStep * 4;
      while (gMax < dMax) { gMax += gStep; }
      function Y(v) { return y1 - (v - gMin) / (gMax - gMin) * (y1 - y0); }

      var g = '';
      for (var gv = gMax; gv >= gMin - 1; gv -= gStep) {
        var gy = Y(gv);
        g += '<line class="av-grid-line" x1="' + x0 + '" y1="' + gy + '" x2="' + x1 + '" y2="' + gy + '"/>';
        var lbl = gv >= 1000 ? (Math.round(gv / 100) / 10) + 'k' : String(Math.round(gv));
        g += '<text class="av-grid-label" x="' + (x0 - 8) + '" y="' + (gy + 3) + '" text-anchor="end">' + lbl + '</text>';
      }

      var xl = '';
      all.forEach(function(d, i) {
        var hiCls = i === curIdx ? ' is-hi' : '';
        xl += '<text class="av-x-label' + hiCls + '" x="' + X(i) + '" y="' + (y1 + 16) + '">' + d.label + '</text>';
      });

      var targetPts = all.map(function(d, i) { return [X(i), Y(d.target)]; });
      var actualPts = [];
      all.forEach(function(d, i) { if (d.actual != null) actualPts.push([X(i), Y(d.actual)]); });

      var targetSlice = targetPts.slice(0, actualPts.length);
      var down = targetSlice.slice().reverse();
      var area = curve(actualPts) + 'L' + down[0][0] + ',' + down[0][1] + ' ' + segs(down) + 'Z';

      var yTop = Math.min.apply(null, actualPts.map(function(p) { return p[1]; }));
      var yBot = Math.max.apply(null, targetSlice.map(function(p) { return p[1]; }));

      var dl = '';
      all.forEach(function(d, i) {
        if (d.actual == null) return;
        var yt = Y(d.target), ya = Y(d.actual);
        if (Math.abs(yt - ya) < 0.5) return;
        dl += '<line class="av-delta-line" x1="' + X(i) + '" y1="' + yt + '" x2="' + X(i) + '" y2="' + ya + '"/>';
      });

      var mk = '';
      targetPts.forEach(function(p) { mk += '<circle class="av-pt av-pt-target" cx="' + p[0] + '" cy="' + p[1] + '" r="4"/>'; });
      actualPts.forEach(function(p) { mk += '<circle class="av-pt av-pt-actual" cx="' + p[0] + '" cy="' + p[1] + '" r="4"/>'; });

      var nowX = X(curIdx);
      var nowMarker =
        '<line class="av-now-line" x1="' + nowX + '" y1="' + y0 + '" x2="' + nowX + '" y2="' + y1 + '"/>' +
        '<text class="av-now-label" x="' + (nowX + 4) + '" y="' + (y0 + 9) + '">Now</text>';

      var defs =
        '<defs><linearGradient id="av-init-grad" gradientUnits="userSpaceOnUse" x1="0" y1="' + yTop + '" x2="0" y2="' + yBot + '">' +
        '<stop offset="0" stop-color="#ff383c" stop-opacity="0.20"/>' +
        '<stop offset="0.75" stop-color="#ff383c" stop-opacity="0.05"/>' +
        '<stop offset="1" stop-color="#ff383c" stop-opacity="0"/>' +
        '</linearGradient></defs>';

      svgEl.setAttribute('viewBox', '0 0 ' + VBW + ' ' + VBH);
      svgEl.innerHTML =
        defs + g + nowMarker +
        '<path style="fill:url(#av-init-grad);stroke:none" d="' + area + '"/>' + dl +
        '<path class="av-line-target" d="' + curve(targetPts) + '"/>' +
        '<path class="av-line-actual" d="' + curve(actualPts) + '"/>' + mk +
        '<line class="av-hover-guide" id="av-guide-init" x1="0" y1="' + y0 + '" x2="0" y2="' + y1 + '" style="opacity:0"/>' +
        '<circle class="av-hover-dot" id="av-dot-init-t" r="4" fill="#283fff" style="opacity:0"/>' +
        '<circle class="av-hover-dot" id="av-dot-init-a" r="4" fill="#16181d" style="opacity:0"/>' +
        '<rect id="av-hit-init" x="' + x0 + '" y="' + y0 + '" width="' + (x1 - x0) + '" height="' + (y1 - y0) + '" fill="transparent" style="cursor:crosshair"/>' +
        xl;

      geom = { X: X, Y: Y, x0: x0, x1: x1, y0: y0, y1: y1 };
      bindInitHover();
    }

    function bindInitHover() {
      var hit = svgEl.querySelector('#av-hit-init');
      var guide = svgEl.querySelector('#av-guide-init');
      var dotT = svgEl.querySelector('#av-dot-init-t');
      var dotA = svgEl.querySelector('#av-dot-init-a');
      var raf = null, lastEvt = null;
      function apply() {
        var e = lastEvt, gm = geom;
        var r = hit.getBoundingClientRect();
        var frac = (e.clientX - r.left) / r.width;
        var i = Math.max(0, Math.min(all.length - 1, Math.round(frac * (all.length - 1))));
        var d = all[i];
        if (d.actual == null) { guide.style.opacity = 0; dotT.style.opacity = 0; dotA.style.opacity = 0; tt.classList.remove('is-on'); return; }
        var gx = gm.X(i), ya = gm.Y(d.actual);
        guide.setAttribute('x1', gx); guide.setAttribute('x2', gx); guide.style.opacity = 1;
        dotT.setAttribute('cx', gx); dotT.setAttribute('cy', gm.Y(d.target)); dotT.style.opacity = 1;
        dotA.setAttribute('cx', gx); dotA.setAttribute('cy', ya); dotA.style.opacity = 1;
        var delta = d.actual - d.target;
        tt.innerHTML =
          '<div class="av-tt-month">' + d.label + '</div>' +
          '<div class="av-tt-row"><span class="dot" style="background:#16181d"></span><span class="lbl">Actual</span><span class="val">' + d.actual.toLocaleString() + ' tCO2e</span></div>' +
          '<div class="av-tt-row"><span class="dot" style="background:#283fff"></span><span class="lbl">Target</span><span class="val">' + d.target.toLocaleString() + ' tCO2e</span></div>' +
          '<div class="av-tt-row"><span class="dot" style="background:#ff383c"></span><span class="lbl">Gap</span><span class="val">' + (delta >= 0 ? '+' : '') + delta.toLocaleString() + ' tCO2e</span></div>';
        tt.style.left = gx + 'px';
        tt.style.top = Math.min(gm.Y(d.target), ya) + 'px';
        tt.classList.add('is-on');
      }
      hit.addEventListener('mousemove', function(e) {
        lastEvt = e; if (raf) return;
        raf = requestAnimationFrame(function() { raf = null; apply(); });
      });
      hit.addEventListener('mouseleave', function() {
        if (raf) { cancelAnimationFrame(raf); raf = null; }
        tt.classList.remove('is-on'); guide.style.opacity = 0; dotT.style.opacity = 0; dotA.style.opacity = 0;
      });
    }

    var lastW = 0;
    function sync(w) { w = Math.round(w); if (w > 0 && w !== lastW) { lastW = w; draw(w); } }
    if (typeof ResizeObserver !== 'undefined') {
      new ResizeObserver(function(entries) { sync(entries[entries.length - 1].contentRect.width); }).observe(wrap);
    }
    requestAnimationFrame(function() { sync(wrap.getBoundingClientRect().width); });
    return card;
  }

  /* ============================================================
     REPORT TILE
  ============================================================ */
  function reportTile() {
    var chip;
    if (state.report === 'awaiting')
      chip = '<span class="av-report-chip chip-awaiting"><span class="dot"></span>Awaiting data</span>';
    else if (state.report === 'inprogress')
      chip = '<span class="av-report-chip chip-progress"><span class="av-spinner"></span>In progress…</span>';
    else
      chip = '<span class="av-report-chip chip-ready">Report ready</span>';

    var readyCls = state.report === 'ready' ? ' is-ready' : '';
    var cur = currentReport();
    var cycle = MONTHS[cur.month - 1] + ' ' + cur.year;
    var isReady = state.report === 'ready';
    var tile = el(
      '<div class="av-report-tile' + readyCls + '"' + (isReady ? ' data-act="open-report"' : '') + '>' +
      '<div class="av-report-globe">' + I.globe + '</div>' +
      '<div class="av-report-mid"><div class="av-report-title">Monthly reports</div>' +
      '<div class="av-report-cycle-row"><div class="av-report-cycle">Current cycle: ' + cycle + '</div>' +
      chip + '</div></div>' +
      '<span class="av-report-arrow">' + I.reportArrow + '</span>' +
      '</div>'
    );
    tile.style.cursor = isReady ? 'pointer' : 'default';
    return tile;
  }

  /* ============================================================
     INITIATIVES GRID
  ============================================================ */
  function initiativeCard(init) {
    var s = init.uiStatus;
    var scope = init.scope.replace('Scope ', 'S'); // "Scope 3" -> "S3"
    var pct = init.percentVsTarget;
    var polCls = pct >= 0 ? 'pol-pos' : 'pol-neg';
    var polNum = (pct >= 0 ? '+' : '') + pct + '%';
    var card = el(
      '<div class="av-card" data-act="open-initiative" data-id="' + init.id + '">' +
      '<div class="av-card-photo" style="background-image:url(\'' + esc(init.image) + '\')">' +
      '<span class="av-scope-chip">' + scope + '</span></div>' +
      '<div class="av-card-body">' +
      statusPill(s) +
      '<div class="av-card-title">' + esc(init.shortName) + '</div>' +
      '<div class="av-card-spacer"></div>' +
      '<div class="av-card-owner">' + esc(init.owner.name) + ' · ' + esc(init.owner.department) + '</div>' +
      '<div class="av-card-change"><span class="' + polCls + '">' + polNum + '</span> vs. YTD target</div>' +
      '</div></div>'
    );
    return card;
  }

  function initiativesGrid() {
    // margin-top doubles the 22px main-column gap between the act panel's bottom
    // edge and the "Initiatives" label (→44px), mirroring the "Act" title → chart
    // heading spacing above.
    var wrap = el('<div style="margin-top:22px"></div>');
    var head = el(
      '<div class="av-init-head"><div class="av-section-title">All actions</div>' +
      '<div style="display:flex;gap:8px">' +
      '<button class="av-btn-outline" style="cursor:default;display:inline-flex;align-items:center;gap:5px">' + I.filter + 'Filter</button>' +
      '<button class="av-btn-outline" style="cursor:default;display:inline-flex;align-items:center;gap:5px">' + I.sort + 'Sort: Status</button>' +
      '</div></div>'
    );
    var grid = el('<div class="av-grid"></div>');
    // Base order: Figma reading order for the documented cards, then the rest in data order.
    var ORDER = ['offgrid-solar', 'network-site-efficiency', 'sustainable-packaging',
                 'cloud-migration', 'backup-power-transition', 'business-travel'];
    var ordered = ORDER.map(function (id) { return initById[id]; }).filter(Boolean);
    db.initiatives.initiatives.forEach(function (init) {
      if (ORDER.indexOf(init.id) === -1) ordered.push(init);
    });
    // Sorted by status: the three actions surfaced in the For You panel lead —
    // Ready for review first, then the two Blocked in the panel's own order —
    // and everything Up to date follows in its existing order (stable sort).
    var FY_ORDER = ['offgrid-solar', 'handset-takeback', 'sustainable-packaging'];
    function statusRank(s) { return s === 'ready' ? 0 : s === 'blocked' ? 1 : 2; }
    ordered.sort(function (a, b) {
      var d = statusRank(a.uiStatus) - statusRank(b.uiStatus);
      if (d !== 0) return d;
      var fa = FY_ORDER.indexOf(a.id), fb = FY_ORDER.indexOf(b.id);
      if (fa !== -1 && fb !== -1) return fa - fb;  // keep the two Blocked in panel order
      return 0;
    });
    ordered.forEach(function (init) { grid.appendChild(initiativeCard(init)); });
    // Gallery lives inside a box that matches the act panel above (same bg, border,
    // radius, padding). The "Initiatives" head + "Add new" CTA stay ABOVE, outside
    // this box, keeping the original 14px head→gallery spacing (now head→box).
    var box = el('<div class="av-init-panel"></div>');
    box.appendChild(grid);
    wrap.appendChild(head);
    wrap.appendChild(el('<div style="height:14px"></div>'));
    wrap.appendChild(box);
    return wrap;
  }

  /* ============================================================
     REPORT PAGE (main column)
  ============================================================ */
  function renderReportMain(reportId) {
    var reports = db.reports.reports;
    var report = null;
    for (var i = 0; i < reports.length; i++) { if (reports[i].id === reportId) { report = reports[i]; break; } }
    if (!report) report = reports[0];

    var page = el('<div class="av-rp-page"></div>');

    page.appendChild(el(
      '<div class="av-back-row"><button class="av-back-btn" data-act="close-wire">' + I.back + ' Act</button></div>'
    ));
    page.appendChild(el('<div class="av-page-title" style="margin-bottom:0">Reports</div>'));
    page.appendChild(skelLines([90, 65]));

    var layout = el('<div class="av-rp-layout"></div>');

    var timeline = el('<div class="av-rp-timeline"></div>');
    reports.forEach(function(r) {
      var isActive = r.id === reportId;
      var sub = r.needsReview ? 'Needs review' : (r.reviewedAt ? 'Reviewed ' + r.reviewedAt : '');
      timeline.appendChild(el(
        '<div class="av-rp-month' + (isActive ? ' is-active' : '') + '" data-act="select-report" data-id="' + esc(r.id) + '">' +
        '<div class="av-rp-dot"></div>' +
        '<div class="av-rp-month-info">' +
        '<span class="av-rp-month-label">' + esc(r.label) + '</span>' +
        '<span class="av-rp-month-sub">' + esc(sub) + '</span>' +
        '</div></div>'
      ));
    });
    layout.appendChild(timeline);

    var body = el('<div class="av-rp-body"></div>');

    if (report.needsReview) {
      body.appendChild(el(
        '<div class="av-review-banner">' +
        '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M12 7v6l4 2"/></svg>' +
        '<span>Generated by Sweepy on ' + esc(report.generatedAt.slice(0, 10)) + ' — please review and finalise.</span>' +
        '<button class="av-rp-btn av-rp-btn--primary" style="margin-left:auto;cursor:default">Review &amp; finalise</button>' +
        '</div>'
      ));
    } else if (report.reviewedBy) {
      body.appendChild(el(
        '<div class="av-reviewed-pill">' +
        '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 6 9 17l-5-5"/></svg>' +
        ' Reviewed by ' + esc(report.reviewedBy) + ' · ' + esc(report.reviewedAt) +
        '</div>'
      ));
    }

    body.appendChild(el('<span class="av-rp-eyebrow">' + esc(report.label) + ' · generated by Sweepy</span>'));
    body.appendChild(el('<h2 class="av-rp-headline">' + esc(report.headline) + '</h2>'));
    body.appendChild(skelLines([100, 88, 70]));
    body.appendChild(el(
      '<div class="av-rp-actions">' +
      '<button class="av-rp-btn" style="cursor:default">Download PDF</button>' +
      '<button class="av-rp-btn av-rp-btn--primary" style="cursor:default">Send to leadership</button>' +
      '</div>'
    ));
    body.appendChild(buildChart());

    var s = report.stats;
    body.appendChild(el(
      '<div class="av-rp-stat-row">' +
      '<div class="av-rp-stat"><span class="av-rp-stat-val">' + s.onTrack + '</span><span class="av-rp-stat-lbl">On track</span></div>' +
      '<div class="av-rp-stat"><span class="av-rp-stat-val">' + s.atRisk + '</span><span class="av-rp-stat-lbl">At risk</span></div>' +
      '<div class="av-rp-stat"><span class="av-rp-stat-val">' + s.stalled + '</span><span class="av-rp-stat-lbl">Stalled</span></div>' +
      '<div class="av-rp-stat"><span class="av-rp-stat-val">' + s.dataOverdue + '</span><span class="av-rp-stat-lbl">Awaiting data</span></div>' +
      '</div>'
    ));

    var grid = el('<div class="av-rp-grid"></div>');
    var hlCol = el('<div></div>');
    hlCol.appendChild(el('<h4 class="av-rp-col-h">Highlights</h4>'));
    var hlList = el('<ul class="av-rp-list av-rp-list--good"></ul>');
    (report.highlights || []).forEach(function(h) {
      hlList.appendChild(el('<li><strong>' + esc(h.shortName) + '</strong> <span style="color:var(--av-sub)">— ' + esc(h.note) + '</span></li>'));
    });
    hlCol.appendChild(hlList);
    var gapCol = el('<div></div>');
    gapCol.appendChild(el('<h4 class="av-rp-col-h">Gaps &amp; flags</h4>'));
    var gapList = el('<ul class="av-rp-list av-rp-list--bad"></ul>');
    (report.gaps || []).forEach(function(g) {
      gapList.appendChild(el('<li><strong>' + esc(g.shortName) + '</strong> <span style="color:var(--av-sub)">— ' + esc(g.note) + '</span></li>'));
    });
    gapCol.appendChild(gapList);
    grid.appendChild(hlCol);
    grid.appendChild(gapCol);
    body.appendChild(grid);

    layout.appendChild(body);
    page.appendChild(layout);
    return page;
  }

  /* ============================================================
     INITIATIVE / ACTION PAGE (main column)
  ============================================================ */
  function renderInitiativeMain(initId) {
    var init = initById[initId];
    if (!init) return el('<div style="padding:20px;color:var(--av-sub)">Initiative not found.</div>');

    var s = uiStatus(init);
    var m = statusMeta(s);
    var nameParts = (init.owner.name || '').split(' ');
    var initials = (nameParts[0] ? nameParts[0][0] : '') + (nameParts[nameParts.length - 1] ? nameParts[nameParts.length - 1][0] : '');

    var page = el('<div class="av-rp-page"></div>');
    page.appendChild(el(
      '<div class="av-back-row"><button class="av-back-btn" data-act="close-wire">' + I.back + ' Act</button></div>'
    ));

    page.appendChild(el('<h1 class="av-init-page-title">' + esc(init.name) + '</h1>'));
    page.appendChild(el(
      '<div class="av-init-owner-row">' +
      '<span class="av-init-owner-avatar">' + esc(initials.toUpperCase()) + '</span>' +
      '<span class="av-init-owner-name">' + esc(init.owner.name) + ' · ' + esc(init.owner.role) + '</span>' +
      '<span class="av-status ' + m.cls + '"><span class="dot"></span>' + m.label + '</span>' +
      '</div>'
    ));
    page.appendChild(el(
      '<div class="av-init-tags">' +
      '<span class="av-init-tag">' + esc(init.scope) + '</span>' +
      '<span class="av-init-tag">' + esc(init.ghgCategory) + '</span>' +
      '<span class="av-init-tag">Target ' + esc(String(init.targetYear)) + '</span>' +
      '</div>'
    ));

    var ovWrap = el('<div class="av-init-section"></div>');
    ovWrap.appendChild(el('<div class="av-init-section-h">Overview</div>'));
    ovWrap.appendChild(skelLines([100, 90, 85, 68]));
    page.appendChild(ovWrap);

    var flagWrap = el('<div class="av-init-flag-skel"></div>');
    flagWrap.appendChild(skelLines([98, 82, 65]));
    page.appendChild(flagWrap);

    var liveWrap = el('<div class="av-init-section"></div>');
    liveWrap.appendChild(el(
      '<div class="av-live-head">' +
      '<span class="av-live-dot"></span>' +
      '<span class="av-live-head-title">Live data</span>' +
      '<span class="av-live-sub" style="margin-left:8px">as of last confirmed check-in</span>' +
      '</div>'
    ));
    liveWrap.appendChild(buildInitiativeChart(init));
    liveWrap.appendChild(el(
      '<div class="av-init-stat-row">' +
      '<div class="av-init-stat"><span class="av-init-stat-val">' + init.baseline.toLocaleString() + '</span><span class="av-init-stat-lbl">Baseline</span></div>' +
      '<div class="av-init-stat"><span class="av-init-stat-val">' + init.current.toLocaleString() + '</span><span class="av-init-stat-lbl">Current</span></div>' +
      '<div class="av-init-stat"><span class="av-init-stat-val">' + init.target.toLocaleString() + '</span><span class="av-init-stat-lbl">Target ' + esc(String(init.targetYear)) + '</span></div>' +
      '</div>'
    ));
    page.appendChild(liveWrap);

    var tableWrap = el('<div class="av-init-section"></div>');
    var rows = db.activityData ? db.activityData.filter(function(r) { return r.initiativeId === initId; }) : [];
    var periods = [];
    rows.forEach(function(r) { if (periods.indexOf(r.reportingPeriod) === -1) periods.push(r.reportingPeriod); });
    periods.sort(function(a, b) { return b.localeCompare(a); });
    var tableRows = periods[0] ? rows.filter(function(r) { return r.reportingPeriod === periods[0]; }).slice(0, 8) : [];
    var periodLabel = tableRows.length > 0 ? tableRows[0].reportingPeriodLabel : '';
    tableWrap.appendChild(el('<div class="av-data-section-h">Activity data' + (periodLabel ? ' — ' + esc(periodLabel) : '') + '</div>'));
    tableWrap.appendChild(skelLines([100]));
    var tWrap = el('<div class="av-data-table-wrap"></div>');
    var thead = '<thead><tr><th>Site</th><th>Activity</th><th>Data</th><th>Factor</th><th>tCO2e</th><th>Quality</th></tr></thead>';
    var tbody = '<tbody>';
    if (tableRows.length > 0) {
      tableRows.forEach(function(r) {
        var dqCls = r.dataQuality === 'Verified' ? 'av-dq-verified' : 'av-dq-estimated';
        tbody += '<tr><td>' + esc(r.siteId) + '</td><td>' + esc(r.activityType) + '</td>' +
          '<td>' + esc(r.activityData.toLocaleString()) + ' ' + esc(r.activityUnit) + '</td>' +
          '<td>' + esc(String(r.emissionFactor)) + ' ' + esc(r.emissionFactorUnit) + '</td>' +
          '<td>' + esc(r.emissionsTco2e.toFixed(1)) + '</td>' +
          '<td><span class="' + dqCls + '">' + esc(r.dataQuality) + '</span></td></tr>';
      });
    } else {
      tbody += '<tr><td colspan="6" style="color:var(--av-sub);font-style:italic">No activity data available</td></tr>';
    }
    tbody += '</tbody>';
    tWrap.appendChild(el('<table class="av-data-table">' + thead + tbody + '</table>'));
    tableWrap.appendChild(tWrap);
    page.appendChild(tableWrap);

    return page;
  }

  /* ============================================================
     AGENT PANEL
  ============================================================ */
  function tabBar() {
    function t(id, ico) {
      return '<button class="av-tab' + (state.activeTab === id ? ' is-active' : '') + '" data-act="tab" data-tab="' + id + '">' + ico + '</button>';
    }
    return el(
      '<div class="av-tabbar">' + t('foryou', I.foryou) + t('activity', I.activity) + t('goals', I.goals) + t('chat', I.chat) + '</div>'
    );
  }

  // -------- For You --------
  function forYouList() {
    var wrap = el('<div class="av-page"></div>');
    var hasReport = state.report === 'ready';

    if (state.fyItems.length === 0 && !hasReport) {
      wrap.appendChild(el(
        '<div class="av-cleared"><div class="mark">🎉</div>' +
        '<div class="big">Nothing to see here</div>' +
        '<div class="small">You\'re up to date - bravo!</div></div>'
      ));
      return wrap;
    }

    wrap.appendChild(el('<div class="av-panel-h">For you</div>'));
    wrap.appendChild(el('<div class="av-panel-sub">The following actions need your attention:</div>'));
    var list = el('<div class="av-fy-list"></div>');

    state.fyItems.forEach(function (item) {
      var init = initById[item.initiativeId];
      var s = uiStatus(init);
      var m = statusMeta(s);
      var row = el(
        '<div class="av-fy-row' + (cardState === 'shown' ? '' : ' av-fy-pre') + '" data-act="open-item" data-id="' + item.initiativeId + '">' +
        '<span class="av-status ' + m.cls + '"><span class="dot"></span>' + m.label + '</span>' +
        '<div class="av-fy-title">' + esc(init.shortName) + '</div>' +
        '<div class="av-fy-owner">' + esc(item.owner.name) + ' · ' + esc(item.owner.department) + '</div>' +
        '<span class="av-fy-arrow">' + I.reportArrow + '</span>' +
        '</div>'
      );
      list.appendChild(row);
    });

    if (hasReport) {
      var cur = currentReport();
      var monthName = MONTHS[cur.month - 1];
      list.appendChild(el(
        '<div class="av-fy-row is-report' + (cardState === 'shown' ? '' : ' av-fy-pre') + '" data-act="open-report">' +
        '<div class="av-fy-report-inner">' +
          '<div class="av-fy-report-icon-box">' + I.globeCard + '</div>' +
          '<div class="av-fy-report-content">' +
            '<div class="av-fy-report-status"><span class="dot"></span>Ready for review</div>' +
            '<div class="av-fy-report-title">' + monthName + ' report is ready</div>' +
          '</div>' +
        '</div>' +
        '<div class="av-fy-report-goal">' +
          '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#858585" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/></svg>' +
          '<span>Goal: Automate monthly leadership report</span>' +
        '</div>' +
        '</div>'
      ));
    }
    wrap.appendChild(list);
    return wrap;
  }

  // -------- Detail view helpers --------
  function buildFileCard(submission) {
    return el(
      '<div class="av-file-card">' +
      '<div class="av-file-card-thumb">' + I.fileSpreadsheet + '</div>' +
      '<div class="av-file-card-info">' +
      '<div class="av-file-card-name">' + esc(submission.filename) + '</div>' +
      '<div class="av-file-card-type">Spreadsheet</div>' +
      '</div></div>'
    );
  }

  function buildTimelineRow(msg, isFirst, hasLineBelow, attachment) {
    var isSweepy = msg.from_ === 'Sweepy';
    var dotCls = isSweepy ? 'av-tl-dot--sweepy' : 'av-tl-dot--user';
    var contentCls = isFirst ? 'av-tl-content--first' : 'av-tl-content--mid';
    var trackCls = isFirst ? 'av-tl-track av-tl-track--first' : 'av-tl-track';

    var track = el('<div class="' + trackCls + '"></div>');
    if (!isFirst) track.appendChild(el('<div class="av-tl-line--fixed"></div>'));
    track.appendChild(el('<div class="av-tl-dot ' + dotCls + '"></div>'));
    if (hasLineBelow) track.appendChild(el('<div class="av-tl-line"></div>'));

    var content = el('<div class="av-tl-content ' + contentCls + '"></div>');
    content.appendChild(el(
      '<div class="av-tl-meta"><b>' + esc(msg.from_) + '</b> via ' + esc(msg.sentVia) +
      ' · ' + fmtDate(msg.timestamp) + '</div>'
    ));
    content.appendChild(el('<div class="av-tl-text">' + esc(msg.text) + '</div>'));
    if (attachment) content.appendChild(buildFileCard(attachment));

    var row = el('<div class="av-tl-row"></div>');
    row.appendChild(track);
    row.appendChild(content);
    return row;
  }

  function buildNoReplyRow(noReplyDate) {
    var track = el('<div class="av-tl-track"></div>');
    track.appendChild(el('<div class="av-tl-line--fixed"></div>'));
    track.appendChild(el('<div class="av-tl-dot av-tl-dot--noreply"></div>'));
    track.appendChild(el('<div class="av-tl-line"></div>'));

    var content = el('<div class="av-tl-content av-tl-content--mid"></div>');
    content.appendChild(el(
      '<div class="av-tl-meta av-tl-noreply">' +
      '<span class="av-tl-noreply-label">No reply</span>' +
      ' · ' + esc(noReplyDate) + '</div>'
    ));
    content.appendChild(el('<div class="av-tl-text av-tl-noreply-body">Sending follow-up…</div>'));

    var row = el('<div class="av-tl-row"></div>');
    row.appendChild(track);
    row.appendChild(content);
    return row;
  }

  function buildTimelineEventRow(item) {
    var isSignoff = item.cardType === 'signoff';

    var track = el('<div class="av-tl-track"></div>');
    track.appendChild(el('<div class="av-tl-line--fixed"></div>'));
    track.appendChild(el('<div class="av-tl-dot av-tl-dot--sweepy"></div>'));
    track.appendChild(el('<div class="av-tl-line"></div>'));

    var content = el('<div class="av-tl-content av-tl-content--event"></div>');
    if (isSignoff) {
      content.appendChild(el('<div class="av-tl-event-label"><b>Sweepy</b> ran data quality check</div>'));
      content.appendChild(el(
        '<div class="av-callout callout-pass"><div class="av-callout-head">' + I.check +
        'Data quality check passed</div><div class="av-callout-body">' +
        esc(item.qualityCheck.text) + ' Take a look yourself and sign off when you\'re ready.</div></div>'
      ));
    } else {
      content.appendChild(el('<div class="av-tl-event-label"><b>Sweepy</b> summary</div>'));
      content.appendChild(el(
        '<div class="av-callout callout-blocked"><div class="av-callout-head">' +
        esc(firstName(item.owner.name)) + ' says this is blocked</div>' +
        '<div class="av-callout-body">' + esc(item.blockerSummary) + '</div></div>'
      ));
    }

    var row = el('<div class="av-tl-row"></div>');
    row.appendChild(track);
    row.appendChild(content);
    return row;
  }

  function buildDetailView(item) {
    var init = initById[item.initiativeId];
    var s = uiStatus(init);
    var m = statusMeta(s);
    var scope = (init.scope || '').replace('Scope ', 'S');
    var ownerFirstName = firstName(item.owner.name);
    var hasChaseUp = item.initiativeId === 'sustainable-packaging';
    var introText;
    if (item.cardType === 'signoff') {
      introText = 'Data has been submitted for this action. Please review and confirm when you\'re ready.';
    } else if (hasChaseUp) {
      introText = 'No data was submitted for this action. When I sent a follow-up, ' +
        ownerFirstName + ' explained that the action was blocked this month. See below for more detail.';
    } else {
      introText = ownerFirstName + ' has flagged a blocker on this action. Here\'s the summary.';
    }

    // Remove the Sweepy chase-up (index 1) unless this card has the chase-up step
    var msgs = (item.messages || []).filter(function (_, idx) {
      return hasChaseUp ? true : idx !== 1;
    });

    var detail = el('<div class="av-panel-detail-side"></div>');

    // Image header
    var header = el('<div class="av-dh"></div>');
    var headerImg = el('<div class="av-dh-img"></div>');
    headerImg.style.backgroundImage = "url('" + (init.image || '') + "')";
    header.appendChild(headerImg);
    header.appendChild(el('<button class="av-dh-back" data-act="back" aria-label="Back to list">' + I.back + '</button>'));
    header.appendChild(el('<div class="av-dh-scope">' + esc(scope) + '</div>'));
    detail.appendChild(header);

    // Scrollable body
    var body = el('<div class="av-detail-body"></div>');

    var meta = el('<div class="av-detail-meta"></div>');
    meta.appendChild(el('<span class="av-status ' + m.cls + '"><span class="dot"></span>' + m.label + '</span>'));
    meta.appendChild(el('<div class="av-detail-action-title">' + esc(init.shortName) + '</div>'));
    meta.appendChild(el('<div class="av-detail-owner-text">' + esc(item.owner.name) + ' · ' + esc(item.owner.department) + '</div>'));
    body.appendChild(meta);

    // Typing intro (text filled by startIntroTyping after slide animation)
    body.appendChild(el(
      '<div class="av-intro-block" data-intro="' + esc(introText) + '">' +
      '<span class="av-intro-text"></span><span class="av-intro-cursor"></span></div>'
    ));

    // Summary section — hidden until typing completes
    var summary = el('<div class="av-detail-summary"></div>');
    summary.appendChild(el('<div class="av-summary-divider"></div>'));
    summary.appendChild(el('<div class="av-summary-heading">Summary of conversation with ' + esc(ownerFirstName) + '</div>'));

    var timeline = el('<div class="av-timeline"></div>');
    if (msgs[0]) timeline.appendChild(buildTimelineRow(msgs[0], true, true));
    if (hasChaseUp) {
      // Insert synthetic "No reply" row between initial check-in and chase-up
      timeline.appendChild(buildNoReplyRow('2026-08-29'));
      // msgs[1] = Sweepy chase-up, msgs[2] = owner response
      if (msgs[1]) timeline.appendChild(buildTimelineRow(msgs[1], false, true));
      if (msgs[2]) timeline.appendChild(buildTimelineRow(msgs[2], false, true));
    } else if (msgs[1]) {
      var attachment = (item.cardType === 'signoff' && item.dataSubmission) ? item.dataSubmission : null;
      timeline.appendChild(buildTimelineRow(msgs[1], false, true, attachment));
    }
    timeline.appendChild(buildTimelineEventRow(item));
    summary.appendChild(timeline);

    var nuanceText = (item.cardType === 'signoff' && item.nuance) ? item.nuance.text : 'No data to sign off.';
    summary.appendChild(el(
      '<div class="av-callout callout-know" style="margin-top:14px">' +
      '<div class="av-callout-head">' + I.info + 'Worth knowing</div>' +
      '<div class="av-callout-body">' + esc(nuanceText) + '</div></div>'
    ));

    if (item.cardType === 'signoff') {
      summary.appendChild(el(
        '<div class="av-detail-action"><button class="av-btn-primary" data-act="submit" data-id="' +
        item.initiativeId + '">Submit data</button></div>'
      ));
    } else {
      summary.appendChild(el(
        '<div class="av-detail-action"><button class="av-btn-secondary" data-act="ack" data-id="' +
        item.initiativeId + '">Acknowledge</button></div>'
      ));
    }

    body.appendChild(summary);
    detail.appendChild(body);
    detail.appendChild(el('<div class="av-detail-input-bar"><div class="av-detail-input-box">Write a message...</div></div>'));

    return detail;
  }

  function startIntroTyping(initiativeId) {
    var introBlock = root.querySelector('.av-intro-block');
    if (!introBlock) return;
    var textEl = introBlock.querySelector('.av-intro-text');
    var cursor = introBlock.querySelector('.av-intro-cursor');
    var summary = root.querySelector('.av-detail-summary');
    if (!textEl) return;

    var fullText = introBlock.getAttribute('data-intro') || '';
    var i = 0;
    var timer = setInterval(function () {
      if (i < fullText.length) {
        textEl.textContent += fullText[i];
        i++;
        var body = root.querySelector('.av-detail-body');
        if (body) body.scrollTop = 0; // keep header visible while typing
      } else {
        clearInterval(timer);
        if (cursor) cursor.style.display = 'none';
        setTimeout(function () {
          if (summary) summary.classList.add('is-visible');
        }, 300);
      }
    }, 16);
  }

  function slideForward(id) {
    if (sliding) return;
    sliding = true;
    state.fyPage = id;
    render();

    var listSide = root.querySelector('.av-panel-list-side');
    var detailSide = root.querySelector('.av-panel-detail-side');
    if (!listSide || !detailSide) { sliding = false; return; }

    // Override to start positions, then animate to final
    listSide.style.transition = 'none';
    detailSide.style.transition = 'none';
    listSide.style.transform = 'translateX(0)';
    detailSide.style.transform = 'translateX(100%)';

    void detailSide.offsetHeight; // force reflow

    var dur = 320;
    var ease = 'transform ' + dur + 'ms cubic-bezier(0.4,0,0.2,1)';
    listSide.style.transition = ease;
    detailSide.style.transition = ease;
    listSide.style.transform = 'translateX(-100%)';
    detailSide.style.transform = 'translateX(0)';

    setTimeout(function () {
      sliding = false;
      startIntroTyping(id);
    }, dur + 10);
  }

  function slideBack() {
    if (sliding) return;
    var listSide = root.querySelector('.av-panel-list-side');
    var detailSide = root.querySelector('.av-panel-detail-side');
    if (!listSide || !detailSide) { state.fyPage = 'list'; render(); return; }

    sliding = true;
    var dur = 300;
    var ease = 'transform ' + dur + 'ms cubic-bezier(0.4,0,0.2,1)';
    listSide.style.transition = ease;
    detailSide.style.transition = ease;
    listSide.style.transform = 'translateX(0)';
    detailSide.style.transform = 'translateX(100%)';

    setTimeout(function () {
      sliding = false;
      state.fyPage = 'list';
      render();
    }, dur);
  }

  function renderForYou() {
    return forYouList();
  }

  // -------- Activity --------
  function renderActivity() {
    var wrap = el('<div class="av-page"><div class="av-panel-h">Activity</div><div class="av-panel-sub">What Sweepy has done recently.</div></div>');
    var list = el('<div class="av-activity"></div>');
    db.activity.forEach(function (a) {
      list.appendChild(el(
        '<div class="av-act-row"><span class="av-act-dot"></span>' +
        '<div><div class="av-act-text">' + esc(a.text) + '</div>' +
        '<div class="av-act-ts">' + esc(a.ts.replace('T', ' · ')) + '</div></div></div>'
      ));
    });
    wrap.appendChild(list);
    return wrap;
  }

  // -------- Goals (3 verbatim, per brief) --------
  var GOALS = [
    { ico: I.goalReport, title: 'Automate monthly leadership report', desc: 'Create a monthly leadership report from confirmed initiative data, never from memory or inference.' },
    { ico: I.goalChase,  title: 'Chase overdue data', desc: 'Chase an overdue initiative owner within 48 hours of a missed check-in, and again a week later.' },
    { ico: I.goalFind,   title: 'Find new initiatives', desc: 'Surface new initiative opportunities worth a look, without adding one to the programme unasked.' }
  ];
  function renderGoals() {
    var wrap = el('<div class="av-page"><div class="av-panel-h">Goals</div><div class="av-panel-sub">What Sweepy is working toward.</div></div>');
    var list = el('<div class="av-goals"></div>');
    GOALS.forEach(function (g) {
      list.appendChild(el(
        '<div class="av-goal"><div class="av-goal-ico">' + g.ico + '</div>' +
        '<div class="av-goal-title">' + esc(g.title) + '</div>' +
        '<div class="av-goal-desc">' + esc(g.desc) + '</div></div>'
      ));
    });
    wrap.appendChild(list);
    return wrap;
  }

  // -------- Chat (4 messages verbatim, per brief) --------
  var CHAT = [
    { side: 'lead',   text: 'Can you double-check the off-grid diesel numbers before I sign off the report? Daniel\'s status still says on track.' },
    { side: 'sweepy', text: 'Already flagged it on his initiative page — diesel volumes haven\'t moved in two months despite the confirmed status. I haven\'t changed what he logged, just surfaced the discrepancy.' },
    { side: 'lead',   text: 'Good, leave it as a flag for now. I\'ll follow up with him directly this week.' },
    { side: 'sweepy', text: 'Noted — I\'ll hold off on a third automated nudge and let you take it from here.' }
  ];
  function renderChat() {
    var wrap = el('<div class="av-page"><div class="av-panel-h">Chat</div></div>');
    var thread = el('<div class="av-chat"></div>');
    CHAT.forEach(function (m) {
      thread.appendChild(el('<div class="av-chat-msg av-chat-' + m.side + '">' + esc(m.text) + '</div>'));
    });
    wrap.appendChild(thread);
    wrap.appendChild(el('<div class="av-list-input-bar"><div class="av-detail-input-box">Write a message...</div></div>'));
    return wrap;
  }

  function panelBody() {
    if (state.activeTab === 'activity') return renderActivity();
    if (state.activeTab === 'goals') return renderGoals();
    if (state.activeTab === 'chat') return renderChat();
    return renderForYou();
  }

  function agentPanelWire() {
    var panel = el('<div class="av-panel"></div>');
    var content = el('<div style="padding:20px 20px 0"></div>');
    content.appendChild(el('<div class="av-sweepy"><img src="assets/agent-avatar.svg" width="74" height="74" alt="Sweepy"></div>'));
    content.appendChild(el(
      '<div class="av-wire-intro-block" style="margin-top:40px">' +
      '<div class="av-intro-block" data-intro="Is there anything I can help you with here?">' +
      '<span class="av-intro-text"></span><span class="av-intro-cursor"></span>' +
      '</div></div>'
    ));
    panel.appendChild(content);
    panel.appendChild(el(
      '<div class="av-detail-input-bar">' +
      '<div class="av-detail-input-box">Write a message…</div>' +
      '</div>'
    ));
    return panel;
  }

  function startWirePanelTyping() {
    if (wireTypingTimer) { clearTimeout(wireTypingTimer); wireTypingTimer = null; }
    wireTypingTimer = setTimeout(function () {
      wireTypingTimer = null;
      var introBlock = root.querySelector('.av-wire-intro-block .av-intro-block');
      if (!introBlock) return;
      var textEl = introBlock.querySelector('.av-intro-text');
      var cursor = introBlock.querySelector('.av-intro-cursor');
      if (!textEl) return;
      var fullText = introBlock.getAttribute('data-intro') || '';
      var i = 0;
      var timer = setInterval(function () {
        if (i < fullText.length) {
          textEl.textContent += fullText[i++];
        } else {
          clearInterval(timer);
          if (cursor) cursor.style.display = 'none';
        }
      }, 16);
    }, 1000);
  }

  function agentPanel() {
    if (state.wire) return agentPanelWire();
    var inList = state.fyPage === 'list';
    var panel = el('<div class="av-panel"></div>');

    // List side: avatar + tabs + content (always rendered so card animations work)
    var listSide = el('<div class="av-panel-list-side"></div>');
    listSide.appendChild(el('<div class="av-sweepy"><img src="assets/agent-avatar.svg" width="74" height="74" alt="Sweepy"></div>'));
    listSide.appendChild(tabBar());
    var pages = el('<div class="av-pages"></div>');
    pages.appendChild(panelBody());
    listSide.appendChild(pages);
    listSide.style.transform = inList ? 'translateX(0)' : 'translateX(-100%)';
    panel.appendChild(listSide);

    // Detail side: full-panel card detail view (or empty placeholder when on list)
    if (!inList) {
      var item = state.fyItems.filter(function (it) { return it.initiativeId === state.fyPage; })[0];
      if (item) {
        var detailSide = buildDetailView(item);
        detailSide.style.transform = 'translateX(0)';
        panel.appendChild(detailSide);
      }
    } else {
      panel.appendChild(el('<div class="av-panel-detail-side" style="transform:translateX(100%)"></div>'));
    }

    return panel;
  }

  /* ============================================================
     WIREFRAME DESTINATION (out-of-scope pages = stubs)
  ============================================================ */
  function wireOverlay() {
    var w = state.wire;
    var isReport = w.type === 'report';
    var tag = isReport ? 'Wireframe — Report page' : 'Wireframe — Initiative page';
    var h = isReport ? (MONTHS[currentReport().month - 1] + ' leadership report') : w.title;
    var sub = isReport ? 'Most recent report · generated by Sweepy, awaiting review' : 'Initiative detail — visual design out of scope this pass';
    var ov = el(
      '<div class="av-wire">' +
      '<button class="av-wire-close" data-act="close-wire" aria-label="Close">✕</button>' +
      '<div class="av-wire-card">' +
      '<span class="av-wire-tag">' + tag + '</span>' +
      '<div class="av-wire-h">' + esc(h) + '</div>' +
      '<div class="av-wire-sub">' + esc(sub) + '</div>' +
      '<div class="av-wire-line w90"></div><div class="av-wire-line w80"></div><div class="av-wire-line w60"></div>' +
      '<div class="av-wire-block"></div>' +
      '<div class="av-wire-line w80"></div><div class="av-wire-line w90"></div><div class="av-wire-line w40"></div>' +
      '</div></div>'
    );
    return ov;
  }

  /* ============================================================
     RENDER
  ============================================================ */
  function render() {
    var savedMainScroll = 0;
    var prevMain = root.querySelector('.av-main');
    if (prevMain) savedMainScroll = prevMain.scrollTop;
    root.innerHTML = '';
    var layout = el('<div class="av-layout"></div>');

    // nav rail — generic #f2f2f2 placeholders (deliberately inert, no invented
    // icons) plus one active worked example carrying the Target icon.
    var nav = el('<div class="av-nav"></div>');
    nav.appendChild(el('<div class="av-logo" data-act="reset" role="button" tabindex="0" title="Reset prototype" style="overflow:hidden;padding:0;background:none"><img src="assets/nav-avatar.png" width="32" height="32" alt="" style="display:block;width:32px;height:32px;object-fit:cover"></div>'));
    nav.appendChild(el('<div class="av-nav-ph"></div>'));
    nav.appendChild(el('<div class="av-nav-ico is-active">' + I.goals + '</div>'));
    nav.appendChild(el('<div class="av-nav-ph"></div>'));
    nav.appendChild(el('<div class="av-nav-ph"></div>'));
    nav.appendChild(el('<div class="av-nav-div"></div>'));
    nav.appendChild(el('<div class="av-nav-ph"></div>'));

    // main column
    var main = el('<div class="av-main"></div>');
    if (state.wire && state.wire.type === 'report') {
      main.appendChild(renderReportMain(state.wire.reportId || '2026-09'));
    } else if (state.wire && state.wire.type === 'initiative') {
      main.appendChild(renderInitiativeMain(state.wire.id));
    } else {
      main.appendChild(el('<div style="display:flex;align-items:center;justify-content:space-between"><div class="av-page-title">Act</div><button class="av-new-action-btn">' + I.plus + 'New Action</button></div>'));
      var chartBlock = el('<div style="margin-top:22px"></div>');
      chartBlock.appendChild(el('<div class="av-section-title">BIG Telecom - total reduction (YTD)</div>'));
      chartBlock.appendChild(el('<div style="height:14px"></div>'));
      var actPanel = el('<div class="av-act-panel"></div>');
      actPanel.appendChild(buildChart());
      actPanel.appendChild(reportTile());
      chartBlock.appendChild(actPanel);
      main.appendChild(chartBlock);
      main.appendChild(initiativesGrid());
    }

    layout.appendChild(nav);
    layout.appendChild(main);
    layout.appendChild(agentPanel());
    root.appendChild(layout);

    if (savedMainScroll && !state.wire) {
      var newMain = root.querySelector('.av-main');
      if (newMain) newMain.scrollTop = savedMainScroll;
    }

    if (state.wire) startWirePanelTyping();
  }

  /* ============================================================
     INTERACTIONS
  ============================================================ */
  function afterAction() {
    // sign-off / acknowledge landed us back on the list
    state.fyPage = 'list';
    // feed empty for the first time → kick off report generation
    if (state.fyItems.length === 0 && state.report === 'awaiting') {
      state.report = 'inprogress';
      render();
      reportTimer = setTimeout(function () { reportTimer = null; state.report = 'ready'; render(); }, 2200);
      return;
    }
    render();
  }

  // Full reset — restore every mutated bit of state to first-load.
  function resetAll() {
    if (reportTimer) { clearTimeout(reportTimer); reportTimer = null; }
    if (wireTypingTimer) { clearTimeout(wireTypingTimer); wireTypingTimer = null; }
    state.activeTab = 'foryou';
    state.fyPage = 'list';
    state.report = 'awaiting';
    state.wire = null;
    // undo the submit-driven data mutations, then re-derive status
    db.initiatives.initiatives.forEach(function (i) {
      i.dataStatus = i._origDataStatus;
      i.uiStatus = uiStatus(i);
    });
    state.fyItems = db.forYou.slice();
    render();
  }

  function onClick(e) {
    var t = e.target.closest('[data-act]');
    if (!t) return;
    var act = t.getAttribute('data-act');
    var id = t.getAttribute('data-id');

    switch (act) {
      case 'tab':
        state.activeTab = t.getAttribute('data-tab');
        render();
        break;
      case 'open-item':
        slideForward(id);
        break;
      case 'back':
        slideBack();
        break;
      case 'submit':
        // Ready → Up to Date, clear card
        initById[id].dataStatus = 'up_to_date';
        initById[id].uiStatus = 'uptodate';
        state.fyItems = state.fyItems.filter(function (it) { return it.initiativeId !== id; });
        afterAction();
        break;
      case 'ack':
        // stays Blocked, just clear the card
        state.fyItems = state.fyItems.filter(function (it) { return it.initiativeId !== id; });
        afterAction();
        break;
      case 'open-initiative':
        state.wire = { type: 'initiative', id: id }; render();
        break;
      case 'open-report':
        state.wire = { type: 'report', reportId: '2026-09' }; render();
        break;
      case 'select-report':
        state.wire = { type: 'report', reportId: id }; render();
        break;
      case 'close-wire':
        state.wire = null; render();
        break;
      case 'reset':
        resetAll();
        break;
    }
  }

  /* ============================================================
     BOOT
  ============================================================ */
  function init() {
    root = document.getElementById('act-root');
    if (!root) return;
    // All theme colors (--av-primary, --pol-pos/neg, --st-ready/blocked/uptodate,
    // etc.) are CSS custom properties scoped to .act-view in css/act-view.css.
    // Without this class present somewhere in the mounted tree, every var(--av-*)
    // reference resolves to nothing and silently falls back to inherited/initial
    // values -- this was why the target line, polarity (+/-%) text, status colors,
    // nav logo fill, and report-tile accents were all rendering as black/invisible
    // instead of their real colors.
    root.classList.add('act-view');

    // ?v= busts the browser cache when the JSON changes (e.g. adding forecast rows);
    // bump alongside the ?v= on the <script>/<link> tags in index.html.
    var V = '?v=fc3';
    Promise.all([
      fetch(DATA + 'initiatives.json' + V).then(function (r) { return r.json(); }),
      fetch(DATA + 'trajectory.json' + V).then(function (r) { return r.json(); }),
      fetch(DATA + 'for-you-items.json' + V).then(function (r) { return r.json(); }),
      fetch(DATA + 'activity-log.json' + V).then(function (r) { return r.json(); }),
      fetch(DATA + 'reports.json' + V).then(function (r) { return r.json(); }),
      fetch(DATA + 'activity-data.json' + V).then(function (r) { return r.json(); })
    ]).then(function (res) {
      db.initiatives = res[0];
      db.trajectory = res[1];
      db.forYou = res[2];
      db.activity = res[3];
      db.reports = res[4];
      db.activityData = res[5].rows;

      db.initiatives.initiatives.forEach(function (i) { i._origDataStatus = i.dataStatus; i.uiStatus = uiStatus(i); initById[i.id] = i; });
      state.fyItems = db.forYou.slice();

      render();
      // If the browser was already ready (scrolled in view) before data loaded, trigger now
      if (cardState === 'animating') {
        if (cardAnimTimeout) { clearTimeout(cardAnimTimeout); cardAnimTimeout = null; }
        setTimeout(triggerCardAnim, 120);
      }
    }).catch(function (err) {
      root.innerHTML = '<div style="padding:40px;font-family:system-ui;color:#6e6e6e">Could not load prototype data (' + esc(String(err)) +
        ').<br>The Act view fetches JSON at runtime — serve the folder over http (e.g. <code>python3 -m http.server</code> or GitHub Pages), not <code>file://</code>.</div>';
    });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
  document.addEventListener('click', onClick);

  // ---- For You card entrance animation (repeatable, scroll-driven) ----
  // cardState: 'hidden' = pre-animation | 'animating' = mid-play | 'shown' = done
  var cardState = 'hidden';
  var cardAnimTimeout = null;

  function triggerCardAnim() {
    var rows = Array.prototype.slice.call(root.querySelectorAll('.av-fy-list .av-fy-row'));
    if (rows.length === 0) return; // data not loaded yet — init() will call this after render
    rows.reverse(); // bottom card enters first
    rows.forEach(function (row, i) {
      row.classList.remove('av-fy-pre');
      row.style.animationDelay = (i * 55) + 'ms';
      row.classList.add('is-animating');
    });
    cardState = 'shown';
  }

  // Fires each time progress crosses 1 (scrolled fully in view)
  document.addEventListener('av-browser-ready', function () {
    if (cardState === 'shown') return;
    cardState = 'animating';
    if (cardAnimTimeout) { clearTimeout(cardAnimTimeout); }
    cardAnimTimeout = setTimeout(function () {
      cardAnimTimeout = null;
      triggerCardAnim();
    }, 120);
  });

  // Fires each time progress drops below 0.1 (scrolled mostly away) — reset for next entry
  document.addEventListener('av-browser-reset', function () {
    cardState = 'hidden';
    if (cardAnimTimeout) { clearTimeout(cardAnimTimeout); cardAnimTimeout = null; }
    var rows = Array.prototype.slice.call(root.querySelectorAll('.av-fy-list .av-fy-row'));
    rows.forEach(function (row) {
      row.classList.remove('is-animating');
      row.style.animationDelay = '';
      if (!row.classList.contains('av-fy-pre')) row.classList.add('av-fy-pre');
    });
  });
})();
