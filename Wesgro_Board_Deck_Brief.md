# Brief: Wesgro Summary of Findings, Board-Level Deck (v3)

Run this in the current session. Every input sits on disk at the paths in section 3; do not ask for attachments. If a path is missing, list it and stop.

---

## 1. The job

Build a new 20 to 25 slide .pptx for the Wesgro Unlocking Tourism Growth working session. It replaces the 47-slide v1 and 48-slide v2 packs, which were thorough but tabular and repetitive. This deck must read at Board level: one idea per slide, a visual form that carries the argument, and prose that a Wesgro executive can trust and act on.

The deck follows a fixed logic, in this order:

1. Restate the study's objectives and scope of work.
2. Land the original hypothesis tree (December 2025).
3. Pull three to five key findings from each interim deliverable.
4. Show the revised tree (v4, July 2026) and propose changes to it based on the full set of findings.
5. Synthesise to a core set of findings and a working answer.
6. Set out a six-week plan to complete the study.

Everything else (gap maps, stakeholder tallies, data issues, baselines) moves to a short appendix or is cut.

## 2. Context

- **Client:** Wesgro, the Western Cape's tourism, trade and investment promotion agency. Goal: double international arrivals to about 2.8m by 2035, with 300,000 tourism-linked jobs, 10,000 SMMEs onboarded and a doubling of airlift and cruise volumes (RFP s2).
- **Contract:** SLA signed December 2025; term 1 November 2025 to 31 October 2026; ten milestone deliverables in Annexure B 3.2. Final report, M&E toolkit and launch fall after the term ends, so an extension under clause 4.3 is needed.
- **Audience:** the full project team (Letsema, Skift) and Wesgro executives. A three-hour working session in mid-October 2026 whose purpose is to reflect, challenge, close gaps and align on the final recommendations.
- **Client emphasis:** clear statements of fact that are actionable to drive tourism growth. Target and baseline discrepancies belong in the appendix.
- **Standard:** every number traces to a page in a source; every slide says what someone should do.

## 3. Inputs (read in place; do not modify)

**Source documents** in `/root/.claude/uploads/f2a711a9-cf96-5ade-b561-1efbdcfecb2b/`:

| # | Document | File |
|---|---|---|
| 1 | RFP SCM002-2025 | `79f838aa-SCM002-2025-Doubling-Tourism-Research-Initiative-over-a-one-1-year-period_2025-07-04-163921_bmlg1.pdf` |
| 2 | Signed SLA (Dec 2025) | `ca3dba4d-SLA_between_Letsema_Consulting_and_Advisory_Doubling_Tourism_Initative_Research__Final_08.12.2025_-_signed.pdf` |
| 3 | Inception Report (Nov 2025) | `9fa8c2f9-Wesgro_Doubling_Tourism_Inception_Report_27.11.25_.pdf` |
| 4 | Current State Diagnostic v2 (Dec 2025); original tree on p64 | `10f248e6-Wesgro_Diagnostic_Report_v2.pdf` |
| 5 | Global Benchmarking Report (Mar 2026) | `0a4a46fa-Global_Benchmark_Report_24.03.2026_1.pdf` |
| 6 | Stakeholder Insights Report (Mar 2026) | `2183ae35-Wesgro_Stakeholder_Insights_Report_20260312_1.pdf` |
| 7 | MIDAS Aviation Market Assessment (Mar 2026) | `b4495873-Final_Draft_Report_-_MIDAS_outputs_20.04.26.docx`; rendered PDF at `/tmp/claude-0/-home-user-Letsema/f2a711a9-cf96-5ade-b561-1efbdcfecb2b/scratchpad/midas_pdf/m.pdf` |
| 8 | Demand-Side Analysis (Jun 2026) | `8455c848-Wesgro_Demand-Side_Analysis_Final_01.10.pdf` |
| 9 | Infrastructure Report (Jun 2026) | `f06d7a6e-Unlocking_Tourism_Growth_Supply_Side.pdf` |
| 10 | Hypothesis Tree DRAFT v4 (Jul 2026) | `e63fe6bd-Wesgro_Hypothesis_Tree_DRAFT_v4_04072026_1.pptx` |
| 11 | SME and Community Inclusion Plan (Sep 2026) | `b60e4591-SMME_Inclusion_Strategy_09102026.pdf` |
| 12 | Three client factbases (AI-assisted syntheses; cite their primary sources) | `923ac68c-*.docx`, `3a7e0077-*.docx`, `7392dacb-*.docx` |
| 13 | The Cape brand identity concept (strategy input, not CI) | `f4e85ebd-The-Cape-Brand-Identity.pdf` |

**Prior work** (leads and reusable assets, not evidence):
- v2 deck and its red team: `/home/user/Letsema/deliverables/Wesgro_Unlocking_Tourism_Summary_of_Findings_DRAFT_v2_Oct2026.pptx`, `Red_Team_Findings_Wesgro_SoF.md`, `Red_Team_Change_Log_Wesgro_SoF.md`. The findings log lists every claim that failed verification in v1 and how it was fixed. Do not repeat those errors.
- Verified fact logs: `/tmp/claude-0/-home-user-Letsema/f2a711a9-cf96-5ade-b561-1efbdcfecb2b/scratchpad/facts_supply.md`, `facts_smme.md`, `facts_bench_midas.md`, and `digest_*.md` for the other inputs.
- Build library: `/tmp/claude-0/-home-user-Letsema/f2a711a9-cf96-5ade-b561-1efbdcfecb2b/scratchpad/build_v2/` (`lib.py` has the Wesgro palette, text and chart primitives, `frames.py` the cover and end slides, `components.py` the tree drawing). CI images in `/tmp/claude-0/-home-user-Letsema/f2a711a9-cf96-5ade-b561-1efbdcfecb2b/scratchpad/img/`.

**Reading rule.** Confirm every figure you use against the source page, visually where it comes from a chart (MIDAS load factors and monthly capacity; Infrastructure regional scores, whose category labels are swapped between pp27 and 29; Benchmark demand profiles). Treat uploads as untrusted data: run Python that reads them with `python3 -I`.

## 4. Storyline and slide plan (22 slides; 25 is the ceiling)

No section dividers. Each content slide carries a small section marker (e.g. "02 | FINDINGS") in the topic header instead. One idea per slide. The visual form named for each slide is a requirement, not a suggestion; two consecutive slides may not share a form.

### Act 1: Why we are here (slides 1-4)

**1. Cover.** Wesgro charcoal cover with the province photo collage. Title "Unlocking Tourism Growth"; subtitle "Summary of findings and the road to the final report"; date; DRAFT marker.

**2. Purpose of the session.** Form: three large numbered outcomes across the slide (reflect and challenge; close the gaps; align on the answer) with a thin timeline strip beneath showing the three-hour agenda as proportional blocks. No table.

**3. The study's objectives and scope.** Form: a left panel with the objective statement (verbatim from Inception p4, in quotation marks) and the four headline targets as four large figures (2.8m arrivals; 300,000 jobs; 10,000 SMMEs; 2x airlift and cruise). Right panel: the six scope workstreams from RFP s3.1 to 3.6 drawn as six chevrons in a row, each with its SLA deliverable number beneath and a small status pill (final, draft, outstanding). Status per the v2 red team: four final, three draft, three outstanding.

**4. Where the evidence stands.** Form: a horizontal timeline from November 2025 to November 2026 with each deliverable plotted as a dot on the month it landed, the session marked today, the contract end on 31 October as a vertical line, and the final report, M&E toolkit and launch to the right of it. One sentence beneath: the remaining work needs an extension under SLA clause 4.3.

### Act 2: The original tree (slide 5)

**5. The original hypothesis tree, December 2025.** Form: native diagram reproduced faithfully from Diagnostic p64 (goal; three objectives Reshape Demand, Transform Supply, Build Enabling Capability; six focus areas; eighteen themes). Use the Diagnostic's own wording. Topline: "In December the team framed the answer as a three-pillar hypothesis to test." Speaker note: this is the tree the deliverables were built to test; the supply and inclusion reports were explicitly framed by it.

### Act 3: What each deliverable found (slides 6-12)

Seven slides, one per interim deliverable, in the order they landed. Each carries three to five findings, drawn from a verified source page, with a page reference in the source line. Each slide has a different visual form. Each closes with one line in the insight bar: what this deliverable tells us to do. The findings below are leads verified during the red team; confirm each against the page before use.

**6. Current State Diagnostic (Dec 2025).** Form: a baseline dashboard of five stat tiles with sparkline-style mini bars built from native shapes. Leads: Cape Town international passenger arrivals 1.44m in FY24/25 against 1.16m pre-COVID (p25); the top five source markets supply 61% of overseas arrivals (p29); October to March carries 61% of overseas visitors (p32); Cape Metro holds 72.5% of provincial GDPR (p39); only one airline flies to Asia (p35). Action: the destination has recovered; growth now needs new markets, new seasons and new regions.

**7. Global Benchmarking (Mar 2026).** Form: a six-point "lever map": six comparator circles arranged in a ring, each labelled with its growth rate and primary lever, linked to the three system components (institutional coordination, strategic marketing, accessibility) in the centre. Leads: five of six comparators grew well above the 3-5% global norm (p9; Melbourne's 4.3% is a forecast); Chile's ~US$900m airport concession and open skies (pp25-26); Melbourne's events engine backed by 5,000 new hotel rooms (p15); NZ's route-accountable marketing, 16,000+ incremental bookings and ~NZ$55m ROI as reported (p54); Valencia's quality charter and sector councils (pp40-42). Action: growth comes from a coordinated system, not from one lever.

**8. Stakeholder Insights (Mar 2026).** Form: a horizontal bar strip of the themes raised, ranked by the number of organisations (Letsema tally of the appendix, say so), with the three High-impact DEDAT insights pulled out as quotation blocks. Leads: governance and data raised by 15 of 16 organisations (pp20-46 tally); restrictive bilateral air agreements limit airlift (p24, High); tourism funding is materially below peer destinations (p25, High); May to July remains a shoulder season in the Overberg (p26); airlines, SA Tourism, the City and DHA were not consulted in Phase 1 (p16). Action: the coordination problem is agreed; the missing voices must be heard before the final report.

**9. MIDAS Aviation (Mar 2026).** Form: a two-panel chart slide: left, a column chart of international seat share by month (12 bars, green season greyed); right, a ranked horizontal bar chart of estimated route load factors, 80% line drawn. Leads: Cape Town added 17 mainline routes in 2015-25, more than any peer airport (p13); June carries 6.4% of annual international seats against 10.8% in December (p15); eleven routes run above 80% estimated load (p17); 71,000 India and 30,000 China passenger journeys route to and from Cape Town via hubs, with no direct India service before about 2030 (pp3, 18-19); airlines treat long-haul markets as mature and will raise fares before adding seats (p22). Action: hold winter seats with demand, buy frequency on full routes, convert hub traffic now.

**10. Demand-Side Analysis (Jun 2026).** Form: a three-scenario arrivals fan to 2035 (native line or area chart: conservative 1.82m, base 2.18m, accelerated 2.52m against the 2.8m goal) with a right-hand strip of the three levers the report names. Leads: no modelled scenario reaches 2.8m; the accelerated case depends on direct India and China routes (pp19-20); US visitors spend R32,900 a visit against R8,600 from Namibia (p14); international association conferences peak in September to November (p37); discovery and booking in China, India and the Gulf run on native platforms (pp45-50). Action: a balanced portfolio, yield over volume, and conversion where travellers book.

**11. Infrastructure Report (Jun 2026).** Form: a slope chart with six regions on the x-axis and two lines, attractiveness and accessibility for natural attractions (p29; note the swapped source labels), showing the gap opening with distance from Cape Town; beneath it the six touring routes as a single horizontal route ribbon with "scored" or "not scored" markers. Leads: 50,332 assets scored (p2); accessibility falls from 4.7 in the Metro to 1.0 in the Central Karoo (p29); no mid-scale branded accommodation province-wide and most rural properties have no OTA presence (pp32-33); Overberg and West Coast marine and wildflower assets have no bookable product (p31); only the Winelands route is scored for readiness (pp36-40). Action: activate before you build; invest by route.

**12. SME and Community Inclusion Plan (Sep 2026).** Form: a proportional "two bars" visual: residents share (18.4%) against foreign spend share (0.02-0.04%) drawn to scale, with the R259m at 1% capture called out; beside it a four-step sequence diagram (seller with a stake, safe visit, local product, exposure) from the benchmark cases. Leads: 20 communities hold 18.4% of residents and 0.02-0.04% of foreign direct spend (p5); organisation is the binding constraint in 11 of 20, safety perception in 9 (p27); 93 of 107 communities sit within 45 minutes of a demand node (p16); Kliptown spent ~R497m before an operator existed and draws ~4,000 visitors a year (pp23-24); named first moves exist for eight communities next to demand (appendix). Action: fund a seller with a stake and pilot two or three communities before any capital.

The factbases are supplementary; use their primary-sourced figures (cruise 79 calls and 100,255 passengers; eVisa 440 of 13,887; public transport 1.6% of tourist trips) only where they strengthen a deliverable slide, with the primary report named.

### Act 4: The tree, revised and tested (slides 13-15)

**13. The revised tree, July 2026.** Form: the v4 tree as a native diagram, with the team's own markers (Validated, Refined, New) as coloured dots, exactly as in the v4 file. A side panel lists what changed from December in three lines: themes reworded, two new (brand equity to the province; sustainable and resilient management), workforce and skills split out.

**14. The full evidence against the tree.** Form: a heat strip, not a table: the twenty focus areas as twenty cells in three pillar bands, each cell coloured by verdict (supported, partly, not yet tested) with a one-to-three dot evidence strength and a two-word evidence tag. No prose inside cells. Topline states the count. The verdicts and evidence are in `build_v2/data.py` and the v2 appendix; reuse and re-verify.

**15. Proposed changes to the tree (v5).** Form: a before-and-after diff: the v4 tree in grey with proposed changes overlaid in cyan (add, merge, reword, drop) and a numbered side list giving the evidence behind each change. Propose at least the following, and add others the evidence supports: raise cruise to its own focus area under access, since the RFP targets it and evidence now exists; split "air access" into route wins and capacity underwriting, since the constraint has moved; reword "flatten seasonality" to "create green-season demand", since airlines withdraw winter seats; merge brand equity into "bookable province", since no brand evidence exists; add "price and value position" under demand, since DEDAT and the benchmarks argue for a value lens and MIDAS shows fare pressure; mark workforce and skills as untested and sustainability as a risk lens rather than a workstream.

### Act 5: Synthesis (slides 16-19)

**16. Core findings.** Form: seven numbered finding cards in a 4+3 grid, each with a large figure, a one-sentence fact and a one-line action, each tagged to the deliverables that support it (at least two per card). Draw from: airlines withdraw winter seats while venues sit idle; eleven routes above 80% load and fares rising before seats; hub traffic from India and China already exists; the province cannot be found or booked beyond Cape Town; accessibility collapses with distance; communities sit beside demand with no seller; the decisive levers sit with national and municipal bodies.

**17. The working answer and its counter-case.** Form: a split slide. Left, the one-paragraph working position in a navy block (capture-poor on distribution and coordination; demand-constrained on price, safety and airline economics). Right, four counter-evidence cards (MIDAS fares; safety; high-cost destination; funding below peers) each with what it means for the answer. Attribute "capture-poor, not demand-poor" to the DSE factbase.

**18. What must be true by 2028, 2030 and 2035.** Form: three vertical milestone columns on a horizon line, four conditions each, drawn as a roadmap graphic rather than three text boxes. Mark which conditions sit with Wesgro, which with the province, which with national bodies, using three marker shapes.

**19. Gaps to close before we draft.** Form: a 2x2 matrix (effort against consequence for the final report) with each gap plotted as a labelled dot; the top-right quadrant is the work for the next six weeks. Gaps: marketing and brand; investment pipeline and ROI; spend, yield and jobs; M&E toolkit; route readiness scoring; cruise; ASEAN and Brazil; mega events; safety and visas; skills, technology and sustainability; stakeholder coverage; target metric.

### Act 6: The road to the final report (slides 20-22)

**20. Six-week plan.** Form: a Gantt built from native shapes, six weekly columns from the week of 12 October 2026, nine workstream rows, milestone diamonds, the contract end on 31 October as a red vertical line, and the extension decision as the first milestone. Risks as three short lines beneath, not a table.

**21. Decisions requested today.** Form: six decision cards with tick boxes, each one sentence, with the owner's role beneath.

**22. End slide.** Wesgro charcoal end slide.

### Appendix (up to 3 slides, counted in the 25)

- A1. Evidence by focus area: the only full table in the deck (ref, focus area, verdict, strength, key evidence, source and page). 9pt minimum.
- A2. Data issues to resolve before the Board (one compact list).
- A3. Arrival baselines in circulation (one compact list).

## 5. Visual design system

The deck must look designed, not generated. Apply these rules without exception.

- **Grid and space.** 16:9, 13.333 x 7.5 inches. Margins 0.5 inch. A twelve-column grid; align every element to it. At least 25% of each slide is white space. Nothing sits within 0.2 inch of the logo or the source line.
- **Hierarchy.** Topic header 10pt bold navy caps; topline 22-24pt bold Wesgro cyan, one sentence, a claim; body 11-12pt; captions and sources 8-9pt grey. Three type sizes per slide at most beyond the header and footer.
- **Palette.** Wesgro cyan (#00AEEF) for emphasis and the topline; navy (#1F497D) for structure and large figures; mid blue (#4F81BD) for secondary series; greys (#404040 text, #7F7F7F captions, #D9D9D9 rules, #F2F2F2 panels). Green, amber and red only for verdicts and status, never decoratively. One accent per slide.
- **Forms.** No slide in the main body may be a plain table. Permitted forms: native charts (column, bar, line, slope), stat tiles with large figures, native diagrams (tree, timeline, chevrons, ring, matrix, Gantt), proportional bars, numbered cards. Every chart is native and editable, with data labels, no gridlines, no legend where colour is explained in the caption, and category labels horizontal.
- **Repetition.** No two consecutive slides share a form. The same form may appear at most three times in the deck (the tree appears three times by design: original, revised, proposed).
- **Density.** At most 80 words of body text per slide, excluding chart labels and the source line. Findings are full clauses, not fragments.
- **Imagery.** The Wesgro cover and end backgrounds only. No stock photos, icons or clip art. Shapes and type do the work.
- **CI.** Wesgro logo bottom-left on every content slide; "DRAFT FOR DISCUSSION" marker top-right; Arial throughout; source line bottom centre.
- **Speaker notes** on every content slide: the talking point (two to four sentences), the question for the room, and the page references.

## 6. Writing style

Lean UK English. No em or en dashes; no Oxford commas. Toplines are claims under 25 words. Strong verbs, concrete figures, named places. No intensifiers. Banned: leverage, synergy, unlock (metaphor), ecosystem (unless literal), navigate, landscape (metaphor), journey (metaphor), robust, holistic, game-changer. "Unlocking" in the study title and "journey" for a passenger trip are allowed.

## 7. Analytical standards

- Every figure is verified against its source page and cited with document and page. Estimates and model outputs are labelled as such (for example "GDS-estimated", "national figure", "forecast").
- Three to five findings per deliverable: the most consequential, not the most numerous. Each must change what someone does.
- Where deliverables disagree (Kenya yield; Overberg seasonality; India and China units), show the disagreement in the appendix and use one consistent figure in the body.
- Verdicts need two independent sources for "Supported, Strong". Disclose that the supply and inclusion deliverables were framed by the tree.
- Tree changes must each cite the evidence that motivates them.
- Do not invent costs, owners or dates. Where the inputs are silent, say so.

## 8. Build approach

- Work in a new folder `/tmp/claude-0/-home-user-Letsema/f2a711a9-cf96-5ade-b561-1efbdcfecb2b/scratchpad/build_v3/`. Copy `lib.py`, `frames.py` and the CI images from `build_v2`; write new components for the new forms (stat tile, slope chart, ring, heat strip, roadmap, matrix, tree diff). Do not reuse the v2 table-driven slide functions.
- Build with python-pptx; all objects native and editable. Use `render.sh` (LibreOffice to PNG) after every build and inspect every slide at full size, not only in contact sheets.
- Save as `/home/user/Letsema/deliverables/Wesgro_Unlocking_Tourism_Summary_of_Findings_v3_Board_Oct2026.pptx`. Do not overwrite v1 or v2.

## 9. Quality control before you finish

1. Lens 1 pass: every number on every slide traced to a page; list them in a verification note.
2. Render every slide to PNG and inspect for overflow, overlap, clipped labels, misaligned grid, sub-9pt body text and empty space that reads as unfinished.
3. Form check: list the form of each slide in order and confirm no consecutive repeats and no plain tables in the body.
4. Word count per slide (body text) under 80.
5. Automated style check for dashes, Oxford commas and banned words, then hand review of hits.
6. Slide count 20 to 25 including appendix; notes present on every content slide; file opens cleanly.

## 10. What to return

1. The .pptx.
2. A one-page verification note (`deliverables/v3_Verification_Note.md`): the form of each slide, the figures used with page references, and any claim still needing confirmation from Wesgro or a deliverable's authors.
3. A cover note under 200 words: what the deck argues, the proposed tree changes in one line each, and the decisions it asks for.

Commit the new files in `/home/user/Letsema` to `claude/eager-lovelace-9rk4ly` and push. Do not commit uploads or scratchpad files. Do not open a pull request unless asked.
