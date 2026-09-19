#!/usr/bin/env python3
"""
Content for the two EY decks. Edit here, then run scripts/deck_build.py.

Each entry names the template slide it is built on and the content that goes
into that slide's placeholders. Slide titles are sentence case and unique, as
EY's accessibility standard requires. The first line of every content
placeholder is the topline: the declarative sentence stating what the slide
argues.

Nothing here is invented. Where an input is missing it carries the same
[[TO CONFIRM: ...]] marker as the two PDFs, and it is logged in
qa/open_items.md.
"""

RFP = "Conservation International  |  RFP 0032026"
SCAN_SOURCE = (
    "Source: EY benchmark scan of 31 brands, networks and mechanisms, September 2026. "
    "Figures are as published by each source and are not yet verified with the "
    "organisations concerned; verification is the first task of Activity One."
)

BOILERPLATE = {
    "base": "slide65.xml",
    "kind": "boilerplate",
    "descriptor": "Business Consulting  |  Sustainability and development advisory",
    "copyright": "© 2026 [[TO CONFIRM: EY member firm legal entity name]]. ",
    "doc_code": "[[TO CONFIRM: document code]]",
    "ed_code": "[[TO CONFIRM: ED code]]",
}


# ============================================================ TECHNICAL DECK ===

TECHNICAL = [
    {
        "base": "slide6.xml",
        "kind": "cover",
        "title": "Brand-delivery support models for emerging protected areas",
        "title_size": 28,
        "subtitle": "EY technical proposal to Conservation International, RFP 0032026",
        "date": "19 September 2026",
    },
    {
        "base": "slide24.xml",
        "kind": "contents",
        "title": "Contents",
        "size": 16,
        "left": [
            "01  Understanding the assignment",
            "02  Where we start",
            "03  Approach and method",
            "04  Team, capability and references",
        ],
        "right": [
            "What CI is asking, the three constraints that define the answer "
            "space, and the aggregation layer that already exists",
            "The Activity One long-list, built before this proposal and at our "
            "own cost",
            "The three activities, how options are built and scored, and the "
            "twelve-week plan",
            "Who delivers, capability against the eight required skills, and "
            "geographical reach",
        ],
    },

    # -- 01 Understanding ----------------------------------------------------
    {
        "base": "slide18.xml",
        "kind": "section",
        "eyebrow": "01",
        "title": "Understanding the assignment",
    },
    {
        "base": "slide32.xml",
        "kind": "content",
        "title": "What Conservation International is actually asking",
        "size": 17,
        "body": [
            "CI is not asking for park brands. It is asking how park brands "
            "should be built, paid for and kept alive once the money that "
            "started them has gone.",
            (1, "The assignment is a design and feasibility study on delivery "
                "models, explicitly not a branding exercise."),
            (1, "Its real test is whether the recommended model still stands in "
                "year five without a grant behind it."),
            (1, "That turns the central design question from how large the grant "
                "should be into who pays, for what and why they keep paying."),
        ],
    },
    {
        "base": "slide34.xml",
        "kind": "columns",
        "title": "Three constraints define the answer space",
        "idx": [1, 13, 14],
        "size": 15,
        "columns": [
            [
                ("h", "Resourcing"),
                (1, "The 15 priority areas have neither the budget nor the "
                    "in-house capacity to run sophisticated brands."),
                (1, "Aggregation is therefore the premise of the brief rather "
                    "than one option inside it."),
            ],
            [
                ("h", "Jurisdiction"),
                (1, "The areas sit across Southern, Eastern and Western Africa "
                    "under different park authorities, co-management partners "
                    "and national tourism boards."),
                (1, "Any model must cross borders without becoming a rival to "
                    "the national destination brands it depends on."),
            ],
            [
                ("h", "Permanence"),
                (1, "CI will fund implementation to start, but the model must "
                    "eventually find its own money."),
                (1, "The payer is the design question, not the size of the "
                    "grant."),
            ],
        ],
    },
    {
        "base": "slide42.xml",
        "kind": "content",
        "title": "The aggregation layer already exists in much of the target geography",
        "size": 15,
        "body": [
            "CI asks that the models be compared against existing efforts so the "
            "chosen one fills a gap rather than duplicating work already under "
            "way. In Africa that instruction bites.",
            (1, "NACSO links the organisations serving Namibia's 86 registered "
                "communal conservancies on a single Event Book monitoring system."),
            (1, "The Northern Rangelands Trust pools governance, security and "
                "enterprise support for 43 conservancies."),
            (1, "MMWCA speaks for 24 Mara conservancies, roughly 16,500 "
                "landowners and 50 tourism partners."),
            (1, "CI has already worked through MMWCA, co-creating the US$5m "
                "Maasai Mara Rescue Fund in 2020."),
            "A model that ignores that layer will duplicate it.",
        ],
        "source": SCAN_SOURCE,
    },

    # -- 02 Where we start ---------------------------------------------------
    {
        "base": "slide19.xml",
        "kind": "section",
        "eyebrow": "02",
        "title": "Where we start",
    },
    {
        "base": "slide36.xml",
        "kind": "keynumbers",
        "title": "The Activity One long-list is already built",
        "size": 13,
        "numbers": [
            ("31", "brands, networks and mechanisms, each profiled on scale and "
                   "offer, funding, governance and read-across for CI"),
            ("7", "archetypes, sorted by what the central entity actually does, "
                  "from shared services to curated commercial collectives"),
            ("13", "deep-dives already selected and scoped: eight case studies, "
                   "two of them clustered, and five light-touch checks"),
        ],
        "source": SCAN_SOURCE,
    },
    {
        "base": "slide26.xml",
        "kind": "statement",
        "text": "Activity One starts at the deep-dive, not the long-list.",
    },
    {
        "base": "slide43.xml",
        "kind": "columns",
        "title": "What the head start buys CI",
        "idx": [16, 15],
        "size": 15,
        "columns": [
            [
                ("h", "Nine weeks of runway instead of six"),
                (1, "Interview requests go out in week one rather than week four."),
                (1, "Boundless Southern Africa, Africa's Eden Tourism, The Long "
                    "Run and Preferred Hotel Group publish neither fees nor "
                    "outcomes, and in our experience a cold approach to a "
                    "regional secretariat takes three to four weeks to produce a "
                    "substantive reply."),
                (1, "Measured to the week 10 draft, the terms nobody publishes "
                    "get nine weeks to surface instead of six."),
            ],
            [
                ("h", "A structure that carries evidence forward"),
                (1, "CI's nine model-elaboration headings become the template "
                    "every deep-dive is written to."),
                (1, "The rating matrix becomes the scoring frame for the options, "
                    "so evidence carries straight from Activity One into Activity "
                    "Two without re-cutting."),
                (1, "The scan also names the four evidence gaps only primary "
                    "contact will close, including CI's own list of the 15 "
                    "priority areas."),
            ],
        ],
        "source": SCAN_SOURCE,
    },

    # -- 03 Approach ---------------------------------------------------------
    {
        "base": "slide20.xml",
        "kind": "section",
        "eyebrow": "03",
        "title": "Approach and method",
    },
    {
        "base": "slide44.xml",
        "kind": "columns",
        "title": "The method follows CI's three activities and uses CI's own structure as its spine",
        "idx": [1, 13, 14],
        "size": 13,
        "columns": [
            [
                ("h", "Activity One: situational analysis and best practice"),
                (1, "We verify and deepen the scan rather than rebuild it."),
                (1, "Every figure is re-checked against its primary source and "
                    "graded as verified with the organisation, published primary "
                    "or secondary. Nothing below the top two grades drives the "
                    "base case of any financial model."),
                (1, "Failure patterns are named as plainly as the successes. The "
                    "European Charter network fell from 164 protected areas in 20 "
                    "countries to 91 in 13."),
            ],
            [
                ("h", "Activity Two: option design and evaluation"),
                (1, "Five or six configurations are built against archetype "
                    "anchors, then screened with CI in week 7 once comments on "
                    "the Activity One draft are in."),
                (1, "Each carried option is elaborated under all nine CI headings, "
                    "with a cost band, its pre-requisites and a ten-year model "
                    "behind it."),
                (1, "We publish the two or three assumptions that would flip the "
                    "result."),
            ],
            [
                ("h", "Activity Three: next steps"),
                (1, "We set out the implementation path for the preferred model, "
                    "the further research and the stakeholder sensitisation "
                    "required."),
                (1, "We then draft the Terms of Reference for the design "
                    "assignment that follows."),
            ],
        ],
    },
    {
        "base": "slide42.xml",
        "kind": "content",
        "title": "Every option is built by setting three switches the benchmarks expose",
        "size": 15,
        "body": [
            "The benchmarks differ from one another on three choices, and those "
            "choices drive cost, control and who pays.",
            (1, "Who belongs and who pays. Park authorities are the obvious "
                "members but the weakest payers; lodges, operators and visitors "
                "hold the money."),
            (1, "How it crosses borders, whether through one regional "
                "secretariat, national operators, mutual recognition of national "
                "schemes or a cross-border legal vehicle."),
            (1, "How it sits with the national destination brand, whether owned "
                "by the tourism board, structured as a co-brand hub or "
                "independent."),
            "Options are then scored on the benchmark matrix extended to eleven "
            "criteria, adding non-duplication of what already exists, resilience "
            "in unstable funding environments and multi-stakeholder brand "
            "management. The weighting is CI's to set.",
        ],
        "source": SCAN_SOURCE,
    },
    {
        "base": "slide45.xml",
        "kind": "columns",
        "title": "Four starting hypotheses, declared so CI can hold us to changing our minds",
        "idx": [1, 13, 14, 15],
        "size": 12,
        "columns": [
            [
                ("h", "The Shared Studio"),
                (1, "Brand toolkit, studio and data spine the areas draw down on, "
                    "delivered through the associations that already serve them."),
                (1, "Paid by CI and Keystone donors first, then association "
                    "subscriptions and per-unit production charges."),
                (1, "NPS Harpers Ferry Center; NACSO; NRT; MMWCA"),
            ],
            [
                ("h", "The Keystone Mark"),
                (1, "Tiered standard certifying areas, plus a mark licensed to "
                    "the businesses and products around them, run through "
                    "national operators."),
                (1, "Areas pay assessment and revalidation; certified businesses "
                    "pay licence fees."),
                (1, "Blue Flag; UNESCO Global Geoparks; Slovenia Green; Fair "
                    "Trade Tourism"),
            ],
            [
                ("h", "The Co-Brand Hub"),
                (1, "Thematic routes and ready-made co-brandable product handed "
                    "to national tourism boards for their own campaigns."),
                (1, "Paid by tourism boards and regional bodies from budgets they "
                    "already spend, with development finance for the build."),
                (1, "World Heritage Journeys; KAZA 'Rivers of Life'; Signature "
                    "Experiences of Australia"),
            ],
            [
                ("h", "The Keystone Collection"),
                (1, "Curated collection of lodges and experiences sold through an "
                    "existing platform's distribution and loyalty infrastructure."),
                (1, "Paid by member lodges and operators through fees and "
                    "commissions, with a licence fee back to the parks."),
                (1, "Beyond Green; SLH Considerate Collection; Experience Mekong "
                    "Collection; LHW"),
            ],
        ],
        "source": SCAN_SOURCE,
    },
    {
        "base": "slide58.xml",
        "kind": "table",
        "title": "Twelve weeks, four deliverables, two clear weeks for comment before the final",
        "widths": [1.0, 1.1, 4.6, 3.1, 2.4],
        "size": 10,
        "table": [
            ["Weeks", "Activity", "Work", "Deliverable", "What CI provides"],
            ["1-2", "Inception",
             "Kick-off; confirm the 15 areas; agree scope, evaluation frame and "
             "interview list; issue interview requests",
             "Inception report (week 2)",
             "Priority-area list, stakeholder contacts, kick-off"],
            ["3-5", "One",
             "Source verification; 13 deep-dives against the nine headings; "
             "interviews; synthesis and design principles",
             "Draft situational analysis and best practice assessment (week 5)",
             "Introductions to named secretariats"],
            ["6-7", "One / Two",
             "Demand-side read; option architecture; week 7 screening session; "
             "financial modelling",
             "Option architecture note and screening record",
             "Comments on the week 5 draft by mid-week 7; screening"],
            ["8-9", "Two",
             "Elaboration of each carried option to the nine headings; "
             "stakeholder pros and cons; scoring",
             "Draft option set for internal review", "-"],
            ["10", "Two",
             "Recommendation and expected results; presentation to CI and "
             "nominated stakeholders",
             "Draft report and presentation on brand delivery models (week 10)",
             "Stakeholder convening and attendance"],
            ["11", "Two / Three",
             "Adapt the preferred model on feedback; implementation path; draft "
             "Terms of Reference",
             "-", "Consolidated comments by end of week 11"],
            ["12", "Three", "Final report combining all elements",
             "Final report (week 12)", "Acceptance"],
        ],
    },

    # -- 04 Team and credentials --------------------------------------------
    {
        "base": "slide21.xml",
        "kind": "section",
        "eyebrow": "04",
        "title": "Team, capability and references",
    },
    {
        "base": "slide58.xml",
        "kind": "table",
        "title": "A deliberately small team, because continuity of thinking beats headcount here",
        "widths": [3.0, 5.6, 3.7],
        "size": 11,
        "table": [
            ["Role", "On this assignment", "Named individual"],
            ["Engagement partner",
             "Direction, quality review of every deliverable, CI escalation, "
             "presentation",
             "Michael Harris, Partner, EY Business Consulting, South Africa"],
            ["Engagement manager",
             "Delivery, work plan, interview programme, drafting lead",
             "[[TO CONFIRM: named manager, grade and CV]]"],
            ["Senior consultant, business models and finance",
             "Financial sustainability model behind each option; cash flows and "
             "funding needs",
             "[[TO CONFIRM: named senior consultant, CV]]"],
            ["Consultant, research and analysis",
             "Deep-dives, source verification, interview support, evidence base",
             "[[TO CONFIRM: named consultant, CV]]"],
            ["Adviser, destination branding",
             "Brand architecture, national brand alignment, review of the option set",
             "[[TO CONFIRM: named adviser; EY-employed or consortium partner]]"],
            ["Adviser, conservation and protected-area tourism",
             "Conservation-led design, community and co-management perspectives",
             "[[TO CONFIRM: named adviser; EY-employed or consortium partner]]"],
        ],
        "source": "CVs are at Annex A of the technical proposal. Effort by role is "
                  "set out in the separate cost proposal.",
    },
    {
        "base": "slide42.xml",
        "kind": "content",
        "title": "Capability against the eight minimum skills the RFP sets",
        "size": 15,
        "body": [
            "Annex C maps EY's evidence against each of the eight. Two warrant "
            "comment here.",
            (1, "Destination branding and protected-area conservation experience "
                "are the two where a mainstream consulting credential is least "
                "likely to satisfy a conservation organisation on its own."),
            (1, "The RFP expressly permits a consortium or partnership. We will "
                "name a specialist partner for either rather than stretch a "
                "general credential to cover it."),
            "Relevant experience, recent services with samples, geographical "
            "reach and staff qualifications carry 60 of the 70 technical marks "
            "between them, so the annexes carry this proposal.",
            (1, "[[TO CONFIRM: outcome of the capability review against the eight "
                "skills, and the consortium decision. Owner: Michael Harris.]]"),
        ],
    },
    {
        "base": "slide43.xml",
        "kind": "columns",
        "title": "Geographical reach, and how we protect the timetable",
        "idx": [16, 15],
        "size": 14,
        "columns": [
            [
                ("h", "Reach argued in three layers, each falsifiable"),
                (1, "Network: EY member firms in the countries holding CI's "
                    "priority areas, stated country by country."),
                (1, "Delivery: assignments actually run in Southern, Eastern and "
                    "Western Africa in the last five years, named by country and "
                    "year."),
                (1, "Subject familiarity: the African evidence this assignment "
                    "turns on is concentrated in Southern and Eastern Africa, "
                    "which is where a South Africa-led team sits."),
                (1, "Western Africa is thin in the published record for everyone "
                    "working on this question, and we say so rather than imply "
                    "coverage the record does not support."),
            ],
            [
                ("h", "The two risks that drive the schedule"),
                (1, "Interview response times, which is why requests go out in "
                    "week one and why no deep-dive depends on a single interview "
                    "landing."),
                (1, "Compression of the final fortnight, which is why a "
                    "consolidated CI comment deadline is agreed at inception for "
                    "the end of week 11."),
                (1, "The full register is at Annex D of the technical proposal."),
            ],
        ],
    },
    {
        "base": "slide27.xml",
        "kind": "statement",
        "text": "A bidder with no starting position has nothing for CI to argue with.",
    },
    BOILERPLATE,
]


# ================================================================= COST DECK ===

COST = [
    {
        "base": "slide6.xml",
        "kind": "cover",
        "title": "Cost proposal",
        "subtitle": "EY cost proposal to Conservation International, RFP 0032026",
        "date": "19 September 2026",
    },
    {
        "base": "slide36.xml",
        "kind": "keynumbers",
        "title": "A fixed price, built bottom-up from the work",
        "size": 13,
        "number_size": 40,
        "numbers": [
            ("US$40,000", "fixed price for the full scope over 12 weeks, "
                          "all-inclusive of profit, fees and taxes, with no cost "
                          "sought after award"),
            ("58 days", "of professional effort across six roles, each mapped to "
                        "a named activity and then to one of the four "
                        "deliverables"),
            ("US$621", "blended rate per day, derived from the effort model and "
                       "the published ceiling rather than from a rate card"),
        ],
    },
    {
        "base": "slide26.xml",
        "kind": "statement",
        "text": "The scope was sized to the budget, not the other way round.",
        "size": 60,
    },
    {
        "base": "slide58.xml",
        "kind": "table",
        "title": "Professional fees by role",
        "widths": [6.0, 1.9, 2.2, 2.2],
        "aligns": ["l", "r", "r", "r"],
        "size": 12,
        "table": [
            ["Role", "Days", "Rate US$ per day", "Total US$"],
            ["Engagement partner", "5", "1,100", "5,500"],
            ["Engagement manager", "16", "725", "11,600"],
            ["Senior consultant, business models and finance", "13", "575", "7,475"],
            ["Consultant, research and analysis", "19", "375", "7,125"],
            ["Adviser, destination branding", "3", "900", "2,700"],
            ["Adviser, conservation and protected-area tourism", "2", "800", "1,600"],
            ["Total professional fees", "58", "", "36,000"],
        ],
        "source": "The rate card is not among the inputs used to build this "
                  "proposal, so nothing is claimed here about how these rates "
                  "compare to it. [[TO CONFIRM: EY Africa rate card and internal "
                  "approval of these rates.]]",
    },
    {
        "base": "slide58.xml",
        "kind": "table",
        "title": "Direct costs, all four of them named and necessary",
        "widths": [5.4, 1.6, 1.5, 2.0, 2.0],
        "aligns": ["l", "l", "r", "r", "r"],
        "size": 12,
        "table": [
            ["Line item", "Unit", "Qty", "Unit price US$", "Total US$"],
            ["Market reports, datasets and database access", "Purchase", "4", "350", "1,400"],
            ["Specialist translation of non-English primary sources", "Word", "10,000", "0.10", "1,000"],
            ["Interview transcription", "Interview", "16", "35", "560"],
            ["Report and presentation design and production", "Hour", "16", "65", "1,040"],
            ["Total direct costs", "", "", "", "4,000"],
        ],
        "source": "No travel, accommodation or subsistence is included. The RFP "
                  "states the assignment is desk-based and requires no travel.",
    },
    {
        "base": "slide58.xml",
        "kind": "table",
        "title": "Effort and payment follow the four contractual deliverables",
        "widths": [5.2, 1.2, 1.4, 1.5, 1.4, 1.6],
        "aligns": ["l", "r", "r", "r", "r", "r"],
        "size": 12,
        "table": [
            ["Deliverable", "Week", "Days", "Share", "%", "US$"],
            ["Inception report", "2", "7", "12%", "10%", "4,000"],
            ["Draft situational analysis and best practice assessment", "5", "19", "33%", "30%", "12,000"],
            ["Draft report and presentation on brand delivery models", "10", "22", "38%", "35%", "14,000"],
            ["Final report, next steps and Terms of Reference", "12", "10", "17%", "25%", "10,000"],
            ["Total", "", "58", "100%", "100%", "40,000"],
        ],
        "source": "No more than 10% sits on the inception report, as the RFP "
                  "requires. Ninety per cent of the price is released only after "
                  "CI has accepted substantive analysis.",
    },
    {
        "base": "slide42.xml",
        "kind": "content",
        "title": "What the budget narrative has to explain, and does",
        "size": 15,
        "body": [
            "The RFP requires an explanation of the basis of every cost element, "
            "so each line is justified against the work it buys.",
            (1, "Partner days sit where partner time changes the answer: "
                "kick-off, the week 7 screening, the recommendation, the week 10 "
                "presentation and final sign-off."),
            (1, "The consultant carries the largest day count because source "
                "verification and the 13 deep-dives are the largest single task."),
            (1, "Activity Three is costed rather than absorbed: 4 of the 10 days "
                "on deliverable 4 cover the implementation path and the Terms of "
                "Reference."),
            (1, "One consolidated CI comment round on each draft is carried "
                "inside the figures, because acceptance is the stated criterion "
                "for both."),
            (1, "There is no contingency line. The price is fixed and scope risk "
                "sits with EY."),
        ],
    },
    {
        "base": "slide34.xml",
        "kind": "columns",
        "title": "Why this represents value, beyond being inside the ceiling",
        "idx": [1, 13, 14],
        "size": 14,
        "columns": [
            [
                ("h", "CI is not paying for the starting line"),
                (1, "EY completed the 31-benchmark scan before this proposal was "
                    "written and at its own cost."),
                (1, "That contribution is why a 58-day programme can carry 13 "
                    "deep-dives, 16 interviews and four elaborated options."),
            ],
            [
                ("h", "Every line is auditable arithmetic"),
                (1, "Unit price times quantity, days mapped to named roles and "
                    "then to the four deliverables, and a total that reconciles "
                    "exactly."),
                (1, "There is no lump sum standing in for a calculation."),
            ],
            [
                ("h", "Risk sits with EY, not CI"),
                (1, "The price is fixed and all-inclusive, and no cost can be "
                    "added after award."),
                (1, "Any transaction tax that proves chargeable is absorbed "
                    "within the total rather than added to it."),
            ],
        ],
    },
    {
        "base": "slide43.xml",
        "kind": "columns",
        "title": "Tax treatment and the assumptions the price holds on",
        "idx": [16, 15],
        "size": 14,
        "columns": [
            [
                ("h", "Taxes"),
                (1, "The expected treatment is that services supplied by a South "
                    "African EY entity to CI, as a non-resident of South Africa, "
                    "are zero-rated for South African VAT as exported services."),
                (1, "That turns on CI's contracting entity and its country of "
                    "registration, neither of which is stated in the RFP."),
                (1, "[[TO CONFIRM: EY tax to confirm the VAT and withholding "
                    "position.]]"),
            ],
            [
                ("h", "Assumptions"),
                (1, "Desk-based with no travel, and all interviews and "
                    "presentations run virtually."),
                (1, "CI supplies the list of 15 priority areas and the "
                    "stakeholder contacts at inception, and brokers introductions "
                    "in week 1."),
                (1, "One consolidated comment round on each draft, within the "
                    "agreed windows."),
                (1, "Deliverables in English; the stakeholder presentation "
                    "delivered twice, both virtually."),
            ],
        ],
    },
    BOILERPLATE,
]


DECKS = {
    "technical": {
        "file": "EY_Technical_Proposal_Deck_CI_RFP_0032026.pptx",
        "plan": TECHNICAL,
    },
    "cost": {
        "file": "EY_Cost_Proposal_Deck_CI_RFP_0032026.pptx",
        "plan": COST,
    },
}
