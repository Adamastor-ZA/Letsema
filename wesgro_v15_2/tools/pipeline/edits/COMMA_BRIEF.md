# Brief: remove ", and" from one part of a report

You are making ONE kind of change to one part of a long report ("Unlocking Tourism Growth: An Action Plan for the Western Cape to 2035"). The author has ruled: **no comma before "and", anywhere**, and no serial comma before "or". Change nothing else. Do not use the web. Do not send content to any outside service. Edit no file except your own output file.

## What to do

Your part is in `work/dump_NAME.txt`. Each line is `[paraId|Style] text`; table cells are indented under `<table>`. Find every `, and` and every `, or` and recast the sentence so the comma construction is gone. Choose the lightest fix that reads well:

1. **A list** ("A, B, and C"; "A, B, or C"): drop the comma. "A, B and C".
2. **Two full clauses joined by ", and"** (each has its own subject and verb): make two sentences. Start the second with its own subject. If the second clause opens with a pronoun that would be unclear on its own, repeat the noun instead; add no other words.
   - Before: "Five markets supply 63% of overseas arrivals, and the UK, Germany and the USA alone account for 52%."
   - After: "Five markets supply 63% of overseas arrivals. The UK, Germany and the USA alone account for 52%."
3. **Short, tightly bound clauses, or a second verb sharing the subject**: just drop the comma, if the sentence stays clear and under 35 words.
   - Before: "A mid-term review in 2030 tests seat growth against the required path, and a terminal evaluation reports in 2035."
   - After: "A mid-term review in 2030 tests seat growth against the required path and a terminal evaluation reports in 2035."
4. **The comma closes an inserted phrase** ("X, which does Y, and Z"; "In 2025, 4 million trips, 15% more than in 2024, and ..."): recast. Split into two sentences, or move the inserted phrase, or put it in brackets. Do not leave a dangling phrase.
5. **A semicolon** is allowed where two short, balanced halves belong together, but use it sparingly; prefer rule 2.
6. **", or" meaning "that is"** ("1,216,601, or 63.7%"): use brackets: "1,216,601 (63.7%)".

## What not to do

- Change no other wording. No synonyms, no reordering beyond what the comma fix needs, no tidying. A reviewer will see each change as a tracked change and must be able to tell at once that it is only the comma fix.
- Change no number, date, name, percentage or source. Keep every footnote marker `[^123]` exactly where it attaches. Keep `**bold**` markers and any `[[QUERY ...]]` text exactly.
- Never start a sentence with "And". No dashes. No sentence over 35 words.
- Do not touch headings or captions.
- If the ", and" sits inside a quoted title, a proper name or a quotation, leave it and list the paragraph under "exceptions" with the reason.

## Output

Write `work/commas_NAME.json`:

```json
{
  "rewrites": {"4DDB063F": "The whole paragraph or cell as it should now read."},
  "exceptions": {"0A1B2C3D": "why this one keeps its comma"},
  "log": ["short notes for the lead editor"]
}
```

Every paragraph and cell in your part that contains `, and` or `, or` must appear in `rewrites` or in `exceptions`. Give the full text of each rewritten paragraph. Include nothing you did not change.

Check your file and fix every ERROR (read the WARN lines too):

`cd /tmp/claude-0/-home-user-Letsema/98b96bfe-2843-55b4-9fb2-4f4083c56589/scratchpad/w16 && python3 ../s16/u_check.py work/commas_NAME.json SECTIONS`

All `work/` paths are under `/tmp/claude-0/-home-user-Letsema/98b96bfe-2843-55b4-9fb2-4f4083c56589/scratchpad/w16/`. A quick way to list your targets: `grep -n ', and\|, or' work/dump_NAME.txt`. Work through them in order; there are several hundred in some parts, so write the JSON with a script or in batches and run the checker as you go. Finish only when the checker prints RESULT: OK.
