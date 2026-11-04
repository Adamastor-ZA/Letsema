"""Chapter 4, section 4.3 Initiative charters. Writes content/ch4/03_charters.json.
Each charter: objective, focus areas, proposed lead and partners, tier, actions by phase (Design / Implement),
dependencies, funding route (rand band open), risks, indicators. Actions come from the Chapter 3 action tables.
I15 to I18 are completed from factsheet_t32.md."""
import json, os
from ch4 import INIT, FUND  # noqa: E402  (re-uses the initiative list and funding routes)

OUT = os.path.join(os.path.dirname(__file__), '..', 'content', 'ch4')
SRC = ["Wesgro operating budget", "provincial and municipal budgets", "national programmes and SOEs", "private capital"]


def funding(code):
    marks = FUND[code].split()
    main = [SRC[i] for i, m in enumerate(marks) if m == '●']
    sup = [SRC[i] for i, m in enumerate(marks) if m == '○']
    s = "Main: " + (", ".join(main) if main else "none") + "."
    if sup:
        s += " Supporting: " + ", ".join(sup) + "."
    return s + " Rand band to be set (section 4.6)."


C = {
 "I1": dict(obj="Raise value per visitor from the mature markets and target every priority market by segment, not by country alone.", tier="Provincial (Wesgro); national alignment with SA Tourism",
   a="Design (2027): segment targets inside each priority market; a shared segment frame with SA Tourism; destination-specific segment research. Implement (2028): move spend from broad awareness to trade-led conversion; luxury-advisor and high-end operator distribution in the UK, USA, Germany, France and Switzerland.",
   e="Segment campaigns at scale; spend per visitor and length of stay added to Wesgro's own targets; segments built into brand tracking.",
   s="Segment research refreshed; budget shifted toward the segments and markets with the highest yield.",
   dep="I6 for seats on the full routes; I16 for spend-per-visitor data; I10 for product quality.",
   risk="Carriers on full routes raise fares rather than seats; SA Tourism's institutional weakness limits joint campaigns (Stakeholder Insights Report, Mar 2026, p25).",
   ind="T1-01, T1-02, T1-03; T2-01, T2-07; T3-01 segment targets in Wesgro's annual plan; T3-02 share of market budget in trade-led conversion."),
 "I2": dict(obj="Build an April to September demand spine from business events and flagship weeks, and sell it with the seats.", tier="Provincial and local; national for delegate visas",
   a="Design (2027): one event acquisition and calendar strategy across Wesgro, the Convention Bureau, the City and the Province; a way to measure meetings, incentives and exhibitions. Implement (2028): publish the calendar; aim bids at May to September; green-season packages with airlines and trade; cooler-season incentive packages for Indian and Gulf planners.",
   e="Regional conferences in Stellenbosch and George; lifestyle events at CTICC in December and January; flower, fynbos and whale events marketed earlier.",
   s="Calendar refreshed each year; a standing bid pipeline for green-season dates.",
   dep="I6 for seats in the trough months; I9 for regional venues; I17 for visas for African delegates.",
   risk="Weather limits summit and outdoor events (Stakeholder Insights Report, Mar 2026, p35); peak hotel prices deter December and January events (p46).",
   ind="T1-05; T2-02 ICCA meetings, T2-03 May to September seat share; T3-03 calendar published; T3-04 bids for May to September events."),
 "I3": dict(obj="Make provincial product bookable where travellers book, district by district.", tier="Provincial and local; national for broadband and payment rules",
   a="Design (2027): a bookability census of provincial product by district. Implement (2028): a digital onboarding drive for small operators and cellars on the West Coast, Route 62 and the Overberg; OTA partnerships with Trip.com, Almosafer and Booking.com; community booking routes with I12.",
   e="Packaged regional itineraries listed on OTAs; CapeNature reservations moved online.",
   s="Census repeated every two years; listing extended to every route.",
   dep="I12 for community routes; I16 for the census data; SA Connect rural broadband.",
   risk="Rural connectivity and payments; compliance cost for small operators.",
   ind="T2-04 share of operators bookable online, T2-05 CapeNature online share; T3-05 census published; T3-06 operators onboarded."),
 "I4": dict(obj="Convert the Indian and Chinese travellers already flying in through hubs, and prepare the direct route case for when runway capacity arrives.", tier="Provincial; national for visas and route designation",
   a="Design (2027): joint market support with Emirates, Qatar Airways and Ethiopian Airlines; activation plans for Xiaohongshu, Douyin and MakeMyTrip. Implement (2028): in-market activation with Trip.com packages and market-specific itineraries; product readiness with Mandarin and Indian-language guiding and Alipay and WeChat Pay.",
   e="Activation at scale; standing relationships with Indian carriers, China Southern and China Eastern.",
   s="Direct route cases taken to carriers as runway capacity arrives, with I6.",
   dep="I6 for route cases; I10 for product readiness; I17 for visas and route designation.",
   risk="Visa processing; no Indian aircraft for a direct route before 2030 (MIDAS Aviation Market Assessment, Mar 2026, Indian Market Opportunity).",
   ind="T1-02; T2-06 India and China hub arrivals; T3-07 hub-carrier agreements; T3-08 route cases prepared."),
 "I5": dict(obj="Hold the regional volume base and grow Nigeria and Kenya as premium markets.", tier="Provincial; national for visas and route liberalisation",
   a="Design (2027): Nigeria and Kenya activation plans; Nigeria and Ghana added to the growth model; consumer research for Botswana, Zambia, Ghana and Rwanda. Implement (2028): premium, trade-led activation; capacity cases on the five full regional routes.",
   e="Conferences with leisure extensions; onward packages for regional travellers who stop in Johannesburg.",
   s="Effort shifted with results; brand seeding in the watch markets.",
   dep="I6 for regional capacity; I2 for conference demand; I17 for visas.",
   risk="Visa friction and budget sensitivity of regional demand (Stakeholder Insights Report, Mar 2026, p45).",
   ind="T1-02; T2-08 African arrivals and spend; T3-09 activation programmes run; T3-10 regional capacity cases made."),
 "I6": dict(obj="Hold and add seats on the full routes until runway relief, and have direct route cases ready when it arrives.", tier="Provincial and local; national for air service agreements; ACSA for airport capacity",
   a="Implement (2027): a seat-retention and frequency programme on the full routes with joint marketing; quarterly runway milestone tracking; a capacity-against-demand model to 2035. Design (2027 to 2028): a public-private air access fund with ring-fenced corridor budgets.",
   e="Fund in operation; frequency and gauge cases on the five full regional routes; growth at George.",
   s="Direct India and China route cases taken to carriers as runway capacity arrives.",
   dep="ACSA's programme at Cape Town International; I17 for air service agreements; I4 and I5 for demand.",
   risk="Runway relief slips; bilateral agreements stay restrictive (section 4.8).",
   ind="T1-01; T2-09 seats and routes, T2-10 routes above 80% load; T3-11 fund constituted; T3-12 runway milestone reports issued."),
 "I7": dict(obj="Grow cruise calls and shore spend through ships that fit, packaged excursions and regional day stops.", tier="Provincial and local; Transnet for ports",
   a="Design (2027): line targeting for ships that fit the 300m berth; Mossel Bay excursion packages; source and define the 250-call plan. Implement (2028): marketing to expedition and home-porting operators; community product on cruise-operator channels.",
   e="Saldanha Bay only if demand is proven; shore power and wind planning with the ports authority.",
   s="Longer itineraries and pre- and post-cruise stays.",
   dep="Berth scheduling by Transnet National Ports Authority; I3 and I12 for bookable shore product.",
   risk="Red Sea reroutes reverse; the 300m ship-length limit (Infrastructure Report, Jul 2026, p110, p112).",
   ind="T2-11 cruise calls and passengers; T3-13 excursion packages listed; T3-14 lines engaged."),
 "I8": dict(obj="Make the transport that exists usable for visitors and aggregate the demand that makes corridor shuttles viable.", tier="Provincial, local and national (PRASA)",
   a="Design and pilot (2027 to 2028): a Southern Line visitor product with the City and PRASA; shuttle demand aggregation on the Garden Route and between Cape Town, Darling and the West Coast; transfers sold inside N2 and R62 itineraries.",
   e="Shuttle products in operation; Central Line recovery, MyCiTi Phase 2 and integrated ticketing.",
   s="A decision on Cape Town to George rapid rail; the last mile to Cape Point.",
   dep="PRASA and the City of Cape Town; the national rule on bank-card payments on the George bus; I9 for itineraries.",
   risk="Rail safety and reliability; shuttle viability at low volumes.",
   ind="T1-06; T2-12 accessibility score, T2-13 corridor transfer products; T3-15 Southern Line product launched; T3-16 shuttle products bookable."),
 "I9": dict(obj="Turn assets outside the Metro into bookable multi-day itineraries, starting with the corridors closest to ready.", tier="Provincial and local; national for SANParks precincts and broadband",
   a="Design (2027 to 2028): itineraries for the six touring routes; a plan to activate cold-zone assets; regional conference offers in Stellenbosch and George.",
   e="Delivery on the Garden Route, the Cape Winelands and the Overberg first, then Route 62 and the West Coast.",
   s="Accommodation and service depth in secondary towns; refreshed flagship product.",
   dep="I3 for bookability; I8 for transfers; I14 for capital.",
   risk="No committed capital for product (Infrastructure Report, Jul 2026, p54, p76); operator capacity.",
   ind="T1-06; T2-14 readiness by district; T3-17 multi-day itineraries listed; T3-18 cold-zone assets activated."),
 "I10": dict(obj="Adopt a provincial quality charter, phased by district, and prepare the province for growth-market visitors.", tier="Provincial; industry",
   a="Design (2027 to 2028): a charter with certification visible on booking platforms; support for SMMEs to comply; readiness standards for language, payments and food.",
   e="Charter adopted and phased by district; investment case for mid-scale hotels with I14.",
   s="Charter embedded in grading; measurement repeated.",
   dep="I14 for mid-scale capital; I18 for skills; I3 for visibility on platforms.",
   risk="Compliance burden on small businesses; skills shortages.",
   ind="T2-15 routes rated Ready; T3-19 charter adopted; T3-20 businesses certified."),
 "I11": dict(obj="Manage visitor flows at the flagship nature sites and steer visitors to under-marketed reserves.", tier="National (SANParks), provincial (CapeNature) and site operators",
   a="Design (2027 to 2028): a baseline of visitor counts and capacity for five flagship sites; marketing of reserves and the Southern Line as alternatives.",
   e="Digital flow management and tiered pricing at the Cableway, Boulders and Cape Point; a visitor management plan for Table Mountain National Park and Boulders.",
   s="Yield measures for nature product; climate-resilient asset formats.",
   dep="I8 for the Southern Line; I16 for data; I13 for climate risk.",
   risk="Operators do not share data; mandates limit pricing (Stakeholder Insights Report, Mar 2026, p44).",
   ind="T2-16 peak Cableway queue; T3-21 flagship baseline published; T3-22 flow tools in place."),
 "I12": dict(obj="Test the Inclusion Plan's model in two or three communities: a seller with a stake, a link to existing demand and gates before any investment.", tier="Local and provincial; national for safety (SAPS)",
   a="Design (2027): pilots chosen on readiness; agreement on who funds a seller with a stake in each; safety plans. Implement (2028): one live booking route per pilot; a fixed-date test; product placed in Wesgro's itineraries and calendars.",
   e="Pilots that meet their thresholds scale; covenants on public assets; links to tourism procurement.",
   s="Extension to more shortlisted communities through channels.",
   dep="I3 for booking routes; I17 for safety; municipal assets.",
   risk="Safety; the selling body is not sustained; capital ahead of demand (SME and Community Inclusion Plan, Sep 2026, p11).",
   ind="T1-07; T2-17 communities with a live booking route; T3-23 pilots selected; T3-24 fixed-date tests held."),
 "I13": dict(obj="Track and plan for climate losses, and give local tourism bodies stable funding with a development mandate.", tier="Provincial and local; national for Treasury Circular 131",
   a="Design (2027 to 2028): a climate and weather risk register for sites and routes; an LTO funding model in response to Circular 131.",
   e="Funding agreements signed; sustainability checks in the quality charter; itineraries routed around closures.",
   s="Climate risk and LTO funding embedded in IDPs with reporting.",
   dep="National Treasury on Circular 131; I10 for the charter.",
   risk="Circular 131 unresolved; further climate events (section 4.8).",
   ind="T2-18 LTOs with a funding agreement, T2-19 weather losses at flagship sites; T3-25 risk register published; T3-26 LTO funding model agreed."),
 "I14": dict(obj="Build a scored pipeline of tourism investments from the gap-closure tables and take it to investors.", tier="Provincial and local; private",
   a="Design (2027 to 2028): a pipeline from the gap tables, scored for return, jobs and inclusion; return projections for the SLA; investment cases for mid-scale and conference hotels and for accommodation at De Hoop and on Route 62.",
   e="Investor engagement; first projects at financial close; a tourism levy and blended finance tested with DEDAT.",
   s="Pipeline refreshed each year; covenants on public assets.",
   dep="I9 and I10 for product and quality; I6 for the air access fund.",
   risk="Capital ahead of demand; tight fiscal space (Stakeholder Insights Report, Mar 2026, p25).",
   ind="T2-20 projects at financial close; T3-27 investment cases prepared; T3-28 investor engagements."),
}


def charter_blocks(code):
    c, n, fa, p, lead, part, cells = next(x for x in INIT if x[0] == code)
    d = C[code]
    rows = [
        ["Objective", d["obj"]],
        ["Focus areas", fa],
        ["Proposed lead", lead],
        ["Partners", part],
        ["Tier of government", d["tier"]],
        ["Activate, 2027 to 2028", d["a"]],
        ["Expand, 2029 to 2031", d["e"]],
        ["Sustain, 2032 to 2035", d["s"]],
        ["Dependencies", d["dep"]],
        ["Funding route", funding(code)],
        ["Risks", d["risk"]],
        ["Indicators", d["ind"]],
    ]
    return [{"type": "pagebreak"}, {"type": "h3", "text": f"{c} {n}"},
            {"type": "grid", "columns": [{"header": "Field", "width": 1.5, "align": "left"}, {"header": "Charter", "width": 6.3, "align": "left"}], "rows": rows, "zebra": True}]


blocks = [
    {"type": "pagebreak"},
    {"type": "h2", "text": "4.3 Initiative charters"},
    {"type": "lead", "text": "Each initiative has a one-page charter that a lead can run from and Steerco can hold to account."},
    {"type": "p", "text": "Every charter uses the same fields. It states the objective, the focus areas served, the proposed lead and partners and the tier of government. It then sets the actions in each phase, marked Design or Implement, and closes with the dependencies, the funding route, the risks and the indicators it moves. Actions come from the Chapter 3 action tables. Leads are proposals for Steerco to confirm, and rand bands are set in section 4.6."},
]
for code in [x[0] for x in INIT]:
    if code in C:
        blocks += charter_blocks(code)
with open(os.path.join(OUT, '03_charters.json'), 'w') as f:
    json.dump({"id": "4.3", "title": "Initiative charters", "blocks": blocks}, f, indent=1, ensure_ascii=False)
    f.write('\n')
print("charters written:", [k for k in C])
