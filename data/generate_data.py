#!/usr/bin/env python3

# ⚠ STALE, 2026-09-13 — this generator still produces the old model: a single
# "overdue" dataStatus and bulletin-threads.json. Both initiatives.json and
# for-you-items.json (which replaced bulletin-threads.json) were hand-edited
# after the last run of this script to the new model instead: dataStatus is
# {up_to_date, pending_review, awaiting_data}, and a real-world blocker is its
# own `blocked`/`blockerShort` flag, independent of dataStatus. Do NOT re-run
# this script without updating it first — it will silently overwrite that
# hand-edited state with the old three-value "overdue" model. See
# decisions-log.md, 2026-09-13.

"""
Generates the mock dataset that drives the Sustain prototype's content.
Single source of truth for every screen — re-run after any content change.

Company: Solandra Telecom (fictional). Emission factors and monthly figures
are illustrative (right order of magnitude, not audited) — the point is the
data model and the product built on it, not a certified carbon footprint.

Run: python3 generate_data.py
"""
import json
import random
from datetime import date
from pathlib import Path
from calendar import month_abbr

random.seed(42)
OUT = Path(__file__).parent
TODAY = date(2026, 9, 12)
COMPANY = "Solandra Telecom"
LEAD = dict(name="Meera Chandra", role="Head of Sustainability")
MONTH_LABELS = [month_abbr[m] for m in range(1, 13)]

# ---------------------------------------------------------------------------
# Initiative definitions — shortName is now a goal, not a topic
# ---------------------------------------------------------------------------

INITIATIVES = [
    dict(
        id="network-site-efficiency", name="Network site energy efficiency",
        shortName="Cut network site energy use",
        scope="Scope 2", category="Purchased Electricity — network sites",
        description="Upgrading power amplifiers and free-cooling at high-draw 4G/5G sites to cut grid electricity per site.",
        owner="Priya Nair", role="Network Operations Lead", dept="Network",
        baseline=9400, target=7200, target_year=2028, ratio=1.02,
        site_type="Cell site", site_ids=["CELL-04521", "CELL-03318", "CELL-07742", "CELL-01199", "CELL-05630"],
        activity_type="Grid electricity consumption", activity_unit="kWh",
        calc_method="Location-based", ef_base=0.192, ef_unit="kgCO2e/kWh",
        ef_source="UK Gov GHG Conversion Factors, 2026 edition",
        data_sources=["Smart meter", "Smart meter", "Utility invoice"],
    ),
    dict(
        id="datacentre-cooling", name="Data centre cooling optimisation",
        shortName="Cool data centres efficiently",
        scope="Scope 2", category="Purchased Electricity — data centres",
        description="Raising cold-aisle set points and adding free-air cooling across the core data centre estate to cut PUE.",
        owner="Marcus Webb", role="Data Centre Operations Lead", dept="IT Infrastructure",
        baseline=6100, target=4600, target_year=2028, ratio=0.985,
        site_type="Data centre", site_ids=["DC-Manchester-01", "DC-Slough-02", "DC-Leeds-01", "DC-Reading-03", "DC-Glasgow-01"],
        activity_type="Grid electricity consumption", activity_unit="kWh",
        calc_method="Location-based", ef_base=0.192, ef_unit="kgCO2e/kWh",
        ef_source="UK Gov GHG Conversion Factors, 2026 edition",
        data_sources=["Smart meter", "Building management system"],
    ),
    dict(
        id="renewable-ppa", name="Renewable electricity PPA — network estate",
        shortName="Power the network on renewables",
        scope="Scope 2", category="Purchased Electricity (market-based) — network estate",
        description="Corporate PPA covering an increasing share of network-estate electricity with wind and solar generation.",
        owner="Sofia Alvarez", role="Energy Procurement Lead", dept="Energy & Sustainability",
        baseline=8800, target=2200, target_year=2029, ratio=1.06,
        site_type="Network region", site_ids=["Region-North", "Region-South", "Region-Midlands", "Region-Scotland", "Region-Wales"],
        activity_type="Electricity — PPA-covered vs. residual grid mix", activity_unit="MWh",
        calc_method="Market-based", ef_base=0.021, ef_unit="kgCO2e/kWh",
        ef_source="REGO certificates + residual fuel mix factor, 2026",
        data_sources=["PPA settlement report", "Supplier statement"],
    ),
    dict(
        id="offgrid-solar", name="Off-grid cell tower solar & battery",
        shortName="Take remote towers off diesel",
        scope="Scope 1", category="Stationary Combustion — remote sites",
        description="Replacing diesel generators at off-grid rural sites with solar-plus-battery power systems.",
        owner="Daniel Osiel", role="Rural Network Lead", dept="Network",
        baseline=2100, target=900, target_year=2027, ratio=1.08,
        site_type="Remote cell site", site_ids=["REMOTE-1102", "REMOTE-1187", "REMOTE-1204", "REMOTE-1329", "REMOTE-1450"],
        activity_type="Diesel — off-grid generator", activity_unit="litres",
        calc_method="Fuel-based", ef_base=2.51, ef_unit="kgCO2e/litre",
        ef_source="UK Gov GHG Conversion Factors, 2026 edition — diesel (average biofuel blend)",
        data_sources=["Fuel delivery log", "Site engineer estimate"],
        overdue=True,
        overview=(
            "Forty off-grid sites still run on diesel generators, mostly in the Highlands and mid-Wales network "
            "where grid connection isn't viable. The goal is to convert all forty to solar-plus-battery by the "
            "end of 2027, cutting roughly 1,200 tCO2e a year and removing ~140,000 litres of diesel resupply "
            "trips annually — a real cost story alongside the carbon one."
        ),
        current_note=(
            "12 of 40 sites converted so far. Two conversions scheduled for August slipped to October — the "
            "planning consent for REMOTE-1329's battery enclosure took longer than expected. Diesel volumes at "
            "the remaining sites haven't moved much this quarter, which is the flag below."
        ),
    ),
    dict(
        id="fleet-electrification", name="Field fleet electrification",
        shortName="Electrify the field fleet",
        scope="Scope 1", category="Mobile Combustion — field engineer vans",
        description="Replacing diesel field-engineer vans with electric vans as the lease cycle turns over, depot by depot.",
        owner="Grace Lindqvist", role="Field Operations Lead", dept="Field Operations",
        baseline=3400, target=1900, target_year=2028, ratio=1.03,
        site_type="Depot", site_ids=["Depot-Leeds", "Depot-Bristol", "Depot-Newcastle", "Depot-Cardiff", "Depot-Birmingham"],
        activity_type="Diesel — field engineer vans", activity_unit="litres",
        calc_method="Fuel-based", ef_base=2.51, ef_unit="kgCO2e/litre",
        ef_source="UK Gov GHG Conversion Factors, 2026 edition — diesel",
        data_sources=["Fuel card", "Fleet telematics"],
    ),
    dict(
        id="business-travel", name="Business travel reduction",
        shortName="Cut business travel emissions",
        scope="Scope 3", category="Category 6 — Business Travel",
        description="Default-to-rail policy for domestic routes and a per-team quarterly travel-carbon budget.",
        owner="Tom Radley", role="Head of People & Culture", dept="People & Culture",
        baseline=1450, target=1000, target_year=2027, ratio=0.97,
        site_type="Business unit", site_ids=["Corporate", "Network Engineering", "Sales", "Product", "Customer Ops"],
        activity_type="Air & rail travel distance (booked)", activity_unit="km",
        calc_method="Distance-based", ef_base=0.093, ef_unit="kgCO2e/km",
        ef_source="DEFRA passenger travel factors, 2026",
        data_sources=["Travel booking system"],
    ),
    dict(
        id="employee-commuting", name="Employee commuting — EV salary sacrifice",
        shortName="Shift commuting off petrol and diesel",
        scope="Scope 3", category="Category 7 — Employee Commuting",
        description="Salary-sacrifice EV lease scheme and an annual commuting survey to model the shift away from petrol/diesel cars.",
        owner="Aisha Rahman", role="HR Programmes Lead", dept="People & Culture",
        baseline=5200, target=3900, target_year=2029, ratio=1.015,
        site_type="Office", site_ids=["HQ-London", "Manchester Hub", "Leeds Hub", "Glasgow Hub", "Birmingham Hub"],
        activity_type="Car commuting distance (annual survey, modelled monthly)", activity_unit="km",
        calc_method="Average-data (survey-based)", ef_base=0.168, ef_unit="kgCO2e/km",
        ef_source="DEFRA commuting factors + internal commuting survey, 2026",
        data_sources=["Commuting survey", "HR headcount by site"],
    ),
    dict(
        id="supplier-engagement", name="Network equipment supplier engagement",
        shortName="Decarbonise the equipment supply chain",
        scope="Scope 3", category="Category 1 — Purchased Goods & Services",
        description="Requiring primary emissions data (not industry-average factors) from the top RAN and core equipment vendors by contract renewal.",
        owner="Ben Fitzgerald", role="Procurement Lead", dept="Procurement",
        baseline=41000, target=33000, target_year=2029, ratio=1.05,
        site_type="Supplier", site_ids=["RAN Vendor A", "RAN Vendor B", "Core Network Vendor", "Fibre Contractor", "Devices Distributor"],
        activity_type="Equipment & services spend", activity_unit="GBP",
        calc_method="Spend-based (EEIO)", ef_base=0.42, ef_unit="kgCO2e/£",
        ef_source="DESNZ / EXIOBASE spend-based factors, 2026",
        data_sources=["AP spend extract", "Supplier-specific PCF (partial coverage)"],
    ),
    dict(
        id="handset-takeback", name="Handset take-back & circular refurbishment",
        shortName="Keep devices in circulation longer",
        scope="Scope 3", category="Category 12 — End-of-Life Treatment of Sold Products",
        description="Expanding trade-in and refurbishment so fewer customers need a newly-manufactured handset, cutting embodied-carbon shipped.",
        owner="Yuki Tanaka", role="Retail & Devices Lead", dept="Retail & Devices",
        baseline=5600, target=3100, target_year=2028, ratio=1.09,
        site_type="Retail region", site_ids=["Retail-North", "Retail-South", "Retail-Midlands", "Retail-Scotland", "Retail-Online"],
        activity_type="New devices shipped without a trade-in/refurb offset", activity_unit="units",
        calc_method="Average product carbon footprint", ef_base=45.0, ef_unit="kgCO2e/unit",
        ef_source="Device manufacturer PCF disclosures (average), 2026",
        data_sources=["Retail POS system", "Trade-in programme records"],
        overdue=True,
    ),
    dict(
        id="device-efficiency-labelling", name="Customer device energy-efficiency labelling",
        shortName="Cut customer device power draw",
        scope="Scope 3", category="Category 11 — Use of Sold Products",
        description="Steering customers toward lower-power routers and handsets at point of sale, modelled against the active install base.",
        owner="Chloe Marchetti", role="Product Sustainability Lead", dept="Product",
        baseline=12800, target=10500, target_year=2029, ratio=1.01,
        site_type="Device category", site_ids=["Smartphones", "Routers/CPE", "Mobile Broadband", "Wearables", "IoT Modules"],
        activity_type="Modelled customer-side electricity use", activity_unit="kWh (modelled)",
        calc_method="Use-phase modelling (power draw x usage hours x install base)", ef_base=0.192, ef_unit="kgCO2e/kWh",
        ef_source="Internal product energy model + UK Gov grid factor, 2026",
        data_sources=["Product energy model", "Active install base extract"],
    ),
    dict(
        id="cloud-migration", name="Cloud & hosting migration to renewable providers",
        shortName="Move workloads to clean cloud",
        scope="Scope 3", category="Category 1 — Purchased Goods & Services (cloud & IT services)",
        description="Migrating core workloads to renewable-powered cloud regions and consolidating legacy on-prem hosting.",
        owner="Liam O'Connor", role="IT Infrastructure Lead", dept="IT Infrastructure",
        baseline=3900, target=2100, target_year=2028, ratio=0.99,
        site_type="Workload", site_ids=["Billing Platform", "Customer App Backend", "Network OSS", "Data Analytics Platform", "CRM"],
        activity_type="Cloud & hosting spend", activity_unit="GBP",
        calc_method="Spend-based (provider-disclosed, blended)", ef_base=0.27, ef_unit="kgCO2e/£",
        ef_source="Cloud provider sustainability disclosures (blended), 2026",
        data_sources=["Cloud billing export"],
        awaiting=True,
    ),
    dict(
        id="retail-store-retrofit", name="Retail store energy retrofit",
        shortName="Retrofit stores for efficiency",
        scope="Scope 2", category="Purchased Electricity — retail estate",
        description="LED lighting, smart HVAC controls and better insulation across the owned retail estate.",
        owner="Nadia Petrov", role="Retail Estates Lead", dept="Retail & Devices",
        baseline=1900, target=1450, target_year=2028, ratio=0.992,
        site_type="Store", site_ids=["Store-Oxford St", "Store-Manchester", "Store-Leeds", "Store-Cardiff", "Store-Glasgow"],
        activity_type="Grid electricity consumption", activity_unit="kWh",
        calc_method="Location-based", ef_base=0.192, ef_unit="kgCO2e/kWh",
        ef_source="UK Gov GHG Conversion Factors, 2026 edition",
        data_sources=["Smart meter", "Landlord service charge statement"],
    ),
    dict(
        id="sustainable-packaging", name="Sustainable packaging for devices & SIM kits",
        shortName="Cut packaging carbon",
        scope="Scope 3", category="Category 1 — Purchased Goods & Services (packaging)",
        description="Shifting device and SIM-kit packaging to recycled card and removing plastic film across the top-selling SKUs.",
        owner="Sam Okafor", role="Packaging & Supply Chain Lead", dept="Supply Chain",
        baseline=980, target=620, target_year=2027, ratio=1.07,
        site_type="Packaging line", site_ids=["Handset Packaging", "SIM Kit Packaging", "Accessories Packaging", "Router Packaging", "Promo Packaging"],
        activity_type="Packaging material weight", activity_unit="kg",
        calc_method="Material-based", ef_base=0.95, ef_unit="kgCO2e/kg",
        ef_source="DEFRA product material factors, 2026",
        data_sources=["Packaging supplier delivery notes"],
        overdue=True,
    ),
    dict(
        id="capital-goods-network-build", name="Low-carbon network build standard",
        shortName="Build the network low-carbon by design",
        scope="Scope 3", category="Category 2 — Capital Goods",
        description="A low-carbon materials and equipment standard applied to new 5G densification and fibre rollout builds.",
        owner="Ella Whitfield", role="Network Planning Lead", dept="Network",
        baseline=16500, target=12000, target_year=2029, ratio=1.04,
        site_type="Build programme", site_ids=["5G Densification", "Fibre Rollout", "Core Upgrade", "Site Rationalisation", "Edge Compute Build"],
        activity_type="Network build materials & equipment spend", activity_unit="GBP",
        calc_method="Spend-based (EEIO)", ef_base=0.38, ef_unit="kgCO2e/£",
        ef_source="DESNZ / EXIOBASE spend-based factors, 2026 — capital goods",
        data_sources=["Capex system extract"],
        awaiting=True,
    ),
    dict(
        id="backup-power-transition", name="Backup power diesel-to-battery transition",
        shortName="Replace diesel backup with batteries",
        scope="Scope 1", category="Stationary Combustion — exchange sites",
        description="Replacing ageing diesel backup generators at telephone exchange sites with battery storage, exchange by exchange.",
        owner="Rohan Desai", role="Facilities Lead", dept="Facilities",
        baseline=2600, target=1300, target_year=2028, ratio=0.98,
        site_type="Exchange site", site_ids=["EX-Leeds-14", "EX-Bristol-07", "EX-Manchester-22", "EX-Glasgow-09", "EX-Cardiff-03"],
        activity_type="Diesel — exchange backup generator", activity_unit="litres",
        calc_method="Fuel-based", ef_base=2.51, ef_unit="kgCO2e/litre",
        ef_source="UK Gov GHG Conversion Factors, 2026 edition — diesel",
        data_sources=["Fuel delivery log"],
    ),
]

assert len(INITIATIVES) == 15

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def trailing_months(n, end=TODAY):
    y, m = end.year, end.month
    out = []
    for _ in range(n):
        m -= 1
        if m == 0:
            m = 12
            y -= 1
        out.append((y, m))
    return list(reversed(out))

def period_str(y, m):
    return f"{y:04d}-{m:02d}"

def human_period(y, m):
    return f"{month_abbr[m]} {y}"

def monthly_series(target, ratio, actual_through=9):
    """12 months, target glide path always declining; actual only through `actual_through`,
    generally above target (gap = ratio - 1, ramped in over the first few months)."""
    year_start = target * 1.09
    year_end = target * 0.965
    months = []
    for m in range(1, 13):
        t = year_start + (year_end - year_start) * (m - 1) / 11
        if m <= actual_through:
            ramp = 0.55 + 0.45 * (m / actual_through)
            gap = (ratio - 1) * ramp + random.uniform(-0.015, 0.015)
            a = t * (1 + gap)
            months.append(dict(month=m, label=MONTH_LABELS[m - 1],
                                target=round(t), actual=round(a), delta=round(a - t)))
        else:
            months.append(dict(month=m, label=MONTH_LABELS[m - 1],
                                target=round(t), actual=None, delta=None))
    return months

# ---------------------------------------------------------------------------
# Build initiatives + activity data + monthly series
# ---------------------------------------------------------------------------

initiatives_out = []
activity_rows = []
row_counter = 1
MONTHS = trailing_months(10)

for init in INITIATIVES:
    current = round(init["target"] * init["ratio"])
    pct = round((current - init["target"]) / init["target"] * 100, 1)

    dataStatus = "overdue" if init.get("overdue") else ("awaiting_data" if init.get("awaiting") else "up_to_date")
    if dataStatus == "overdue":
        staleDays = random.choice([12, 15, 19])
        lastCheckIn = None
    elif dataStatus == "awaiting_data":
        staleDays = 0
        lastCheckIn = None
    else:
        staleDays = 0
        lastCheckIn = str(TODAY.replace(day=max(1, TODAY.day - random.randint(1, 13))))

    if pct > 4 or dataStatus == "overdue":
        status = "stalled" if (pct > 6 or dataStatus == "overdue") else "at_risk"
    elif pct > 0:
        status = "at_risk"
    else:
        status = "on_track"

    initiatives_out.append(dict(
        id=init["id"], name=init["name"], shortName=init["shortName"],
        scope=init["scope"], ghgCategory=init["category"],
        description=init["description"],
        owner=dict(name=init["owner"], role=init["role"], department=init["dept"]),
        unit="tCO2e",
        baseline=init["baseline"], current=current, target=init["target"],
        targetYear=init["target_year"], percentVsTarget=pct, status=status,
        dataStatus=dataStatus, staleDays=staleDays, lastCheckIn=lastCheckIn,
        overview=init.get("overview"), currentNote=init.get("current_note"),
        monthly=monthly_series(init["target"], init["ratio"]),
    ))

    sites = init["site_ids"]
    start_level = current * 1.10 / 12
    end_level = current * 0.94 / 12
    for i, (y, m) in enumerate(MONTHS):
        month_factor = start_level + (end_level - start_level) * (i / (len(MONTHS) - 1))
        ef = init["ef_base"] * (1 - 0.01 * (i / len(MONTHS)))
        for site in sites:
            share = random.uniform(0.14, 0.26)
            noise = random.uniform(0.88, 1.14)
            tco2e_row = round(month_factor * share * noise, 2)
            activity_data = round((tco2e_row * 1000) / ef, 1) if ef else 0
            quality = random.choices(["Verified", "Estimated", "Pending review"], weights=[0.7, 0.22, 0.08])[0]
            activity_rows.append(dict(
                rowId=row_counter, initiativeId=init["id"],
                reportingPeriod=period_str(y, m), reportingPeriodLabel=human_period(y, m),
                businessUnit=init["dept"], siteType=init["site_type"], siteId=site,
                scope=init["scope"], ghgCategory=init["category"], activityType=init["activity_type"],
                activityData=activity_data, activityUnit=init["activity_unit"],
                calculationMethod=init["calc_method"], emissionFactor=round(ef, 4),
                emissionFactorUnit=init["ef_unit"], emissionFactorSource=init["ef_source"],
                emissionsTco2e=tco2e_row, dataSource=random.choice(init["data_sources"]),
                dataQuality=quality,
            ))
            row_counter += 1

# ---------------------------------------------------------------------------
# Company-wide monthly (the main Act page chart)
# ---------------------------------------------------------------------------

# ⚠ STALE, 2026-09-15 — the live trajectory.json is HAND-EDITED and this
# function is documentation only; it is NOT re-run (see the same discipline
# applied to the initiatives model at the top of this file). The model it now
# describes — and that data/trajectory.json matches — is:
#   * target   — always present; a SEASONAL glidepath (~20% down over the year),
#                NOT a straight line. It eases (falls slowest) in deep winter
#                (Jan/Feb: heating + backup generators) and peak summer (Jul:
#                cooling load), and dips fastest in the shoulder months
#                (Apr–May, Oct–Nov) when neither season is under strain.
#   * actual   — populated for months that have happened (Jan–Sep). Runs above
#                target all year (the red zone), widest in the same seasonal
#                peaks, narrowing but non-monotonically (May and Jul tick back up)
#                as initiatives land.
#   * forecast — populated for months that haven't (Oct–Dec); never both actual
#                and forecast on the same month. Hands off from Sep's real number
#                (no jump at the boundary) and keeps narrowing the gap without
#                closing it by December.
#   * delta    — (actual ?? forecast) − target, so it stays meaningful across the
#                whole year rather than going null at the actual/forecast boundary.
# The literal per-month figures below are the authored values, not regenerated
# from a formula — do NOT "simplify" this back into a linear interpolation.
def company_monthly():
    rows = [
        # month, label, target, actual, forecast
        (1,  "Jan", 167200, 183100, None),
        (2,  "Feb", 162700, 177000, None),
        (3,  "Mar", 156400, 167500, None),
        (4,  "Apr", 152200, 160400, None),
        (5,  "May", 150000, 159000, None),
        (6,  "Jun", 149400, 156300, None),
        (7,  "Jul", 148600, 158700, None),
        (8,  "Aug", 145000, 153600, None),
        (9,  "Sep", 138100, 143500, None),
        (10, "Oct", 134500, None,   139900),
        (11, "Nov", 134400, None,   138700),
        (12, "Dec", 134600, None,   137400),
    ]
    months = []
    for m, label, target, actual, forecast in rows:
        upper = actual if actual is not None else forecast
        months.append(dict(
            month=m, label=label, target=target,
            actual=actual, forecast=forecast,
            delta=(upper - target) if upper is not None else None,
        ))
    return months

company_monthly_series = company_monthly()

trajectory = dict(company=COMPANY, unit="tCO2e", year=2026, monthly=company_monthly_series)

# ---------------------------------------------------------------------------
# Bulletin threads — the 3 overdue owners
# ---------------------------------------------------------------------------

bulletin_threads = []
for init in initiatives_out:
    if init["dataStatus"] != "overdue":
        continue
    first_name = init["owner"]["name"].split()[0]
    bulletin_threads.append(dict(
        initiativeId=init["id"], initiativeName=init["name"], owner=init["owner"], channel="Teams",
        messages=[
            dict(from_="Sweepy", to=first_name, sentVia="Teams", timestamp="2026-08-21T09:14:00+01:00",
                 text=f"Hi {first_name} — quick check on {init['name'].lower()}. How's it tracking against target this cycle? A sentence or two is all I need."),
            dict(from_="Sweepy", to=first_name, sentVia="Teams", timestamp="2026-09-11T08:02:00+01:00",
                 text=f"Hi {first_name} — following up on the check-in below, this one's now overdue for the leadership review. Even a rough status helps: on track, at risk, or stalled, plus anything blocking you."),
        ],
        replyReceived=False, takeControlAvailable=True, takeControlActive=False,
    ))

assert len(bulletin_threads) == 3

# ---------------------------------------------------------------------------
# Reports — 6 monthly, latest needs review
# ---------------------------------------------------------------------------

on_track = [i for i in initiatives_out if i["status"] == "on_track"]
at_risk = [i for i in initiatives_out if i["status"] == "at_risk"]
stalled = [i for i in initiatives_out if i["status"] == "stalled"]
overdue = [i for i in initiatives_out if i["dataStatus"] == "overdue"]

STATS = dict(total=len(initiatives_out), onTrack=len(on_track), atRisk=len(at_risk),
             stalled=len(stalled), dataOverdue=len(overdue))

REPORT_MONTHS = [(2026, 4), (2026, 5), (2026, 6), (2026, 7), (2026, 8), (2026, 9)]
REVIEW_DATES = {4: "2026-05-07", 5: "2026-06-08", 6: "2026-07-06", 7: "2026-08-05", 8: "2026-09-04"}

reports = []
for idx, (y, m) in enumerate(REPORT_MONTHS):
    is_latest = idx == len(REPORT_MONTHS) - 1
    cm = company_monthly_series[m - 1]
    gap_pct = round((cm["actual"] - cm["target"]) / cm["target"] * 100, 1)
    headline = f"{cm['actual']:,} tCO2e tracked in {human_period(y, m)} — {gap_pct}% above this year's internal target"
    summary = (
        f"{STATS['total']} active initiatives against the 2023-2030 reduction pathway. "
        f"{STATS['onTrack']} on track, {STATS['atRisk']} at risk, {STATS['stalled']} stalled. "
        f"{STATS['dataOverdue']} initiatives have not reported this cycle and are flagged rather than assumed."
    ) if is_latest else (
        f"{STATS['total']} active initiatives tracked. Overall emissions {gap_pct}% above the internal target "
        f"for the month, in line with the surrounding quarter."
    )
    entry = dict(
        id=period_str(y, m), label=human_period(y, m), month=m, year=y,
        generatedBy="Sweepy",
        generatedAt=f"{y:04d}-{m:02d}-{12 if is_latest else 10:02d}T07:30:00+01:00",
        needsReview=is_latest,
        headline=headline, summary=summary, stats=STATS,
    )
    if is_latest:
        entry["highlights"] = [
            {"initiativeId": i["id"], "name": i["name"], "shortName": i["shortName"],
             "note": f"{abs(i['percentVsTarget'])}% {'ahead of' if i['percentVsTarget'] < 0 else 'behind'} target, owned by {i['owner']['name']}."}
            for i in sorted(initiatives_out, key=lambda x: x["percentVsTarget"])[:3]
        ]
        entry["gaps"] = [
            {"initiativeId": i["id"], "name": i["name"], "shortName": i["shortName"], "owner": i["owner"]["name"],
             "note": "No confirmed status this cycle — Sweepy has followed up twice; status shown as last confirmed, not inferred."}
            for i in overdue
        ]
    else:
        entry["reviewedBy"] = LEAD["name"]
        entry["reviewedAt"] = REVIEW_DATES[m]
    reports.append(entry)

reports_out = dict(company=COMPANY, lead=LEAD, reports=list(reversed(reports)))  # newest first

# ---------------------------------------------------------------------------
# Sweepy — Activity feed + Goals
# ---------------------------------------------------------------------------

activity_log = [
    dict(ts="2026-09-12T07:30", text="Generated the September leadership report from confirmed initiative data. Awaiting your review."),
    dict(ts="2026-09-11T08:02", text="Sent a second follow-up via Teams to Daniel Osiel, Yuki Tanaka and Sam Okafor — all three still overdue this cycle."),
    dict(ts="2026-09-10T14:18", text="Flagged a discrepancy on Off-grid cell tower solar & battery: diesel volumes unchanged for two months despite “on track” status."),
    dict(ts="2026-09-09T11:05", text="Consolidated 6 stakeholder responses for the Renewable PPA review. One disagreement flagged on site scope — sent to Sofia Alvarez to resolve."),
    dict(ts="2026-09-08T09:40", text="Suggested Ben Fitzgerald as owner for a new supplier-engagement initiative on fibre contractor emissions. Awaiting confirmation."),
    dict(ts="2026-09-05T16:22", text="Drafted the assignment message for the Q4 packaging initiative. Edited by the lead before sending."),
    dict(ts="2026-09-03T08:00", text="Sent the monthly check-in to all 15 initiative owners via Teams."),
    dict(ts="2026-09-01T10:15", text="Closed out August's discrepancy flag on Retail store energy retrofit — confirmed resolved by Nadia Petrov."),
    dict(ts="2026-08-28T13:47", text="Chased Marcus Webb for August data centre cooling figures. Received same day."),
    dict(ts="2026-08-25T09:12", text="Mapped 3 new emission-factor updates from the 2026 UK Gov conversion factors release across affected initiatives."),
    dict(ts="2026-08-21T09:14", text="Sent the first check-in of the cycle to Daniel Osiel, Yuki Tanaka and Sam Okafor."),
    dict(ts="2026-08-19T15:30", text="Generated the August leadership report. Reviewed and approved by Meera Chandra."),
]

goals = [
    "Create a monthly leadership report from confirmed initiative data, never from memory or inference.",
    "Chase an overdue initiative owner within 48 hours of a missed check-in, and again a week later.",
    "Flag a possible discrepancy without ever overriding a confirmed status — the human decides what happens next.",
    "Keep every initiative's data source, method and quality tagged, so any number can be traced back to where it came from.",
    "Suggest the best-placed owner for a new initiative, and step back once a human has decided.",
    "Surface new initiative opportunities worth a look, without adding one to the programme unasked.",
]

# ---------------------------------------------------------------------------
# Write output
# ---------------------------------------------------------------------------

OUT.mkdir(parents=True, exist_ok=True)
(OUT / "initiatives.json").write_text(json.dumps(dict(company=COMPANY, asOf=str(TODAY), lead=LEAD, initiatives=initiatives_out), indent=2))
(OUT / "activity-data.json").write_text(json.dumps(dict(
    description="Illustrative GHG Protocol-style activity data (5 sites x 10 trailing months = 50 rows per initiative).",
    rowsPerInitiative=50, rows=activity_rows,
), indent=2))
(OUT / "bulletin-threads.json").write_text(json.dumps(bulletin_threads, indent=2))
(OUT / "trajectory.json").write_text(json.dumps(trajectory, indent=2))
(OUT / "reports.json").write_text(json.dumps(reports_out, indent=2))
(OUT / "activity-log.json").write_text(json.dumps(activity_log, indent=2))
(OUT / "goals.json").write_text(json.dumps(goals, indent=2))

old_report = OUT / "leadership-report.json"
if old_report.exists():
    old_report.unlink()

print(f"Wrote {len(initiatives_out)} initiatives, {len(activity_rows)} activity rows, "
      f"{len(bulletin_threads)} bulletin threads, {len(reports)} reports, "
      f"{len(activity_log)} activity-log entries, {len(goals)} goals -> {OUT}")
