import sys, re, json, csv
from collections import OrderedDict
sys.path.insert(0, '/tmp/claude-0/-home-user-Letsema/98b96bfe-2843-55b4-9fb2-4f4083c56589/scratchpad/scripts')
from dxst import *
OUT = '/home/user/Letsema/wesgro_v15_style/output/'
d = Doc(); kids = list(d.body)
units = []; s1 = s2 = ''
for el in kids:
    if el.tag == q('w:p'):
        st = pstyle(el); t = ptext(el).strip()
        if st in ('Heading1', 'Heading1Front'): s1 = t; s2 = ''; continue
        if st == 'Heading2': s2 = t; continue
        if st in ('TOCL1', 'TOCL2') or not t: continue
        units.append((s1, s2, t))
    else:
        for p in el.iter(q('w:p')):
            t = ptext(p).strip()
            if t: units.append((s1, s2, t))
units = [u for u in units if u[0] not in ('Foreword', 'Contents', 'Figures', 'Tables', 'Abbreviations')]
def loc(s1, s2):
    if s1 == 'Executive summary': return 'ES'
    m = re.match(r'^(\d\.\d|A\d)', s2); return m.group(1) if m else s1[:12]
def scan(pats):
    forms = OrderedDict(); locs = OrderedDict(); n = 0
    for s1, s2, t in units:
        for p in pats:
            for m in re.finditer(p, t):
                forms[m.group(0).strip()] = forms.get(m.group(0).strip(), 0) + 1; locs[loc(s1, s2)] = 1; n += 1
    return forms, list(locs), n
M = [  # id, measure, patterns, canonical, unit, period, source, note
 ('H01', 'International arrivals through Cape Town International, latest year', [r'\b1\.57 ?(?:m\b|million)'], '1.57 million', 'arrivals', 'FY25/26', 'Diagnostic p25; Demand-Side Analysis p11 (ACSA count)', '35% above FY19/20: 1.57 / 1.16 = 1.353, reconciles'),
 ('H02', 'International arrivals, FY24/25', [r'\b1\.44 ?(?:m\b|million)'], '1.44 million', 'arrivals', 'FY24/25', 'Diagnostic p25', ''),
 ('H03', 'International arrivals, last pre-pandemic year', [r'\b1\.16 ?(?:m\b|million)'], '1.16 million', 'arrivals', 'FY19/20', 'Diagnostic p25', ''),
 ('H04', 'Growth model base', [r'1,498,829', r'about 1\.5 million', r'\b1\.5 ?m\b(?! international tourists)', r'the 1\.5 million of 2025'], '1,498,829', 'arrivals', '2025', 'Market Assessment p19', 'Rounded to 1.5 million in the summary and 4.1. Counting basis unconfirmed (register OI-50, OI-51)'),
 ('H05', 'Base case, 2035', [r'2,175,778', r'\b2\.18 ?(?:m\b|million)', r'about 2\.2 million', r'2\.2 million to 2\.5 million', r'about 2\.2m'], '2,175,778', 'arrivals', '2035', 'Market Assessment p19; Demand-Side Analysis p20', 'Three roundings in use: 2,175,778; 2.18m; about 2.2 million'),
 ('H06', 'Accelerated case and target, 2035', [r'2,516,282', r'\b2\.52 ?m\b', r'\b2\.5 ?(?:m\b|million)'], '2,516,282 (target stated as 2.5 million)', 'arrivals', '2035', 'Market Assessment p19', 'The target is the accelerated case rounded (1.1)'),
 ('H07', 'Conservative case, 2035', [r'1,822,634', r'\b1\.82 ?(?:m\b|million)', r'conservative path reaches about 1\.8 million'], '1,822,634', 'arrivals', '2035', 'Market Assessment p19', 'QUERY: "about 1.8 million" is used for this arrivals figure and for the 1.8 million seat marker (H08)'),
 ('H08', 'Seat marker in the growth model', [r'1\.8 million inbound seats', r'1\.8 million seats?', r'\b1\.8M\b', r'1\.8 million (?:figure|seat figure|marker)', r'1\.8m marker'], '1.8 million', 'inbound seats', '2025 capacity', 'Demand-Side Analysis p21', 'Stated as a marker of 2025 capacity, not a limit'),
 ('H09', 'Seats the target requires', [r'3,125,000', r'(?:about )?3\.1 million(?: inbound)? seats', r'about 3\.1 million'], '3,125,000 (about 3.1 million)', 'inbound seats a year', '2035', 'Calculated in 2.4: 2,500,000 / 0.80', 'Reconciles: 2,500,000 / 0.80 = 3,125,000'),
 ('H10', 'International seats, year to November 2025', [r'3,816,797', r'3\.8 million international seats', r'1,908,399', r'about 1\.9 million(?: each way)?'], '3,816,797 two-way; 1,908,399 each way', 'seats', 'year to Nov 2025', 'Aviation Market Assessment, "Seasonality"', 'Reconciles: 3,816,797 / 2 = 1,908,399 (rounded 1,908,398.5)'),
 ('H11', 'Additional seats the target requires', [r'1,216,601', r'(?:about|some) 1\.2 million(?: more)?', r'63\.7%', r'two thirds more'], '1,216,601 (about 1.2 million; 63.7%)', 'inbound seats', '2025 to 2035', 'Calculated in 2.4', 'Reconciles: 3,125,000 - 1,908,399 = 1,216,601; / 1,908,399 = 63.7%. NOTE "about 1.2 million a year" in 2.3 is a different measure (average annual arrivals 2022 to 2024)'),
 ('H12', 'Seats the base case requires', [r'2,719,723', r'about 2\.7 million', r'811,324', r'0\.8 million more', r'42\.5%'], '2,719,723 (gap 811,324; 42.5%)', 'inbound seats', '2035', 'Calculated in 2.4', 'Reconciles: 2,175,778 / 0.80 = 2,719,722.5; gap 811,324'),
 ('H13', 'Implied seat growth and the record', [r'5\.1% a year', r'about 5\.1%', r'3\.6%', r'6\.8% a year'], '5.1% (target); 3.6% (base); 6.8% (record 2015 to 2024)', '% a year', '2025 to 2035; 2015 to 2024', 'Calculated in 2.4; 2.2 for the record', 'Reconciles: (3,125,000/1,908,399)^(1/10) = 1.051; (2,719,723/1,908,399)^(1/10) = 1.036; (3.1/1.71)^(1/9) = 1.068'),
 ('H14', 'Interested travellers and arrivals', [r'97 ?(?:m\b|million)', r'1\.4 ?(?:m\b|million)', r'one in seventy'], '97 million interested; 1.4 million arrive', 'travellers', 'survey 2025; arrivals year not stated', 'Market Assessment p41', 'Reconciles: 97 / 1.4 = 69 (about one in seventy). The source gives no year for the 1.4 million'),
 ('H15', 'Share of world travel', [r'0\.1%', r'0\.05%', r'0\.27%', r'under 0\.3%'], '0.1% of arrivals; 0.05% of spend; 0.27% of UK air trips', '%', '2022 to 2024', 'Wesgro Research, Tourism Source Market Analysis, Nov 2025, p2, p4', ''),
 ('H16', 'Route load factors', [r'76(?:\.0)?%', r'[Ee]leven of (?:the )?27', r'11 of (?:the )?27', r'\b79%'], '76.0% network; 11 of 27 routes above 80%; 79% all seats', '%', 'year to Nov 2025', 'Aviation Market Assessment, "Seasonality"', 'Format variants: 76% and 76.0%; "eleven" and "11"'),
 ('H17', 'Runway movements', [r'about 30(?: movements)? an hour', r'30 movements an hour', r'45(?: movements)? an hour', r'a 50% rise', r'40% more'], 'about 30 an hour now; 45 after relocation', 'movements an hour', 'n/a', 'Infrastructure Report p101; parliamentary reply, Apr 2025', 'The report states that the Infrastructure Report prints "about 40% more", against 50% (30 to 45)'),
 ('H18', 'Runway and terminal dates', [r'about 2033', r'December 2029', r'completion in 2031', r'about 2032', r'about 2034', r'early 2030s'], 'Runway about 2033 (planning date); terminal about 2032; domestic about 2034', 'date', 'n/a', 'Infrastructure Report p103; ACSA, Aug 2026 and May 2025', 'Three runway dates are stated (2033, Dec 2029, 2031); register OI-69'),
 ('H19', 'Seat seasonality', [r'6\.4%', r'10\.8%'], 'June 6.4%; December 10.8%', '% of annual international seats', '2025', 'Aviation Market Assessment, "Seasonality"', ''),
 ('H20', 'April to September passenger movements', [r'662,771', r'1,342,770', r'102\.6%', r'85\.7%', r'38\.7%', r'41\.6%', r'40\.8%'], '662,771 (2015) to 1,342,770 (2025); up 102.6%', 'passenger movements', '2015 to 2025', 'Calculated from ACSA traffic release, Sep 2026', 'Reconciles: 1,342,770 / 662,771 = 2.026'),
 ('H21', 'Market concentration', [r'\b63%', r'\b52%', r'\b61%'], 'Five markets 63%; UK, Germany and USA 52%', '% of overseas arrivals', '2025', 'Demand-Side Analysis p13', 'Source prints 63% and 61%; the report uses 63% and footnotes the difference. 61% also appears as the lower bound of the summer share (H23)'),
 ('H22', 'Hub routes', [r'\b53% of (?:arrivals|them)', r'carry 53%', r'carried 53%'], '53% of arrivals on the ten largest routes', '%', '2025', 'Demand-Side Analysis p13', 'NOTE 53% is also June 2023 hotel occupancy (H43)'),
 ('H23', 'Seasonal split', [r'61% (?:and|to) 62%', r'38\.1%', r'61\.9%', r'104\.9%'], 'October to March 61% to 62%; green season 38.1% (normalised)', '% of overseas visitor travel', '2024; 2025', 'Demand-Side Analysis p12; Diagnostic p32', 'The 2025 month shares sum to 104.9%; register OI-03'),
 ('H24', 'Spend premium', [r'1\.6 times', r'US\$890', r'US\$500'], '1.6 times the national average; US$890 against US$500 per arrival', 'ratio; US$', '2025 quarters; 2024', 'Demand-Side Analysis p11, p15', ''),
 ('H25', 'Foreign direct spend', [r'R22\.7 ?(?:bn|billion)', r'R25\.9 ?(?:bn|billion)', r'\b14% in (?:one|a) year', r'gain of 14%'], 'R22.7bn (FY2024) to R25.9bn (FY2025); up 14%', 'rand', 'FY2024; FY2025', 'Demand-Side Analysis p11', 'Reconciles: 25.9 / 22.7 = 1.141. FORMAT: bn and billion both used'),
 ('H26', 'Modelled spend path', [r'R27\.12 ?bn', r'R33\.7 ?bn', r'R40\.6 ?bn', r'R40\.59 ?bn', r'\b19% above'], 'R27.12bn (2024); R33.7bn (2030); R40.59bn (2035)', 'constant 2024 rand', '2024; 2030; 2035', 'Market Assessment p24', 'ROUNDING: 2035 appears as R40.6bn and R40.59bn. Reconciles: 27.12 / 22.7 = 1.195'),
 ('H27', 'Mapped tourism assets', [r'50,332', r'20,281', r'40\.3%'], '50,332 assets; Cape Metro 20,281 (40.3%)', 'assets', 'n/a', 'Infrastructure Report p2, p23', 'Reconciles: 20,281 / 50,332 = 40.3%. Count is provisional (register OI-52)'),
 ('H28', 'Readiness and accessibility', [r'4\.7(?: out of 5)?', r'\b1\.0 in the Central Karoo', r'one touring route of six', r'[Oo]ne of six touring routes'], 'Accessibility 4.7 (Metro) to 1.0 (Central Karoo); one of six touring routes rated Ready', 'score out of 5', 'n/a', 'Infrastructure Report p88 to p90', ''),
 ('H29', 'Hub journeys from India and China', [r'101,000', r'71,000', r'about 30,000', r'\b81%'], 'About 101,000 (India about 71,000; China about 30,000); 81% of Indian travellers through Addis Ababa and Dubai', 'journeys a year', 'not stated', 'Demand-Side Analysis p46, p48; Aviation Market Assessment', 'Reconciles: 71,000 + 30,000 = 101,000. Hub tables sum to 68,564 and 29,015'),
 ('H30', 'India and China arrivals, 2026', [r'30\.0%', r'23\.7%'], 'India down 30.0%; China down 23.7%', '% change', 'Jan to Sep 2026 on 2025', 'Stats SA, 2026', ''),
 ('H31', 'Scenario growth rates', [r'3\.8%', r'5\.3%', r'\b2\.0%', r'3% to 5%'], 'Conservative 2.0%; base 3.8%; accelerated 5.3%; norm 3% to 5%', '% a year', '2025 to 2035', 'Market Assessment p19; Benchmarking p8', ''),
 ('H32', 'Arrivals the base case adds, by group', [r'676,949', r'206,584', r'178,780', r'175,818', r'110,298', r'5,469'], '676,949 (hubs 206,584; mature 178,780; acceleration 175,818; regional 110,298; strategic 5,469)', 'arrivals', '2025 to 2035', 'Market Assessment p20, computed', 'Reconciles: 206,584 + 178,780 + 175,818 + 110,298 + 5,469 = 676,949 = 2,175,778 - 1,498,829. Hubs share 30.5% ("about 30%")'),
 ('H33', 'Community share', [r'18\.4%', r'15\.4% of employed', r'0\.02% to 0\.04%', r'R4m to R10m', r'R259m', r'R547m'], '18.4% of residents; 0.02% to 0.04% of foreign direct spend; R4m to R10m a year', '%; rand', 'Census 2011; FY2025', 'Inclusion Plan p4, p5', 'Reconciles: 1% of R25.9bn = R259m. NOTE 15.4% is also domestic trip growth (H41)'),
 ('H34', 'Long-listed and shortlisted communities', [r'\b107\b', r'93 (?:lie|of the 107)', r'35 tourism nodes', r'49 long-listed', r'43 long-listed', r'7 long-listed', r'8 long-listed'], '107 long-listed (49 + 43 + 7 + 8); 20 shortlisted (11 + 6 + 2 + 1); 93 within 45 minutes', 'communities', 'n/a', 'Inclusion Plan p15 to p18', 'Reconciles: 49 + 43 + 7 + 8 = 107; 11 + 6 + 2 + 1 = 20. The archetype counts give 92 near a node against the 93 printed (footnoted)'),
 ('H35', 'Jobs and GDP', [r'300,000', r'257,000', r'257,987', r'R28\.6 ?(?:bn|billion)', r'about 17%', r'10,000 SMMEs?'], '300,000 jobs ambition; over 257,000 jobs supported and R28.6 billion gross value added (2023)', 'jobs; rand', '2023', 'DEDAT, Tourism Month 2025', 'Reconciles: 300,000 / 257,000 = 1.167. Definition unconfirmed (register OI-62)'),
 ('H36', 'Cruise season', [r'\b64 (?:cruise liner visits|vessels|cruise)', r'\b79 (?:cruise liner visits|vessels|vessel visits|in 2024/25)', r'106,240', r'127,178', r'127,128', r'R1\.35 ?bn', r'R1\.79 ?bn', r'1,701'], '64 visits and 106,240 passengers (2025/26); 79 visits and 127,178 passengers (2024/25)', 'visits; passengers', '2025/26; 2024/25', 'Wesgro prospectus, Oct 2026, p29; Wesgro release, 23 Oct 2026', 'Two passenger counts for 2024/25 are stated: 127,178 (prospectus) and 127,128 (study), footnoted'),
 ('H37', 'Stakeholder record', [r'\b223\b', r'115 High', r'102 Medium', r'\b64 (?:fall|insights)', r'\b68 (?:are|insights)', r'\b91 (?:are|of)'], '16 organisations; 223 insights (115 High, 102 Medium, 6 Low); demand 64, supply 68, enabling 91', 'insights', 'Jan to Mar 2026', 'Stakeholder Insights p20 to p46, counted', 'Reconciles: 64 + 68 + 91 = 223; 115 + 102 + 6 = 223; High 23 + 44 + 48 = 115; Medium 40 + 24 + 38 = 102; Low 1 + 0 + 5 = 6'),
 ('H38', 'Plan architecture', [r'[Tt]wenty objectives', r'[Ee]ighteen initiatives', r'\b146 actions', r'[Ee]ight impact indicators', r'[Tt]hirty-one', r'[Ff]orty-one output', r'\b80 indicators', r'8 at impact, 31 at outcome and 41'], '3 goals; 6 themes; 20 objectives; 18 initiatives; 146 actions; 80 indicators (8, 31, 41)', 'count', 'n/a', 'Chapters 3 to 5', 'Reconciles: 8 + 31 + 41 = 80; 146 action rows in Chapter 3 = 146 rows in A7; 12 initiatives "convene and deliver" + 6 "convene and support" = 18'),
 ('H39', 'Risks and first actions', [r'[Tt]welve of the sixteen', r'[Ss]ixteen (?:material )?risks', r'[Ff]ourteen actions', r'[Ee]leven of the fourteen', r'eleven of them inside', r'[Tt]wenty-eight data gaps'], '16 risks, 12 outside Wesgro\'s control; 14 first-24-month actions, 11 inside the mandate; 28 data gaps', 'count', 'n/a', '4.5, 4.8, 5.4', 'Table 4.5 holds 16 rows: 2 high/high, 6 medium/high, 2 high/medium, 6 medium/medium'),
 ('H40', 'Airport programme costs', [r'R11\.3 ?(?:bn|billion)', r'R10\.1 ?(?:bn|billion)', r'R6\.39 ?(?:bn|billion)', r'R2\.39 ?(?:bn|billion)', r'R500 ?(?:m\b|million)', r'R863 ?(?:m\b|million)'], 'R11.3bn (Infrastructure Report) against about R10.1bn (ACSA items: R6.39bn, R2.39bn, R500m, R863m)', 'rand', 'Feb 2026', 'Infrastructure Report p103; ACSA, Feb 2026', 'Reconciles: 6.39 + 2.39 + 0.5 + 0.863 = 10.143. The report says the two totals are not reconciled (register OI-18). FORMAT: bn and billion both used'),
 ('H41', 'Length of stay', [r'12\.5 nights', r'14\.8', r'13\.0 (?:in the province|nights)', r'2\.9 days', r'3\.0 in 2023', r'31\.5%'], '12.5 nights in the province (2025); 2.9 days in Cape Town (2025)', 'nights; days', '2025; 2023', 'Wesgro Research (SA Tourism departure survey; mobile-location data)', 'Three measures on different bases (register OI-65)'),
 ('H42', 'Domestic tourism', [r'4\.0 million', r'R12\.7 ?(?:bn|billion)', r'31\.9%', r'15\.4% more'], 'About 4.0 million overnight trips; R12.7bn; spend down 31.9%', 'trips; rand', '2025', 'Provincial sources cited in 1.1', 'FORMAT: bn and billion both used'),
 ('H43', 'Hotel occupancy', [r'61\.7%', r'45\.1%', r'\b53% in June 2023', r'51\.8%'], '61.7% (2025); June 45.1% (2025) and 53% (2023)', '%', '2025; June 2023', 'Cape Town Tourism sample; Demand-Side Analysis p34', 'June 2023 is 53% as sourced, 52.6% in the sample'),
 ('H44', 'Business events', [r'33 in 2022 to 58 in 2024', r'\b136\b', r'\b35th\b', r'37 of (?:South Africa\'s )?64', r'36 (?:conference )?bids', r'R745(?:\.1)? million', r'R6,400'], '58 ICCA meetings (2024); 136 over 2022 to 2024; 36 bids secured (2024/25)', 'meetings; bids', '2022 to 2024; 2024/25', 'Demand-Side Analysis p36 to p38', 'Yearly counts sum to 137 against 136 monthly records (source note under Table 3.3)'),
 ('H45', 'African markets', [r'323,971', r'\b62% of', r'R4\.2 ?(?:bn|billion)', r'R1\.94 ?bn'], '323,971 arrivals from 16 markets (2024); 62% from Zimbabwe and Namibia; R4.2bn spend (2025)', 'arrivals; rand', '2024; 2025', 'Demand-Side Analysis p27, p29', 'Table rows sum to R3,944.6m against the R4.2bn headline (footnoted)'),
 ('H46', 'Airport passengers and secondary gateways', [r'11\.1 ?(?:m\b|million)', r'\b3\.3 ?(?:m\b|million)', r'911,000', r'R310 ?m', r'R8 ?bn', r'5\.2 million'], '11.1 million passengers, 3.3 million international (2025); George 911,000', 'passengers', '2025', 'Diagnostic p25, p35; Infrastructure Report p22, p104, p106', ''),
 ('H47', 'DEDAT budget', [r'R596\.765 ?million', r'R127\.355 ?million', r'R6\.8 ?million', r'R7 ?(?:m\b|million) Tourism Growth Fund'], 'R596.765 million main budget; R127.355 million transfer to Wesgro', 'rand', '2026/27', 'DEDAT Annual Performance Plan 2026/27', ''),
 ('H48', 'Phases and gates', [r'2027 to 2028', r'2029 to 2031', r'2032 to 2035', r'[Ee]nd (?:of )?2028', r'[Ee]nd (?:of )?2031'], 'Activate 2027 to 2028; Expand 2029 to 2031; Sustain 2032 to 2035; Gate 1 end 2028; mid-term review 2030; Gate 2 end 2031; terminal evaluation 2035', 'date range', 'n/a', '4.2, 4.7', 'One date range per phase everywhere checked'),
 ('H49', 'Entry and funding events', [r'12 August 2026', r'31 March 2025', r'17 August 2026', r'1 July 2026'], 'ETA launched 12 August 2026; MFMA Circular No. 131 issued 31 March 2025', 'date', 'n/a', 'Presidency; National Treasury', ''),
 ('H50', 'Gulf disruption', [r'\b91% of (?:its|the)', r'at 91%', r'22% fewer'], 'Emirates at 91% of its network on 30 September 2026; passengers down 22% April to September', '%', '2026', 'Emirates, 2026', ''),
]
rows = []
for mid, name, pats, canon, unit, period, src, note in M:
    forms, locs, n = scan(pats)
    rows.append([mid, ' / '.join('%s (x%d)' % (f, c) for f, c in forms.items()), canon, unit, period, src, '; '.join(locs), (name + '. ' + note).strip()])
    if n == 0: print('NO HITS', mid, name)
auto = json.load(open('numbers_auto.json'))
with open(OUT + 'numbers_register.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['id', 'value_as_written', 'canonical_value', 'unit', 'period_or_date', 'source_cited', 'location(s)', 'notes'])
    for r in rows: w.writerow(r)
    for r in auto: w.writerow([r[0], r[1], r[2], r[3], r[4], r[5], r[6], 'AUTO: every value that appears in two or more sections; one row may hold several measures that share a value. ' + r[7]])
print('headline rows', len(rows), 'auto rows', len(auto))
for r in rows:
    if 'x' in r[1] and len(r[1]) < 400: print(r[0], '|', r[1][:230], '|', r[6][:80])
