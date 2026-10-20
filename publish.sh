#!/usr/bin/env bash
# Rebuild the timeline and publish it to GitHub Pages on Joe's PERSONAL account (jfjdev).
# Repo: https://github.com/jfjdev/history-timeline   Site: https://jfjdev.github.io/history-timeline/
# Usage: bash publish.sh ["commit message"]
set -euo pipefail
export GH_CONFIG_DIR=/home/box/.config/gh-personal
REPO=jfjdev/history-timeline
HERE="$(cd "$(dirname "$0")" && pwd)"
SITE=/workspace/timeline/site
WORK=/workspace/timeline/repo
MSG="${1:-Update timeline $(date '+%Y-%m-%d %H:%M')}"

python3 "$HERE/build.py"
mkdir -p "$SITE"
cp "$HERE/timeline.html" "$SITE/index.html"
cp "$HERE/data.json" "$HERE/build.py" "$HERE/template.html" "$HERE/README.md" "$HERE/publish.sh" "$SITE/"
touch "$SITE/.nojekyll"

gh auth setup-git >/dev/null
if [ ! -d "$WORK/.git" ]; then gh repo clone "$REPO" "$WORK"; fi
cd "$WORK"
git pull --ff-only -q || true
cp -a "$SITE/." "$WORK/"
git add -A
if git diff --cached --quiet; then echo "Nothing changed; site already up to date."; exit 0; fi
git -c user.name="jfjdev" -c user.email="jfjdev@users.noreply.github.com" commit -q -m "$MSG"
git push -q origin HEAD:main
echo "Pushed. Live in ~1 min at https://jfjdev.github.io/history-timeline/"
