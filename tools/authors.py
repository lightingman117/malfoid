import yaml, os, re, json, subprocess, statistics
subs = yaml.safe_load(open('/config/subscriptions.yaml'))
def norm(s): return re.sub(r'[^a-z0-9]', '', (s or '').lower())
queued = set(yaml.safe_load(open('/config/catchup-2026-11-15.yaml')) or {})
queued |= {l.strip() for l in open('/config/hist_order.txt') if l.strip()}
queued |= set(re.findall(r'run "([^"]+)"', open('/config/malfoid-queue13.sh').read()))
begun = []
logs = [p for p in ['/config/malfoid-catchup-2026-11-15.log', '/config/malfoid-stories-2026-11-15.log', '/config/malfoid-history-2026-11-15.log'] if os.path.exists(p)]
logs.sort(key=os.path.getmtime)
for p in logs:
    begun += re.findall(r'Beginning subscription download for (.+)', open(p, errors='ignore').read())
running = begun[-1].strip() if begun else None
begun = {b.strip() for b in begun}
ia_creators = {}
for got, c, vid, mb, t in json.load(open('/config/ia_diff.json')):
    ia_creators.setdefault(norm(c), c)
EXT = ('.mkv', '.mp4', '.webm', '.m4a', '.opus', '.mp3')
def files(d):
    out = []
    for r, ds, fs in os.walk(d):
        ds[:] = [x for x in ds if not x.startswith('.')]
        out += [os.path.join(r, f) for f in fs if f.lower().endswith(EXT) and not f.startswith('.')]
    return out
def kind(cat, fl):
    durs = []
    for f in fl[:15]:
        try:
            durs.append(float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f], capture_output=True, text=True, timeout=20).stdout.strip()))
        except Exception:
            pass
    if durs and statistics.median(durs) <= 75:
        return 'short'
    return {'malfoid-series': 'series', 'malfoid-music': 'music', 'malfoid-stories': 'story', 'malfoid-commentary': 'commentary'}.get(cat, '?')
def in_ia(*names):
    for n in names:
        k = norm(n)
        if len(k) >= 4 and any(k in c or (len(c) >= 4 and c in k) for c in ia_creators):
            return True
    return False
authors, mixed = [], []
for name, s in subs.items():
    ov = (s or {}).get('overrides', {}) or {}
    d = ov.get('tv_show_directory', '')
    if not d.startswith('/youtube/malfoid-'):
        continue
    cat = d.rsplit('/', 1)[1]
    url = ov.get('url') or ''
    urls = [v for k, v in ov.items() if k.startswith('url') and v]
    fl = files(os.path.join('/youtube', cat, name))
    st = 'in-progress' if (name == running or (name in queued and name not in begun)) else 'complete'
    loc = ['YT'] + (['Archive'] if in_ia(name, url.rstrip('/').rsplit('/', 1)[-1].lstrip('@')) else []) + (['Mine'] if fl else [])
    row = [name, url if len(urls) <= 1 else '%d links' % len(urls), kind(cat, fl), st, ', '.join(loc), len(fl)]
    (mixed if ('playlist?list=' in url or len(urls) > 1 or 'Singles' in name or name.startswith('Malfoid')) and 'list=' in url or len(urls) > 1 else authors).append(row)
extra = []
for cat in ['malfoid-series', 'malfoid-music', 'malfoid-stories']:
    for d in sorted(os.listdir('/youtube/' + cat)):
        if d.startswith('.') or d in subs: continue
        fl = files(os.path.join('/youtube', cat, d))
        if not fl: continue
        loc = 'Archive, Mine' if 'archive.org' in d else ('Site, Mine' if '(site)' in d else 'Mine')
        extra.append([d, '', kind(cat, fl), 'complete', loc, len(fl)])
json.dump({'authors': authors, 'mixed': mixed, 'extra': extra, 'running': running}, open('/config/authors.json', 'w'), ensure_ascii=False)
print('done', len(authors), len(mixed), len(extra), running)
