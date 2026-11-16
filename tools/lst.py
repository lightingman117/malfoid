import os, re, collections
root = '/youtube'
EXT = ('.mkv', '.mp4', '.webm', '.m4a', '.opus', '.mp3')
cats = sorted(d for d in os.listdir(root) if d.startswith('malfoid-'))
out = []
tot = 0; totb = 0
summary = []
for c in cats:
    cp = os.path.join(root, c)
    chans = sorted((d for d in os.listdir(cp) if os.path.isdir(os.path.join(cp, d)) and not d.startswith('.')), key=str.lower)
    block = []
    cn = 0
    for ch in chans:
        items = []
        for r, ds, fs in os.walk(os.path.join(cp, ch)):
            ds[:] = [d for d in ds if not d.startswith('.')]
            for f in fs:
                if f.lower().endswith(EXT) and not f.startswith('.'):
                    b = os.path.getsize(os.path.join(r, f)); totb += b
                    n = os.path.splitext(f)[0]
                    m = re.match(r'^s(\d{4})\.e(\d{2})(\d{2})\d*\s*-\s*(.*)$', n)
                    if m:
                        items.append(('%s-%s-%s' % (m.group(1), m.group(2), m.group(3)), m.group(4)))
                    else:
                        items.append(('', n))
        if not items: continue
        items.sort()
        cn += len(items)
        block.append('\n## %s (%d)' % (ch, len(items)))
        for d, t in items:
            block.append(('%s  %s' % (d, t)) if d else t)
    tot += cn
    summary.append('%s: %d videos, %d channels/sources' % (c, cn, sum(1 for l in block if l.startswith('\n## '))))
    out.append('\n\n==================== %s (%d) ====================' % (c.upper(), cn))
    if c == 'malfoid-commentary':
        out.append('Note: reaction/review/analysis videos about the trend, not fan works. Kept for now; may be pruned later.')
    out.extend(block)
hdr = ['Malfoid archive - file list (updated %s)' % __import__('time').strftime('%Y-%m-%d'), 'Total: %d videos, %.1f GB' % (tot, totb / 1e9)] + summary
open('<CONFIG_DIR>/public/archive-list.txt', 'w', encoding='utf-8').write('\n'.join(hdr + out) + '\n')
print('\n'.join(hdr))
