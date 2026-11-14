#!/usr/bin/env bash
# Tags the current commit as v<VERSION> if that tag does not exist yet.
# Env: GITHUB_SHA (default HEAD), PUSH_TAG (default 1; 0 skips the push).
set -euo pipefail

if [[ ! -f VERSION ]]; then
  echo "VERSION file not found" >&2
  exit 1
fi

version="$(tr -d '[:space:]' < VERSION)"
if [[ ! "$version" =~ ^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$ ]]; then
  echo "VERSION '$version' is not MAJOR.MINOR.PATCH" >&2
  exit 1
fi

tag="v$version"
sha="${GITHUB_SHA:-$(git rev-parse HEAD)}"

if git rev-parse -q --verify "refs/tags/$tag" >/dev/null; then
  echo "Tag $tag already exists, nothing to do"
  exit 0
fi

git tag -a "$tag" -m "Release $tag" "$sha"
echo "Created tag $tag on $sha"

if [[ "${PUSH_TAG:-1}" == "1" ]]; then
  git push origin "refs/tags/$tag"
  echo "Pushed tag $tag"
fi
