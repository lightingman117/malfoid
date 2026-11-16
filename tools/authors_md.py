import json, re, sys, urllib.parse
d = json.load(open(sys.argv[1]))
names = {}
for ln in open(sys.argv[2], encoding='utf-8'):
    p = ln.rstrip('\n').split('\t')
    if len(p) == 2 and '|' in p[1]:
        names[p[0]] = [x.strip() for x in p[1].rsplit('|', 1)]
def norm(s): return re.sub(r'[^a-z0-9]', '', (s or '').lower())
ia = {}
for got, c, vid, mb, t in json.load(open(sys.argv[3])):
    if c: ia.setdefault(norm(c), c)
def ia_match(*cands):
    for n in cands:
        k = norm(n)
        if len(k) < 4: continue
        if k in ia: return ia[k]
        for ck, c in ia.items():
            if len(ck) >= 4 and (k in ck or ck in k): return c
    return None
# Hand-set names (fandom names) and extra locations. Edit here.
COMMON = {'ADayASMR': 'Lumos Lumos (complete)', 'belcourtsisters': 'Draco Female Adventures', 'j.a.vazquez5946 (Historias Impact)': 'Historias Impact', 'galakushi': 'Galakushi', 'MalfoidTV': 'Katechon Studio (Malfoid TV)'}
IA_NAME = {'j.a.vazquez5946 (Historias Impact)': 'J.A. V\u00e1zquez'}
EXTRA = {
    'belcourtsisters': ['Mine'],
    'j.a.vazquez5946 (Historias Impact)': ['[X](https://x.com/AzratemES)', 'Mine'],
    'Nextrealmstudio': ['[Site](https://draconiamalfoid.com/)', 'Mine'],
    'Fo_yege1664': ['[X](https://x.com/Foyege24)'],
    'MadMax000': ['[X](https://x.com/MadMax_Series)'],
    'LouieVerseCinematics': ['[X](https://x.com/LadyWasabee)'],
    'zeyhashimoto': ['[X](https://x.com/ZeyHashimoto)'],
    'MalfoidTV': ['[X](https://x.com/katechon_studio)', '[Site](https://malfoid.tv/)', 'Mine'],
    'OtakuAI2345': ['[X](https://x.com/otakuai2345)'],
}
NO_YT = {'galakushi': 'Mine (reupload)'}
def line(sub, r):
    disp, handle = names.get(sub, ['', ''])
    disp = COMMON.get(sub) or (disp if disp and disp != 'NA' else sub)
    handle = handle if handle.startswith('@') else ''
    url = 'https://www.youtube.com/' + handle if handle else r[1]
    where = [NO_YT[sub]] if sub in NO_YT else ['[YouTube](%s)' % url]
    c = IA_NAME.get(sub) or ia_match(sub, handle.lstrip('@'), disp)
    if c:
        where.append('[Archive](https://archive.org/search?query=%s)' % urllib.parse.quote('creator:"%s"' % c))
    for e in EXTRA.get(sub, []):
        if e not in where and e != 'Mine': where.append(e)
    if sub not in NO_YT and ('Mine' in r[4] or 'Mine' in EXTRA.get(sub, [])):
        where.append('Mine')
    return '- %s | %s | %s' % (disp.replace('|', '-').strip(), handle or '-', ', '.join(where))
rows = {r[0]: r for r in d['authors']}
sections = [('series', 'Series'), ('story', 'Stories'), ('short', 'Shorts'), ('music', 'Music')]
out = ['# Authors', '', 'Name | Channel | Where', '', 'Mine = in this archive.']
for key, title in sections:
    out += ['', '## ' + title, '']
    out += sorted((line(s, r) for s, r in rows.items() if r[2] == key), key=str.casefold)
out += ['', '## Playlists (mixed authors)', '']
for r in d['mixed']:
    where = (['[YouTube](%s)' % r[1]] if r[1].startswith('http') else []) + (['Mine'] if 'Mine' in r[4] else [])
    out.append('- %s | - | %s' % (r[0], ', '.join(where) or '-'))
open(sys.argv[4], 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print(len(rows), 'authors,', len(names), 'channel names')
