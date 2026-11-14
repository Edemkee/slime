# Slime Balance

A short physics arcade game: a blob of slippery goo is dropped on a plate, and you tilt the plate to keep it there for as long as you can. There is no safe spot. Planned for itch.io and Steam.

**Status**: planning (v0.1.0). No playable build yet.

## Documents

- [GAME_DESIGN_DOCUMENT.md](GAME_DESIGN_DOCUMENT.md) - what the game is
- [PLAN.md](PLAN.md) - milestones, todos and ideas
- [ARCHITECTURE.md](ARCHITECTURE.md) - tech and structure
- [FEATURES.md](FEATURES.md) - features and their tests
- [CHANGELOG.md](CHANGELOG.md) - changes per version
- [CLAUDE.md](CLAUDE.md) - working decisions

## Run

The Godot project arrives with plan item 3. It will open with Godot 4.7.x: import `project.godot` and press Play.

## Test

```sh
bash tests/test_tag_release.sh
```

Game tests (GUT, headless) arrive with the Godot project.

## Layout

```
src/      game code (planned)
tests/    tests
assets/   art and audio (planned)
scripts/  repository tooling
```
