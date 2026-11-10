#!/usr/bin/env python3
"""style_metrics.py: house-style and editorial metrics for long-form strategy reports.

Usage:
  python3 style_metrics.py REPORT.(docx|md|txt) [--term-sheet TERMS.md] [--json OUT.json]
         [--summary-heading REGEX] [--stop-headings REGEX] [--number-format sa|intl]

Reads prose only: tables, captions, tables of contents and anything under glossary,
references, acknowledgements or appendix headings are excluded. Prints a markdown
report with PASS / CHECK / FAIL against the thresholds in TARGETS. Exit code 1 if any FAIL.

Term sheet format (one concept per line, canonical first, variants after pipes):
  Enhanced Tourism Support Package | Tourism Supply Support Package | extended Tourism Supply Support Package
Lines starting with # are ignored.
"""
import argparse, collections, json, re, statistics, sys, zipfile
from difflib import SequenceMatcher

TARGETS = {  # metric: (comparison, threshold, severity if missed)
    "mean_sentence_words": ("<=", 22, "FAIL"),
    "p90_sentence_words": ("<=", 32, "FAIL"),
    "pct_sentences_over_35": ("<=", 5, "FAIL"),
    "pct_sentences_12_or_fewer": (">=", 15, "CHECK"),
    "hedges_per_10k": ("<=", 30, "FAIL"),
    "therefore_per_10k": ("<=", 6, "FAIL"),
    "significant_per_10k": ("<=", 5, "CHECK"),
    "agentless_per_10k": ("<=", 4, "FAIL"),
    "vague_positive_per_10k": ("<=", 6, "CHECK"),
    "intensifiers": ("<=", 3, "CHECK"),
    "em_dashes": ("==", 0, "FAIL"),
    "en_dashes_in_prose": ("==", 0, "FAIL"),
    "oxford_comma_candidates": ("==", 0, "CHECK"),
    "semicolon_as_colon": ("==", 0, "FAIL"),
    "us_spellings": ("==", 0, "FAIL"),
    "spelling_pairs_mixed": ("==", 0, "CHECK"),
    "first_person_plural": ("==", 0, "CHECK"),
    "tell_words": ("==", 0, "CHECK"),
    "number_format_conflicts": ("==", 0, "FAIL"),
    "unfinished_paragraphs": ("==", 0, "FAIL"),
    "possible_verbless_sentences": ("==", 0, "CHECK"),
    "repeated_words": ("==", 0, "FAIL"),
    "stale_time_phrases": ("==", 0, "CHECK"),
    "placeholder_or_field_errors": ("==", 0, "FAIL"),
    "internal_or_draft_links": ("==", 0, "FAIL"),
    "auto_alt_text": ("==", 0, "CHECK"),
    "summary_words": ("<=", 1500, "FAIL"),
    "pct_summary_reused_in_body": ("<=", 15, "FAIL"),
    "cross_chapter_duplicate_sentences": ("<=", 3, "CHECK"),
    "term_sheet_variants": ("==", 0, "FAIL"),
}

HEDGES = r"\b(may|might|could|perhaps|possibly|potentially|arguably|appears? to|seems? to)\b"
AGENTLESS = (r"\bit is (proposed|estimated|expected|hoped|believed|recommended|suggested|considered|anticipated|"
             r"envisaged|important to (note|recognise)|necessary to|possible that|clear that|worth noting)\b"
             r"|\bshould be (explored|considered|investigated|examined|reviewed|looked at)\b"
             r"|\bwill need to be (taken care of|addressed|considered|explored)\b")
VAGUE_POSITIVE = (r"\b(robust|innovative|scalable|agile|holistic|dynamic|vibrant|compelling|world-class|"
                  r"best-in-class|cutting-edge|seamless|transformative|purpose-led|purpose-driven|exceptional|"
                  r"outstanding|breath-?taking|unique|unparalleled|stunning|iconic)\b")
INTENSIFIERS = r"\b(really|very|incredibly|absolutely|truly|deeply|extremely|hugely|profoundly)\b"
TELL_WORDS = (r"\b(leverag(e|es|ed|ing)|unlock(s|ed|ing)?|delve|navigat(e|es|ed|ing)|tapestry|synerg(y|ies)|"
              r"paradigm|game-?changer|ever-evolving|realm|fast-paced|dive into|ecosystems?|landscapes?|journeys?)\b")
# ecosystem, landscape and journey are often literal in tourism writing: listed for a human check, not auto-fixed.
SEMI_AS_COLON = (r"\b(is|are|was|were|include|includes|including|of|as follows|follows|namely|such as|between|"
                 r"on|for|from|with|into|towards|across|are as follows);\s")
US_SPELL = [  # -ize forms and -or/-our words are handled separately in main()
    r"\b(center|centers|centered|theater|meter|meters|liter|fiber|caliber)\b",
    r"\b(analyz|paralyz|catalyz)\w*\b", r"\b(defense|offense)\b", r"\b(traveler|traveled|traveling|travelers)\b",
    r"\b(modeling|modeled|labeled|labeling|canceled|canceling|fueled|fueling)\b", r"\b(fulfill|enroll|skillful|willful)\b",
    r"\b(catalog|dialog|program|programs)\b", r"\btoward\b", r"\b(aging|judgment)\b",
]
IZE_EXCEPTIONS = {"size", "sizes", "sized", "seize", "seized", "seizes", "prize", "prizes", "prized", "capsize",
                  "maize", "baize", "belize", "assize", "downsize", "downsized", "oversized", "upsize", "outsize"}
SPELLING_PAIRS = [("re-open", r"\bre-open"), ("reopen", r"\breopen"), ("focussed", r"\bfocuss"), ("focused", r"\bfocuse"),
                  ("lockdown", r"\blockdown"), ("lock down", r"\block down\b"), ("co-ordinat", r"\bco-ordinat"),
                  ("coordinat", r"\bcoordinat"), ("re-ignit", r"\bre-ignit"), ("reignit", r"\breignit"),
                  ("e-visa", r"\be-visa"), ("evisa", r"\bevisa"), ("roll-out", r"\broll-out"), ("rollout", r"\brollout"),
                  ("long-term (adj)", r"\blong-term\b"), ("long term (adj)", r"\blong term (growth|plan|strateg)")]
STALE = r"\b(at the time of writing|as at the time of writing|currently|recently|to date|at present|this year|last year|next year)\b"
PLACEHOLDERS = r"(error! reference source not found|error! bookmark not defined|\bTBC\b|\bTBD\b|\bTODO\b|\bXX+\b|\[insert|\?\?)"
INTERNAL_LINK = r"(sharepoint\.com|onedrive|-my\.sharepoint|file:///|\\\\[a-z0-9_-]+\\|localhost|\.docx#|/personal/)"
FIRST_PERSON = r"\b([Ww]e|[Oo]urs?|us)\b"  # case-sensitive so that "US" (United States) is not counted
ABBREV = r"\b(eg|ie|etc|vs|Dr|No|al|St|Mr|Ms|Mrs|Prof|Fig|approx|Dept|Inc|Ltd|Co)\."


def per10k(n, words):
    return round(n * 10000 / max(words, 1), 1)


def norm_heading(t):
    t = re.sub(r"\{[^}]*\}", "", t)
    return re.sub(r"[\[\]*_#]", "", t).strip()


def load_docx(path, stop_re):
    from docx import Document
    from docx.oxml.ns import qn
    doc = Document(path)
    blocks, section, links, alt = [], "FRONT MATTER", [], 0
    for p in doc.paragraphs:
        style = p.style.name if p.style is not None else ""
        text = p.text.strip()
        if style.startswith("Heading 1") or style == "Title":
            section = norm_heading(text).upper() or section
            continue
        if style.startswith("Heading") or "Caption" in style or style.lower().startswith(("toc", "table of")) \
                or style == "TableofFigures":
            continue
        ppr = p._p.find(qn("w:pPr"))
        is_list = ppr is not None and ppr.find(qn("w:numPr")) is not None or "List" in style
        blocks.append({"section": section, "text": text, "list": is_list})
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        rels = [n for n in names if n.endswith(".rels")]
        for r in rels:
            data = z.read(r).decode("utf8", "ignore")
            links += re.findall(r'Target="([^"]+)"[^>]*TargetMode="External"', data)
        body = z.read("word/document.xml").decode("utf8", "ignore")
        alt = len(re.findall(r"automatically generated", body, re.I))
        extra = {"comments": len(re.findall(r"<w:comment ", z.read("word/comments.xml").decode("utf8", "ignore")))
                 if "word/comments.xml" in names else 0,
                 "tracked_insertions": body.count("<w:ins "), "tracked_deletions": body.count("<w:del ")}
        field_errors = len(re.findall(r"Error! (Reference source|Bookmark)", body))
    return blocks, links, alt, extra, field_errors


def load_text(path, stop_re):
    raw = open(path, encoding="utf8", errors="ignore").read()
    links = re.findall(r"\]\((https?://[^)\s]+|file:[^)\s]+)\)", raw) + re.findall(r"<(https?://[^>]+)>", raw)
    alt = len(re.findall(r"automatically generated", raw, re.I))
    blocks, section, buf = [], "FRONT MATTER", []

    def flush():
        if buf:
            t = " ".join(x.strip() for x in buf).strip()
            is_list = bool(re.match(r"^([-*+]|\d+[.)])\s", buf[0].strip()))
            t = re.sub(r"^([-*+]|\d+[.)])\s+", "", t)
            blocks.append({"section": section, "text": t, "list": is_list})
            buf.clear()
    for line in raw.splitlines():
        s = line.rstrip()
        if re.match(r"^#\s", s):
            flush(); section = norm_heading(s[1:]).upper(); continue
        if re.match(r"^#{2,6}\s", s) or not s.strip():
            flush(); continue
        bare = re.sub(r"\[\]\{#[^}]*\}", "", s).strip()
        if re.match(r"^\s*(\||\+[-=+]|-{3,}|:\s|!\[)", s) or re.match(r"^\*?(Figure|Table)\s+\d+", bare):
            flush(); continue  # tables, captions, images
        if re.match(r"^\s{2,}\S", s) and not (buf and re.match(r"^\s*([-*+]|\d+[.)])\s", buf[0])):
            flush(); continue  # indented table cell text outside a list item
        if re.match(r"^\s*([-*+]|\d+[.)])\s", s):
            flush()
        buf.append(s)
    flush()
    for b in blocks:  # strip inline markdown
        t = re.sub(r"!\[[^\]]*\]\([^)]*\)(\{[^}]*\})?", "", b["text"])
        t = re.sub(r"\[([^\]]*)\]\{[^}]*\}", r"\1", t)
        t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t)
        t = re.sub(r"\[\^\d+\]", "", t)
        t = re.sub(r"[*_`]", "", t).replace("\\", "")
        t = t.replace("---", "\u2014").replace("--", "\u2013")  # pandoc dash notation
        b["text"] = t.strip()
    return blocks, links, alt, {"comments": 0, "tracked_insertions": 0, "tracked_deletions": 0}, \
        len(re.findall(r"Error! (Reference source|Bookmark)", raw))


def sentences(text):
    t = re.sub(ABBREV, lambda m: m.group(1), text)
    parts = re.split(r"(?<=[.!?])[\"'\u2019\u201d)]?\s+(?=[A-Z0-9\"'\u2018\u201c(])", t)
    return [p.strip() for p in parts if len(p.split()) >= 3]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("report")
    ap.add_argument("--term-sheet")
    ap.add_argument("--json")
    ap.add_argument("--summary-heading", default=r"executive summary|summary of (the )?(report|plan|strategy)")
    ap.add_argument("--stop-headings", default=r"glossary|abbreviation|acronym|reference|bibliograph|acknowledg|appendi|annex|author credit|endnote")
    ap.add_argument("--number-format", choices=["sa", "intl"], default=None,
                    help="sa = decimal comma, space thousands (R82,5 billion; 725 000). intl = decimal point, comma thousands.")
    a = ap.parse_args()
    stop_re = re.compile(a.stop_headings, re.I)
    loader = load_docx if a.report.lower().endswith(".docx") else load_text
    blocks, links, alt, extra, field_errors = loader(a.report, stop_re)

    prose = [b for b in blocks if not stop_re.search(b["section"]) and b["section"] != "FRONT MATTER"
             and len(b["text"].split()) >= 4]
    body_paras = [b for b in prose if not b["list"] and len(b["text"].split()) >= 12]
    text_all = "\n".join(b["text"] for b in prose)
    low = text_all.lower()
    words = len(re.findall(r"[A-Za-z][A-Za-z'\-]*", text_all))

    sents = [(b["section"], s) for b in body_paras for s in sentences(b["text"])]
    lens = [len(s.split()) for _, s in sents] or [0]
    m = {}
    m["prose_words"] = words
    m["sentences"] = len(sents)
    m["mean_sentence_words"] = round(statistics.mean(lens), 1)
    m["median_sentence_words"] = statistics.median(lens)
    m["p90_sentence_words"] = sorted(lens)[int(0.9 * (len(lens) - 1))]
    m["pct_sentences_over_35"] = round(100 * sum(l > 35 for l in lens) / len(lens), 1)
    m["pct_sentences_12_or_fewer"] = round(100 * sum(l <= 12 for l in lens) / len(lens), 1)
    m["mean_paragraph_words"] = round(statistics.mean([len(b["text"].split()) for b in body_paras] or [0]))

    def hits(pattern, src=low, flags=0):
        return [mm.group(0) for mm in re.finditer(pattern, src, flags)]

    def examples(pattern, n=6, flags=re.I):
        out = []
        for sec, s in sents:
            if re.search(pattern, s, flags):
                out.append(f"[{sec[:28]}] {s[:160]}")
            if len(out) >= n:
                break
        return out

    ex = {}
    m["hedges_per_10k"] = per10k(len(hits(HEDGES)) + len(hits(r"\blikely\b")) + len(hits(r"\bpotential(ly)?\b")), words)
    m["therefore_per_10k"] = per10k(len(hits(r"\btherefore\b")), words)
    m["significant_per_10k"] = per10k(len(hits(r"\bsignificant(ly)?\b")), words)
    ag = hits(AGENTLESS); m["agentless_per_10k"] = per10k(len(ag), words); ex["agentless"] = examples(AGENTLESS)
    vp = hits(VAGUE_POSITIVE); m["vague_positive_per_10k"] = per10k(len(vp), words)
    ex["vague_positive_clusters"] = [f"[{sec[:28]}] {s[:160]}" for sec, s in sents
                                     if len(re.findall(VAGUE_POSITIVE, s.lower())) >= 2][:6]
    m["intensifiers"] = len(hits(INTENSIFIERS)); ex["intensifiers"] = examples(INTENSIFIERS)
    m["tell_words"] = len(hits(TELL_WORDS)); ex["tell_words (check literal use)"] = examples(TELL_WORDS)
    m["em_dashes"] = text_all.count("\u2014")
    m["en_dashes_in_prose"] = len(re.findall(r"(?<!\d)\s?\u2013\s?(?!\d)", text_all))
    ox = r",\s(?!(?:however|therefore|though|thus|too|indeed|respectively|in turn|for example),)(?:[\w'-]+\s){0,3}[\w'-]+,\s(and|or)\s"
    m["oxford_comma_candidates"] = len(re.findall(ox, text_all)); ex["oxford_comma_candidates"] = examples(ox, flags=0)
    m["semicolon_as_colon"] = len(re.findall(SEMI_AS_COLON, low)); ex["semicolon_as_colon"] = examples(SEMI_AS_COLON)
    us_words = [w for w in re.findall(r"\b\w+iz(?:e|es|ed|ing|ation|ations|er|ers)\b", text_all, re.I)
                if w.lower() not in IZE_EXCEPTIONS]
    us_words += [w for w in re.findall(r"\b(?:colou?r|favou?r|honou?r|labou?r|neighbou?r|behaviou?r|endeavou?r|harbou?r)\w*", text_all, re.I)
                 if "ou" not in w.lower()]
    for pat in US_SPELL:
        us_words += [mm.group(0) for mm in re.finditer(pat, text_all, re.I)]
    m["us_spellings"] = len(us_words); ex["us_spellings"] = sorted(set(us_words))[:20]
    mixed = []
    for i in range(0, len(SPELLING_PAIRS), 2):
        (n1, p1), (n2, p2) = SPELLING_PAIRS[i], SPELLING_PAIRS[i + 1]
        c1, c2 = len(re.findall(p1, low)), len(re.findall(p2, low))
        if c1 and c2:
            mixed.append(f"{n1} x{c1} vs {n2} x{c2}")
    m["spelling_pairs_mixed"] = len(mixed); ex["spelling_pairs_mixed"] = mixed
    fp = re.findall(FIRST_PERSON, text_all); m["first_person_plural"] = len(fp); ex["first_person_plural"] = examples(FIRST_PERSON, flags=0)

    # number formats
    comma_dec = re.findall(r"(?<![\d,])\d{1,3},\d{1,2}(?![\d,])", text_all)
    point_dec = re.findall(r"(?<![\d.])\d+\.\d+(?![\d.])", text_all)
    comma_thou = re.findall(r"(?<![\d,])\d{1,3}(?:,\d{3})+(?![\d,])", text_all)
    space_thou = re.findall(r"(?<![\d])\d{1,3}(?:[ \u00a0\u202f]\d{3})+(?![\d])", text_all)
    conflicts = []
    if comma_dec and point_dec:
        conflicts.append(f"decimal comma x{len(comma_dec)} and decimal point x{len(point_dec)} both used")
    if comma_dec and comma_thou:
        conflicts.append(f"comma is both decimal (x{len(comma_dec)}) and thousands separator (x{len(comma_thou)})")
    if comma_thou and space_thou:
        conflicts.append(f"comma thousands x{len(comma_thou)} and space thousands x{len(space_thou)} both used")
    if a.number_format == "sa" and (point_dec or comma_thou):
        conflicts.append(f"sa format requested: {len(point_dec)} decimal points, {len(comma_thou)} comma thousands")
    if a.number_format == "intl" and (comma_dec or space_thou):
        conflicts.append(f"intl format requested: {len(comma_dec)} decimal commas, {len(space_thou)} space thousands")
    m["number_format_conflicts"] = len(conflicts); ex["number_format_conflicts"] = conflicts

    unfinished = []
    for b in prose:
        t = b["text"]
        if b["list"] or t.isupper():
            continue
        if t.endswith(",") or (len(t.split()) >= 12 and not re.search(r"[.:;?!)\"'\u2019\u201d]$", t)):
            unfinished.append(f"[{b['section'][:28]}] ...{t[-110:]}")
    verbless = []
    finite = (r"\b(is|are|was|were|be|been|will|would|can|could|should|shall|may|might|must|has|have|had|does|do|did|"
              r"requires?|remains?|creates?|means|helps?|allows?|offers?|provides?|drives?|depends?|becomes?|involves?|"
              r"needs?|makes?|includes?|focus(es|ses)|invests?|generates?|shows?|indicates?|suggests?|represents?|"
              r"accounts|enables?|supports?|reduces?|increases?|takes?|gives?|leads?)\b")
    skip_start = r"^(According|Following|Including|Regarding|Considering|Notwithstanding|Excluding|Assuming|Leading|Existing|Emerging|Growing|Remaining|Building)\b"
    for sec, s in sents:  # verbless sentences such as "Identifying routes with ... at the greatest risk."
        core = re.sub(r"\b(that|which|who|whose|where|when|while)\b[^,;.]*", "", s)
        if re.match(r"^[A-Z][a-z]+ing\b", s) and not re.match(skip_start, s) and not re.search(finite, core):
            verbless.append(f"[{sec[:28]}] {s[:150]}")
    m["possible_verbless_sentences"] = len(verbless); ex["possible_verbless_sentences"] = verbless[:8]
    m["unfinished_paragraphs"] = len(unfinished); ex["unfinished_paragraphs"] = unfinished[:10]
    rep = re.findall(r"\b(\w+)\s+\1\b", low)
    rep = [r for r in rep if r not in {"that", "had", "is"}]
    m["repeated_words"] = len(rep); ex["repeated_words"] = rep[:10]
    m["stale_time_phrases"] = len(hits(STALE)); ex["stale_time_phrases"] = examples(STALE)
    m["placeholder_or_field_errors"] = len(re.findall(PLACEHOLDERS, text_all, re.I)) + field_errors
    bad_links = [l for l in links if re.search(INTERNAL_LINK, l, re.I)]
    m["internal_or_draft_links"] = len(bad_links); ex["internal_or_draft_links"] = bad_links[:5]
    m["auto_alt_text"] = alt
    m.update({k: v for k, v in extra.items()})

    # summary length and duplication
    sum_re = re.compile(a.summary_heading, re.I)
    summary_blocks = [b for b in prose if sum_re.search(b["section"])]
    m["summary_words"] = sum(len(b["text"].split()) for b in summary_blocks)

    def norm(s):
        return re.sub(r"\W+", " ", s.lower()).strip()
    sum_sents = {norm(s) for b in summary_blocks for s in sentences(b["text"]) if len(s.split()) >= 8}
    body_sents = [(b["section"], norm(s)) for b in prose if not sum_re.search(b["section"])
                  for s in sentences(b["text"]) if len(s.split()) >= 8]
    reused, where = set(), collections.Counter()
    for ss in sum_sents:
        for sec, bs in body_sents:
            if ss == bs or (abs(len(ss) - len(bs)) < 0.3 * len(ss) and SequenceMatcher(None, ss, bs).ratio() > 0.85):
                reused.add(ss); where[sec[:40]] += 1; break
    m["pct_summary_reused_in_body"] = round(100 * len(reused) / max(len(sum_sents), 1), 1)
    ex["summary_reuse_by_section"] = [f"{k}: {v}" for k, v in where.most_common()]
    seen, dup = {}, []
    for sec, bs in body_sents:
        if bs in seen and seen[bs] != sec:
            dup.append(f"{seen[bs][:25]} -> {sec[:25]}: {bs[:90]}")
        seen.setdefault(bs, sec)
    m["cross_chapter_duplicate_sentences"] = len(dup); ex["cross_chapter_duplicate_sentences"] = dup[:8]

    # term sheet
    variants = []
    if a.term_sheet:
        for line in open(a.term_sheet, encoding="utf8"):
            line = line.strip()
            if not line or line.startswith("#") or "|" not in line:
                continue
            terms = [t.strip() for t in line.split("|") if t.strip()]
            canon, alts = terms[0], terms[1:]
            for v in alts:
                n = len(re.findall(r"(?<![\w-])" + re.escape(v) + r"(?![\w-])", text_all, re.I))
                if n:
                    variants.append(f"'{v}' x{n} (use '{canon}')")
    m["term_sheet_variants"] = len(variants) if a.term_sheet else None
    ex["term_sheet_variants"] = variants

    # longest sentences
    ex["longest_sentences"] = [f"({len(s.split())}w) [{sec[:28]}] {s[:150]}"
                               for sec, s in sorted(sents, key=lambda x: -len(x[1].split()))[:8]]
    sec_stats = collections.defaultdict(list)
    for sec, s in sents:
        sec_stats[sec].append(len(s.split()))

    # output
    def judge(k, v):
        if k not in TARGETS or v is None:
            return ""
        op, th, sev = TARGETS[k]
        ok = {"<=": v <= th, ">=": v >= th, "==": v == th}[op]
        return "PASS" if ok else sev
    print(f"# Style metrics: {a.report}\n")
    print("| Metric | Value | Target | Result |\n|---|---|---|---|")
    fails = 0
    for k, v in m.items():
        r = judge(k, v)
        fails += r == "FAIL"
        tgt = f"{TARGETS[k][0]} {TARGETS[k][1]}" if k in TARGETS else ""
        print(f"| {k} | {v} | {tgt} | {r} |")
    print("\n## Sentence length by chapter\n")
    for sec, ls in sec_stats.items():
        print(f"- {sec[:50]}: {len(ls)} sentences, mean {statistics.mean(ls):.1f}, "
              f"{100 * sum(l > 35 for l in ls) / len(ls):.0f}% over 35 words")
    print("\n## Examples to review\n")
    for k, v in ex.items():
        if v:
            print(f"### {k}")
            for item in v:
                print(f"- {item}")
            print()
    if a.json:
        json.dump({"metrics": m, "examples": ex}, open(a.json, "w"), indent=2)
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
