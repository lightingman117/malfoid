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
