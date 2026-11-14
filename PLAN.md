# Plan

States: `open`, `in progress`, `rejected`, `done`. Milestones M0-M5 group the items.

| # | Item | State | Notes |
|---|------|-------|-------|
| 1 | M0: Repo setup: docs, VERSION, .gitignore, tag-release workflow, CI | done | v0.1.0 |
| 2 | M0: Confirm open design questions (session cap, 2D side-on, business model, cap vs endless) | open | GDD section 9; blocks tuning, not the prototype |
| 3 | M1: Godot project skeleton (project.godot, Compatibility renderer, GUT, headless tests in CI) | open | next up |
| 4 | M1: Physics core: plate on pivot + soft-body goo, grey-box visuals | open | fixed-step, engine-independent sim |
| 5 | M1: Grab-and-drag control (mouse and touch) | open | spring from grab point to cursor |
| 6 | M1: "No stable point" invariant test for the default kit | open | cursor held still -> loss within 20 s |
| 7 | M1: **Fun gate**: playable grey-box build on itch.io (restricted page) | open | decide go / adjust before building content |
| 8 | M2: Run loop: drop, lose condition, score card, instant retry | open | retry under 1 s |
| 9 | M2: Difficulty ramp and 3:00 session cap with perfect-run finish | open | depends on #2 |
| 10 | M2: Scoring, multiplier, edge-rider bonus, HUD | open | |
| 11 | M3: Pickup spawner and six powerups | open | Firm Up, Shrink, Score Orb, Double, Slow-Mo, Rim Guard |
| 12 | M3: Unlocks by best score, kit select screen, save data | open | invariant test extended to every kit combination |
| 13 | M4: Goo rendering (smooth outline, gloss shader, eyes), particles, plate art | open | |
| 14 | M4: Audio: squelches, tension music layers, splat | open | |
| 15 | M4: Menus, settings, accessibility (reduced motion, non-colour pickup cues, remappable keys) | open | |
| 16 | M4: Balance pass from playtests; re-tune unlock thresholds | open | |
| 17 | M5: itch.io public release: HTML5 + desktop builds via butler, page, screenshots | open | CHANGELOG as patch notes |
| 18 | M5: Steam integration via GodotSteam: achievements, Classic/Open leaderboards, cloud save | open | behind a platform-service interface; web build has no Steam code |
| 19 | M5: Steam Deck check (controls, text size, performance) | open | |
| 20 | M5: Steam store page, capsule art, trailer, release build via SteamPipe | open | page must be live as "coming soon" ahead of release; check Valve's current lead times and fee |
| 21 | Idea: gamepad support (stick = torque) | open | helps Steam Deck |
| 22 | Idea: daily challenge with a fixed seed | open | deterministic sim makes this cheap |
| 23 | Idea: hazard pickups (grease, growth) | open | after balance pass |
| 24 | Idea: mobile store release | open | touch already works in the web build |
| 25 | 3D plate with two-axis tilt | rejected | much larger scope; side-on reads better (revisit if #2 says otherwise) |
| 26 | Goo built from engine rigid bodies and joints | rejected | jittery, hard to tune, not deterministic; custom soft body instead |
