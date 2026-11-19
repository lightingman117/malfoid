# Malfoid Archive
Draconia | Dracena Malfoy #Malfoid # Yearn

A fan archive of Malfoid videos and music: AI fan animations, music videos and stories, saved before they disappear. Some of them already have.

## Get the files
**https://malfoid.duckdns.org/**: a read-only file browser for the archive. You can watch in the browser, download single files, or download a whole folder as a zip. The folders are `series/`, `music/`, `stories/`, `archive.org/` (reuploads of videos that were removed from YouTube) and `commentary/` (reaction and analysis videos about the trend, not fan works; kept for now, may be pruned later).

The site lags a little behind the lists here while downloads are still running.

This archive is listed in the **Malfoid Index**, a curated directory of Malfoid fan works (fanfics, comics, art and videos): https://rhedak.github.io/malfoid-gallery/malfoid-index/

## What's here
- `lists/archive-list.txt`: everything archived so far (updated daily; older versions are in the git history), grouped by category (series, music, stories) and by channel. Each line is the upload date and the title.
- `lists/missing.md`: missing videos (needed and found).
- `lists/authors.md`: every author we archive, by type, with links to where their videos are.
- `lists/youtube/`: the YouTube master list as Markdown: `channels.md` (every channel we follow, how many Malfoid videos, how many saved) and `videos-<category>-<part>.md` (every Malfoid video by channel, with its status). Search it with GitHub search.
- `lists/x/`: Malfoid videos (`videos-<part>.md`) and Malfoid fiction (`literature-<part>.md`) posted on X, by creator, with their status. A video that is also archived from YouTube is marked "Skipped (YouTube copy)".
- `lists/bili/`: Malfoid videos posted on Bilibili (`videos-<part>.md`), by creator, with their status. A video that is also archived from YouTube is marked "Skipped (YouTube copy)".
- `tools/master/`: the same master lists as tab-separated files (`youtube-channels.tsv`, `youtube-videos.tsv`, `x-videos.tsv`, `x-literature.tsv`, `x-literature-creators.tsv`, `bili-videos.tsv`); `tools/master_md.py` turns them into the Markdown pages.
- `tools/`: the ytdl-sub setup (Malfoid subscriptions, config, cron line) and the scripts that build these lists and pull from archive.org. Paths are placeholders: `<CONFIG_DIR>` is your ytdl-sub config folder, `<TV_SHOWS_DIR>` your TV-shows folder.

## Folder names
Each author's folder is named `English Name (Original Name) [Sources, Role]`, for example:
- `616 STUDIO (616Studioph) [YT, Creator]`
- `KYL0REN (KYL0ЯЁП) [YT, ReUp]`
- `Enoki Saori (榎木纱织) [Bili, Creator]`
- `Katechon Studio (MalfoidTV) [YT+X+Web, Creator]`

The English name matches the Malfoid Index where the author is listed there. `(Original Name)` is left out when it's the same.

**Sources** (joined with `+`): `YT` YouTube · `X` x.com · `Bili` Bilibili · `IA` archive.org · `Rmbl` Rumble · `TT` TikTok · `IG` Instagram · `Nico` Niconico · `Web` the creator's own site · `Pixiv` · `AO3` · `Wtpad` Wattpad

**Role:** `Creator` makes their own videos · `ReUp` reuploads other people's · `Mixed` does both · blank if we don't know yet. Credit goes to the creator, not the reuploader.

Folders are being renamed to this format in batches, so some still use the old channel names.

The lists are snapshots. Downloads are still running, and new lists will be added as the archive grows.

## Sources
- YouTube channels and playlists
- Reuploads of removed videos found on archive.org
- Bilibili
- A few videos from X and creator sites

## Send us a link
Know a Malfoid video, channel or playlist we're missing, or where a removed video was reuploaded?
**[Send it with this form](https://docs.google.com/forms/d/e/1FAIpQLSd-ak0lKIAx56Z_Gy-yU3EYruaesNUjaIpp8sBxpXeTVwu-dQ/viewform)** A link is best, but just a title and who made it helps too. Every tip is checked before anything is added.

You can also open a GitHub issue.
