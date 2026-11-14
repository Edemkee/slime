# Changelog

## v0.1.2 - 2026-11-14
### Changed
- Design: "endgame bonuses" are now prestige awards earned across sessions (working assumption: a Drops currency), replacing best-score unlock thresholds
- Design: two modes, Freeplay with optional challenge modifiers and a Challenge level ladder
- Plan: items 19 and 20 rewritten for prestige awards and the shop; new items 51 (challenge modifiers) and 52 (challenge levels)

## v0.1.1 - 2026-11-14
### Added
- Reference simulation prototype (tools/reference_sim.py) with a design-invariant check in CI
- Simulation spec, parameter table, layout and testing strategy in ARCHITECTURE.md
- Design round 2: heat as the single difficulty ramp and timer, hang-time and close-call bonuses, alternate inputs, mid-run events, achievements list
### Changed
- PLAN.md restructured into self-contained work items with acceptance criteria, dependencies and human gates
- Goo defaults and difficulty ramp replaced with values measured in the prototype

## v0.1.0 - 2026-11-14
### Added
- Game design document and milestone plan
- Architecture, features and decision documents
- Godot-ready .gitignore and .env.example
- Automatic release tagging from VERSION, with tests and CI
