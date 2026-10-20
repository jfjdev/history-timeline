# Joe's History Timeline

Files in this folder:
- `data.json`: **the source of truth**. Edit only this file (and `template.html` for design changes).
- `build.py`: checks data.json and renders it into `timeline.html`, then copies it to `/workspace/timeline/timeline.html`.
- `template.html`: the page (all CSS/JS inline; the data goes in at `/*__TIMELINE_DATA__*/null`).
- `timeline.html`: the built page. Self-contained, works offline, single file. Don't edit it by hand.

## Rebuild
```bash
python3 /cursor/stores/store-70d7b241-1d80-4655-9f84-7392257e4e2f/timeline/build.py          # validate + build
python3 /cursor/stores/store-70d7b241-1d80-4655-9f84-7392257e4e2f/timeline/build.py --check  # validate only
```
On an error (bad date, unknown source id, duplicate id) the build stops and nothing gets written.
Note: `sed -i` fails on the store filesystem. Edit with Python (json.load / json.dump with indent=2, ensure_ascii=False) or a full rewrite.

## Add a source
Append to `sources`:
```json
{"id":"the-wager","title":"The Wager: A Tale of Shipwreck, Mutiny and Murder","type":"book",
 "author":"David Grann","year":2023,"notes":"","dateAdded":"2026-10-20"}
```
`type` is one of `book | documentary | article | other`. Optional: `"readFinished":"2026-10"` (YYYY, YYYY-MM or YYYY-MM-DD), the date Joe finished the book or watched the documentary. It shows as "✓ Finished October 2026" in the source list, the header and the event detail panel. `id` is a lowercase slug; it is used in links (`timeline.html#source=the-wager`).

## Add an event
Append to `events`:
```json
{"id":"wager-wrecked","title":"The Wager is wrecked","start":"1741-05-14","datePrecision":"day","approx":false,
 "category":"exploration","sources":["the-wager"],"description":"…","people":["David Cheap"],
 "location":"Wager Island, Chile","dateAdded":"2026-10-20"}
```
- **Dates**: `"YYYY"`, `"YYYY-MM"` or `"YYYY-MM-DD"`. **BCE = negative year**: `"-2560"` is 2560 BCE (there is no year 0; `-1` is 1 BCE).
- **Spans**: add `"end"` in the same format (reigns, wars, voyages, lives). Month/year-precision ends run to the end of that month/year.
- `datePrecision`: `year | month | day`. Optional, worked out from the date string if left out.
- `approx: true` gives a dashed outline, a "c." prefix and an "approximate" badge. Use it whenever a date is uncertain.
- `lifespan: true` (optional) on a person's life span. Other events then show "X was N years old" in "At that moment…".
- `category` must be a category id: `politics, science, leaders, people, war, culture, exploration`. Add more in `categories` with `{id,name,color}`.
- One event can cite several sources: `"sources":["a","b"]`.
- Ids must be unique. Prefer slugs like `cozens-shot`.

## Viewer features (for reference)
Wheel/pinch zoom (millennia down to days), drag to pan, double-click to zoom, `+ − ← → F T / Esc` keys. Lanes per category.
Spans are drawn as bars, points as dots with cards. Click an event for details: how long ago, generations/lifetimes, how long it lasted, what else was happening (including people's ages), and nearby events from the same source.
Hovering one event while another is selected shows the gap between them. Filters drawer: search, pick a source ("only" or "highlight"), toggle lanes, era bands, 80-year lifetimes ruler, and your birth year for a "your lifetime" band.
The overview bar shows where you are in all of history. URL `#source=<id>` preselects a source; `#event=<id>` opens an event.

## Demo data
The source `example-events` ("Example events (delete me)") and its 9 events are only a demo. To delete: remove the source and every event whose `sources` is `["example-events"]`.

## Publishing (website)
- Repo: https://github.com/jfjdev/history-timeline (public, Joe's **personal** account; never the work account joejames-clarity).
  GitHub Pages serves `index.html` from `main` at the repo root (branch-based, no Actions workflow).
- Live site: https://jfjdev.github.io/history-timeline/ (deep link: `…/history-timeline/#source=the-wager`)
- To update: edit `data.json`, then run
  `bash /cursor/stores/store-70d7b241-1d80-4655-9f84-7392257e4e2f/timeline/publish.sh "Add events from <book>"`
  This runs build.py, copies the files into `/workspace/timeline/site/`, then commits and pushes to `jfjdev/history-timeline` main.
  It uses the gh CLI with `GH_CONFIG_DIR=/home/box/.config/gh-personal`, which is already logged in as jfjdev. Pages redeploys in about a minute.
- `index.html` in the repo is just a copy of `timeline.html`.
