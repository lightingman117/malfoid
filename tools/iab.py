import json, os, re, collections
rows = json.load(open('/config/ia_diff.json'))
names = []
for r, ds, fs in os.walk('/youtube'):
    names.append('\n'.join(fs))
names = '\n'.join(names)
by = collections.defaultdict(list)
for got, creator, vid, mb, title in rows:
    if got or vid in names:
        continue
    c = re.sub(r'[/\\:*?"<>|]', '_', (creator or 'unknown').strip())[:80] or 'unknown'
    by[c].append(vid)
os.makedirs('/config/ia-bulk', exist_ok=True)
lines = ['#!/bin/sh', '# archive.org bulk pull. Rerunnable: --download-archive skips done items.']
n = 0
for i, (c, ids) in enumerate(sorted(by.items())):
    f = '/config/ia-bulk/%03d.txt' % i
    open(f, 'w').write('\n'.join('https://archive.org/details/youtube-' + v for v in ids) + '\n')
    n += len(ids)
    d = '/youtube/malfoid-archiveorg/' + c
    lines.append("yt-dlp --no-overwrites --ignore-errors --sleep-requests 1 --download-archive /config/ia-bulk-done.txt -a '%s' -o '%s/%%(title).100B [%%(id)s].%%(ext)s'" % (f, d.replace("'", "'\\''")))
lines.append('echo FINISHED')
open('/config/ia-bulk.sh', 'w').write('\n'.join(lines) + '\n')
print('creators', len(by), 'items', n)
