"""Apply the red-team changes (brief of 4 November 2026, draft v1 to v2) to the content modules.

Every edit is an entry below with its change ID, the exact find string, the replacement and the number of
occurrences the brief lists. An entry whose count differs is not applied and is logged as Blocked.
D1 is on Michael's skip line: C6.1 decision 1 and M1 are skipped, and every "goal" statement is kept.

Usage: python3 apply_v2.py [--dry]   (writes redteam/applied.json, the edit log the change log is built from)
Run once, on the v1 content (git tag draft-v1 plus the formatting commit). On the v2 content every find has already been
replaced, so a second run reports every entry as Blocked and writes nothing useful.
"""
import json, glob, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
C = os.path.join(HERE, '..', 'content')
DRY = '--dry' in sys.argv
FILES = {os.path.relpath(f, C): json.load(open(f)) for f in sorted(glob.glob(os.path.join(C, '*', '*.json')))}
LOG, BLOCKED = [], []


def walk(x, path):
    """Yield (container, key, path, string) for every string in x."""
    if isinstance(x, list):
        for i, y in enumerate(x):
            if isinstance(y, str): yield x, i, f'{path}[{i}]', y
            else: yield from walk(y, f'{path}[{i}]')
    elif isinstance(x, dict):
        for k, v in x.items():
            if isinstance(v, str): yield x, k, f'{path}.{k}', v
            else: yield from walk(v, f'{path}.{k}')


def in_scope(f, path, scope):
    if scope is None: return True
    for s in (scope if isinstance(scope, list) else [scope]):
        sf, _, sp = s.partition(':')
        if sf in f and path.startswith(sp): return True
    return False


def R(cid, find, repl, n=1, scope=None, kind='Done', note=''):
    """Replace every occurrence of find (in scope) with repl, if the total count equals n."""
    hits = [(f, c, k, p, s) for f, d in FILES.items() for c, k, p, s in walk(d, '') if in_scope(f, p, scope) and find in s]
    total = sum(s.count(find) for *_, s in hits)
    if total != n:
        BLOCKED.append({'id': cid, 'find': find, 'expected': n, 'found': total, 'where': [f'{f} {p}' for f, _, _, p, _ in hits], 'note': note})
        return False
    for f, c, k, p, s in hits:
        c[k] = s.replace(find, repl)
        LOG.append({'id': cid, 'kind': kind, 'file': f, 'path': p, 'before': find, 'after': repl, 'note': note})
    return True


def block_index(anchor, scope=None):
    """Return (file, index) of the single top-level block whose strings contain anchor."""
    found = []
    for f, d in FILES.items():
        if scope and scope not in f: continue
        for i, b in enumerate(d['blocks']):
            if any(anchor in s for *_, s in walk(b, '')): found.append((f, i))
    return found


def INS(cid, anchor, blocks, scope=None, before=False, kind='Done', note=''):
    found = block_index(anchor, scope)
    if len(found) != 1:
        BLOCKED.append({'id': cid, 'find': f'[insert anchor] {anchor}', 'expected': 1, 'found': len(found), 'where': [f'{f} block {i}' for f, i in found], 'note': note})
        return False
    f, i = found[0]
    at = i if before else i + 1
    FILES[f]['blocks'][at:at] = blocks
    for b in blocks:
        LOG.append({'id': cid, 'kind': kind, 'file': f, 'path': f'.blocks[{at}] (new {b["type"]})', 'before': '', 'after': b.get('text') or json.dumps(b.get('items') or b, ensure_ascii=False), 'note': note})
    return True


def DELB(cid, anchor, scope=None, kind='Done', note=''):
    found = block_index(anchor, scope)
    if len(found) != 1:
        BLOCKED.append({'id': cid, 'find': f'[delete block] {anchor}', 'expected': 1, 'found': len(found), 'where': [f'{f} block {i}' for f, i in found], 'note': note})
        return False
    f, i = found[0]
    b = FILES[f]['blocks'].pop(i)
    LOG.append({'id': cid, 'kind': kind, 'file': f, 'path': f'.blocks[{i}] (deleted {b["type"]})', 'before': b.get('text') or json.dumps(b, ensure_ascii=False)[:400], 'after': '', 'note': note})
    return True


def table(anchor, scope=None):
    found = [(f, i) for f, i in block_index(anchor, scope) if FILES[f]['blocks'][i]['type'] in ('table', 'grid')]
    assert len(found) == 1, (anchor, found)
    f, i = found[0]
    return f, i, FILES[f]['blocks'][i]


def ROWDEL(cid, tanchor, cell0, kind='Done', note=''):
    f, i, t = table(tanchor)
    idx = [r for r, row in enumerate(t['rows']) if row[0] == cell0]
    if len(idx) != 1:
        BLOCKED.append({'id': cid, 'find': f'[delete row] {cell0}', 'expected': 1, 'found': len(idx), 'where': [f], 'note': note}); return False
    row = t['rows'].pop(idx[0])
    LOG.append({'id': cid, 'kind': kind, 'file': f, 'path': f'.blocks[{i}].rows[{idx[0]}] (deleted row)', 'before': ' / '.join(row), 'after': '', 'note': note})
    return True


def ROWADD(cid, tanchor, rows, after_cell0=None, kind='Done', note=''):
    f, i, t = table(tanchor)
    at = len(t['rows']) if after_cell0 is None else [r for r, row in enumerate(t['rows']) if row[0] == after_cell0][0] + 1
    assert all(len(r) == len(t['columns']) for r in rows)
    t['rows'][at:at] = rows
    for k, r in enumerate(rows):
        LOG.append({'id': cid, 'kind': kind, 'file': f, 'path': f'.blocks[{i}].rows[{at + k}] (new row)', 'before': '', 'after': ' / '.join(r), 'note': note})


def FN(cid, desc, fn, kind='Done', note=''):
    """Custom edit: fn() makes the change and returns (file, path, before, after) or raises."""
    f, p, before, after = fn()
    LOG.append({'id': cid, 'kind': kind, 'file': f, 'path': p, 'before': before, 'after': after, 'note': note or desc})


def S(f, anchor, sub=''):
    """Scope string for the single block in file f containing anchor (indices move when blocks are inserted)."""
    found = [i for ff, i in block_index(anchor, f) if ff == f]
    assert len(found) == 1, (f, anchor, found)
    return f'{f}:.blocks[{found[0]}]{sub}'


def blk(f, i):
    return FILES[f]['blocks'][i]


def find_block(f, pred):
    idx = [i for i, b in enumerate(FILES[f]['blocks']) if pred(b)]
    assert len(idx) == 1, (f, idx)
    return idx[0]


SFINDINGS = 'Summary of Findings, 14 Oct 2026'
ACSA_TN = '(ACSA, Q1 2026/27 presentation to the Portfolio Committee on Transport, as reported by Travel News, Aug 2026)'

# =====================================================================================================
# C1. The 1.8 million seat line, and the runway date
# =====================================================================================================
# C1.1. Longer finds first: the p25 find also sits inside the p115 title and the p118 sentence, which the brief names
# separately, so those two are applied before it.
R('C1.1', 'before the base case reaches the seat ceiling, and the direct routes wait for runway relief',
  "before the base case crosses the model's seat line, and the direct routes wait for runway relief")
R('C1.1', 'two years before the base case reaches the seat ceiling at its 2030 point',
  "two years before the base case crosses the model's seat line around 2030")
R('C1.1', 'Current air access caps inbound seats at 1.8 million, and the base case passes that ceiling at its 2030 point; runway relief at Cape Town International lands about 2033 (Demand-Side Analysis, Jun 2026, p21; Infrastructure Report, Jul 2026, p103).',
  "The growth model draws current air access as a line at 1.8 million inbound seats, and the base case crosses it around 2030. Runway relief is planned for about 2033, though ACSA now schedules the realigned runway for December 2029 (Demand-Side Analysis, Jun 2026, p21; Infrastructure Report, Jul 2026, p103; ACSA, Q1 2026/27 presentation to the Portfolio Committee on Transport, as reported by Travel News, Aug 2026).")
R('C1.1', 'scales what works and meets the seat ceiling at the 2030 mid-term review', "scales what works and meets the model's seat line at the 2030 mid-term review")
R('C1.1', 'and the base path passes the 1.8m seat ceiling before 2031', "and the base path crosses the model's 1.8m seat line before 2031", n=2)
R('C1.1', '(2028 and 2035 points; 1.8m ceiling)', '(2028 and 2035 points; 1.8m seat line)')
R('C1.1', 'Even the base case runs into a ceiling. Current air access caps inbound capacity at 1.8 million seats, and the base case first passes that line at the 2030 plotted year',
  "Even the base case runs into the model's seat line. The growth model draws inbound capacity at 1.8 million seats, and the base case first passes that line at the 2030 plotted year")
R('C1.1', 'inbound capacity capped at 1.8 million seats', 'inbound capacity drawn at 1.8 million seats')
R('C1.1', 'lift the 1.8 million ceiling', 'lift the 1.8 million seat line')
R('C1.1', 'before the base case reaches the seat ceiling', "before the base case crosses the model's seat line")
R('C1.1', 'The binding supply is seats. Current air access places a hard ceiling at 1.8 million inbound seats, and the base case',
  'The binding supply is peak capacity at the gateway. The growth model draws current air access as a line at 1.8 million inbound seats, and the base case')
R('C1.1', 'The chart below sets the base case against that ceiling.', 'The chart below sets the base case against that line.')
R('C1.1', 'The base case crosses the 1.8m inbound seat ceiling at the 2030 plotted year, two years before the earliest relief at Cape Town International.',
  "The base case crosses the model's 1.8m seat line at the 2030 plotted year, before runway relief on the planning date of about 2033.")
R('C1.1', 'Seat ceiling as drawn on the same slide.', 'Seat line as drawn on the same slide.')
R('C1.1', 'Concentration, seasonality and seats cap growth before demand does, and the base case meets the 1.8m inbound seat ceiling by 2030.',
  "Concentration, seasonality and peak seats cap growth before demand does, and the base case crosses the model's 1.8m seat line by 2030.")
R('C1.1', 'The base case passes the 1.8m inbound seat ceiling at the 2030 year point', "The base case crosses the model's 1.8m seat line at the 2030 year point")
R('C1.1', 'and the seat ceiling as drawn', 'and the seat line as drawn')
R('C1.1', '4. Seats bind before demand does.', '4. Seats bind at the peak before demand does.')
R('C1.1', 'with 1,802,929 arrivals (Market Assessment Report, May 2026, p20).',
  "with 1,802,929 arrivals (Market Assessment Report, May 2026, p20). The line is the model's assumption, not a measured cap (section 1.3).")
R('C1.1', 'Seats bind by 2030', 'Seat line crossed by 2030')
R('C1.1', '1.8m inbound seats;', '1.8m inbound seats as drawn;', scope='ch2/01_demand.json:.blocks[33]')
R('C1.1', 'Current air access caps inbound seats at 1.8 million, and the base case passes that ceiling at the 2030 year point (Demand-Side Analysis, Jun 2026, p21).',
  'The growth model draws current air access as a line at 1.8 million inbound seats, and the base case crosses it at the 2030 year point (Demand-Side Analysis, Jun 2026, p21); the runway binds at peak hours.')
R('C1.1', 'The network is full on its best routes, the airport is full at its runway, and relief lands after the base case passes the seat ceiling.',
  "The network is full on its best routes, the airport is full at its runway at peak, and planned relief lands after the base case crosses the model's seat line.")
R('C1.1', 'A seat ceiling in 2030', 'A seat line in 2030')
R('C1.1', 'Current air access caps inbound seats at 1.8 million; the base case passes it at the 2030 year point (1,802,929)',
  'The model draws current air access at 1.8 million inbound seats; the base case crosses it at the 2030 year point (1,802,929)')
R('C1.1', 'The gateway binds first.** Current air access places a hard ceiling at 1.8 million inbound seats, and the base case passes it at the 2030 year point',
  'The gateway binds first, at peak.** The growth model draws current air access as a line at 1.8 million inbound seats, and the base case crosses it at the 2030 year point')
R('C1.1', 'Before the base case reaches the seat ceiling at the 2030 point', "Before the base case crosses the model's seat line around 2030")
R('C1.1', 'The 2030 mid-term review tests the ceiling', 'The 2030 mid-term review tests the seat line')
R('C1.1', 'seat ceiling from Demand-Side Analysis', 'seat line from Demand-Side Analysis')
R('C1.1', 'Phase 2 scales what Phase 1 proved and meets the seat ceiling.', "Phase 2 scales what Phase 1 proved and meets the model's seat line.")
R('C1.1', 'Arrivals against the base path at the seat ceiling (T1-01)', "Arrivals against the base path at the model's seat line (T1-01); peak-hour runway headroom")
R('C1.1', 'Re-sequence Phase 2 if the ceiling binds early or relief slips', 'Re-sequence Phase 2 if peak capacity binds early or relief slips')
R('C1.1', 'a mid-term review in 2030, when the seat ceiling binds', "a mid-term review in 2030, when the base case crosses the model's seat line")
R('C1.1', 'It falls in 2030 because that is when the base case reaches the 1.8 million seat ceiling (Demand-Side Analysis, Jun 2026, p21) and two years before relief at Cape Town International (Infrastructure Report, Jul 2026, p103).',
  "It falls in 2030 because that is when the base case crosses the model's 1.8 million seat line (Demand-Side Analysis, Jun 2026, p21), before runway relief on the planning date (Infrastructure Report, Jul 2026, p103).")
R('C1.1', 'and its base case passes the 1.8 million seat ceiling at the 2030 year point', 'and its base case crosses the 1.8 million seat line the model draws, at the 2030 year point')
R('C1.1', 'Seat ceiling and model limits', 'Seat line and model limits')
R('C1.1', 'The model prints its seat ceiling and six base-case year points', 'The model prints its seat line and six base-case year points')
R('C1.1', 'Seat ceiling', 'Seat line', scope='appendices/02_a2_demand_model.json:.blocks[25].rows')
R('C1.1', 'Year the ceiling binds', 'Year the line is crossed')
R('C1.1', 'Seat ceiling', 'Seat line', scope='appendices/09_a9_glossary.json:.blocks[4].rows')
R('C1.1', 'The 1.8 million inbound seats that current air access provides, as drawn in the Demand-Side Analysis',
  'The 1.8 million inbound seats the growth model draws as current air access, as drawn in the Demand-Side Analysis; a model assumption, not a measured cap (section 1.3)')
R('C1.1', '1.8m inbound seat ceiling', '1.8m seat line (model)', n=4, note='Chart line label in Figures ES.2, 1.4, 2.1 and 5.2.')
# C1.1 sweep: remaining "ceiling" hits that refer to the seat line and are not quotations.
R('C1.1', 'If the supply moves slip, the case stops at the ceiling.', 'If the supply moves slip, the case stops at the seat line.', kind='Sweep',
  note='Run-in heading in section 3.4 (p114) referring to the seat line.')
R('C1.1', 'tests arrivals against the base path when the ceiling binds', "tests arrivals against the base path when the base case crosses the model's seat line", kind='Sweep',
  note='Section 4.2 (p119), second mention in the Phase 2 paragraph.')

# C1.2. The caveat.
C12 = ("The line is the model's assumption, not a measured cap. At Cape Town International's 79% average load factor, 1.8 million inbound seats would carry about 1.42 million arrivals, "
       "fewer than the 1.57 million ACSA recorded in FY25/26 (MIDAS Aviation Market Assessment, Mar 2026, \"The South African Market\"; Demand-Side Analysis, Jun 2026, p11; computed). "
       "MIDAS tables 3,816,797 international seats for the year to November 2025, more than 1.8 million each way even if that total counts both directions (\"Seasonality\"). "
       "What binds is the runway at peak hours in the summer peak, at about 30 movements an hour (Infrastructure Report, Jul 2026, p101). "
       "[Open item: ACSA or OAG to supply peak-hour and seasonal slot headroom at Cape Town International.]")
INS('C1.2', 'fig_base_case_seat_ceiling', [{'type': 'p', 'text': C12}], scope='ch1/03')
R('C1.2', 'Neither deck prints the seats behind the line or a load factor that converts seats into arrivals.',
  "Neither deck prints the seats behind the line or a load factor that converts seats into arrivals. At the 79% average load factor, 1.8 million seats would carry about 1.42 million arrivals, below the 1.57 million recorded in FY25/26, so this report reads the line as the model's assumption, not a measured cap (section 1.3).")

# C1.3. Runway date (D3).
R('C1.3', "and ACSA's programme of about R11.3bn brings relief only from about 2032 to 2034 (Infrastructure Report, Jul 2026, p101 to p103).",
  "and ACSA's programme of about R11.3bn brings relief from about 2032 for the international terminal and about 2033 for the runway (Infrastructure Report, Jul 2026, p101 to p103). "
  "ACSA's latest schedule shows the realigned runway from December 2026 to December 2029, subject to contract award " + ACSA_TN + ".")
R('C1.3', "and ACSA's programme of about R11.3bn brings relief only from about 2032 (p101 to p103).",
  "and ACSA's programme of about R11.3bn brings relief from about 2032 for the terminal and about 2033 for the runway (p101 to p103).")
R('C1.3', 'The R6.39bn runway relocation adds about 40% more movements an hour but completes around 2033, and relief across the airport lands from about 2032 (p103).',
  "The R6.39bn runway relocation lifts capacity from 30 to 45 movements an hour, a 50% rise, and completes around 2033 on the Infrastructure Report's timing, with terminal relief from about 2032 (p103; Minister of Transport, parliamentary reply, Apr 2025). "
  "ACSA's latest schedule shows the runway finished by December 2029 (ACSA, Q1 2026/27 presentation to the Portfolio Committee on Transport, Aug 2026).")
R('C1.3', 'the runway about 2033', "the runway about 2033; ACSA's latest schedule shows the runway by December 2029", scope='ch3/21_fa07.json:.blocks[10].rows')
R('C1.3', 'IR p101 to p103', 'IR p101 to p103; ACSA, Aug 2026', scope='ch3/21_fa07.json:.blocks[10].rows')
R('C1.3', 'and about 2033 for the runway (Infrastructure Report, Jul 2026, p103).',
  'and about 2033 for the runway (Infrastructure Report, Jul 2026, p103). ACSA now schedules the realigned runway for December 2029, subject to contract award. '
  'This plan keeps about 2033 as its planning date and treats the earlier date as upside ' + ACSA_TN + '.', scope='ch3/40')
R('C1.3', 'confirm route cases for India and China', 'confirm route cases for India and China, and bring them into Phase 2 if ACSA awards the runway contract on its December 2029 schedule',
  scope='ch4/07_governance.json')

# =====================================================================================================
# C2. Narrow the thesis (D7). The ES opening (p13) is handled under M13.
# =====================================================================================================
R('C2', 'the evidence has reframed that ambition as growth to 2.5 million arrivals, set by supply rather than demand.',
  'the evidence has reframed that ambition as growth to 2.5 million arrivals, paced by gateway capacity in the summer peak and by demand in the green season.',
  note='D1 skipped: "growth to 2.5 million arrivals" kept as the goal; only the thesis clause changed.')
R('C2', 'The recovery is complete, and the growth that follows is capped by supply rather than demand.',
  'The recovery is complete; gateway capacity caps growth in the summer peak, and demand and conversion cap it in the green season.')
R('C2', 'Demand without seats', 'Seats in summer, demand in winter')
R('C2', 'Growth is now supply-constrained, not demand-constrained.',
  "Growth is now supply-constrained in the summer peak and demand-constrained in the green season, when airlines withdraw seats: June carries 6.4% of the year's international capacity (MIDAS Aviation Market Assessment, Mar 2026, \"Seasonality\").")
R('C2', 'why the next step is supply-constrained', 'why the next step is constrained by peak capacity')
R('C2', 'Marketing cannot make up for missing seats, because carriers on full routes raise fares instead (MIDAS Aviation Market Assessment, Mar 2026, In Conclusion).',
  'On the eleven full routes, marketing cannot make up for missing seats, because carriers raise fares instead (MIDAS Aviation Market Assessment, Mar 2026, In Conclusion). '
  'On the hub routes, which run at 65% to 72% load and add the most base-case arrivals, it can ("Seasonality").')
R('C2', 'Demand work cannot make up the gap, because marketing into full routes raises fares rather than seats (MIDAS Aviation Market Assessment, Mar 2026, In Conclusion).',
  'On the full routes, demand work cannot make up the gap, because marketing raises fares rather than seats (MIDAS Aviation Market Assessment, Mar 2026, In Conclusion); on the hub routes, which have seats to spare, it can.')
R('C2', 'Demand is not what holds Pillar 1 back; conversion is.', 'Latent interest is not what holds Pillar 1 back; turning it into bookings is.')

# =====================================================================================================
# C3. Mark the arrivals basis as unconfirmed
# =====================================================================================================
# The brief's text has a comma before "or" in the list of three bases; removed under rule 7 (no Oxford comma).
C31 = ("The model's 2025 base of 1,498,829 sits close to, but below, SA Tourism's 1,538,142 for 2025 (Wesgro Research, Western Cape Tourism Performance: Annual 2025). "
       "Each market group's step from the June deck's 2024 base also tracks its own growth rate to within 0.2 points (Appendix A2; computed). "
       "This report therefore treats the 2025 base as a model value until the basis is confirmed. "
       "[Open item: Skift to confirm in writing what the model counts (SA Tourism tourist arrivals, ACSA passengers including returning residents or OAG origin-and-destination flows) and how the Hubs group is built.]")
INS('C3', 'The report uses airport passenger arrivals for baselines, the demand model for targets', [{'type': 'p', 'text': C31}], scope='ch1/01',
    note='Oxford comma in the brief text removed ("returning residents, or OAG" to "returning residents or OAG").')
R('C3', '(Wesgro, presentation to the parliamentary committee, 1 Apr 2026; public source). [G4J 2023 document',
  '(Wesgro, presentation to the parliamentary committee, 1 Apr 2026; public source). If the model counts arrivals on the SA Tourism basis, G4J\'s 3 million for 2035 sits above both paths. '
  'The difference is method: G4J adds 1 million to 2019\'s 2 million, while the growth model builds up market by market against the seats and routes the gateway can carry. [G4J 2023 document')
R('C3', "tourist arrivals on the model's basis, and international passenger arrivals at Cape Town International.",
  "arrivals on the growth model's basis, which Skift is to confirm (section 1.1), and international passenger arrivals at Cape Town International.")
R('C3', "On the growth model's basis, tourist arrivals;", "On the growth model's basis, which Skift is to confirm;")
R('C3', '1,498,829 (2025)', '1,498,829 (2025, model value)', n=2, scope=['exec/01_summary.json:.blocks[31].rows', 'ch5/03_baselines_targets.json:.blocks[5].rows'])
R('C3', 'SA Tourism', 'SA Tourism [Open item: SA Tourism cannot report the Hubs group; Skift to define it.]', scope='ch5/02_indicators.json:.blocks[4].rows[1][3]')

# =====================================================================================================
# C4. Green season, spend and jobs
# =====================================================================================================
R('C4.1', 'and about 65% of overseas visitor travel falls between October and March, a provisional figure',
  'and about 62% of overseas visitor travel falls between October and March')
R('C4.1', 'October to March together account for about 65% of the year.',
  'October to March together account for about 62% of the year once the twelve printed shares, which sum to 104.9%, are scaled to 100% [Wesgro Research to confirm the 2025 month-of-travel shares].',
  note='The brief\'s find runs across two source paragraphs; the replacement closes the first and the second keeps its 2024 sentence.')
R('C4.1', 'That 65% is derived, not printed. The twelve monthly shares on the 2025 slide sum to 104.9%, so the October to March figure is provisional and flagged wherever it appears [Wesgro Research to confirm the 2025 month-of-travel shares]. ',
  '', note='Second half of the same find (p30).')
R('C4.1', 'between 61% and 65%', 'between 61% and 62%')
R('C4.1', '65%', '62%', scope='ch1/02_system_today.json:.blocks[24].rows[1][13]')
R('C4.1', '(Stats SA and SAT 2025; the printed shares sum to 104.9%, so the 2025 row and its October to March share are provisional)',
  '(Stats SA and SAT 2025; the printed shares sum to 104.9%, and the October to March share is computed with the 2025 shares normalised to 100%)')
R('C4.1', 'October to March hold about 65% on that table, a provisional figure because its twelve shares sum to 104.9%. On a Cape Town overseas air-arrivals basis for January to August 2024 the split was 61% and 39% (Market Assessment Report, May 2026, p25).',
  'October to March hold about 62% on that table once its twelve shares, which sum to 104.9%, are normalised. The 2024 Wesgro Visitor Tracking Survey gives 61% and 39% (Current State Diagnostic, Dec 2025, p32).')
R('C4.1', 'October to March about 65%, 2025 (provisional; shares sum to 104.9%); 61%, Jan to Aug 2024, Cape Town overseas air arrivals',
  'October to March about 62%, 2025 (normalised; printed shares sum to 104.9%); 61%, 2024, Wesgro Visitor Tracking Survey')
R('C4.1', 'DSA p12; MA p25', 'DSA p12; Diag p32', scope='ch2/01_demand.json:.blocks[33].rows[2]')
R('C4.1', 'DSA: Demand-Side Analysis, Jun 2026.', 'DSA: Demand-Side Analysis, Jun 2026. Diag: Current State Diagnostic, Dec 2025.', scope='ch2/01_demand.json:.blocks[33].source',
  kind='Consequential', note='Table 2.2 source key gains "Diag", which the new source cell uses.')
R('C4.1', 'About 65% of 2025 overseas visitor travel fell between October and March (provisional)', 'About 62% of 2025 overseas visitor travel fell between October and March (normalised)')
R('C4.1', ', while the Market Assessment, p25, prints the same split on a Cape Town overseas air-arrivals basis', '')
R('C4.1', 'The October to March share is about 65% for 2025, but the figure is provisional: it is computed from a month-of-travel table whose shares sum to 104.9% (Demand-Side Analysis, Jun 2026, p12).',
  'The October to March share is about 62% for 2025, computed from a month-of-travel table whose shares sum to 104.9% and normalised (Demand-Side Analysis, Jun 2026, p12).')
R('C4.1', 'About 35% (2025, provisional); 39% (2024)', '38.1% (2025, normalised); 39% (2024)')
R('C4.1', 'About 35% (2025, provisional; 38.1% normalised); 39% (2024)', '38.1% (2025, normalised); 39% (2024)')


def c41_green():
    f = 'ch5/03_baselines_targets.json'
    i = find_block(f, lambda b: b.get('text', '').startswith('**Green season.** Plan decision 6 sets'))
    b = blk(f, i); before = b['text']
    assert before.endswith('[Michael to confirm: switch the T1-05 baseline to 38.1%].')
    b['text'] = ('**Green season.** The 2025 month table sums to 104.9%. Normalised, it gives 61.9% for October to March and 38.1% for the green season, '
                 'in line with the printed 61% and 39% for 2024 (Demand-Side Analysis, Jun 2026, p12; Current State Diagnostic, Dec 2025, p32). T1-05 uses 38.1% as its baseline.')
    return f, f'.blocks[{i}].text', before, b['text']


FN('C4.1', 'Section 5.3 green-season paragraph replaced whole (also closes C5 "Plan decision 6" and "[Michael to confirm: ...]").', c41_green)

# C4.2 Spend.
R('C4.2', 'R25.9bn (FY2025)', 'R25.9bn (FY2025, nominal)', n=2, scope=['exec/01_summary.json:.blocks[31].rows[2]', 'ch5/03_baselines_targets.json:.blocks[5].rows[2]'])
R('C4.2', 'R40.6bn (base, modelled)', 'R40.6bn (base, modelled, constant 2024 rand)', n=2, scope=['exec/01_summary.json:.blocks[31].rows[2]', 'ch5/03_baselines_targets.json:.blocks[5].rows[2]'])
R('C4.2', 'R33.7bn in 2030 (base, modelled)', 'R33.7bn in 2030 (base, modelled, constant 2024 rand)')
SPEND = ("**Spend.** T1-03's path holds spend per arrival fixed, so its targets are in constant 2024 rand, while SA Tourism reports nominal rand; progress is read after deflating by CPI. "
         "The model's 2024 spend of R27.12bn sits 19% above the R22.7bn SA Tourism reported for FY2024 (Market Assessment Report, May 2026, p10, p24). "
         "[Open item: Skift to rebase the spend path on the FY2025 actual of R25.9bn.]")
INS('C4.2', '**Arrivals.** The model', [{'type': 'p', 'text': SPEND}], scope='ch5/03')

# C4.3 Jobs (D4).
R('C4.3', 'Tourism jobs (ratio)', 'Tourism jobs', n=2)
R('C4.3', 'About 30,000 (2025)', 'Set by the labour analysis (I18)')
R('C4.3', 'About 30,000 jobs supported (2025)', 'Set by the labour analysis (I18)')
R('C4.3', '33,500 / 35,000*', 'Set at Gate 1', n=2)
R('C4.3', '37,400 / 40,900*', 'Set at Gate 1')
R('C4.3', '43,500 / 50,300*', 'Set at Gate 1', n=2)
R('C4.3', "Jobs use Wesgro's ratio of two jobs per 100 international passengers (public source), a ratio-based projection until the labour analysis reports.",
  'Tourism jobs have no provincial baseline; the labour analysis (I18) sets one by Gate 1.')
R('C4.2', 'Tourism jobs have no provincial baseline; the labour analysis (I18) sets one by Gate 1.',
  'Tourism jobs have no provincial baseline; the labour analysis (I18) sets one by Gate 1. T1-03 targets are in constant 2024 rand.', note='Table ES.6 source note: appended sentence.')
R('C4.3', "T1-04: Wesgro's ratio of two jobs per 100 international passengers, applied to T1-01 (computed; public source, see the note below).",
  'T1-04: baseline and targets to be set by the labour analysis (I18).')
R('C4.3', "The Tier 1 measure is therefore jobs supported by international air arrivals, on Wesgro's own rule of thumb of two jobs for every 100 international passengers, which counts direct, indirect and induced jobs (public source: Wesgro and Cape Town Air Access releases, 2023 to 2024) [methodology note for the ratio: Cape Town Air Access to supply]. Applied to the arrivals paths, it gives about 30,000 jobs in 2025 and adds about 13,500 on the base path and 20,300 on the accelerated path by 2035. It is a ratio-based projection, not a labour-market measure.",
  'T1-04 therefore carries no baseline or modelled path until the labour analysis sets a provincial measure (I18).', note='First part of the run (p153, "Jobs." paragraph).')
R('C4.3', "The ratio does not reach the 300,000 tourism-linked jobs in the Inception Report's ambition, because it counts only jobs linked to international air arrivals (Inception Report, Nov 2025, p4). ",
  '', note='End of the same run: the next paragraph opens with it in the source. The 300,000 restatement and the context figures are kept.')
R('C4.3', "Until it reports, Chapter 5 carries jobs as a ratio-based measure on Wesgro's own rule of two jobs per 100 international passengers (section 5.3).",
  'Until it reports, Chapter 5 carries jobs without a baseline or target.')
R('C4.3', 'carried as a ratio-based projection until the analysis reports', 'with its baseline set by the analysis')
R('C4.3', "Jobs supported by international air arrivals, on Wesgro's ratio, until the labour analysis sets a provincial measure",
  'Tourism jobs in the Western Cape, on the measure the labour analysis sets (I18)')
ROWDEL('C4.3', 'Eleven data gaps stand between the plan', 'Methodology for two jobs per 100 passengers', note='Table 5.9 in v1 (the brief calls it Table 5.8).')
# C4.3 consequential edits.
R('C4.3', 'Wesgro ratio; Stats SA TSA', 'Labour analysis (I18); Stats SA TSA', kind='Consequential', note='Table 5.4, T1-04 Source cell named the ratio the change removes.')
R('C4.3', 'Eleven data gaps stand between the plan and a full baseline', 'Ten data gaps stand between the plan and a full baseline', kind='Consequential', note='Table 5.9 title count after the row deletion.')
R('C4.3', 'Carried to Chapter 5 as a ratio-based projection, pending the labour analysis the strategy commissions',
  'Carried to Chapter 5 with its baseline set by the labour analysis the strategy commissions', kind='Consequential',
  note='Table 1.1 (p23), found by the "ratio-based" grep; worded as the brief words p113.')
R('C4.3', 'Arrivals and jobs carry targets on both paths, while season, spread and community spend start from dated baselines.',
  'Arrivals carry targets on both paths, while jobs wait on the labour analysis and season, spread and community spend start from dated baselines.', kind='Consequential',
  note='Table ES.6 title: jobs no longer carry targets.')
R('C4.3', "Arrivals and jobs carry targets on both paths; spend carries the working analysis's base path; the other Tier 1 indicators carry dated baselines first.",
  "Arrivals carry targets on both paths; spend carries the working analysis's base path; jobs and the other Tier 1 indicators set baselines first.", kind='Consequential',
  note='Table 5.7 title (the brief\'s Table 5.6): jobs no longer carry targets.')
R('C4.3', 'The arrivals targets come straight from the growth model, the jobs targets from a stated ratio, and the other Tier 1 targets wait for baselines that do not yet exist.',
  'The arrivals targets come straight from the growth model, while the jobs and other Tier 1 targets wait for baselines that do not yet exist.', kind='Consequential',
  note='Section 5.3 topline: the jobs ratio is removed.')

# =====================================================================================================
# C5. Errata and internal workings out of the report (D6)
# =====================================================================================================
DELB('C5', 'The reconciliation behind this rule logged 55 discrepancies', scope='ch1/04')
R('C5', 'Four carry a later file date than their cover, which the report records rather than hides. ', '')
R('C5', 'SLA Annexure B clause numbers as assigned in the agreed report structure of 2 November 2026 [to be checked against the signed Annexure B]',
  'SLA Annexure B clause numbers [to be checked against the signed Annexure B]')
R('C5', 'The agreed report structure assigns this work to SLA Annexure B clause', 'This work answers SLA Annexure B clause', n=6)
R('C5', 'Sixteen ran at 75% or more, the count the agreed structure attributes to the 80% line (computed from the same table).', 'Sixteen ran at 75% or more (computed from the same table).')
R('C5', ' The structure\'s "16 of 27 above 80%" is corrected to eleven.', '')
R('C5', 'The October record gives the reason as 16 of 27 routes above 80% and fares before seats. MIDAS, the source, prints eleven routes above 80%; sixteen is the count at 75% or more, and the report uses both on that basis [Summary of Findings, 14 Oct 2026: the deck\'s basis for 16 to confirm].',
  'The reason is full routes and fares before seats: eleven routes run above 80% load and sixteen at 75% or more (MIDAS Aviation Market Assessment, Mar 2026, "Seasonality").')
R('C5', 'The same slide prints 61% in its text; the report uses 63%, the sum of the printed shares, and logs the conflict.', 'The report uses 63%, the sum of the printed shares.')
R('C5', '(the Winelands gauge misprints 40.3%; 7,730 of 50,332 is 15.4%)', '(Winelands share computed: 7,730 of 50,332 is 15.4%)', n=2)
R('C5', "The main gauge on the Cape Winelands asset slide prints 40.3%, the Cape Metro's share, while the slide's text layer carries 15.4% (p45). The count supports 15.4%, since 7,730 of 50,332 assets is 15.4% (computed). This appendix uses 15.4%.",
  'This appendix uses 15.4%, computed from the count (7,730 of 50,332).')
R('C5', ' The body of the report counts fourteen new routes since 2014, a difference this report logs.', ' Other study documents count new routes from 2014 on a different basis.',
  note='Deleted under C5; P9\'s replacement line sits in its place, because the paragraph has no separate source note.')
R('C5', ' It printed ranks 7 to 30 with scores and reasons for exclusion; ranks 1 to 6 and their scores appear nowhere (p31).', '')


def c5_overall():
    f = 'appendices/04_a4_readiness.json'
    i = find_block(f, lambda b: b.get('text', '').startswith('**Overall rating.** The printed overall ratings do not follow the stated weights.'))
    b = blk(f, i); before = b['text']
    b['text'] = "**Overall rating.** The overall ratings are the Infrastructure Report's evidence-informed judgement, not a weighted formula, so this report does not re-derive them."
    return f, f'.blocks[{i}].text', before, b['text']


FN('C5', 'A4 "Overall rating." paragraph replaced from its second sentence to its end.', c5_overall)
R('C5', 'The printed overall ratings do not reproduce from the weighted dimension scores, so this report quotes them as printed.',
  "The overall ratings are the Infrastructure Report's evidence-informed judgement, not a weighted formula, so this report does not re-derive them.")
R('C5', "; the label 'Road Netowrk' is corrected", '')
R('C5', " The slides spell Cederberg 'Cederburg' and title both p72 and p73 'West Coast / Overberg'.", '')
R('C5', ' Slide titles print Mossell Bay, Dep Mobility, Dep Economic Development, Statistic SA, Table Mountain Ariel Cable and Cape Nature.', '')
R('C5', 'house style', "this report's style", n=2)
R('C5', 'This report uses the 2025 base and logs the difference.', 'This report uses the 2025 base.', kind='Sweep', note='"logs the" sweep hit (p42).')

# =====================================================================================================
# C6. Board decisions by authority (D2; D1 skipped)
# =====================================================================================================
OLD_D1 = "Adopt growth to 2.5 million arrivals by 2035 as the plan's goal, with the base and accelerated paths as its targets."


def c61():
    f = 'exec/01_summary.json'
    i = find_block(f, lambda b: b['type'] == 'numbered' and b['items'][0] == OLD_D1)
    old = blk(f, i)
    assert len(old['items']) == 5
    new = [
        {'type': 'p', 'text': 'The Wesgro Board decides:'},
        {'type': 'numbered', 'items': [
            OLD_D1,
            "Constitute the Tourism Growth Steerco, co-chaired by Wesgro's CEO and DEDAT's Head of Department with Cape Town Tourism as a standing member, and confirm the twelve initiative leads that sit with Wesgro.",
            "Approve the nine first-24-month actions that sit inside Wesgro's mandate and budget. Ask Wesgro Finance and DEDAT to set rand bands for every initiative, and to name what Wesgro deprioritises to fund them, before Gate 1. [Open item: Wesgro Finance to give an indicative rand band for the first 24 months.]",
            'Commission the bookability census in 2027, so the plan\'s missing baselines exist by Gate 1.',
            'Table the first national escalation agenda on visas, air service agreements and immigration processing at Cape Town International.']},
        {'type': 'p', 'text': 'The Board recommends to the Provincial Minister, DEDAT and the municipalities:'},
        {'type': 'numbered', 'continue': True, 'items': [
            'That DEDAT commission the tourism labour analysis in 2027 and lead I10, I13 and I18, and that the Department of Mobility lead I8.',
            'That the municipalities and LTOs lead and fund I12, and that the site operators lead I11.']},
    ]
    FILES[f]['blocks'][i:i + 1] = new
    return f, f'.blocks[{i}] (numbered list replaced by four blocks)', ' | '.join(old['items']), json.dumps(new, ensure_ascii=False)


FN('C6.1', 'Decisions list replaced; decision 1 kept as in v1 because D1 is skipped.', c61)
R('C6.2', "Twelve actions can start inside Wesgro's current mandate and budgets, and each opens a seat, a baseline or a booking path a later initiative needs.",
  "Twelve actions can start in the first 24 months, nine of them inside Wesgro's current mandate and budget, and each opens a seat, a baseline or a booking path a later initiative needs.")
R('C6.2', "Twelve actions can start by mid-2028 inside Wesgro's current mandate, and each one opens",
  "Twelve actions can start by mid-2028, nine of them inside Wesgro's current mandate and budget, and each one opens")
R('C6.4', 'A Tourism Growth Steerco chaired at Wesgro CEO level, with DEDAT and Cape Town Tourism as standing members and the City of Cape Town, the district municipalities and the industry bodies at the table.',
  "A Tourism Growth Steerco co-chaired by Wesgro's CEO and DEDAT's Head of Department, with Cape Town Tourism as a standing member and the City of Cape Town, the district municipalities and the industry bodies at the table. It is distinct from the Unlocking Tourism Steerco that oversees this study.")
R('C6.4', 'Chair: Wesgro CEO. With DEDAT and Cape Town Tourism', 'Co-chairs: Wesgro CEO and DEDAT HOD. With Cape Town Tourism', note='Figure 4.3 box label (inline SVG).')
R('C6.4', 'Constitute the Tourism Growth Steerco with DEDAT and Cape Town Tourism, and agree a decision-rights map by tier',
  'Constitute the Tourism Growth Steerco, co-chaired with DEDAT and with Cape Town Tourism as a standing member, and agree a decision-rights map by tier', n=2)
R('C6.4', "Wesgro CEO's office", "Wesgro CEO's office; DEDAT", n=2, scope=['exec/01_summary.json:.blocks[27].rows[3][2]', 'ch4/05_tactical.json:.blocks[4].rows[3][2]'])

# =====================================================================================================
# M1 skipped (D1). M2 to M13.
# =====================================================================================================
R('M2', 'Chile grew about 35%, Singapore about 19%, Kenya 12.8 to 14.6%, Valencia 13 to 14% and New Zealand about 12%.',
  'Chile grew 40.4%, Singapore 21%, Kenya 14.6%, Valencia 13 to 14% and New Zealand about 12%, against global growth of 11% in 2024 (Sernatur, Anuario de Turismo 2024, Dec 2025; Singapore Tourism Board, Feb 2025; UN Tourism, World Tourism Barometer, Jan 2025).')
R('M2', 'so the comparator range runs from about 4% to 35%.', 'so the comparator range runs from about 4% to 40%.', kind='Consequential',
  note='p35: the range end follows Chile\'s corrected 40.4% in the sentence before.')
R('M2', '(Global Benchmarking Report, Mar 2026, p7).',
  "(Global Benchmarking Report, Mar 2026, p7). UN Tourism's own figures put global growth at 11% in 2024, while recovery was still running, and about 4% in 2025 (World Tourism Barometer, Jan 2025 and Jan 2026).",
  scope='ch2/03_benchmarking.json:.blocks[9]')
R('M2', '**1. Five of the six comparators grew well above the norm.** Chile grew about 35% between 2023 and 2024, Singapore about 19%, Kenya 12.8% to 14.6%, Valencia 13% to 14% and New Zealand about 12% (Global Benchmarking Report, Mar 2026, p9).',
  '**1. Two of the six comparators grew well above the world.** Chile grew 40.4% between 2023 and 2024 and Singapore 21%, against global growth of 11%; Kenya (14.6%), Valencia (13% to 14%) and New Zealand (about 12%) grew slightly faster than the world (Global Benchmarking Report, Mar 2026, p9; Sernatur, Dec 2025; Singapore Tourism Board, Feb 2025).')
R('M2', 'Five of the six comparators grew above the 3% to 5% global norm in 2023 to 2024, each through a primary lever of its own.',
  'Against global growth of 11% in 2024, only Chile and Singapore grew clearly faster, and three of the six were still below 2019.')
T25 = 'ch2/03_benchmarking.json:.blocks[12].rows'
R('M2', 'About 35%', '40.4%', scope=T25)
R('M2', 'About 82% recovered', '116% of 2019; 55.6% of arrivals overland, 40% from Argentina', scope=T25)
R('M2', 'About 19%', '21%', scope=T25)
R('M2', 'Slightly below; spend recovered', '86% of 2019; receipts at a record', scope=T25)
R('M2', '12.8% to 14.6%', '14.6%', scope=T25)
R('M2', 'p53 (New Zealand arrivals), p17 (Australian forecast) and p61 (system type).',
  'p53 (New Zealand arrivals), p17 (Australian forecast) and p61 (system type). Chile: Sernatur, Anuario de Turismo 2024 (Dec 2025). Singapore: Singapore Tourism Board (Feb 2025). Kenya growth: Kenya Tourism data as reported, May 2025.',
  scope='ch2/03_benchmarking.json:.blocks[12].source')
INS('M2', 'Against global growth of 11% in 2024, only Chile and Singapore grew clearly faster',
    [{'type': 'p', 'text': "[Open item: add one comparator that underperformed, as the Inception Report's plan asked (Inception Report, Nov 2025, p16).]"}], scope='ch2/03')
R('M2', 'Five of the six comparators grew three to nine times the roughly 4% global rate of 2024 to 2025.',
  'Against global growth of 11% in 2024, Chile and Singapore grew two to four times as fast, and Kenya, Valencia and New Zealand slightly faster.')


def m2_chart():
    f = 'ch2/03_benchmarking.json'
    i = find_block(f, lambda b: b.get('id') == 'fig_23_growth')
    ch = blk(f, i)['chart']
    before = json.dumps({'categories': ch['categories'], 'values': ch['values']}, ensure_ascii=False)
    assert ch['values'] == [35, 19, 13.7, 13.5, 12, 4.3, 4] and ch['categories'][6] == 'Global, 2024 to 2025'
    ch['values'] = [40.4, 21, 14.6, 13.5, 12, 4.3, 11]
    ch['categories'][6] = 'World, 2024 (UN Tourism)'
    return f, f'.blocks[{i}].chart', before, json.dumps({'categories': ch['categories'], 'values': ch['values']}, ensure_ascii=False)


FN('M2', 'Figure 2.5 bars: Chile 40.4, Singapore 21, Kenya 14.6; reference bar 11, labelled "World, 2024 (UN Tourism)".', m2_chart)
R('M2', 'Kenya (range midpoint)', 'Kenya', kind='Consequential', note='Figure 2.5 category label: 14.6 is no longer a range midpoint.')
R('M2', 'Global Benchmarking Report, Mar 2026, p7 (global rate, UN Tourism World Tourism Barometer, January 2025) and p9 (comparators). Where the report prints a range, the bar shows its midpoint: Kenya 12.8% to 14.6%, Valencia 13% to 14%.',
  'Global Benchmarking Report, Mar 2026, p9 (comparators); Sernatur, Dec 2025 (Chile); Singapore Tourism Board, Feb 2025 (Singapore); Kenya Tourism data as reported, May 2025 (Kenya); UN Tourism, World Tourism Barometer, Jan 2025 (world, 2024). Where the report prints a range, the bar shows its midpoint: Valencia 13% to 14%.',
  kind='Consequential', note='Figure 2.5 source note follows the new bar values.')
R('M2', 'It received 13 million international visitors in 2024, 19% more than in 2023, and visitor spend reached $31.3 billion (p39).',
  'It received 16.5 million international visitors in 2024, 21% more than in 2023, and tourism receipts reached a record of about S$29 billion (Singapore Tourism Board, Feb 2025).')
R('M2', 'Singapore: stopover programme; 13m arrivals (+19%) and $31.3bn spend, 2024', 'Singapore: stopover programme; 16.5m arrivals (+21%) and about S$29bn receipts, 2024')
R('M2', 'p39, p40', 'p39, p40; STB, Feb 2025', scope=S('ch2/03_benchmarking.json', 'Eight benchmark findings carry into the hypothesis tree', '.rows[4][2]'))
R('M2', 'Norm 3% to 5% a year; Chile about 35%, Singapore about 19%, Valencia 13% to 14%', 'World 11% in 2024; Chile 40.4%, Singapore 21%, Valencia 13% to 14%')
R('M2', 'Five of the six printed growth rates exceed the 3% to 5% global norm, and four of the six cases pair structural demand creation with demand activation.',
  "Five of the six printed growth rates exceed the report's 3% to 5% norm, two clearly beat 2024's actual global growth of 11%, and four of the six cases pair structural demand creation with demand activation.")
R('M2', 'raises value per traveller without increasing arrivals.',
  'raises value per traveller without increasing arrivals. Corrected 2024 figures: Chile 40.4% (116% of 2019), Singapore 21% (86% of 2019), Kenya 14.6% (section 2.2).',
  scope='appendices/03_a3_benchmark.json:.blocks[12].source')

# M3 (D8): qualifiers in the text, no label changes.
R('M3', '**October 2026: Reworded.**', '**October 2026: Reworded, with the scope narrowed.**', scope='ch3/14_fa04.json')
R('M3', '**October 2026: Validated.** Full routes.', '**October 2026: Validated, without fare or yield data.** Full routes.')
R('M3', '**October 2026: Validated.** No pipeline.', '**October 2026: Validated, on inference.** No pipeline.')
R('M3', 'The Stakeholder Insights Report mapped all 223 of its insight statements to tree entries before aggregating them (Stakeholder Insights Report, Mar 2026, p5, p20 to p46).',
  'The Stakeholder Insights Report mapped all 223 of its insight statements to tree entries before aggregating them (Stakeholder Insights Report, Mar 2026, p5, p20 to p46). '
  'Because the study team mapped the insights to tree entries, the counts show where views cluster; they do not on their own validate an entry.')
M3P = ('**What the evidence argued against.** No entry was withdrawn, but the evidence narrowed or overturned three parts of the December case. '
       'First, the pivot to four growth markets narrowed to converting India and China traffic already flying through hubs; the Middle East and ASEAN cases did not survive (focus area 4). '
       'Second, the ambition to double arrivals did not survive: the growth model supports 2.2 million to 2.5 million by 2035 (section 1.1). '
       'Third, the 300,000 tourism-linked jobs ambition has no baseline behind it and is flagged untested (focus area 20). '
       'Two Validated entries also rest on less than direct evidence: focus area 5 has no fare or yield data, and focus area 15 is an inference from the pipeline tables (section 3.3).')
INS('M3', 'Seven labels record what the evidence did to each December hypothesis', [{'type': 'p', 'text': M3P}], scope='ch1/05',
    note='Table 1.9 sits in section 1.5 (pp40 to 41); the passage goes directly after it, run-in bold as elsewhere.')

# M4.
FA2_OLD = "The green season is a seat problem and an events problem at once: June holds 6.4% of the year's international seats, while international meetings already cluster in the months leisure travel leaves empty."
FA2_NEW = "The green season is a seat problem and an events problem at once. June holds 6.4% of the year's international seats, and business events are the lever best placed to fill the trough, though international meetings now peak from September to November."
R('M4', FA2_OLD, FA2_NEW, n=2)
R('M4', 'Meetings fill the trough', 'Meetings sit beside the trough')
R('M4', 'Business events fill the green season', 'Business events can fill the green season')

# M5.
R('M5', 'the six demand-side engagements were proposed for phase 2 (Stakeholder Insights Report, Mar 2026, p16).',
  'the six demand-side engagements were proposed for phase 2 (Stakeholder Insights Report, Mar 2026, p16). [Open item: test the gateway and governance chapters with ACSA, the Cape Town Air Access airline partners, the City of Cape Town and Cape Town Tourism before Steerco.]',
  scope='ch1/04')
R('M5', 'Insights are the project team\'s statements, attributed to the organisation engaged.',
  "Insights are the project team's statements, attributed to the organisation engaged. [Open item: each organisation named in this table to approve its paraphrase before publication.]",
  scope='ch2/04_stakeholders.json:.blocks[22].source')

# M6.
R('M6', '[Supply dataset limits to confirm: neither part of the Infrastructure Report, Jul 2026 (p1 to p114) states that the dataset has no geography below district or that records added after May 2026 are placeholders; the source of this statement is needed.]',
  'The supply dataset behind the Infrastructure Report (Supply_Infrastructure.xlsx) holds no geography below district, and its 17,195 records added after May 2026 are generated placeholders, as the study team found when it checked the file. '
  '[Open item: confirm whether the Infrastructure Report\'s count of 50,332 assets includes those records; if it does, restate Tables 1.4, 2.11 and A.20 and the district shares drawn from them.]')

# M7.
T55 = 'ch5/02_indicators.json:.blocks[5].rows'
R('M7', 'India 71,000; China 29,600 (2025)', 'India 76,547; China with Hong Kong 43,412 (2025, model value)', scope=T55)
R('M7', 'MIDAS, The Indian Market Opportunity; The Chinese Market Opportunity', 'MA p20, p22', scope=T55)
R('M7', '323,971 arrivals (2024); R4.2bn spend (2025)', '292,514 arrivals (2025, model value, regional group); R4.2bn spend (2025)', scope=T55)
R('M7', 'DSA p27, p29', 'MA p20; DSA p29', scope=T55 + '[7]')
R('M7', 'Spend traced to businesses trading inside the 20 shortlisted communities, as a share of foreign direct spend',
  'Spend traced to businesses trading inside the pilot communities, as a share of foreign direct spend; widened to the 20 shortlisted communities once a source covers them')
R('M7', 'Routes above 80% load', 'Seats added on routes above 80% load', n=2, scope=['ch5/02_indicators.json:.blocks[5].rows[9][1]', 'appendices/08_a8_toolkit.json:.blocks[4].rows[9][1]'])
R('M7', '11 of 27 (year to Nov 2025)', '11 routes above 80% (year to Nov 2025); seats added from the capacity-against-demand model (I6)')
R('M7', 'T2-10 routes above 80% load', 'T2-10 seats added on full routes', n=2, scope=['ch3/21_fa07.json', 'ch4/03_charters.json'])
R('M7', 'T2-10 routes above 80% load', 'T2-10 seats added on full routes', scope='ch5/01_results_chain.json', kind='Consequential',
  note='Third match of the find, in Table 5.2 (p147), which the brief does not list; the indicator is renamed there to match.')
R('M7', 'Re-score in 2029 and 2032',
  "Re-score in 2029 and 2032 [Open item: publish the scoring formula before the 2029 re-score; the Infrastructure Report's overall ratings are judgement-based (Appendix A4).]",
  scope='ch5/04_data.json:.blocks[4].rows[4]')
INS('M7', 'Twenty-five Tier 2 indicators give each focus area one or two outcome measures',
    [{'type': 'p', 'text': 'The seven without a baseline are T2-04, T2-18, T2-20, T2-21, T2-23, T2-24 and T2-25. Each carries no target until its baseline exists, on the dates in Table 5.9.'}],
    scope='ch5/02', note='Baseline column checked: the seven are those the brief names. The dated-gaps table is Table 5.9 in the report (the brief calls it Table 5.8).')

# M8.
FA13_OLD = "Twenty communities hold 18.4% of the province's residents but a traced 0.02% to 0.04% of foreign direct spend, and in eleven the binding constraint is organisation, not distance or product."
FA13_NEW = "Twenty communities hold 18.4% of the province's residents but receive only a small documented share of foreign direct spend, and in eleven the binding constraint is organisation, not distance or product."
R('M8', FA13_OLD, FA13_NEW, n=2)
R('M8', '0.02% to 0.04% (floor)', 'R4m to R10m a year (documented floor)', scope='exec/01_summary.json:.blocks[31].rows')
INS('M8', 'The shortlisted communities sit close to visitors but earn almost nothing from them',
    [{'type': 'p', 'text': '[Open item: the Inclusion Plan to set out how the R4m to R10m floor was traced.]'}], scope='ch3/31')
R('M8', 'Distance is the binding constraint in none of the 20 (p30).',
  'Distance is the binding constraint in none of the 20 (p30). Proximity and access carried 35% of the shortlist score (Table A.21), so this result is partly built into the selection.')
R('M8', 'Archetypes abbreviated: N = near a node (45 minutes or less); R = remote; A = assets underused; 0 = no community-based product.',
  'Archetypes abbreviated: N = near a node (45 minutes or less); R = remote; A = assets underused; 0 = no community-based product. [Open item: re-measure Metro travel times to a visitor node such as the V&A Waterfront or the CBD, not CTIA.]')
R('M8', 'Walter Sisulu Square cost R160 million to R180 million before an operator was in place',
  'Walter Sisulu Square cost R160 million to R180 million, out of the R436 million first allocated to Kliptown (section 2.6), before an operator was in place')

# M9.
R('M9', 'Set up a public-private air access fund for route support, on the Chilean model',
  "Scale and ring-fence Cape Town Air Access's route fund as a public-private fund for route support, with a set size and governance", n=2)
R('M9', 'Set up the public-private air access fund with ring-fenced corridor budgets (focus area 7)',
  "Scale Cape Town Air Access's route fund into the public-private air access fund, with ring-fenced corridor budgets (focus area 7)", n=2,
  note='Found twice: p103 and its verbatim copy in Appendix A7 (p186). Applied to both, as the brief pairs the Chapter 3 and A7 pages for every other A7 action it changes.')
R('M9', 'The required change for the Western Cape is a permanent, well-funded public-private air access fund and active lobbying for air service liberalisation (p28).',
  'For the Western Cape the lesson splits by tier. The province can scale its existing route fund; open skies and private airport finance are national levers, so this report carries them in the escalation agenda (focus area 19). '
  "Chile's 2024 surge also came mostly overland: land borders carried 55.6% of arrivals and Argentina about 40% (Sernatur, Anuario de Turismo 2024, Dec 2025).")
R('M9', 'The air access fund draws public and private money on the Chilean model (I6; Global Benchmarking Report, Mar 2026, p28).',
  "The air access fund scales Cape Town Air Access's existing route fund with public and private money (I6).")
R('M9', 'Rand band to be set (section 4.6).', 'Rand band to be set (section 4.6). [Open item: Air Access to give the current size and funders of its route fund.]',
  scope='ch4/03_charters.json:.blocks[21].rows[9]')

# M10 (D9).
R('M10', 'George as second gateway', 'George for domestic connections', n=2)
R('M10', 'and from George, whose terminal doubles by 2028 (focus areas 5, 6 and 7)', 'and, for domestic connections, from George, whose terminal doubles by 2028 or 2029 (focus areas 5, 6 and 7)')
R('M10', 'George, above its design limit at 911,000 passengers in 2025, doubles by 2028 (p104, p105)',
  'George, above its design limit at 911,000 passengers in 2025, doubles by 2028 or 2029, with construction from October 2026 (p104, p105; George Herald, Jul 2026)')
R('M10', 'George, domestic only, doubles by 2028', 'George, domestic only, doubles by 2028 or 2029')
R('M10', 'doubles it to about 2 million by 2028', 'doubles it to about 2 million by 2028 or 2029')
R('M10', 'George to about 2m by 2028', 'George to about 2m by 2029')
R('M10', 'terminal doubles capacity by 2028', 'terminal doubles capacity by 2028 or 2029')
R('M10', 'George R310m by 2028', 'George R310m by 2029')
R('M10', 'George is solved by 2028 (R310m, to about 2m passengers)', 'George doubles by 2028 or 2029 (R310m, to about 2m passengers)')

# M11. Six of the existing ten confirmed outside Wesgro's control (see change log), so ten of fourteen.
ROWADD('M11', 'could move the plan off its path', [
    ['Gulf hub disruption cuts connecting capacity', 'Hub routes carry 53% of arrivals on the ten largest routes (DSA p13)', 'Medium', 'High',
     'Spread hub-carrier work across Dubai, Doha, Addis Ababa and Istanbul; keep direct-route cases ready (I4, I6)', 'Air Access'],
    ['A downturn in the core markets', 'The UK, Germany and the USA supply 52% of overseas arrivals (DSA p13)', 'Medium', 'High',
     'Rebalance activation towards Africa and the hub markets (I1, I4, I5)', 'Destination Marketing'],
    ["Wesgro's operating budget is cut", "Thirteen initiatives draw mainly on Wesgro's operating budget (Table 4.5)", 'Medium', 'High',
     'Rand bands and a stop list agreed with DEDAT before Gate 1 (Decision 3)', "Wesgro CEO's office; DEDAT"],
    ['Resident pushback in the Metro', "Public debate on locals' costs and access (Hypertext, Apr 2026)", 'Medium', 'Medium',
     'Spread visitors in time and space (I2, I8, I9); track resident sentiment', 'City of Cape Town; Cape Town Tourism'],
])
R('M11', "Six of the ten material risks sit outside Wesgro's control", "Ten of the fourteen material risks sit outside Wesgro's control")
R('M11', 'Ten risks could move the plan off its path', 'Fourteen risks could move the plan off its path', kind='Consequential', note='Table 4.7 title count.')
R('M11', 'Current State Diagnostic, Dec 2025 (Diag); Stakeholder Insights Report, Mar 2026 (SIR);', 'Current State Diagnostic, Dec 2025 (Diag); Demand-Side Analysis, Jun 2026 (DSA); Stakeholder Insights Report, Mar 2026 (SIR);',
  scope='ch4/08_risks.json', kind='Consequential', note='Table 4.7 source key gains "DSA", which two new rows cite.')

# M12.
FA6_OLD = "Regional Africa is the province's steadiest volume and its least developed premium market: Zimbabwe and Namibia supply 62% of African arrivals, while Nigerian and Ghanaian visitors spend R31,000 and R27,700 each."
FA6_NEW = "Regional Africa is the province's steadiest volume and its least developed premium market: Zimbabwe and Namibia supply 62% of African arrivals, while West African visitors spend the most per visit."
R('M12', FA6_OLD, FA6_NEW, n=2)
R('M12', 'Regional routes run above 80% load; Nigerian and Ghanaian visitors spend R31,000 and R27,700 each', 'Regional routes run above 80% load; West African visitors spend the most per visit')
R('M12', 'Nigeria R31,000, Ghana R27,700 and Kenya R16,900', 'Nigeria R31,000, Ghana R27,700 and Kenya R16,900 (printed averages; they do not reconcile with the printed totals)', scope='ch3/16_fa06.json')
R('M12', 'Self-catering at 17.4% and guesthouses at 9.7% lead accommodation choice, ahead of hotels at 3.6% (p27).',
  'Self-catering at 17.4% and guesthouses at 9.7% lead accommodation choice, ahead of hotels at 3.6% (p27); together these shares cover under a third of respondents.')
R('M12', 'The only accommodation figure in hand is a demand share: 3.6% of 2024 visitors stayed in hotels, against 17.4% in self-catering (Current State Diagnostic, Dec 2025, p27).',
  'The only accommodation figure in hand is a demand share from the 2024 visitor survey: 3.6% of respondents named hotels and 17.4% self-catering, shares that cover under a third of the sample (Current State Diagnostic, Dec 2025, p27).')
R('M12', 'Cape Town hotel occupancy was 53% in June 2023 (Demand-Side Analysis, Jun 2026, p34).',
  'Cape Town hotel occupancy was 53% in June 2023 (Demand-Side Analysis, Jun 2026, p34). [Open item: Wesgro Research to supply June 2025 occupancy.]')
R('M12', 'Kenya earned about US$1,650 per visitor in 2024 by building conservation and community participation into one governed product system (p32, p33).',
  'Kenya earned about US$1,460 per visitor in 2024 (Demand-Side Analysis, Jun 2026, p15) by building conservation and community participation into one governed product system (Global Benchmarking Report, Mar 2026, p32, p33).')
R('M12', 'Kenya: about US$1,650 per visitor', 'Kenya: about US$1,460 per visitor')
R('M12', 'p32, p56', 'p32, p56; DSA p15', scope=S('ch2/03_benchmarking.json', 'Eight benchmark findings carry into the hypothesis tree', '.rows[7][2]'))

# M13.
M13A = ('The Western Cape can grow international arrivals from about 1.5 million in 2025 to 2.2 million by 2035 on the base path, and to 2.5 million on the accelerated path. '
        'Gateway capacity sets the pace in the summer peak; demand and conversion set it in the green season and beyond the Metro.')
M13B = ('From 1,498,829 arrivals in 2025 the growth model reaches 2,175,778 on the base path and 2,516,282 on the accelerated path in 2035 (Market Assessment Report, May 2026, p19; Demand-Side Analysis, Jun 2026, p20). '
        'International passenger arrivals at Cape Town International, the series ACSA reports, stood at 1.44m in FY24/25 and 1.57m in FY25/26 (Demand-Side Analysis, Jun 2026, p11).')
M13C = ('The study tested an eighteen-entry hypothesis tree against seven deliverables and four working analyses between December 2025 and October 2026. '
        'This report sets out what the evidence found, what Wesgro and its partners should do and how progress will be measured.')


def m13():
    f = 'exec/01_summary.json'
    bl = FILES[f]['blocks']
    assert bl[0]['text'] == 'The case in brief' and bl[1]['text'].startswith('The Western Cape can grow international arrivals from about 1.5 million in 2025')
    assert bl[3]['text'].endswith('stood at 1.44m in FY24/25 and 1.57m in FY25/26 (Demand-Side Analysis, Jun 2026, p11).') and bl[4]['text'] == 'Five constraints cap the case'
    before = ' || '.join(b['text'] for b in bl[1:4])
    bl[1]['text'], bl[2]['text'], bl[3]['text'] = M13A, M13B, M13C
    return f, '.blocks[1] to .blocks[3]', before, ' || '.join([M13A, M13B, M13C])


FN('M13', 'ES opening replaced by the three paragraphs, without "The base path is the plan\'s target and the accelerated path its stretch." because D1 is skipped.', m13)
R('M13', 'The Diagnostic records specific dysfunctions, "SAT is in turmoil" among them, and the added pressure of a lack of fiscal space (Current State Diagnostic, Dec 2025, p58).',
  'Stakeholders described strain at SA Tourism and a lack of fiscal space (Current State Diagnostic, Dec 2025, p58).')
R('M13', 'and the national marketing body is weak, so the province needs one shared agenda with clear decision rights.',
  'and the national marketing body is under strain, so the province needs one shared agenda with clear decision rights.', n=2)

# =====================================================================================================
# P1 to P20 (P6, P8, P10 and P14 are closed by C changes; P1 and P4 also need renderer fixes, P3 a chart option)
# =====================================================================================================


def p2():
    f = 'ch1/03_recovery_to_growth.json'
    i = find_block(f, lambda b: b.get('id') == 'fig_base_case_seat_ceiling')
    b = blk(f, i); fn = b['chart'].pop('footnote')
    before = b['source']
    b['source'] = before + ' ' + fn
    return f, f'.blocks[{i}].source', 'chart footnote: ' + fn, b['source']


FN('P2', 'Figure 1.4 note moved from inside the chart to the end of its source line, wording kept.', p2)


def p3():
    out = []
    for f, fid in [('exec/01_summary.json', 'fig_0_paths'), ('ch1/03_recovery_to_growth.json', 'fig_base_case_seat_ceiling'),
                   ('ch2/01_demand.json', 'fig_21_scenarios'), ('ch5/03_baselines_targets.json', None)]:
        i = find_block(f, (lambda b, fid=fid: b.get('id') == fid) if fid else (lambda b: b['type'] == 'figure' and b.get('chart', {}).get('type') == 'line'))
        ch = blk(f, i)['chart']
        ch['timeAxis'] = True
        fn = ch.get('footnote', '')
        if fn == 'Milestone years only; the intervals are three, three and four years.':
            del ch['footnote']; out.append(f'{f}: footnote removed ("{fn}")')
        out.append(f'{f} block {i}: x positions on calendar years {ch["categories"][0]} to {ch["categories"][-1]}')
    return 'exec, ch1/03, ch2/01, ch5/03', 'chart.timeAxis', 'evenly spaced year points', '; '.join(out)


FN('P3', 'True time axis for Figures ES.2, 1.4, 2.1 and 5.2 (charts.js lineChart timeAxis option); the ES.2 and 5.2 spacing note removed.', p3)


def p4():
    f = 'ch4/02_sequencing.json'
    i = find_block(f, lambda b: b.get('chart', {}).get('type') == 'gantt')
    rows = blk(f, i)['chart']['rows']
    titles = {}
    for b in FILES['ch4/03_charters.json']['blocks']:
        if b['type'] == 'h3' and b.get('text', '')[:1] == 'I':
            code, _, name = b['text'].partition(' ')
            titles[code] = name
    changed = []
    for r in rows:
        full = titles[r['code']]
        assert full.startswith(r['name'].rstrip(',')), (r['name'], full)
        if full != r['name']: changed.append(f'{r["code"]}: "{r["name"]}" to "{full}"'); r['name'] = full
    return f, f'.blocks[{i}].chart.rows[*].name', 'labels cut short in the data', '; '.join(changed)


FN('P4', 'Figure 4.1 labels restored to the full initiative names from the section 4.3 charters; charts.js ganttChart wraps long names to two lines.', p4)


def p5():
    f = 'exec/01_summary.json'
    item1 = '[Summary of Findings, 14 Oct 2026, slides 3 and 4: align these five constraints with the deck\'s own list once the deck is in hand.]'
    item2 = '[Summary of Findings, 14 Oct 2026, pp15 to 16: deck page reference to be confirmed]'
    i = find_block(f, lambda b: b['type'] == 'note' and b['text'] == item1)
    FILES[f]['blocks'].pop(i)
    j = find_block(f, lambda b: b.get('id') == 'fig_0_tree')
    src = blk(f, j)['source']
    assert src.count(' ' + item2) == 1
    blk(f, j)['source'] = src.replace(' ' + item2, '')
    f2 = 'ch1/05_how_to_read.json'
    FILES[f2]['blocks'].append({'type': 'bullets', 'items': [item1, item2]})
    return f + ' and ' + f2, f'{f} .blocks[{i}] deleted; .blocks[{j}].source; {f2} new last block', item1 + ' (ES p13) | ' + item2 + ' (Figure ES.1 source, p14)', 'both items listed at the end of section 1.5'


FN('P5', 'The two ES open items moved, wording kept, to the end of section 1.5 (which has no open-items list).', p5)
R('P7', '+328,805', '+323,805', scope='appendices/02_a2_demand_model.json:.blocks[10].rows')
R('P7', 'The May deck prints Conservative absolute growth of +328,805, but its own end points give +323,805; its 10-year CAGRs do match the end points (computed; Market Assessment Report, May 2026, p19). ', '',
  note='Note on the misprinted value removed; logged under C5 in reconciliation_log.md.')
R('P9', 'and the network averaged 76.0% on the printed total (MIDAS Aviation Market Assessment, Mar 2026, "Seasonality").',
  'and the network averaged 76.0% on the printed total (MIDAS Aviation Market Assessment, Mar 2026, "Seasonality"). MIDAS tables 27 routes for the year to November 2025; 29 serve the airport in 2026.',
  scope='ch1/03')
R('P11', 'New Zealand, Auckland Park', 'New Zealand')
R('P12', 'formalise conservation and community inclusion as part of the tourism value proposition', 'build conservation and community inclusion into the tourism value proposition')
R('P12', 'shortened only by cutting', 'shortened by cutting, with one verb paraphrased', scope='appendices/03_a3_benchmark.json:.blocks[18].source')
R('P15', 'The 2025 ICCA row of 65 covers Stellenbosch and Cape Town and is not comparable.',
  'The 2025 ICCA row of 65 covers Stellenbosch and Cape Town and is not comparable. [Open item: Wesgro Convention Bureau to confirm the 2023 ICCA count (46 printed; Wesgro reported 42 in May 2025) and reconcile the yearly total of 137 with the 136 monthly records.]',
  scope='ch3/12_fa02.json:.blocks[9].source')
R('P16', 'building on the 2024 Ghana visa waiver', 'building on the Ghana visa waiver of November 2023', n=2)
R('P16', 'The 2024 Ghana visa waiver drove 36,656 arrivals to South Africa', 'Ghanaian arrivals reached 36,656 in 2024, the first full year of the visa waiver that took effect on 1 November 2023')
R('P17', 'Escalate the cap on US carriers, the unsigned Open Skies agreement and the bilateral agreements that limit airlift',
  'Escalate the cap on US carriers, the absence of an Open Skies agreement and the bilateral agreements that limit airlift', n=2)
R('P18', 'National Treasury Circular 131', "National Treasury's MFMA Circular No. 131 of 31 March 2025", scope='ch2/04_stakeholders.json:.blocks[14]')
R('P18', 'National Treasury Circular 131', 'MFMA Circular No. 131', scope='ch2/04_stakeholders.json:.blocks[22]')
R('P18', 'Treasury Circular 131', 'MFMA Circular No. 131', n=8)
R('P19', 'about 1.5 million international tourist arrivals in 2025, an 11.1% increase (Hypertext, Apr 2026, reporting the Provincial Minister; public source)',
  '1,538,142 international tourist arrivals in 2025, an 11.1% increase (Wesgro Research, Western Cape Tourism Performance: Annual 2025, from SA Tourism data; public source)')
R('P19', ' [Wesgro Research to confirm the 2025 SAT figure and the series behind it.]', '')
R('P19', 'About 1.5m', '1,538,142', scope='ch1/01_mandate.json:.blocks[29].rows[4][0]')
R('P19', 'Hypertext, Apr 2026, reporting the Provincial Minister; public source', 'Wesgro Research, Western Cape Tourism Performance: Annual 2025; public source', n=2,
  scope='ch1/01_mandate.json:.blocks[29]', note='Table 1.2 row source and the table\'s source list (p26).')
R('P19', ' [Wesgro Research to confirm the figure and its series]', '', scope='ch1/01_mandate.json:.blocks[29].rows[4]', note='Same open item as the one deleted from the paragraph.')
R('P20', "De Rust's pass-through trade cut", "De Rust's pass-through trade cut; a temporary one-lane reopening is targeted for December 2026")
R('P20', 'SCIP p24', 'SCIP p24; Western Cape Government, Jul 2026', scope='ch3/32_fa14.json:.blocks[8].rows[2]')

# Sources table (A9).
ROWADD('Sources', 'Twelve study documents, six public and reference sources', [
    ['Western Cape Tourism Performance: Annual 2025', 'Wesgro Research (SA Tourism data)', '2026', 'Public source'],
    ['Q1 2026/27 performance presentation to the Portfolio Committee on Transport, as reported by Travel News', 'ACSA', 'August 2026', 'Public source'],
    ['Parliamentary reply on Cape Town International runway capacity', 'Minister of Transport', 'April 2025', 'Public source'],
    ['Anuario de Turismo 2024', 'Sernatur, Chile', 'December 2025', 'Public source'],
    ['Singapore achieves historical high in tourism receipts in 2024', 'Singapore Tourism Board', 'February 2025', 'Public source'],
    ['World Tourism Barometer', 'UN Tourism', 'January 2025 and January 2026', 'Public source'],
    ['George Airport expansion reporting', 'George Herald', 'July 2026', 'Public source'],
    ['Meiringspoort temporary reinstatement', 'Western Cape Government', 'July 2026', 'Public source'],
    ['Kenya 2024 tourism performance, as reported', 'The Star (Kenya)', 'May 2025', 'Public source'],
], after_cell0='Western Cape tourism is booming, but can locals afford to enjoy it?', note='Placed after the existing public sources and before the SLA row; the brief\'s "Type" is the table\'s Status column.')
R('Sources', 'Twelve study documents, six public and reference sources and one deck not yet in hand support the report.',
  'Twelve study documents, fifteen public and reference sources and one deck not yet in hand support the report.')
R('Sources', 'nineteen documents', 'twenty-eight documents')

# =====================================================================================================
if BLOCKED:
    print(f'{len(BLOCKED)} BLOCKED:')
    for b in BLOCKED: print('  ', b['id'], f'expected {b["expected"]} found {b["found"]}:', b['find'][:110], b['where'])
print(f'{len(LOG)} edits logged')
if not DRY:
    for f, d in FILES.items():
        with open(os.path.join(C, f), 'w') as fh:
            json.dump(d, fh, indent=1, ensure_ascii=False); fh.write('\n')
    json.dump({'log': LOG, 'blocked': BLOCKED}, open(os.path.join(HERE, 'applied.json'), 'w'), indent=1, ensure_ascii=False)
