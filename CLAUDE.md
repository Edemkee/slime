# Operative decisions

Newest at the top. Each entry: date, decision, reason.

- 2026-11-14 - **`tools/reference_sim.py` is the reference for the simulation**; `--check` runs in CI. If it and ARCHITECTURE.md disagree, the reference wins. Reason: a working, measured algorithm to port beats prose. Keep it until the GDScript sim passes the same checks, then decide with the user whether to keep or delete it.
- 2026-11-14 - **An AI session never judges feel.** It uses invariant tests, bot reports and budgets; feel is decided by the user at the Human gates in PLAN.md. Reason: a model cannot play the game.
- 2026-11-14 - **Tests and invariant thresholds are never weakened to pass**; tunables change instead, recorded in ARCHITECTURE.md "Tuning". Reason: the thresholds are the design.
- 2026-11-14 - **Playtest builds go to GitHub Pages on every merge** (PLAN item 8); itch.io is for releases. Reason: the user can play each step in a browser without store setup.
- 2026-11-14 - **PLAN.md is the work queue, written to be executed item by item by a fresh session (e.g. Claude Opus 5.5).** Follow PLAN.md section 1; one item = one PR; item numbers are never reused or renumbered. Reason: user request.
- 2026-11-14 - **Commits and PRs never contain a Claude session link.** Co-Authored-By trailer only. Reason: dev-workflow rule.
- 2026-11-14 - **Tags are created by `.github/workflows/tag-release.yml`** from `VERSION` on every push to `main`; the logic lives in `scripts/tag_release.sh` and is tested by `tests/test_tag_release.sh`. Reason: sessions cannot push tags.
- 2026-11-14 - **Steam features go behind a `PlatformService` interface** (null implementation for web/itch, GodotSteam implementation for Steam builds). Reason: one codebase, no Steam dependency in the browser build.
- 2026-11-14 - **Goo and plate are simulated by our own fixed-step code (GDScript), not Godot's physics bodies.** Reason: soft-body feel needs full control; deterministic; unit-testable headless; identical on web and desktop.
- 2026-11-14 - **GDScript only, no GDExtension or C#.** Reason: simplest reliable web export.
- 2026-11-14 - **Engine: Godot 4.7.x stable, Compatibility renderer, web export with threads off.** Reason: free, exports to HTML5 (itch.io) and desktop (Steam), light 2D runtime; threads off runs on any host without special headers.
- 2026-11-14 - **Godot project lives in the repo root** (`project.godot` at top level, code in `src/`, tests in `tests/`, art and audio in `assets/`).
- 2026-11-14 - **Claude project: yes**, the session is attached to the Claude project "Slime Balance"; an overview doc is kept there.
- 2026-11-14 - **Project size: larger.** All documents and CI from the start. Reason: commercial release on two stores.
- 2026-11-14 - **Workflow: dev-workflow skill.** Every change goes through a PR against `main`, one version bump per PR, PR link reported to the user.
