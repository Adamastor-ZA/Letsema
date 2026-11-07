"""Style scan of the text the v2 edits inserted: banned words, dashes, Oxford commas, sentence length."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from diff_v1_v2 import parts  # noqa
HERE = os.path.dirname(os.path.abspath(__file__))
log = json.load(open(os.path.join(HERE, 'applied.json')))['log']
BANNED = re.compile(r'\b(unlock\w*|ecosystem\w*|leverag\w*|landscape\w*|navigat\w*)\b', re.I)
OXF = re.compile(r',\s[^,.;:()\[\]]{1,60},\s(and|or)\s(?!then\b)', re.I)
seen, rows = set(), []
for e in log:
    for a in parts(e['after']) if e['after'] else []:
        before = ' '.join(parts(e['before'])) if e['before'] else ''
        for s in re.split(r'(?<=[.!?])\s+(?=[A-Z\[(])', a):
            s = s.strip()
            if not s or s in before or s in seen or len(s) < 4: continue
            seen.add(s)
            iss = []
            if BANNED.search(s): iss.append('banned word: ' + BANNED.search(s).group(0))
            if re.search('[–—]', s): iss.append('dash')
            m = OXF.search(s)
            if m: iss.append('check comma: ' + m.group(0))
            n = len(re.findall(r"[A-Za-z0-9][\w'%,.:/-]*", re.sub(r'\([^)]*\)|\[[^\]]*\]', '', s)))
            if n > 25: iss.append(f'{n} words')
            if iss: rows.append((e['id'], iss, s))
print(len(seen), 'new sentences scanned')
for r in rows: print(r[0], '|', '; '.join(r[1]), '|', r[2][:220])
