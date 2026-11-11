"""Lead editor's targeted edits for the update pass -> work/store.json"""
import sys
sys.path.insert(0, '/tmp/claude-0/-home-user-Letsema/98b96bfe-2843-55b4-9fb2-4f4083c56589/scratchpad/s16')
from stp import *
d = Doc(); store = {}
def cur(pid): return store.get(pid, marked_plain(d.P(pid)))
def sub(pid, old, new, n=1):
    t = cur(pid)
    if old not in t: print('MISS', pid, old[:50]); return
    store[pid] = t.replace(old, new, n)
# ---- C1 balance
sub('14B01311', 'Reaching it depends first on turning interest into visits, and then on seats at the summer peak.',
    'Reaching it depends on all three goals: reshaping demand so that interest converts into visits, transforming supply so that seats, reach and product can carry the growth and building the enabling capability that sustains both. The key constraints are conversion and seat capacity at the summer peak.')
sub('37A136E5', 'Reaching 2.5 million arrivals by 2035 depends on conversion work that starts in 2027 and on seats held on the full routes until the runway brings relief.',
    'Reaching 2.5 million arrivals by 2035 depends on conversion work that starts in 2027, on seats held on the full routes until the runway brings relief and on the shared decisions, capital and data that sustain both.')
sub('732A8E88', 'Reaching it depends first on converting interest into visits, and then on seats at the summer peak.',
    'Reaching it depends on action across demand, supply and enablement. The key constraints are the conversion of interest into visits and seat capacity at the summer peak.')
sub('0FC1C520', 'why the step from recovery to growth depends on conversion.', 'why the step from recovery to growth turns on conversion and on seats at the peak.')
sub('59FA2459', 'Conversion comes first, and seats pace growth at the peak. The base case holds',
    'Growth to 2.5 million rests on all three goals: demand that converts, supply that can carry and deliver it and the enabling capability that sustains both. Conversion and seat capacity at the peak are the constraints that bind first. The base case holds')
# ---- C2 phrasing (and C3 in the same sentences)
sub('560EEDA1', 'The premium rests on a few markets, six months and one metro. Five markets supply 63% of overseas arrivals, and the UK,',
    'The premium rests on a few mature markets, the peak season and the Cape Town Metro. Five markets supply 63% of overseas arrivals. The UK,')
sub('270298CD', 'rests on five source markets, six summer months and one metro.', 'rests on a few mature markets, the peak season and the Cape Town Metro.')
sub('5339A390', 'The premium rests on five markets, six summer months, one gateway and one metro.', 'The premium rests on a few mature markets, the peak season, one gateway and the Cape Town Metro.')
sub('45850C74', 'Five markets', 'Mature markets'); sub('3BC87C17', 'Six summer months', 'Peak season'); sub('19EF77C3', 'One metro', 'Cape Town Metro')
sub('17B42456', 'About one in seventy interested high-value travellers arrives, and six barriers stand between interest and a visit. Seats pace growth at the summer peak, and five markets and six months carry most overseas visits. Beyond the Metro, visitors who will not drive find little they can reach, and in townships and rural settlements the missing piece is a local seller.',
    'About one in seventy interested high-value travellers arrives and six barriers stand between interest and a visit. Seats pace growth at the summer peak. A few mature markets and the peak season carry most overseas visits. Beyond the Metro, visitors who will not drive find little they can reach. In townships and rural settlements the missing piece is a local seller.')
sub('4DDB063F', 'concentrated in five markets and six months', 'concentrated in a few mature markets and the peak season')
sub('0626DEBE', 'Six summer months, October to March, carry', 'The peak season, October to March, carries')
sub('3A936115', 'Five markets dominate', 'A few mature markets dominate')
# ---- C5 outcomes, not actors
sub('6D96A107', "In the first half of 2027 Wesgro convenes each initiative's stakeholders and, with the Department of Economic Development and Tourism (DEDAT), formalises the Unlocking Tourism Growth Steerco. It then tables the first national escalation agenda and agrees the data-sharing protocol.",
    "By mid-2027 the stakeholder agreements for each initiative, a formal Unlocking Tourism Growth Steerco, a first national escalation agenda and an agreed data-sharing protocol are in place.")
sub('6D96A107', 'It takes direct route cases to carriers as the international terminal', 'Direct route cases go to carriers as the international terminal')
sub('693DCFF8', "Phase 1 works inside Wesgro's mandate and budget and on the levers that move before the airport can. Wesgro first convenes each initiative's stakeholders and agrees roles and accountabilities with them in 2027 (section 4.4).",
    "Phase 1 works on the levers that move before the airport can, inside existing mandates and budgets. Stakeholder agreements on roles and accountabilities are in place for each initiative in 2027 (section 4.4).")
sub('693DCFF8', 'The Cape Town Air Access partnership is re-termed with its partners to hold', 'The Cape Town Air Access partnership is re-termed to hold')
sub('3E05BFFC', 'Air Access completes correlated hub-closure scenarios (I6). Two flow pilots run with the site operators, at Boulders',
    'Correlated hub-closure scenarios are complete (I6). Two flow pilots run, at Boulders')
sub('3E05BFFC', 'The safety workstream agrees one referral pathway and tests its handoffs, and the visa ask is rebuilt on ETA performance (I17).',
    'One referral pathway across the safety services is agreed and its handoffs tested. The visa ask is rebuilt on ETA performance (I17).')
# ---- C8
sub('54AEAF81', 'comprises overlapping workstreams', 'comprises connected workstreams')
sub('03022E19', 'the three local or district tourism bodies overlap the p16 supply-side entry', 'the three local or district tourism bodies are also counted in the p16 supply-side entry')
sub('4FA44752', 'The entry for district tourism offices overlaps the Mossel Bay,', 'The entry for district tourism offices takes in the Mossel Bay,')
# ---- C3/C7 in the summary, Chapter 1 and the Chapter 2 opening
sub('22BFA5FA', 'against the required path, and a terminal evaluation', 'against the required path and a terminal evaluation')
sub('34C853C6', 'gives this plan its policy foundation, and its emphasis on', 'gives this plan its policy foundation. Its emphasis on')
sub('1159A7F9', '15.4% more than in 2024, and spent 14.3 million bed nights', '15.4% more than in 2024. They spent 14.3 million bed nights')
sub('1159A7F9', 'below the start of 2020, and provinces such as', 'below the start of 2020. Provinces such as')
sub('45B0F3DE', 'carry regional and local content, and DEDAT', 'carry regional and local content. DEDAT')
sub('5986B757', 'describe the system, and this chapter', 'describe the system and this chapter')
save_store(store)
print(len(store), 'paragraphs in the lead editor store')
for pid, t in store.items():
    if re.search(r', (and|or)\b', t): print('STILL', pid, re.findall(r'.{30}, (?:and|or)\b.{20}', t))
