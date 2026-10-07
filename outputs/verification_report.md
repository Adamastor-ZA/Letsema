# Verification report: AFS cost benchmark workbook

Workbook: /home/user/Letsema/outputs/afs_cost_benchmark.xlsx (read only, copied to verify/wb_copy.xlsx). Inputs: build/out/referenced_ids.csv (404 referenced data_ids), build/out/raw_all.csv (5 451 rows), build/out/sources_all.csv. Date: 2026-10-07.

## 1. Method

1. Spot-check. The 404 referenced data_ids were sorted, `random.seed(7)` was set and `random.sample(ids, 81)` drawn (81 = 20 percent of 404, rounded up; the sample is reproducible from verify/scripts/sample.py). For each id the local file was resolved (absolute path, then the cluster directory, then dl/, dl/stray_from_repo_root/ and the scratchpad stray/ folder). PDF pages were extracted with `pdftotext -layout` for the stated page and two pages either side into verify/txt/ (the dl directories were not written to). Text, HTML and Markdown extracts were searched directly. Each value was searched in the number formats used by the documents (space, comma or dot thousands separators, brackets for negatives, thousands or billions where the source table is in R'000, kEUR, RM'000, R$ thousand or EUR bn). Every automated hit was then read in context to confirm the line item, column (entity and year) and unit; the remaining items were traced by hand. Derived ids were checked by locating each component on the stated page and recomputing the formula in the raw formula column.
2. Ratio recomputation. Every Benchmark row (rows 4 to 153) was recomputed from raw_all.csv without reading the workbook's link cells: absolute values of the numerator ids summed, less the commission ids in column O where present, divided by the sum of the denominator ids; pct source values divided by 100; M6 as numerator (Rm) x 1e6 x ZAR per unit over policy count (count in millions where the source states millions); M7 and M8 as numerator x ZAR per unit over headcount; M10 x 10 000 for basis points. ZAR per unit was recomputed independently from the Normalisation input column D (units per EUR and ZAR per EUR) for the FX period in column K, and the Normalisation inputs were in turn compared with the ECB csv downloads in the scratchpad (fx_annual_*.csv, fx_2026h1.txt). The ids in columns L and M were compared with the ids inside the N, O and P formulas. Rows that link to the AFS cost base tab were recomputed from raw values and Normalisation inputs under step 4.
3. Summary statistics. For each summary row (158 to 178) the W range in the COUNT formula was read, the included rows were selected independently from the include flag in column V and the normalised value in column U, and n, median, QUARTILE(...,1) and QUARTILE(...,3) were recomputed (Excel inclusive quartile definition) and compared with columns F, G, H and I. The mix tags (column E) of the included rows were checked against the peer-group label in column C, and the tab was scanned for included rows of the same metric lying outside the range.
4. AFS cost base and Gap sizing. All FY2025 pool figures (rows 105 to 128, low, base and high) were rebuilt from raw_all.csv values and the Normalisation assumption inputs (rows 39 to 51), including the allocation shares, allocated amortisation, onerous losses, claims, cash acquisition flows and the derived ratios in column E. On the Gap sizing tab the rand gaps were checked as gap in percentage points x AFS base, the hypothesis columns as rand gap x realisation factor, the links to the summary block were checked for matching metric and peer group, and the cross-check block (rows 16 to 22) was compared with cost base rows 122 to 128.

Scripts: verify/scripts/sample.py, extract.py, ratios.py, summary.py, pool.py, spotcheck_csv.py, report.py. Intermediate outputs: verify/sample.json, extract_hits.json, ratio_check.json, summary_check.json.

## 2. Spot-check of referenced data_ids

Sample: 81 of 404 referenced ids (20.0 percent), seed 7. Result: 81 match, 0 sign-or-scale difference, 0 not found, 0 document missing. Match rate 100.0 percent. Two referenced ids with no local file (PR-082, PR-089) were not drawn in the sample; every sampled file resolved. Where the raw value is negative the document shows the figure in brackets; this is a sign convention, not a difference, and is marked as a match. Full detail in verify/spotcheck.csv.

| data_id | Entity | Metric | Period | Raw value | Unit | Stated page | Value found in document | Page found | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| AFS-096 | Non-Life Insurance SA (AIC and ARTIC, divisio | Insurance service expenses (total) | 2025-12-31 | -3181 | m ZAR | pdf90/print88 | 3 181 | pdf 90 | match |
| AFS-112 | Non-Life Insurance SA (AIC and ARTIC, divisio | Insurance revenue | 2024-12-31 | 3986 | m ZAR | pdf90/print88 | 3 986 | pdf 90 | match |
| AFS-113 | Non-Life Insurance SA (AIC and ARTIC, divisio | Insurance service expenses (total) | 2024-12-31 | -3274 | m ZAR | pdf90/print88 | 3 274 | pdf 90 | match |
| AFS-123 | Non-Life Insurance SA (AIC and ARTIC, divisio | Other operating expenses (non-attributable, insurance S | 2024-12-31 | -466 | m ZAR | pdf90/print88 | 466 | pdf 90 | match |
| AFS-1269 | Absa Bank Limited | Insurance commission received (Bank fee and commission  | 2023-12-31 | 739 | m ZAR | pdf79/print77 | 739 | pdf 79 | match |
| AFS-1282 | Absa Life Limited (legal entity, licence I121 | Insurance revenue | 2024-12-31 | 4944.007 | m ZAR | pdf190/print189 | 4 944 007 | pdf 190 | match |
| AFS-1283 | Absa Life Limited (legal entity, licence I121 | Insurance service expenses (total) | 2024-12-31 | -3700.721 | m ZAR | pdf190/print189 | 3 700 721 | pdf 190 | match |
| AFS-129 | Insurance HO (AFS insurance head office, SA) | Insurance revenue | 2025-12-31 | -333 | m ZAR | pdf91/print89 | 333 | pdf 91 | match |
| AFS-1298 | Absa Life Limited (legal entity, licence I121 | Total shareholders' funds | 2024-12-31 | 1825.415 | m ZAR | pdf185/print184 | 1 825 415 | pdf 185 | match |
| AFS-1302 | Absa Life Limited (legal entity, licence I121 | Insurance revenue | 2023-12-31 | 4774.879 | m ZAR | pdf190/print189 | 4 774 879 | pdf 190 | match |
| AFS-1318 | Absa Life Limited (legal entity, licence I121 | Total shareholders' funds | 2023-12-31 | 1423.59 | m ZAR | pdf185/print184 | 1 423 590 | pdf 185 | match |
| AFS-1372 | Absa Insurance Company Limited (legal entity) | Administration, management and other expenses (non-attr | 2024-12-31 | -471.976 | m ZAR | pdf202/print201 | 471 976 | pdf 202 | match |
| AFS-1377 | Absa Insurance Company Limited (legal entity) | Total shareholders' funds | 2024-12-31 | 1828.392 | m ZAR | pdf195/print194 | 1 828 392 | pdf 195 | match |
| AFS-1381 | Absa Insurance Company Limited (legal entity) | Insurance service expenses (total) | 2023-12-31 | -3189.022 | m ZAR | pdf202/print201 | 3 189 022 | pdf 202 | match |
| AFS-1390 | Absa Insurance Company Limited (legal entity) | Administration, management and other expenses (non-attr | 2023-12-31 | -431.926 | m ZAR | pdf202/print201 | 431 926 | pdf 202 | match |
| AFS-140 | Insurance HO (AFS insurance head office, SA) | Other operating expenses (non-attributable, insurance S | 2025-12-31 | -326 | m ZAR | pdf91/print89 | 326 | pdf 91 | match |
| AFS-163 | Insurance SA (Absa Group PPB sub-segment: Abs | Insurance revenue | 2025-12-31 | 9079 | m ZAR | pdf91/print89 | 9 079 | pdf 91 | match |
| AFS-166 | Insurance SA (Absa Group PPB sub-segment: Abs | Insurance service result | 2025-12-31 | 1655 | m ZAR | pdf91/print89 | 1 655 | pdf 91 | match |
| AFS-183 | Insurance SA (Absa Group PPB sub-segment: Abs | Insurance service expenses (total) | 2024-12-31 | -7031 | m ZAR | pdf91/print89 | 7 031 | pdf 91 | match |
| AFS-196 | Insurance SA (Absa Group PPB sub-segment: Abs | Net operating income (profit before tax) | 2024-12-31 | 1556 | m ZAR | pdf91/print89 | 1 556 | pdf 91 | match |
| AFS-218 | Insurance SA (Absa Group PPB sub-segment: Abs | Total equity | 2024-12-31 | 5188 | m ZAR | pdf92/print90 | 5 188 | pdf 92 | match |
| AFS-287 | Absa Group (consolidated, SA + Africa Regions | Life contracts not under PAA (GMM/VFA): Amortisation of | 2025-12-31 | -507 | m ZAR | pdf84/print82 | 507 | pdf 84 | match |
| AFS-298 | Absa Group (consolidated, SA + Africa Regions | Life contracts not under PAA (GMM/VFA): Incurred claims | 2024-12-31 | -3018 | m ZAR | pdf84/print82 | 3 018 | pdf 84 | match |
| AFS-319 | Absa Group (consolidated, SA + Africa Regions | Life contracts under PAA: Insurance service expenses (t | 2025-12-31 | -695 | m ZAR | pdf87/print85 | 695 | pdf 87 | match |
| AFS-333 | Absa Group (consolidated, SA + Africa Regions | Life contracts under PAA: Insurance service expenses (t | 2023-12-31 | -674 | m ZAR | pdf87/print85 | 674 | pdf 87 | match |
| AFS-342 | Absa Group (consolidated, SA + Africa Regions | Non-life contracts (PAA): Amortisation of insurance acq | 2025-12-31 | -710 | m ZAR | pdf88/print86 | 710 | pdf 88 | match |
| AFS-343 | Absa Group (consolidated, SA + Africa Regions | Non-life contracts (PAA): Losses and reversal of losses | 2025-12-31 | -102 | m ZAR | pdf88/print86 | 102 | pdf 88 | match |
| AFS-362 | Absa Group (consolidated, SA + Africa Regions | Non-life contracts (PAA): Amortisation of insurance acq | 2023-12-31 | -566 | m ZAR | pdf89/print87 | 566 | pdf 89 | match |
| AFS-363 | Absa Group (consolidated, SA + Africa Regions | Non-life contracts (PAA): Losses and reversal of losses | 2023-12-31 | 2 | m ZAR | pdf89/print87 | 2 | pdf 89 | match |
| AFS-441 | Absa Life Limited (legal entity, licence I121 | Solo SAM SCR cover ratio (solo in-country regulatory ca | 2025-12-31 | 1.51 | ratio ZAR | pdf242/print240 | 1.51 | pdf 242 | match |
| AFS-546 | Non-Life Insurance SA (AIC and ARTIC, divisio | Insurance revenue | 2023-12-31 | 3717 | m ZAR | pdf87/print85 | 3 717 | pdf 87 | match |
| AFS-547 | Non-Life Insurance SA (AIC and ARTIC, divisio | Insurance service expenses (total) | 2023-12-31 | -3188 | m ZAR | pdf87/print85 | 3 188 | pdf 87 | match |
| AFS-584 | Insurance SA (Absa Group PPB sub-segment: Abs | Net income/(expense) from reinsurance contracts held | 2023-12-31 | -341 | m ZAR | pdf87/print85 | 341 | pdf 87 | match |
| AFS-596 | Insurance SA (Absa Group PPB sub-segment: Abs | Net operating income (profit before tax) | 2023-12-31 | 1686 | m ZAR | pdf87/print85 | 1 686 | pdf 87 | match |
| AFS-608 | Absa Group (consolidated, SA + Africa Regions | Insurance revenue: Product Solutions Cluster segment (S | 2023-12-31 | 8393 | m ZAR | pdf36/print34 | 8 393 | pdf 36 | match |
| AFS-681 | Advice and Investments / Non-Banking Financia | Non-interest income (PSC Head office, Advice and Invest | 2023-12-31 | 1104 | m ZAR | pdf81/print79 | 1 104 (2023 column, PSC Head office, Advice and Investments, non-interest income line) | pdf 81 | match |
| AFS-737 | Life Insurance SA (Absa Life Ltd incl Instant | Insurance service expenses (total) | 2026-06-30 | -1912 | m ZAR | pdf102/print100 | 1 912 | pdf 102 | match |
| AFS-786 | Insurance HO (AFS insurance head office, SA) | Profit for the period | 2026-06-30 | -91 | m ZAR | pdf103/print101 | 91 | pdf 103 | match |
| AFS-790 | Insurance SA (Absa Group PPB sub-segment: Abs | Insurance service expenses (total) | 2026-06-30 | -3494 | m ZAR | pdf103/print101 | 3 494 | pdf 103 | match |
| AFS-801 | Insurance SA (Absa Group PPB sub-segment: Abs | Gross operating income (net insurance income incl inves | 2026-06-30 | 1281 | m ZAR | pdf103/print101 | 1 281 | pdf 103 | match |
| EM-175 | Brasilseg (BB Seguridade affiliate, 74.99pct) | Headcount Brasilseg (approximate) | 2024-12-31 | 1970 | count BRL | 9 | 1,970 | pdf 9 | match |
| EM-176 | Brasilseg (BB Seguridade affiliate, 74.99pct) | Premiums written (gross) | 2025-12-31 | 16003.3 | m BRL | 12 | 16,003,313 (R$ thousand, Premiums written, 2025 column) | pdf 12 | match |
| EM-410 | Bradesco Seguros (Grupo Bradesco Seguros, man | Selling (commission) expenses | 2025-12-31 | 4948 | m BRL | 23 | 4,948 | pdf 23 | match |
| EM-498 | Bradesco Seguros (Grupo Bradesco Seguros, man | Headcount Insurance Group | 2025-12-31 | 8148 | count BRL | 41 | 8,148 | pdf 41 | match |
| EM-503 | Bradesco Seguros (Grupo Bradesco Seguros, man | Life, personal accident and loss of income insurance co | 2025-12-31 | 24480000 | count BRL | 26 | 24,480 (thousand contracts, Dec-25) | pdf 26 | match |
| EM-515 | Maybank Group Insurance and Takaful segment ( | Cost-to-income ratio (overhead expenses / net operating | 2025-12-31 | 15.91 | pct MYR | 246 | Overhead expenses 247,736 / net operating income 1,556,690 = 15.915 percent | pdf 246 | match |
| EM-740 | Etiqa Life Insurance Bhd | Insurance revenue | 2025-12-31 | 644.6 | m MYR | 32 | 644,568 (RM thousand) | pdf 32 | match |
| EM-800 | Etiqa Family Takaful Bhd | Total other expenses excluding commission (expense anal | 2025-12-31 | 282.6 | m MYR | 150-152 | Total other expenses (B) 282,641 (RM thousand) | pdf 151 | match |
| EU-060 | Credit Agricole Assurances | Gross written premiums (premium income, non-GAAP, IFRS  | 2025-12-31 | 52400 | m EUR | 11 | 52.4 (EUR bn, gross written premiums total) | pdf 11 | match |
| EU-234 | VidaCaixa | Gross written premiums, life (Solvency II, primas bruta | 2025-12-31 | 11827.1 | m EUR | 21 | 11.827.080 (kEUR, Primas Brutas, total) | pdf 21 | match |
| EU-249 | Intesa Sanpaolo Assicurazioni | Insurance revenue (insurance contracts issued) | 2025-12-31 | 3222.7 | m EUR | 75 | 3,222,749 (kEUR, insurance revenue from insurance contracts issued) | pdf 75 | match |
| EU-275 | Intesa Sanpaolo Assicurazioni | Number of life contracts in force | 2025-12-31 | 4383281 | count EUR | 11 | 4,383,281 | pdf 11 | match |
| EU-337 | KBC Insurance | Insurance revenue before reinsurance (KBC Insurance gro | 2025-12-31 | 3214 | m EUR | 14 | 3.214 | pdf 14 | match |
| EU-397 | Lloyds IP&I / Scottish Widows | General insurance combined ratio | 2025-12-31 | 0.89 | ratio GBP | md lines 6952-6975 | General insurance combined ratio 89 percent (2024: 97 percent) | md table within lines 6952-6975 | match |
| EU-412 | Lloyds IP&I / Scottish Widows | Scottish Widows Limited: other operating expenses (non- | 2024-12-31 | 707 | m GBP | 35 | 707 | pdf 35 | match |
| EU-431 | Lloyds IP&I / Scottish Widows | Scottish Widows Limited: fees and commissions payable | 2024-12-31 | 50 | m GBP | 74 | 50 | pdf 74 | match |
| LB-1096 | Capitec Bank Holdings - Insurance segment (Ca | Insurance segment total operating expenses before reall | 2026-02-28 | 557.681 | m ZAR | see inputs | Operating expenses Insurance column (232 965) plus attributable insurance service expenses reallocated 324 716 = 557 681 (R thousand) | text extract, segment note (group 2026) | match |
| LB-156 | Standard Bank Group - Insurance & Asset Manag | Liberty Group Limited SCR cover | 2025-12-31 | 1.5 | ratio ZAR | PDF p30 (printed 58) | 1.5 (times covered, SCR cover of Liberty Group Limited) | pdf 30 | match |
| LB-209 | Standard Bank Group - consolidated insurance  | Directly attributable expenses (within insurance servic | 2025-12-31 | 3947 | m ZAR | PDF p21 (IS), PDF p109-111 (printed 135-137) | 3 947 (directly attributable expenses, total column) | pdf 110 | match |
| LB-215 | Standard Bank Group - consolidated insurance  | Amortisation of insurance acquisition cash flows | 2025-12-31 | 3478 | m ZAR | PDF p21 (IS), PDF p109-111 (printed 135-137) | 3 478 (amortisation of insurance acquisition cash flows, total column) | pdf 110 | match |
| LB-274 | Liberty Group Limited (consolidated) | Directly attributable expenses (within insurance servic | 2025-12-31 | 4229 | m ZAR | printed p28 (statement of profit or loss), p166 (note 32), p163 (note 31) | 4 229 | text extract (no page numbers) | match |
| LB-279 | Liberty Group Limited (consolidated) | Amortisation of insurance acquisition cash flows | 2025-12-31 | 3282 | m ZAR | printed p28 (statement of profit or loss), p166 (note 32), p163 (note 31) | 3 282 | text extract (no page numbers) | match |
| LB-344 | Liberty Group Limited (consolidated) | Total operating expenses (before allocation to insuranc | 2025-12-31 | 16293 | m ZAR | printed p175 (note 41) | 16 293 | text extract (no page numbers) | match |
| LB-392 | Standard Insurance Limited (Liberty segment v | Insurance revenue | 2025-12-31 | 3729 | m ZAR | printed p35 and p37 (segment note 1) | 3 729 | text extract (no page numbers) | match |
| LB-393 | Standard Insurance Limited (Liberty segment v | Insurance service expenses | 2025-12-31 | 2487 | m ZAR | printed p35 and p37 (segment note 1) | 2 487 | text extract (no page numbers) | match |
| LB-396 | Standard Insurance Limited (Liberty segment v | Other operating expenses (non-attributable) | 2025-12-31 | 158 | m ZAR | printed p35 and p37 (segment note 1) | 158 | text extract (no page numbers) | match |
| LB-397 | Standard Insurance Limited (Liberty segment v | Total operating expenses (segment, before IFRS 17 alloc | 2025-12-31 | 1418 | m ZAR | printed p35 and p37 (segment note 1) | 1 418 | text extract (no page numbers) | match |
| LB-401 | Standard Insurance Limited (Liberty segment v | Commissions and other acquisition costs | 2025-12-31 | 627 | m ZAR | printed p35 and p37 (segment note 1) | 627 | text extract (no page numbers) | match |
| LB-910 | Nedgroup Insurance Company Limited (KPMG surv | Insurance revenue | 2024-12-31 | 1559.287 | m ZAR | PDF p206 (printed 205) | 1 559 287 | pdf 206 | match |
| LB-956 | Capitec Bank Holdings - Insurance segment (Ca | Amortisation of insurance acquisition cash flows | 2026-02-28 | 15.436 | m ZAR | printed p162 (income statement), p302-303 (note 24), p313-315 (note 32) | 15 436 | text extract (no page numbers) | match |
| LN-026 | Sanlam Limited (group) | amortisation_insurance_acquisition_cash_flows | 2025-12-31 | 4408 | m ZAR | 78 | 4 408 | pdf 78 | match |
| LN-043 | Sanlam Limited (group) | attributable_insurance_service_expenses_excl_claims | 2025-12-31 | 13950 | m ZAR | 105 | 13 950 | pdf 105 | match |
| LN-088 | Sanlam Life and Savings (SA segment of Sanlam | administration_and_other_costs | 2024-12-31 | 15698 | m ZAR | 49 | (15 698) (2024 column, Sanlam Life and Savings, administration and other costs) | pdf 49 | match |
| LN-118 | Santam Limited (group) | insurance_service_expenses_total | 2025-12-31 | 41691 | m ZAR | 21 | 41 691 | pdf 21 | match |
| LN-244 | Old Mutual Limited (group) | expense_fee_commission_and_other_acquisition_costs | 2025-12-31 | 13927 | m ZAR | 54 | 13 927 | pdf 54 | match |
| LN-255 | Old Mutual Limited (group) | opex_excl_claims_total | 2025-12-31 | 38736 | m ZAR | 54 | Total operating and administration expenses 52 663 less fee and commission expense and other acquisition costs 13 927 = 38 736 | pdf 54 | match |
| LN-352 | Old Mutual Mass and Foundation (SA retail mas | other_operating_and_administrative_expenses | 2024-12-31 | 3627 | m ZAR | 53 | 3 627 | pdf 53 | match |
| LN-454 | Momentum Group Limited (group) | expense_sales_remuneration_total | 2026-06-30 | 9196 | m ZAR | 173 | 9 196 | pdf 172 | match |
| LN-624 | Momentum Insure (Momentum segment: SA non-lif | combined_ratio | 2026-06-30 | 0.875 | ratio ZAR | 88 | Underwriting margin 12.5 percent (F2026); 1 - 0.125 = 0.875 | pdf 88 | match |
| PR-095 | Phoenix Group: Standard Life Assurance acquis | savings target as pct of cost base | 2023-12-31 | 12.5 | pct  | CEO report | Savings of GBP 75 million per annum from a combined cost base of GBP 600 million; 75/600 = 12.5 percent | html, CEO report section | match |
| PR-113 | Aegon: expense savings programme (2021-2023,  | savings target as pct of cost base | 2023-12-31 | 13 | pct  | 2 | 13 | pdf 2 | match |

## 3. Ratio recomputation (Benchmark tab, column R)

139 rows recomputed from raw_all.csv; 11 rows (36, 37, 57 to 61, 82, 83, 107, 117) link to the AFS cost base tab and were recomputed under section 5. None of the 139 rows differs from column R by more than 0.5 percent relative; the largest relative difference is 3.0e-15 (floating point only) once EU-078 is read in millions of policies as its note states. The id lists in columns L and M agree with the ids inside the N, O and P formulas on every row. The ZAR per unit in column Q agrees with the independent recomputation on every row, and all 30 Normalisation FX inputs agree with the ECB downloads to the sixth decimal. All numerator and denominator ids on each row carry the same period end, except row 140 (see observations).

| Row | Metric | Entity | Numerator ids | Less | Denominator ids | Recomputed | Column R | Relative difference |
|---|---|---|---|---|---|---|---|---|
| 4 | M1 | AFS Life Insurance SA | AFS-070 |  | AFS-057 | 0.0399247 | 0.0399247 | 1.7e-16 |
| 5 | M1 | AFS Non-Life Insurance SA | AFS-106 |  | AFS-095 | 0.122867 | 0.122867 | 1.7e-15 |
| 6 | M1 | AFS Insurance SA (Absa Life, AIC, ARTIC, | AFS-176 |  | AFS-163 | 0.11477 | 0.11477 | 1.6e-15 |
| 7 | M1 | Capitec Life (Capitec) | LB-970 |  | LB-949 | 0.0184669 | 0.0184669 | 1.5e-15 |
| 8 | M1 | Discovery Life | LN-703 |  | LN-697 | 0.0422427 | 0.0422427 | 1.6e-16 |
| 9 | M1 | Hollard Life Assurance | LN-1123 |  | LN-1118 | 0.0838608 | 0.0838608 | 0.0e+00 |
| 10 | M1 | Liberty Group (Standard Bank) | LB-285 |  | LB-268 | 0.20559 | 0.20559 | 5.4e-16 |
| 11 | M1 | Metropolitan Life (Momentum, retail mass | LN-517 |  | LN-512 | 0.0395058 | 0.0395058 | 3.5e-16 |
| 12 | M1 | Momentum Retail (retail affluent) | LN-497 |  | LN-492 | 0.159079 | 0.159079 | 2.3e-15 |
| 13 | M1 | Nedgroup Life Assurance (Nedbank) | LB-881 |  | LB-874 | 0.0246548 | 0.0246548 | 7.0e-16 |
| 14 | M1 | OUTsurance Life | LN-1153 |  | LN-1148 | 0.11751 | 0.11751 | 3.5e-16 |
| 15 | M1 | Old Mutual Mass and Foundation (SA retai | LN-352 |  | LN-348 | 0.31509 | 0.31509 | 5.3e-16 |
| 16 | M1 | Old Mutual Personal Finance (SA retail a | LN-359 |  | LN-355 | 0.49077 | 0.49077 | 1.1e-16 |
| 17 | M1 | Sanlam Life and Savings (SA) | LN-088 |  | LN-083 | 0.342295 | 0.342295 | 8.1e-16 |
| 18 | M1 | Scottish Widows Limited (Lloyds) | EU-412 |  | EU-407 | 0.267905 | 0.267905 | 1.2e-15 |
| 19 | M1 | Discovery Insure | LN-751 |  | LN-745 | 0.0262097 | 0.0262097 | 1.5e-15 |
| 20 | M1 | Hollard Insurance Company | LN-1193 |  | LN-1188 | 0.0687221 | 0.0687221 | 4.0e-16 |
| 21 | M1 | Momentum Insure | LN-537 |  | LN-532 | 0.154133 | 0.154133 | 7.2e-16 |
| 22 | M1 | Nedgroup Insurance Company (Nedbank) | LB-918 |  | LB-910 | 0.0171129 | 0.0171129 | 2.0e-16 |
| 23 | M1 | OUTsurance SA | LN-884 |  | LN-879 | 0.0330872 | 0.0330872 | 1.0e-15 |
| 24 | M1 | Old Mutual Insure | LN-322 |  | LN-318 | 0.042997 | 0.042997 | 8.1e-16 |
| 25 | M1 | Santam Group | LN-122 |  | LN-117 | 0.0313753 | 0.0313753 | 1.1e-15 |
| 26 | M1 | Standard Insurance Limited (Standard Ban | LB-396 |  | LB-392 | 0.0423706 | 0.0423706 | 9.8e-16 |
| 27 | M1 | BNP Paribas Cardif | EU-141 |  | EU-111 | 0.0877248 | 0.0877248 | 3.2e-16 |
| 28 | M1 | Brasilseg (BB Seguridade) | EM-258 |  | EM-254 | 0.0684632 | 0.0684632 | 4.1e-16 |
| 29 | M1 | Credit Agricole Assurances | EU-035 |  | EU-001 | 0.027399 | 0.027399 | 2.5e-16 |
| 30 | M1 | Etiqa (Maybank insurance and takaful seg | EM-513 |  | EM-533 | 0.0273089 | 0.0273089 | 1.7e-15 |
| 31 | M1 | Intesa Sanpaolo Assicurazioni | EU-256, EU-255 |  | EU-249 | 0.0389735 | 0.0389735 | 1.2e-15 |
| 32 | M1 | KBC Insurance | EU-339 |  | EU-337 | 0.0591164 | 0.0591164 | 7.0e-16 |
| 33 | M1 | Momentum Group | LN-425 |  | LN-417 | 0.233934 | 0.233934 | 2.0e-15 |
| 34 | M1 | Old Mutual Group | LN-240 |  | LN-236 | 0.343255 | 0.343255 | 8.1e-16 |
| 35 | M1 | Sanlam Group | LN-007 |  | LN-001 | 0.232335 | 0.232335 | 2.4e-16 |
| 38 | M2 | Capitec Life (Capitec) | LB-1096 |  | LB-949 | 0.0442069 | 0.0442069 | 4.7e-16 |
| 39 | M2 | Etiqa Family Takaful | EM-800 |  | EM-774 | 0.14708 | 0.14708 | 1.1e-15 |
| 40 | M2 | Etiqa Life Insurance | EM-764 |  | EM-740 | 0.31632 | 0.31632 | 8.8e-16 |
| 41 | M2 | Liberty Group (Standard Bank) | LB-344 | LB-350 | LB-268 | 0.3082 | 0.3082 | 1.4e-15 |
| 42 | M2 | SBI Life (opex / GWP) | EM-005 |  | EM-079, EM-080 | 0.0614678 | 0.0614678 | 2.3e-16 |
| 43 | M2 | Scottish Widows Limited (Lloyds) | EU-430 |  | EU-407 | 0.366048 | 0.366048 | 6.1e-16 |
| 44 | M2 | VidaCaixa (CaixaBank) attributable expen | EU-213 | EU-209 | EU-182 | 0.0536256 | 0.0536256 | 0.0e+00 |
| 45 | M2 | Etiqa General Insurance | EM-730 |  | EM-700 | 0.078991 | 0.078991 | 3.5e-16 |
| 46 | M2 | OUTsurance SA | LN-882 |  | LN-879 | 0.220465 | 0.220465 | 1.1e-15 |
| 47 | M2 | Santam Group | LN-154 |  | LN-117 | 0.149286 | 0.149286 | 1.9e-15 |
| 48 | M2 | Standard Insurance Limited (Standard Ban | LB-397 | LB-401 | LB-392 | 0.212121 | 0.212121 | 6.5e-16 |
| 49 | M2 | BNP Paribas Cardif | EU-136 | EU-132 | EU-111 | 0.118491 | 0.118491 | 2.0e-15 |
| 50 | M2 | Bradesco Seguros (personnel + admin / pr | EM-414, EM-415 |  | EM-407 | 0.0663438 | 0.0663438 | 2.1e-16 |
| 51 | M2 | Brasilseg (BB Seguridade) admin / retain | EM-183 |  | EM-179 | 0.0615804 | 0.0615804 | 0.0e+00 |
| 52 | M2 | Credit Agricole Assurances | EU-030 | EU-027 | EU-001 | 0.0866121 | 0.0866121 | 3.2e-16 |
| 53 | M2 | KBC Insurance | EU-324, EU-339 |  | EU-337 | 0.233043 | 0.233043 | 4.8e-16 |
| 54 | M2 | Momentum Group | LN-464 | LN-454 | LN-417 | 0.237126 | 0.237126 | 9.4e-16 |
| 55 | M2 | Old Mutual Group | LN-255 | LN-244 | LN-236 | 0.304136 | 0.304136 | 3.7e-16 |
| 56 | M2 | Sanlam Group | LN-047 |  | LN-001 | 0.380902 | 0.380902 | 8.7e-16 |
| 62 | M3 | Capitec Life (Capitec) | LB-956 |  | LB-949 | 0.0012236 | 0.0012236 | 1.6e-15 |
| 63 | M3 | Discovery Life | LN-699 |  | LN-697 | 0.12734 | 0.12734 | 1.3e-15 |
| 64 | M3 | Liberty Group (Standard Bank) | LB-279 |  | LB-268 | 0.0866169 | 0.0866169 | 0.0e+00 |
| 65 | M3 | Scottish Widows Limited (Lloyds) | EU-431 |  | EU-407 | 0.0189466 | 0.0189466 | 1.8e-16 |
| 66 | M3 | VidaCaixa (CaixaBank) | EU-209 |  | EU-182 | 0.197731 | 0.197731 | 9.8e-16 |
| 67 | M3 | Discovery Insure | LN-747 |  | LN-745 | 0.154001 | 0.154001 | 5.4e-16 |
| 68 | M3 | Etiqa General Insurance | EM-728 |  | EM-700 | 0.0560636 | 0.0560636 | 5.0e-16 |
| 69 | M3 | Santam Group | LN-151 |  | LN-117 | 0.123933 | 0.123933 | 2.7e-15 |
| 70 | M3 | Standard Insurance Limited (Standard Ban | LB-401 |  | LB-392 | 0.168142 | 0.168142 | 0.0e+00 |
| 71 | M3 | BNP Paribas Cardif | EU-132 |  | EU-111 | 0.514084 | 0.514084 | 0.0e+00 |
| 72 | M3 | Bradesco Seguros (selling expenses / pre | EM-410 |  | EM-407 | 0.0671307 | 0.0671307 | 2.1e-16 |
| 73 | M3 | Brasilseg (BB Seguridade) | EM-248 |  | EM-254 | 0.285281 | 0.285281 | 1.8e-15 |
| 74 | M3 | Credit Agricole Assurances | EU-027 |  | EU-001 | 0.270095 | 0.270095 | 2.1e-16 |
| 75 | M3 | Etiqa (Maybank insurance and takaful seg | EM-540 |  | EM-533 | 0.110878 | 0.110878 | 2.6e-15 |
| 76 | M3 | FirstRand insurance activities (FNB Life | LB-575, LB-576 |  | LB-530 | 0.0530822 | 0.0530822 | 2.6e-16 |
| 77 | M3 | Momentum Group | LN-442 |  | LN-417 | 0.101169 | 0.101169 | 2.6e-15 |
| 78 | M3 | Nedbank Insurance | LB-819 |  | LB-810 | 0.156969 | 0.156969 | 3.0e-15 |
| 79 | M3 | Old Mutual Group | LN-259 |  | LN-236 | 0.149206 | 0.149206 | 2.2e-15 |
| 80 | M3 | Sanlam Group | LN-026 |  | LN-001 | 0.0428365 | 0.0428365 | 3.2e-16 |
| 81 | M3 | Standard Bank Group consolidated (includ | LB-215 |  | LB-203 | 0.0835937 | 0.0835937 | 1.7e-16 |
| 84 | M4 | SBI Life (commission / GWP) | EM-004 |  | EM-079, EM-080 | 0.044389 | 0.044389 | 0.0e+00 |
| 85 | M4 | VidaCaixa (CaixaBank) | EU-209 |  | EU-234 | 0.0545273 | 0.0545273 | 2.5e-16 |
| 86 | M4 | Santam conventional (management basis) | LN-171 |  | LN-165 | 0.1154 | 0.1154 | 4.8e-16 |
| 87 | M4 | Standard Insurance Limited (Standard Ban | LB-401 |  | LB-150 | 0.168142 | 0.168142 | 0.0e+00 |
| 88 | M4 | BNP Paribas Cardif | EU-132 |  | EU-157 | 0.128135 | 0.128135 | 2.2e-15 |
| 89 | M4 | Brasilseg (BB Seguridade) | EM-248 |  | EM-176 | 0.312429 | 0.312429 | 1.4e-15 |
| 90 | M4 | Credit Agricole Assurances | EU-027 |  | EU-060 | 0.0793893 | 0.0793893 | 5.2e-16 |
| 91 | M4 | FirstRand insurance activities (FNB Life | LB-575, LB-576 |  | LB-621 | 0.050784 | 0.050784 | 1.4e-16 |
| 92 | M5 | AFS Non-Life Insurance SA | AFS-096, AFS-097 |  | AFS-095 | 0.815212 | 0.815212 | 5.4e-16 |
| 93 | M5 | Discovery Insure | LN-746, LN-749 |  | LN-745 | 0.88477 | 0.88477 | 1.3e-16 |
| 94 | M5 | FirstRand short-term insurance (non-life | LB-581 |  | LB-579 | 0.791209 | 0.791209 | 2.8e-16 |
| 95 | M5 | Hollard Insurance Company | LN-1189, LN-1190 |  | LN-1188 | 0.930408 | 0.930408 | 3.6e-16 |
| 96 | M5 | Nedgroup Insurance Company (Nedbank) | LB-911, LB-912 |  | LB-910 | 0.945741 | 0.945741 | 2.3e-16 |
| 97 | M5 | Old Mutual Insure | LN-319, LN-320 |  | LN-318 | 0.905194 | 0.905194 | 0.0e+00 |
| 98 | M5 | Santam Group | LN-118, LN-119 |  | LN-117 | 0.874428 | 0.874428 | 2.5e-16 |
| 99 | M5 | Standard Insurance Limited (Standard Ban | LB-393, LB-394 |  | LB-392 | 0.736927 | 0.736927 | 3.0e-16 |
| 100 | M5b | AFS Non-Life Insurance SA | AFS-096, AFS-097, AFS-106 |  | AFS-095 | 0.938079 | 0.938079 | 2.4e-16 |
| 101 | M5b | Discovery Insure | LN-746, LN-749, LN-751 |  | LN-745 | 0.91098 | 0.91098 | 3.7e-16 |
| 102 | M5b | Hollard Insurance Company | LN-1189, LN-1190, LN-1193 |  | LN-1188 | 0.999131 | 0.999131 | 2.2e-16 |
| 103 | M5b | Nedgroup Insurance Company (Nedbank) | LB-911, LB-912, LB-918 |  | LB-910 | 0.962854 | 0.962854 | 0.0e+00 |
| 104 | M5b | Old Mutual Insure | LN-319, LN-320, LN-322 |  | LN-318 | 0.948191 | 0.948191 | 2.3e-16 |
| 105 | M5b | Santam Group | LN-118, LN-119, LN-122 |  | LN-117 | 0.905803 | 0.905803 | 2.5e-16 |
| 106 | M5b | Standard Insurance Limited (Standard Ban | LB-393, LB-394, LB-396 |  | LB-392 | 0.779297 | 0.779297 | 4.3e-16 |
| 108 | M5r | Brasilseg (BB Seguridade) | EM-191 |  |  | 0.644 | 0.644 | 0.0e+00 |
| 109 | M5r | Credit Agricole Assurances (Pacifica, P& | EU-084 |  |  | 0.946 | 0.946 | 0.0e+00 |
| 110 | M5r | Etiqa General Insurance (1 minus service | EM-706 |  |  | 0.9591 | 0.9591 | 0.0e+00 |
| 111 | M5r | Etiqa General Takaful (1 minus service r | EM-816 |  |  | 0.905 | 0.905 | 0.0e+00 |
| 112 | M5r | Intesa Sanpaolo Assicurazioni (non-life) | EU-278 |  |  | 0.759 | 0.759 | 0.0e+00 |
| 113 | M5r | KBC Insurance (non-life) | EU-325 |  |  | 0.87 | 0.87 | 0.0e+00 |
| 114 | M5r | Lloyds general insurance | EU-397 |  |  | 0.89 | 0.89 | 0.0e+00 |
| 115 | M5r | Momentum Insure | LN-624 |  |  | 0.875 | 0.875 | 0.0e+00 |
| 116 | M5r | OUTsurance SA | LN-891 |  |  | 0.652 | 0.652 | 0.0e+00 |
| 118 | M6 | Capitec Life (Capitec) | LB-1096 |  | LB-1049, LB-1050, LB-1051 | 92.6273 | 92.6273 | 4.6e-16 |
| 119 | M6 | SBI Life (opex per in-force life) | EM-005 |  | EM-133 | 149.653 | 149.653 | 1.5e-15 |
| 120 | M6 | Credit Agricole Assurances (P&C, Solvenc | EU-083 |  | EU-078 | 2613.11 | 2613.11 | 1.7e-16 |
| 121 | M6 | OUTsurance Group (SA, Australia, Ireland | LN-854 |  | LN-942 | 2633.78 | 2633.78 | 1.7e-16 |
| 122 | M6 | Bradesco Seguros | EM-414, EM-415 |  | EM-503, EM-504, EM-505 | 495.152 | 495.152 | 5.7e-16 |
| 123 | M6 | Intesa Sanpaolo Assicurazioni (Solvency  | EU-295, EU-296 |  | EU-275, EU-276 | 2348.84 | 2348.84 | 1.4e-15 |
| 124 | M7 | SBI Life | EM-005 |  | EM-120 | 0.434517 | 0.434517 | 7.7e-16 |
| 125 | M7 | OUTsurance Group | LN-854 |  | LN-944 | 1.40598 | 1.40598 | 1.9e-15 |
| 126 | M7 | Santam Group | LN-154 |  | LN-223 | 1.20474 | 1.20474 | 1.7e-15 |
| 127 | M7 | BNP Paribas Cardif | EU-136 | EU-132 | EU-164 | 2.55599 | 2.55599 | 1.7e-16 |
| 128 | M7 | Bradesco Seguros | EM-414, EM-415 |  | EM-498 | 1.92008 | 1.92008 | 1.2e-16 |
| 129 | M7 | Credit Agricole Assurances | EU-030 | EU-027 | EU-075 | 6.65478 | 6.65478 | 0.0e+00 |
| 130 | M7 | KBC Insurance | EU-324, EU-339 |  | EU-351 | 3.79652 | 3.79652 | 3.5e-16 |
| 131 | M7 | Momentum Group | LN-464 | LN-454 | LN-491 | 0.985915 | 0.985915 | 5.6e-16 |
| 132 | M7 | Old Mutual Group | LN-255 | LN-244 | LN-404 | 0.891384 | 0.891384 | 2.5e-16 |
| 133 | M7 | Sanlam Group | LN-047 |  | LN-045 | 1.6777 | 1.6777 | 7.9e-16 |
| 134 | M8 | SBI Life (GWP per employee) | EM-079, EM-080 |  | EM-120 | 7.06902 | 7.06902 | 0.0e+00 |
| 135 | M8 | VidaCaixa (GWP per employee) | EU-234 |  | EU-230 | 235.827 | 235.827 | 1.3e-15 |
| 136 | M8 | OUTsurance Group | LN-829 |  | LN-944 | 5.14599 | 5.14599 | 8.6e-16 |
| 137 | M8 | Santam Group | LN-117 |  | LN-223 | 8.07002 | 8.07002 | 2.2e-16 |
| 138 | M8 | BNP Paribas Cardif (GWP per employee) | EU-157 |  | EU-164 | 86.5449 | 86.5449 | 0.0e+00 |
| 139 | M8 | Bradesco Seguros (premiums earned per em | EM-407 |  | EM-498 | 28.9414 | 28.9414 | 1.1e-15 |
| 140 | M8 | Brasilseg (premiums written per employee | EM-176 |  | EM-175 | 25.99 | 25.99 | 1.5e-15 |
| 141 | M8 | Credit Agricole Assurances (premium inco | EU-060 |  | EU-075 | 261.402 | 261.402 | 8.7e-16 |
| 142 | M8 | Intesa Sanpaolo Assicurazioni (GWP per e | EU-273, EU-274 |  | EU-277 | 302.773 | 302.773 | 1.1e-15 |
| 143 | M8 | KBC Insurance | EU-337 |  | EU-351 | 16.2911 | 16.2911 | 1.7e-15 |
| 144 | M8 | Momentum Group | LN-417 |  | LN-491 | 4.15777 | 4.15777 | 1.1e-15 |
| 145 | M8 | Old Mutual Group | LN-236 |  | LN-404 | 2.93087 | 2.93087 | 1.5e-15 |
| 146 | M8 | Sanlam Group | LN-001 |  | LN-045 | 4.40453 | 4.40453 | 4.0e-16 |
| 147 | M9 | AFS Insurance SA (segment cost-to-income | AFS-010 |  |  | 0.4 | 0.4 | 0.0e+00 |
| 148 | M9 | Etiqa (Maybank segment cost-to-income) | EM-515 |  |  | 0.1591 | 0.1591 | 0.0e+00 |
| 149 | M9 | Intesa Sanpaolo Insurance Division | EU-304 |  |  | 0.214 | 0.214 | 0.0e+00 |
| 150 | M9 | Lloyds Insurance, Pensions and Investmen | EU-371 |  |  | 0.7289 | 0.7289 | 0.0e+00 |
| 151 | M10 | Brasilprev (BB Seguridade) admin / pensi | EM-271 |  | EM-312 | 10.0601 | 10.0601 | 3.0e-15 |
| 152 | M11 | AFS Advice and Investments block (Non-Ba | AFS-675 |  | AFS-674 | 1.56159 | 1.56159 | 4.3e-16 |
| 153 | M11 | BB Corretora (captive broker, BB Segurid | EM-337 |  |  | 0.0556 | 0.0556 | 0.0e+00 |

## 4. Summary statistics (Benchmark rows 158 to 178)

All 21 summary rows agree: peer n, median, Q1 and Q3 recomputed from the include flags and normalised values match columns F to I exactly (Excel inclusive quartiles). Each mix-group range contains only rows with the matching mix tag, no AFS row carries include flag 1, and no included row of the same metric lies outside the 'all' ranges. For the mix sub-groups the rows outside the range are, as intended, the other mixes. The M11 row has a single peer, so Q1 and Q3 are blank in the workbook and in the recomputation.

| Row | Metric | Group | Range | n (calc / wb) | Median (calc / wb) | Q1 (calc / wb) | Q3 (calc / wb) | Mixes in range | Result |
|---|---|---|---|---|---|---|---|---|---|
| 158 | M1 | all | W7:W35 | 29 / 29 | 0.0684632 / 0.0684632 | 0.0330872 / 0.0330872 | 0.20559 / 0.20559 | composite, life, nonlife | OK |
| 159 | M1 | life | W7:W18 | 12 / 12 | 0.138295 / 0.138295 | 0.0415585 / 0.0415585 | 0.279701 / 0.279701 | life | OK |
| 160 | M1 | nonlife | W19:W26 | 8 / 8 | 0.0377289 / 0.0377289 | 0.0300839 / 0.0300839 | 0.0494283 / 0.0494283 | nonlife | OK |
| 161 | M1 | composite | W27:W35 | 9 / 9 | 0.0684632 / 0.0684632 | 0.0389735 / 0.0389735 | 0.232335 / 0.232335 | composite | OK |
| 162 | M2 | all | W38:W56 | 15 / 15 | 0.220465 / 0.220465 | 0.132786 / 0.132786 | 0.306168 / 0.306168 | composite, life, nonlife | OK |
| 163 | M2 | composite | W49:W56 | 6 / 6 | 0.235084 / 0.235084 | 0.147129 / 0.147129 | 0.287384 / 0.287384 | composite | OK |
| 164 | M2 | life | W38:W44 | 5 / 5 | 0.3082 / 0.3082 | 0.14708 / 0.14708 | 0.31632 / 0.31632 | life | OK |
| 165 | M2 | nonlife | W45:W48 | 4 / 4 | 0.180704 / 0.180704 | 0.131713 / 0.131713 | 0.214207 / 0.214207 | nonlife | OK |
| 166 | M3 | all | W62:W81 | 13 / 13 | 0.110878 / 0.110878 | 0.0560636 / 0.0560636 | 0.149206 / 0.149206 | composite, life, nonlife | OK |
| 167 | M3 | composite | W71:W81 | 6 / 6 | 0.106024 / 0.106024 | 0.065104 / 0.065104 | 0.139624 / 0.139624 | composite | OK |
| 168 | M3 | life | W62:W66 | 3 / 3 | 0.0866169 / 0.0866169 | 0.0439202 / 0.0439202 | 0.106979 / 0.106979 | life | OK |
| 169 | M3 | nonlife | W67:W70 | 4 / 4 | 0.138967 / 0.138967 | 0.106966 / 0.106966 | 0.157536 / 0.157536 | nonlife | OK |
| 170 | M4 | all | W84:W91 | 4 / 4 | 0.0830922 / 0.0830922 | 0.0491852 / 0.0491852 | 0.128586 / 0.128586 | composite, life, nonlife | OK |
| 171 | M5 | nonlife | W93:W99 | 6 / 6 | 0.894982 / 0.894982 | 0.877013 / 0.877013 | 0.924105 / 0.924105 | nonlife | OK |
| 172 | M5b | nonlife | W101:W106 | 6 / 6 | 0.929585 / 0.929585 | 0.907097 / 0.907097 | 0.959188 / 0.959188 | nonlife | OK |
| 173 | M5r | nonlife | W108:W117 | 9 / 9 | 0.887 / 0.887 | 0.87 / 0.87 | 0.905 / 0.905 | nonlife | OK |
| 174 | M6 | all | W118:W123 | 6 / 6 | 1422 / 1422 | 236.028 / 236.028 | 2547.04 / 2547.04 | composite, life, nonlife | OK |
| 175 | M7 | all | W124:W133 | 10 / 10 | 1.54184 / 1.54184 | 1.04062 / 1.04062 | 2.39701 / 2.39701 | composite, life, nonlife | OK |
| 176 | M8 | all | W134:W146 | 13 / 13 | 16.2911 / 16.2911 | 5.14599 / 5.14599 | 86.5449 / 86.5449 | composite, life, nonlife | OK |
| 177 | M9 | all | W148:W150 | 3 / 3 | 0.214 / 0.214 | 0.18655 / 0.18655 | 0.47145 / 0.47145 | composite | OK |
| 178 | M11 | all | W153:W153 | 1 / 1 | 0.0556 / 0.0556 |  /  |  /  | intermediary | OK |

## 5. AFS cost base pools (FY2025) and Gap sizing

Rebuilt from raw values (AFS-163, 164, 165, 176, 057, 058, 095, 096, 285 to 288, 319, 320, 340 to 343, 293, 348, 1267, 209, 204, 446, 029, 043, 048) and the Normalisation inputs. Every figure agrees with the workbook to floating-point precision.

| Line | Low | Base | High | Workbook | Result |
|---|---|---|---|---|---|
| Allocation share, life (E51) / non-life (E52) | 0.884982 | 0.750590 | | same | OK |
| Allocated amortisation life / non-life / total (E53 to E55) | 448.686 | 532.919 | 981.605 | same | OK |
| Allocated onerous losses (E56), claims (E57), cash acquisition flows (E58) | 356.214 | 5 899.647 | 1 386.539 | same | OK |
| Acquisition ratios E66 / E67 / E68 | 0.108118 | 0.152719 | 0.067468 | same | OK |
| Pool 1 claims and benefits, net (row 106) | 5 456.171 | 5 728.541 | 6 091.701 | same | OK |
| Pool 2 expense view (107) / cash view (108) | 981.605 | 1 386.539 | | same | OK |
| of which bank fee (109) / other commission (110) | 774.000 | 612.539 | | same | OK |
| Pool 3a (111) | 1 042 | 1 042 | 1 042 | same | OK |
| Pool 3b attributable estimate (112) | 363.16 | 726.32 | 998.69 | same | OK |
| Pool 3c intermediary block (113) | 1 500 | 1 724 | 1 900 | same | OK |
| Pool 3 total (114) | 2 905.16 | 3 492.32 | 3 940.69 | same | OK |
| Pool 4 investment management (115) | 6.588 | 9.882 | 13.176 | same | OK |
| Pool 5a cost of capital (116) | 803.30 | 836.54 | 886.40 | same | OK |
| Pool 5b trapped capital (117) | 0 | 78.601 | 129.391 | same | OK |
| Pool 5c licence (118) | 10 | 20 | 40 | same | OK |
| Addressable base (122) | 3 524.287 | 4 114.741 | 4 566.405 | same | OK |
| Savings hypothesis (123) | 211.457 | 370.327 | 593.633 | same | OK |
| Claims leakage (124) | 54.562 | 114.571 | 182.751 | same | OK |
| Reinsurance price (125) | 9.95 | 19.90 | 29.85 | same | OK |
| Trapped capital and licence (126) | 10 | 98.601 | 169.391 | same | OK |
| Total hypothesis, accounting lines (127) | 275.969 | 504.798 | 806.234 | same | OK |
| Cost to achieve (128) | 137.984 | 504.798 | 1 451.221 | same | OK |

The Benchmark rows that link to this tab (36, 37, 57 to 61, 82, 83, 107 and 117) also agree with the independent rebuild.

Gap sizing rows 4 to 12: on every row J = (C - D) x F and K = (C - E) x F hold exactly (rand gap equals gap in percentage points times the AFS base), L = J x low realisation factor (0.5), M = J x base factor (0.75) and N = K x high top-quartile factor (0.75) hold, the base in column F links to the AFS revenue named in column G (9 079 Insurance SA, 5 310 Life, 4 102 Non-Life) and the C, D and E links point to the summary row with the same metric and peer group. Rows 16 to 22 equal cost base rows 122 to 128.

| Gap row | Metric, group | AFS value | Peer median | Base (Rm) | Gap (pp) | Rand gap to median | Rand gap to Q1 |
|---|---|---|---|---|---|---|---|
| 4 | M1 all | 0.1148 | 0.0685 | 9 079 | 4.63 | 420.42 | 741.60 |
| 5 | M1 life | 0.0399 | 0.1383 | 5 310 | -9.84 | -522.35 | -8.68 |
| 6 | M1 nonlife | 0.1229 | 0.0377 | 4 102 | 8.51 | 349.24 | 380.60 |
| 7 | M2 all | 0.1948 | 0.2205 | 9 079 | -2.57 | -233.28 | 562.76 |
| 8 | M2 composite | 0.1948 | 0.2351 | 9 079 | -4.03 | -366.01 | 432.54 |
| 9 | M3 composite | 0.0675 | 0.1060 | 9 079 | -3.86 | -350.05 | 21.46 |
| 10 | M3 nonlife | 0.1299 | 0.1390 | 4 102 | -0.91 | -37.12 | 94.15 |
| 11 | M5 nonlife | 0.8152 | 0.8950 | 4 102 | -7.98 | -327.22 | -253.51 |
| 12 | M5b nonlife | 0.9381 | 0.9296 | 4 102 | 0.85 | 34.84 | 127.09 |

## 6. Discrepancies requiring correction

No numerical discrepancy was found: all 81 sampled values match their documents, all 139 recomputed ratios agree with column R within floating-point precision, all 21 summary statistics agree, and all pool, ratio and gap figures agree. Items below are labelling or basis observations; none changes a computed value.

| Item | Cell or data_id | Finding | Correct value or action |
|---|---|---|---|
| 1 (labelling) | Raw data EU-078 (Credit Agricole Assurances, number of P&C contracts) | Value 17.9 with unit `count`; the notes say "in million policies" and Benchmark R120 correctly divides by 1e6. The unit label is inconsistent with the value. | Set unit to `m` (millions of policies) and leave the value and the R120 formula unchanged; or store 17 900 000 as `count` and remove the `*1000000` from the denominator in R120. Either way R120 stays 2 613.1 ZAR per contract. |
| 2 (basis note) | Benchmark row 140 (Brasilseg premiums written per employee) | Numerator EM-176 is FY2025 premiums; denominator EM-175 is an approximate headcount (about 1 970) from the 2024 sustainability report. Only row on the tab mixing period ends. | Add to column X: "headcount is the approximate 2024 figure from the sustainability report". No value change. |
| 3 (basis note) | Benchmark rows 42, 84, 119, 124, 134 (SBI Life, FY to 31 March 2026) | FX period in column K is 2025 (calendar-year ECB average) for a year ending March 2026. The choice is defensible (nine of twelve months overlap) and affects only the per-unit rows 119, 124 and 134; rows 42 and 84 are currency-neutral ratios. | Note the convention in column X or on the Normalisation tab. No value change. |
