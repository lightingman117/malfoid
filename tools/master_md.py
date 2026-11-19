# master_md.py - turn the master lists (tools/master/*.tsv) into Markdown pages under lists/youtube/ that GitHub search can read.
# GitHub only searches files under ~384 KB, so the video list is split by category and then into parts.
# Usage: python3 tools/master_md.py   (run from the repo root)
import csv, os, collections
SRC, OUT, LIMIT = 'tools/master', 'lists/youtube', 300_000
os.makedirs(OUT, exist_ok=True)
rows = lambda f: list(csv.DictReader(open(os.path.join(SRC, f), encoding='utf-8'), delimiter='\t', quoting=csv.QUOTE_NONE))
esc = lambda s: (s or '').replace('|', '\\|').replace('\n', ' ')
ch = rows('youtube-channels.tsv')
with open(os.path.join(OUT, 'channels.md'), 'w', encoding='utf-8') as f:
    f.write('# YouTube channels\n\nOne row per YouTube channel we follow. Malfoid = videos we count as Malfoid; Saved = archived; '
            'To download = queued. Class: Curated = our name filter catches every Malfoid video we checked; '
            'Manual review = the channel sometimes posts Malfoid with no name in the text, so new uploads get looked at.\n\n')
    f.write('Channel | Category | Class | Malfoid | Saved | To download | Link\n--- | --- | --- | --- | --- | --- | ---\n')
    for r in sorted(ch, key=lambda r: r['Channel'].lower()):
        f.write(f"{esc(r['Channel'])} | {r['Category']} | {r['Class']} | {r['Malfoid']} | {r['Saved']} | {r['To download']} | [YouTube]({r['Link']})\n")
vids = collections.defaultdict(list)
for r in rows('youtube-videos.tsv'): vids[r['Category'] or 'other'].append(r)
for c, rs in sorted(vids.items()):
    rs.sort(key=lambda r: (r['Channel'].lower(), r['Uploaded']))
    part, size, n, f = 0, 0, 0, None
    for r in rs:
        line = f"- {r['Uploaded'] or '?'} | {esc(r['Title'])} | {r['Status']} | [YouTube]({r['YouTube']})\n"
        if f is None or size + len(line.encode()) > LIMIT:
            if f: f.close()
            part += 1; size = 0; last = None
            f = open(os.path.join(OUT, f'videos-{c}-{part}.md'), 'w', encoding='utf-8')
            f.write(f'# YouTube Malfoid videos: {c} (part {part})\n\nUploaded | Title | Status | Link, grouped by channel.\n')
        if r['Channel'] != last:
            h = f"\n## {r['Channel']}\n\n"; f.write(h); size += len(h.encode()); last = r['Channel']
        f.write(line); size += len(line.encode()); n += 1
    if f: f.close()
    print(c, n, 'videos in', part, 'file(s)')
# ---- X (Twitter): videos and literature, same idea (public posts only, no file paths)
XO = 'lists/x'; os.makedirs(XO, exist_ok=True)
def xlist(src, name, title, intro, cols, line):
    if not os.path.exists(os.path.join(SRC, src)): return
    rs = sorted(rows(src), key=lambda r: (r['Creator'].lower(), r.get('Posted') or r.get('Uploaded') or ''))
    part, size, f, last = 0, 0, None, None
    for r in rs:
        s = line(r)
        if f is None or size + len(s.encode()) > LIMIT:
            if f: f.close()
            part += 1; size = 0; last = None
            f = open(os.path.join(XO, f'{name}-{part}.md'), 'w', encoding='utf-8'); f.write(f'# {title} (part {part})\n\n{intro}\n\n{cols}\n')
        if r['Creator'] != last:
            h = f"\n## {r['Creator']}\n\n"; f.write(h); size += len(h.encode()); last = r['Creator']
        f.write(s); size += len(s.encode())
    if f: f.close()
    print(name, len(rs), 'rows in', part, 'file(s)')
xlist('x-videos.tsv', 'videos', 'X Malfoid videos', 'Videos posted on X that we count as Malfoid. "Skipped (YouTube copy)" = the same video is archived from YouTube.',
      'Posted | Post | Status | Category | Link',
      lambda r: f"- {r['Posted']} | {esc(r['Post text'])} | {r['Status']} | {r['Category']} | [X]({r['Link']})" + (f" [YouTube]({r['YouTube copy']})" if r['YouTube copy'] else '') + '\n')
xlist('x-literature.tsv', 'literature', 'X Malfoid fiction', 'Malfoid stories posted on X, one row per chapter or post.',
      'Posted | Work | Chapter | Status | Link',
      lambda r: f"- {r['Posted']} | {esc(r['Work'])} | {esc(r['Chapter'])} | {r['Status']} | " + (f"[X]({r['Link']})" if r['Link'] else '(not found yet)') + '\n')
# ---- Bilibili
XO = 'lists/bili'; os.makedirs(XO, exist_ok=True)
xlist('bili-videos.tsv', 'videos', 'Bilibili Malfoid videos', 'Videos on Bilibili that we count as Malfoid. "Skipped (YouTube copy)" = the same video is archived from YouTube.',
      'Uploaded | Title | Status | Category | Link',
      lambda r: f"- {r['Uploaded']} | {esc(r['Title'])} | {r['Status']} | {r['Category']} | [Bilibili]({r['Link']})" + (f" [YouTube]({r['YouTube copy']})" if r['YouTube copy'] else '') + '\n')
