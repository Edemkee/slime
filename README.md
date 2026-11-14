# Slime Balance

A short physics arcade game: a blob of slippery goo is dropped on a plate, and you tilt the plate to keep it there for as long as you can. There is no safe spot. Planned for itch.io and Steam.

**Status**: planning. No playable build yet. Next: PLAN.md item 4.

## Documents

- [GAME_DESIGN_DOCUMENT.md](GAME_DESIGN_DOCUMENT.md) - what the game is
- [PLAN.md](PLAN.md) - the work queue: how to work it, items with acceptance criteria, ideas
- [ARCHITECTURE.md](ARCHITECTURE.md) - tech and structure
- [FEATURES.md](FEATURES.md) - features and their tests
- [CHANGELOG.md](CHANGELOG.md) - changes per version
- [CLAUDE.md](CLAUDE.md) - working decisions

## Run

The Godot project arrives with plan item 4. It will open with Godot 4.7.x: import `project.godot` and press Play.

## Test

```sh
bash tests/test_tag_release.sh
python3 tools/reference_sim.py --check   # design invariant on the reference prototype
python3 tools/reference_sim.py           # full scenario report, about a minute
```

Game tests (GUT, headless) arrive with the Godot project.

## Layout

```
src/      game code (planned)
tests/    tests
assets/   art and audio (planned)
scripts/  repository tooling
tools/    reference simulation prototype (not shipped)
```
