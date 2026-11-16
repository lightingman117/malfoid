import json, re, os, urllib.request, urllib.parse, glob
RX = re.compile(r"(?i)malfoid|malfoy|draconia|dracaena|draco|(?<![a-z])potter(?!y)|hogwarts|slytherin|hermione|snape|dumbledore|voldemort|weasley|wizarding|quidditch|gryffindor|yule ball")
qs = ['malfoid', 'draconia', 'malfoy', 'dracaena', '"female malfoy"', 'hogwarts AND (ai OR anime)']
items = {}
for q in qs:
    u = 'https://archive.org/advancedsearch.php?' + urllib.parse.urlencode([('q', q), ('fl[]', 'identifier'), ('fl[]', 'title'), ('fl[]', 'creator'), ('fl[]', 'item_size'), ('rows', '3000'), ('output', 'json')])
    d = json.load(urllib.request.urlopen(u, timeout=60))['response']
    print(q, d['numFound'])
    for x in d['docs']:
        i = x['identifier']
        if i.startswith('youtube-'):
            items[i] = x
have = []
for p in glob.glob('/youtube/**/.ytdl-sub-*-download-archive.json', recursive=True):
    have.append(open(p, encoding='utf-8', errors='ignore').read())
for root, ds, fs in os.walk('/youtube'):
    have.append('\n'.join(fs))
have = '\n'.join(have)
rows = []
for i, x in items.items():
    vid = i[len('youtube-'):]
    t = x.get('title') or ''
    t = t if isinstance(t, str) else ' '.join(t)
    c = x.get('creator') or ''
    c = c if isinstance(c, str) else ' '.join(c)
    if not RX.search(t + ' ' + c):
        continue
    got = vid in have
    rows.append((got, c, vid, round((x.get('item_size') or 0) / 1e6), t[:90]))
rows.sort()
json.dump(rows, open('<CONFIG_DIR>/ia_diff.json', 'w'))
print('youtube items', len(items), 'wizardry', len(rows), 'already have', sum(r[0] for r in rows), 'missing', sum(not r[0] for r in rows), 'missing MB', sum(r[3] for r in rows if not r[0]))
