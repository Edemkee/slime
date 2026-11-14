# Features and test coverage

Nothing is implemented yet. Features are added here in the PR that builds them; the planned list is in PLAN.md and the design in GAME_DESIGN_DOCUMENT.md.

## Feature: Release tagging  (major, tooling)
- Description: every version merged to `main` gets an annotated tag `v<VERSION>`.
- Related minor features: VERSION format check; no-op when the tag exists.
- Config: `VERSION` file; `GITHUB_SHA`; `PUSH_TAG=0` skips the push (used by tests).
- Tests: `tests/test_tag_release.sh` (new version, existing tag, malformed VERSION); run in CI. Not covered: the push to GitHub itself.
- Changes:
  - v0.1.0: added.
