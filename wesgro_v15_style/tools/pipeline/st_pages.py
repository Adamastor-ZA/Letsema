import sys, re, json, subprocess
WORK = '/tmp/claude-0/-home-user-Letsema/98b96bfe-2843-55b4-9fb2-4f4083c56589/scratchpad/wst/work/'
pdf = sys.argv[1]
n = int(re.search(r'Pages:\s+(\d+)', subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout).group(1))
txt = [None] + [re.sub(r'\s+', ' ', subprocess.run(['pdftotext', '-f', str(i), '-l', str(i), pdf, '-'], capture_output=True, text=True).stdout) for i in range(1, n + 1)]
e = json.load(open(WORK + 'toc_entries.json'))
start = [i for i in range(1, n + 1) if 'Abbreviation Meaning' in txt[i]][0] + 1
pages = {}; ptr = start; miss = []
for lvl, t in e['toc']:
    hit = next((i for i in range(ptr, n + 1) if t in txt[i]), None)
    if hit is None: miss.append(t); continue
    pages['H|' + t] = str(hit); ptr = hit
for lst in (e['figs'], e['tabs']):
    ptr = start
    for t in lst:
        hit = next((i for i in range(ptr, n + 1) if t[:60] in txt[i]), None)
        if hit is None: miss.append(t); continue
        pages['C|' + t] = str(hit); ptr = hit
json.dump(pages, open(WORK + 'pages.json', 'w'))
print('pages', n, 'body starts', start, 'found', len(pages), 'missing', miss)
