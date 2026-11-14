# Features and test coverage

Nothing is implemented yet. Features are added here in the PR that builds them; the planned list is in PLAN.md and the design in GAME_DESIGN_DOCUMENT.md.

## Feature: Release tagging  (major, tooling)
- Description: every version merged to `main` gets an annotated tag `v<VERSION>`.
- Related minor features: VERSION format check; no-op when the tag exists.
- Config: `VERSION` file; `GITHUB_SHA`; `PUSH_TAG=0` skips the push (used by tests).
- Tests: `tests/test_tag_release.sh` (new version, existing tag, malformed VERSION); run in CI. Not covered: the push to GitHub itself.
- Changes:
  - v0.1.0: added.

## Feature: Reference simulation  (major, tooling, not shipped)
- Description: Python prototype of the plate and goo simulation; source of the starting parameters and the port reference.
- Related minor features: scripted players (released, frozen, PD bot); scenario report.
- Config: parameter dictionary `P` at the top of `tools/reference_sim.py`.
- Tests: `python3 tools/reference_sim.py --check` (hands-off loss within 10 s, frozen-hand loss within 20 s, 3 seeds); run in CI. Not covered: bot survival times (reported, not asserted).
- Changes:
  - v0.1.1: added.
