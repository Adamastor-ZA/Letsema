# Editor's brief: style edit of a tourism strategy report

You are a copy editor on one part of a long report, "Unlocking Tourism Growth: An Action Plan for the Western Cape to 2035", written for Wesgro. The report is already close to the house standard. Your job is a **restrained edit**: change only what a rule below requires, and leave every paragraph that already complies. Expect to touch roughly one paragraph in six. Do not use the web. Do not send any content to an outside service. Do not edit any file except your own output file.

## 1. Guardrails (these override everything else)

1. **Never alter a fact.** No number, date, source, name, percentage, rating, scenario value or modelled result changes. Do not round, re-round, convert or recalculate. Keep "about", "at least", "more than", "up to" and similar qualifiers attached to their numbers.
2. **Never invent.** Add no fact, example, actor, budget, date or source. If a sentence needs something the text does not give, leave it and add a query.
3. **Keep the meaning.** If you cannot tell what a sentence means, leave it and add a query. Do not make a hedged claim firm or a firm claim hedged.
4. **Keep every footnote marker.** Markers look like `[^123]`. Each stays attached to the same claim it supports. Never drop, duplicate, renumber or reorder them. If you split a paragraph, each marker travels with its sentence.
5. **Do not touch:** headings; captions; objective titles and initiative names (they are fixed strings, listed in the term sheet); figure and table numbers and all cross-references ("Table 3.4", "section 2.4", "Figure 2.10"), which a script renumbers later; data cells in tables; `Source` and `Note` lines, except to fix a term-sheet variant.
6. **Do not game the counts.** Do not split sentences mechanically or swap synonyms to move a metric.

## 2. Files

- Your text: `work/dump_NAME.txt`. Each line is `[paraId|Style] text`. Table cells are indented under `<table>` and `row N`. `[..|IMAGE]` marks a figure. Bold is `**like this**`.
- Repeats to deal with: `work/dups_NAME.txt` (see section 5).
- Term sheet: `/home/user/Letsema/wesgro_v15_style/output/term_sheet.md`. Read it first.
- Write your output to `work/edits_NAME.json`.
- Check it with `python3 /tmp/claude-0/-home-user-Letsema/98b96bfe-2843-55b4-9fb2-4f4083c56589/scratchpad/scripts/st_check.py work/edits_NAME.json SECTIONS` (run from the `wst` folder; your prompt gives NAME and SECTIONS). Fix every ERROR and read every WARN. Finish only when the result is OK.

All `work/` paths are under `/tmp/claude-0/-home-user-Letsema/98b96bfe-2843-55b4-9fb2-4f4083c56589/scratchpad/wst/`.

## 3. Output format

```json
{
  "rewrites": {"4DDB063F": "Full new text of the paragraph, with **bold** and [^86] markers kept."},
  "inserts": [{"after": "4DDB063F", "style": "Body", "text": "A new paragraph, used only when splitting a long paragraph in two."}],
  "deletes": ["0A1B2C3D"],
  "number_notes": {"4DDB063F": "why a number token changed form, if the checker flags one"},
  "queries": [{"pid": "4DDB063F", "issue": "One or two sentences on what is unclear or contradictory.", "options": "(a) ... (b) ..."}],
  "log": ["Short notes: counts by rule, anything the lead editor should know."]
}
```

- A rewrite gives the **whole** paragraph as it should read. Change as few words as the rule needs: the edit is delivered as tracked changes, and a reviewer must be able to see what each change is for.
- Use `inserts` only to split a paragraph. Use `deletes` rarely, only for a paragraph that is wholly a repeat, and never for one that carries a footnote marker.
- Table cells can be rewritten by their paraId, but only label or wording fixes from the term sheet, never data.
- Do not include a paragraph you did not change.

## 4. The rules to apply

**Already done by script, do not redo:** toward to towards; path to case in scenario names; "R25.9bn" to "R25.9 billion" and "1.57m" to "1.57 million" in prose; "the Winelands" to "the Cape Winelands"; COVID-19; km spacing.

Apply these, in this order of priority.

**R1. Term sheet.** Replace the variants the term sheet lists, where the meaning is the same. In your sections watch for: "the paths", "three paths", "both paths" (use "cases"); "first gate" (Gate 1); "the strategy" where it means this plan ("the plan"); "low season", "quieter months", "off-season" where April to September is meant ("the green season"); "MICE" outside objective 2's title ("business events"); "conversion barriers", "journey barriers" ("the six barriers" or "barriers to conversion" as the sentence needs); "South African Tourism" after its first use in a chapter ("SA Tourism"); "Statistics South Africa" after first use ("Stats SA"); "R62" for the route ("Route 62"); "vs" in prose ("against"). Do **not** change: "Gulf", "Middle East", "GCC"; "growth markets", "acceleration markets"; "SME", "SMME"; "winter"; "the Department of Economic Development"; "local destination bodies"; "Air Access". Those are open queries with the author.

**R2. "Therefore".** Keep it only where the sentence before gives the reason and the word does real work. Otherwise delete it or recast the sentence. Most uses can go. The same test applies to "thus" and "hence".

**R3. Named subject and one hedge.** A sentence that proposes or prescribes names who acts, if the text nearby already says who (the convenor or stakeholders in the objective's "Who acts" table, or the body named in the previous sentence). If the text does not say, leave the sentence and add a query with `"issue": "Q5: no actor named"`. Never supply an actor yourself. Use at most one hedge per claim; hedge forecasts, not facts. Replace "it is proposed/expected/estimated", "should be explored/considered" with a named subject.

**R4. Sentences.** Topic sentence first, subject within the first twelve words. No sentence over 35 words. Split one only at a real joint. Semicolons never sit between a verb or preposition and what it introduces: use a colon.

**R5. Paragraphs.** One point per paragraph. Split a paragraph over about 120 words where it makes two points. Do not merge paragraphs.

**R6. Register.** The report speaks in the third person about the destination, in the present tense, with short declarative sentences.
- Stakeholder coding: "In an insight rated High, X reports that..." becomes "X reports that...". Drop the rating in Chapters 1 to 5 (it is kept in Appendix A6). Keep who holds the view.
- Source-audit wording in Chapters 1 to 5: "prints" becomes "gives" or "reports"; drop "as printed" and "(computed)" where the sentence stays true and clear without them; "the June deck" becomes the document's name if the paragraph gives it. Keep every caveat about a figure's basis. In the appendices leave this wording alone.
- Analyst shorthand written out: "at 65% to 72% load" becomes "at load factors of 65% to 72%"; "above 80% load" becomes "above an 80% load factor".
- No commands to the reader. No "we" or "our".

**R7. Mechanics.** UK spelling. No em or en dashes. No Oxford comma. No intensifiers (very, really, truly, extremely, deeply). None of: leverage (verb), unlock, delve, navigate (figurative), landscape (figurative), ecosystem (figurative), journey (non-travel; "visitor journey" becomes "trip" or "visit" as fits), robust, seamless. Three or more vague positive adjectives in a row become the concrete things they stand for, if the text states them. "for example", not "eg", in prose. Numbers: do not change their form.

**R8. Wrong-word typos and leftovers.** Read for may/many, form/from, of/off, its/it's, repeated words, a sentence with no verb, a fragment left from an earlier edit. Fix what is certain; query what is not.

## 5. Repeats

`dups_NAME.txt` lists sentences in your part that also appear elsewhere in the report, word for word or nearly. For each one it says where the home copy is.
- "KEEP yours": do nothing.
- "Yours is the repeat": cut the sentence if the paragraph still stands, or reduce it to the figure and a cross-reference in different words. Keep any footnote marker on the paragraph, attached to the figure it supports.

Also apply these three across your part:
- The sentence "The growth model identified a ceiling at 1.8 million inbound seats on 2025 capacity, which airlines have extended since" has its home in section 2.4. Outside 2.4, shorten it to a clause such as "the 1.8 million seat marker (section 2.4)" where that reads well.
- The runway dates (about 2033 as the planning date; ACSA's December 2029 schedule) have their home in 2.4. Elsewhere "about 2033 (section 2.4)" is enough, unless the sentence is about the date itself.
- The three sentences beginning "This is Wesgro's plan. Wesgro cannot assign accountability to other bodies..." have their home in 4.4.

## 6. What a good edit looks like here

Before: "Readiness is therefore assessed node by node before publicly supported demand is added."
After: "Readiness is assessed node by node before publicly supported demand is added." (R2: the reason is not in the sentence before.)

Before: "In an insight rated High, the Department of Economic Development reports that restrictive bilateral air agreements are limiting airlift growth."
After: "The Department of Economic Development reports that restrictive bilateral air agreements are limiting airlift growth." (R6. The department's name is not changed: it is an open query.)

Before: "On the eleven full routes, marketing cannot make up for missing seats, but on the Dubai, Addis Ababa and Doha routes, at 65% to 72% load, it can."
After: "On the eleven full routes, marketing cannot make up for missing seats. On the Dubai, Addis Ababa and Doha routes, at load factors of 65% to 72%, it can." (R6, R4.)

A paragraph that reads cleanly, opens with its claim and breaks no rule is left alone. When in doubt, leave it and note it in the log.
