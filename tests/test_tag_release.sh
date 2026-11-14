#!/usr/bin/env bash
# Tests scripts/tag_release.sh in throwaway repositories (no pushes).
set -uo pipefail

script="$(cd "$(dirname "$0")/.." && pwd)/scripts/tag_release.sh"
fails=0

new_repo() {
  local dir
  dir="$(mktemp -d)"
  git -C "$dir" init -q
  git -C "$dir" config user.email test@example.com
  git -C "$dir" config user.name test
  printf '%s\n' "$1" > "$dir/VERSION"
  git -C "$dir" add VERSION
  git -C "$dir" commit -q -m init
  echo "$dir"
}

check() {
  if [[ "$2" == "$3" ]]; then echo "ok   $1"; else echo "FAIL $1 (expected '$3', got '$2')"; fails=$((fails + 1)); fi
}

run() { (cd "$1" && unset GITHUB_SHA && PUSH_TAG=0 bash "$script" >/dev/null 2>&1); echo $?; }

# New version creates an annotated tag on HEAD
d="$(new_repo 1.2.3)"
check "new version exits 0" "$(run "$d")" "0"
check "tag created" "$(git -C "$d" tag -l)" "v1.2.3"
check "tag is annotated" "$(git -C "$d" cat-file -t v1.2.3)" "tag"
check "tag points at HEAD" "$(git -C "$d" rev-parse 'v1.2.3^{commit}')" "$(git -C "$d" rev-parse HEAD)"

# Existing tag is a no-op
before="$(git -C "$d" rev-parse v1.2.3)"
check "existing tag exits 0" "$(run "$d")" "0"
check "existing tag unchanged" "$(git -C "$d" rev-parse v1.2.3)" "$before"

# Malformed versions fail and create nothing
for bad in "1.2" "v1.2.3" "1.2.3-beta" "01.2.3" ""; do
  d="$(new_repo "$bad")"
  check "malformed '$bad' exits 1" "$(run "$d")" "1"
  check "malformed '$bad' creates no tag" "$(git -C "$d" tag -l)" ""
done

if [[ "$fails" -gt 0 ]]; then echo "$fails failure(s)"; exit 1; fi
echo "all passed"
