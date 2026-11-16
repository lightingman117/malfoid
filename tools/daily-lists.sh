#!/bin/sh
# Output: <CONFIG_DIR>/public/archive-list.txt and <CONFIG_DIR>/public/authors.md
cd <CONFIG_DIR> && mkdir -p public
python3 lst.py
python3 authors.py
# channel names: fetch only authors not looked up yet
python3 -c "
import json
have = {l.split('\t')[0] for l in open('<CONFIG_DIR>/chan_names.tsv', encoding='utf-8')}
for r in json.load(open('<CONFIG_DIR>/authors.json'))['authors']:
    if r[1].startswith('http') and r[0] not in have: print(r[0] + '\t' + r[1])
" > chan_new.tsv
while IFS="$(printf '\t')" read -r name url; do
  t=$(yt-dlp --flat-playlist --playlist-items 1 --print "%(playlist_channel)s|%(playlist_uploader_id)s" "$url" 2>/dev/null | head -1)
  printf '%s\t%s\n' "$name" "$t" >> chan_names.tsv
  sleep 2
done < chan_new.tsv
python3 authors_md.py authors.json chan_names.tsv ia_diff.json public/authors.md
echo DAILY-FINISHED
