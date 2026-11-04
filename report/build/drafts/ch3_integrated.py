"""Chapter 3, section 3.4 The integrated case. Writes content/ch3/40_integrated.json.
Sources: Demand-Side Analysis p19 to p21 (scenario matrix, end points, seat ceiling), Market Assessment p19 (2025 base),
Infrastructure Report p103 (CTIA relief dates), MIDAS In Conclusion; discrepancies.md A2.7, B10."""
from ch3_lib import write

blocks = [
    {"type": "pagebreak"},
    {"type": "h2", "text": "3.4 The integrated case"},
    {"type": "lead", "text": "The three pillars make one case. Demand work fills seats only if the seats exist, supply work pays only if the product can be booked, and both need the enabling base to last."},
    {"type": "p", "text": "The growth model sets out three paths from the 2025 base of 1,498,829 arrivals: 1,822,634 in 2035 on the conservative path, 2,175,778 on the base path and 2,516,282 on the accelerated path (Market Assessment Report, May 2026, p19; Demand-Side Analysis, Jun 2026, p20). The deck is explicit that the paths differ by intervention, not by demand potential (Demand-Side Analysis, Jun 2026, p19). Each step up the case therefore rests on a set of moves, and the table below maps each set to the focus areas that deliver it."},
    {"type": "table", "caption": "Each step of the growth case rests on a named set of interventions, and each set draws on focus areas in all three pillars.",
     "source": "Demand-Side Analysis, Jun 2026, p19 (assumptions) and p20 (2035 end points); Market Assessment Report, May 2026, p19 (2025 base). Increments between paths are computed from the printed end points. The mapping to focus areas is this report's.",
     "columns": [
         {"header": "Path", "width": 1.2, "align": "left"},
         {"header": "Arrivals in 2035", "width": 1.4, "align": "right"},
         {"header": "What the model assumes", "width": 3.6, "align": "left"},
         {"header": "Focus areas that deliver it", "width": 1.6, "align": "left"},
     ],
     "rows": [
         ["Conservative", "1,822,634", "Existing air access held with no added frequencies or routes; continued trade and marketing; growth in the mature markets and current corridors", "5 and 7 hold the base"],
         ["Base", "2,175,778 (+353,144)", "Emirates, Qatar, Ethiopian and Turkish Airlines add frequency and capacity; existing Wesgro programmes expand; India, China and regional Africa grow through hub connections", "1 to 7, 9 and 10"],
         ["Accelerated", "2,516,282 (+340,504)", "Direct India and China routes secured; dedicated activation in India, China, the USA and the GCC; India, China and the Middle East grow ahead of their source markets", "4, 7, 16 and 19, on top of the base"],
     ], "boldFirstCol": True},
    {"type": "p", "text": "**The gateway binds first.** Current air access places a hard ceiling at 1.8 million inbound seats, and the base case passes it at the 2030 year point (Demand-Side Analysis, Jun 2026, p21). Relief at Cape Town International arrives about 2032 for the international terminal and about 2033 for the runway (Infrastructure Report, Jul 2026, p103). Between those dates, growth has to come from larger aircraft and added frequency on the full routes, from hub-carrier capacity and from George, whose terminal doubles by 2028 (focus areas 5, 6 and 7)."},
    {"type": "note", "text": "The deck draws arrivals and seats against one axis and prints no seat table behind the 1.8 million line. The crossing year is read from the chart: after the 2028 point (1,673,855) and by the 2030 point (1,802,929)."},
    {"type": "p", "text": "**If the supply moves slip, the case stops at the ceiling.** The deck states that the projected growth cannot be realised without additional capacity or frequency (Demand-Side Analysis, Jun 2026, p21), and that without confirmed routes the accelerated case reverts to base (p20). Demand work cannot make up the gap, because marketing into full routes raises fares rather than seats (MIDAS Aviation Market Assessment, Mar 2026, In Conclusion)."},
    {"type": "p", "text": "**Below the gateway, the pillars depend on each other.** Green-season demand needs seats in the months carriers now cut (focus areas 2 and 7). Dispersal needs product that can be booked and reached (focus areas 3, 9 and 10). Inclusion needs a seller and a safe visit before exposure (focus areas 13 and 19). Every target needs data that today sits with SA Tourism, ACSA and the booking platforms (focus area 18)."},
    {"type": "p", "text": "**Air access and bookability move first, because every other lever runs through them.** The table below sets the order. Chapter 4 turns it into eighteen initiatives with owners, phases and decision gates."},
    {"type": "table", "caption": "The first phase works the seats and the booking path before the base case reaches the seat ceiling, and the direct routes wait for runway relief.",
     "source": "Chapter 3 entries 1 to 20; phase years as set in section 4.2; seat ceiling from Demand-Side Analysis, Jun 2026, p21; airport relief dates from Infrastructure Report, Jul 2026, p103.",
     "columns": [
         {"header": "Phase", "width": 1.4, "align": "left"},
         {"header": "What moves (focus areas)", "width": 4.0, "align": "left"},
         {"header": "Why then", "width": 2.4, "align": "left"},
     ],
     "rows": [
         ["Activate, 2027 to 2028", "Seats held and added on full routes (5, 6, 7); green-season calendar (2); bookability census and onboarding (3); two or three inclusion pilots (13); Steerco, data protocol and escalation agenda (16, 18, 19); labour analysis commissioned (20)", "Before the base case reaches the seat ceiling at the 2030 point"],
         ["Expand, 2029 to 2031", "Hub conversion at scale (4); corridor product and mobility (9, 10); quality charter (11); flagship flow management (12); cruise product (8); investment pipeline at financial close (15)", "The 2030 mid-term review tests the ceiling; terminal relief from about 2032"],
         ["Sustain, 2032 to 2035", "Direct India and China routes as runway capacity arrives (4, 7); inclusion scaled after thresholds are met (13); climate risk and LTO funding embedded (14)", "Runway relief about 2033; the accelerated case depends on direct routes"],
     ], "boldFirstCol": True},
]
write("40_integrated.json", "3.4", "The integrated case", blocks)
print("3.4 written")
