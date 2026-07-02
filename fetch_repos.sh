#!/usr/bin/env bash
# Vendor a real GitHub repo as a reproducible, pinned snapshot for a real-repo task.
# usage: fetch_repos.sh <name> <git-url> <commit-sha>
# Clones, checks out the exact SHA, strips .git, and writes PROVENANCE.txt.
set -u
HB="$(cd "$(dirname "$0")" && pwd)"
name="$1"; url="$2"; sha="$3"
dest="$HB/tasks/repos/$name"
tmp="$HB/.fetch_$name"
rm -rf "$tmp" "$dest"; mkdir -p "$dest"
git clone --quiet "$url" "$tmp" || { echo "clone failed"; exit 1; }
git -C "$tmp" checkout --quiet "$sha" || { echo "checkout $sha failed"; exit 1; }
license=$(ls "$tmp" | grep -iE '^license' | head -1)
# copy everything except .git
( cd "$tmp" && tar --exclude=.git -cf - . ) | ( cd "$dest" && tar -xf - )
cat > "$dest/PROVENANCE.txt" <<EOF
source: $url
commit: $sha
license: ${license:-CHECK MANUALLY}
vendored: $(date +%Y-%m-%d)
EOF
rm -rf "$tmp"
echo "vendored $name @ $sha -> tasks/repos/$name"
echo "next: create tasks/<task_id>/ that copies the buggy file(s) into fixtures/, writes a hidden"
echo "      grade.py that runs the repo and checks the fix, and a ref/ with the corrected file(s)."
echo "      validate with: bash engine/preflight.sh <task_id>"
