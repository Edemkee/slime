# Plan

This plan is written so that a fresh session (for example Claude Opus 5.5) with no memory of earlier chats can pick up the next item and finish it. Everything needed is in this repository.

## 1. How to work this plan

**At the start of every session**

1. Read `CLAUDE.md`, this file, `CHANGELOG.md`, `GAME_DESIGN_DOCUMENT.md` (GDD), `ARCHITECTURE.md`, `FEATURES.md`. If the dev-workflow skill is available, follow it; this section agrees with it.
2. Check `VERSION`, the latest tag, and open PRs. If an earlier PR is still unmerged, tell the user before starting new work.
3. Tell the user in 2-3 sentences where the project stands and which item you are taking.

**Choosing the item**

- Take the item that is `in progress`. If none, take the lowest-numbered `open` item in the Scheduled table whose "Depends on" items are all `done`.
- Items marked **Human** in the "Who" column cannot be completed by you. Prepare what the spec says, then stop and ask the user. Do not start items that depend on an unfinished Human item.
- Do not start Ideas (section 5) unless the user asks.

**Doing the item**

- One item = one branch (`feature/<short-name>` or `fix/<short-name>`) = one pull request against `main`. Open the PR yourself and give the user the link.
- In that PR: set the item to `in progress` when you start and to `done` (with the version in Notes) in the final commit.
- Each item's spec in section 4 lists **Build**, **Accept** and **Tests**. The item is done only when every Accept line is true and the general checklist below passes.
- Build only what the spec says. If you think of something extra, check sections 3 and 5 for an item it overlaps and add a note there; otherwise add a new Ideas row. Never renumber or reuse item numbers.
- One version bump per PR: feature items raise MINOR, fixes/tuning/docs raise PATCH. Never raise MAJOR unless the user explicitly asks.

**Rules that prevent the usual mistakes**

- **You cannot judge how the game feels.** Never claim something "feels good". Use the measurable proxies (invariant tests, bot reports, performance budgets) and leave feel to the Human gates.
- **Never weaken a test, an invariant threshold or an Accept line to make it pass.** Change the implementation or the tunable parameters. If that fails after a real attempt, stop and tell the user what you tried.
- **Numbers in the GDD and ARCHITECTURE.md are starting values.** You may change tunables (in `SimParams` and data resources) to meet Accept lines. Record every change in the tuning table in ARCHITECTURE.md with the reason.
- **Verify facts that change over time before relying on them**: current Godot 4.7.x patch version, the GUT release that supports it, GitHub Action versions, GodotSteam release, butler usage, Steam and itch.io requirements. Look them up; do not trust memory. Record what you pinned in `CLAUDE.md`.
- **The simulation stays pure** (ARCHITECTURE.md "Rules"). No scene-tree, rendering, input or time calls inside `src/sim/`.
- **No secrets in the repo.** Store credentials go into GitHub Actions secrets, which only the user can create.
- **Stop and ask the user** when: a GDD section 9 question blocks you; something needs an account, money, credentials or a repository setting; an Accept line cannot be met; or two documents contradict each other.

**Running Godot and tests**

- `scripts/get_godot.sh` (created in item 4) downloads the pinned Godot build; `scripts/run_tests.sh` runs all tests headless.
- If the session cannot download Godot, push the branch and read the CI result with `gh api repos/Edemkee/slime/actions/runs`. Never mark an item done while CI is red.
- For anything visual: check it if the session can (a screenshot through a virtual display, or opening the playtest build from item 8 in a browser tool). If it cannot, say so in the PR and list exactly what the user should look at.

**General checklist for every PR**

- [ ] Every Accept line of the item is true; tests added or updated and passing locally or in CI
- [ ] Every bug found on the way has a regression test
- [ ] Staged diff reviewed for secrets
- [ ] `PLAN.md` and `CHANGELOG.md` updated; `FEATURES.md`, `ARCHITECTURE.md`, GDD, `CLAUDE.md` updated where the change touches them
- [ ] `VERSION` (and the Godot project version once it exists) bumped once
- [ ] PR opened; description says what changed, why, how it was tested, the version and bump kind; no Claude session link
- [ ] Reply to the user contains the PR link, what to look at, and what comes next

## 2. What the human must do, and when

| When | Action |
|---|---|
| Any time | Answer the open questions in GDD section 9 (item 3) |
| Before item 8 | Repository Settings -> Pages -> Source: "GitHub Actions" |
| Item 12 | Play the grey-box build and give feedback (fun gate) |
| Before item 19 | Decide how prestige awards are unlocked (GDD section 9 question 5). If undecided, the Drops currency default is built |
| Item 22 | Play the content build; confirm or adjust award costs and challenge goals |
| Before item 25 | Decide where audio comes from (commissioned, licensed packs, other) |
| Item 28 | Review look, sound and menus |
| Before item 30 | Create the itch.io project page; add `BUTLER_API_KEY` as an Actions secret |
| Before item 31 | Steamworks partner account, app fee, app ID; create achievements and leaderboards in Steamworks |
| Item 33 | Approve store text and images; submit page and build for Valve review |
| Item 34 | Final release decision; say explicitly if this should be version 1.0.0 |

## 3. Scheduled items

States: `open`, `in progress`, `rejected`, `done`. "Who": AI = a session can finish it; Human = needs the user.

| # | Item | State | Milestone | Depends on | Who | Notes |
|---|------|-------|-----------|------------|-----|-------|
| 1 | Repo setup: docs, VERSION, .gitignore, tag-release, CI | done | M0 | - | AI | v0.1.0 |
| 2 | Design round 2, reference simulation, executable plan | done | M0 | 1 | AI | v0.1.1; prestige awards and challenge modes added in v0.1.2 |
| 3 | Answer open design questions (GDD section 9) | open | M0 | - | Human | Does not block M1 |
| 4 | Godot project skeleton, GUT, headless tests in CI | open | M1 | 1 | AI | next up |
| 5 | Simulation: plate | open | M1 | 4 | AI | |
| 6 | Simulation: goo, contact, lose check | open | M1 | 5 | AI | |
| 7 | Grey-box playable: view, grab input, fixed-step loop, restart | open | M1 | 6 | AI | |
| 8 | Playtest build deployed to GitHub Pages on every merge | open | M1 | 7 | AI | Human step first, see section 2 |
| 9 | Heat ramp and the "no stable point" invariant tests | open | M1 | 6 | AI | |
| 10 | Bot players and difficulty report | open | M1 | 9 | AI | |
| 11 | Live tuning panel | open | M1 | 7, 9 | AI | |
| 12 | **Fun gate**: user plays the grey-box build | open | M1 | 8, 10, 11 | Human | Go / adjust / stop |
| 13 | Run state machine, instant retry, pause on focus loss | open | M2 | 12 | AI | |
| 14 | Scoring logic | open | M2 | 13 | AI | |
| 15 | HUD and score card | open | M2 | 14 | AI | |
| 16 | Save data | open | M2 | 14 | AI | |
| 17 | Pickup spawner and collection | open | M3 | 15 | AI | |
| 18 | Six powerups | open | M3 | 17 | AI | |
| 19 | Prestige awards: kit system, Drops currency, unlock rules | open | M3 | 16, 18 | AI | Unlock method is the user's call; default is built if undecided |
| 20 | Prestige shop, kit select, reward on the score card | open | M3 | 19 | AI | |
| 21 | Mid-run events: gust, sliding pivot, goo rain | open | M3 | 18 | AI | Confirm with the user after item 12 before starting; also used as modifiers by item 51 |
| 22 | **Content gate**: user plays; costs and goals re-tuned | open | M3 | 20, 52 | Human | |
| 23 | Goo rendering: smooth outline, shader, heat colour, face | open | M4 | 12 | AI | |
| 24 | Plate and background art, particles, reduced motion | open | M4 | 23 | AI | |
| 25 | Audio: effects and layered music | open | M4 | 13 | AI | Human decides the asset source first |
| 26 | Menus, settings, onboarding hint, translatable strings | open | M4 | 15, 16 | AI | |
| 27 | Alternate inputs: gamepad, keyboard, toggle-grab | open | M4 | 13 | AI | Needed for Steam Deck |
| 28 | **Presentation gate**: user reviews look, sound, menus | open | M4 | 24, 25, 26, 27 | Human | |
| 29 | Release builds: export presets and CI build on tag | open | M5 | 22, 28 | AI | |
| 30 | itch.io release | open | M5 | 29 | AI | Human steps first, see section 2 |
| 31 | PlatformService and Steam integration | open | M5 | 29 | AI | Human steps first, see section 2 |
| 32 | Steam Deck pass | open | M5 | 27, 31 | AI | |
| 33 | Steam store page, images, trailer, build upload | open | M5 | 31 | Human | AI prepares text, screenshots, upload script |
| 34 | **Release gate** | open | M5 | 30, 32, 33 | Human | |
| 51 | Challenge modifiers and freeplay modifier select | open | M3 | 19 | AI | Do after 20 or 21, before 22. Absorbs idea 38 |
| 52 | Challenge levels: ladder, goals, stars, level select | open | M3 | 51 | AI | Before 22 |

## 4. Item specs

Each spec assumes you have read the GDD and ARCHITECTURE.md. "Sim spec" means ARCHITECTURE.md section "Simulation spec"; `tools/reference_sim.py` is the working reference for it.

### 3. Answer open design questions (Human)
- Ask the user the questions in GDD section 9 if they are still open. Record answers in the GDD decision log and adjust affected values (for example the session cap in `SimParams.cap`) in a PATCH PR.

### 4. Godot project skeleton, GUT, headless tests in CI
- **Build**: `project.godot` in the repo root (Godot 4.7.x, Compatibility renderer, 1920x1080 base, stretch mode `canvas_items`, aspect `expand`); folders from ARCHITECTURE.md "Layout"; an empty main scene that shows the version string read from `VERSION`; GUT vendored in `addons/gut/`; `scripts/get_godot.sh` (pinned version, download from the official release location); `scripts/run_tests.sh`; CI job that runs both the existing shell/Python checks and the GUT tests headless.
- **Accept**: `scripts/run_tests.sh` exits 0 locally or in CI; the project opens and runs with no errors or warnings in the output; the project version setting equals `VERSION` and a test asserts that; pinned versions recorded in `CLAUDE.md`.
- **Tests**: one GUT smoke test; the version-sync test.
- **Bump**: minor.

### 5. Simulation: plate
- **Build**: `src/sim/sim_params.gd` (a `Resource` holding every tunable from the Sim spec parameter table), `src/sim/plate_profile.gd` (surface height and slope for local x, including crown and optional lip), `src/sim/sim_state.gd`, and the plate part of `src/sim/sim.gd`: grab spring, damping, tilt limit, external torque input.
- **Accept**: matches Sim spec step 1; with no torque the plate stays still; a constant external torque produces the angular acceleration `torque / inertia` within 1%; the tilt limit holds and zeroes angular velocity; with a frozen cursor and no goo the plate settles at the cursor (overshoot under 20%).
- **Tests**: GUT unit tests for each Accept line and for `plate_profile` (centre is higher than the rim by `crown`; lip raises the last 8% of each side).
- **Bump**: minor.

### 6. Simulation: goo, contact, lose check
- **Build**: the goo part of `sim.gd` following Sim spec steps 2-4 exactly (skin, volume, firmness, one-sided plate collision, viscous contact drag, reaction torque, lose check). Use `PackedVector2Array`. Seeded `RandomNumberGenerator` owned by the sim state.
- **Accept**: same seed and inputs give identical state after 10,000 ticks (run twice in one process); goo area stays within 5% of target while resting; resting goo is wider than tall (width/height at least 1.8 with default params); on a plate fixed at a 0.1 rad tilt with wobble 0, the goo's sliding speed settles to a constant that is not zero (viscous grip, no static friction); reaction torque for goo resting at local x = 1 is within 15% of `mass * g * 1`; lose check fires only after the centroid passes the lower rim; 120 ticks take under 150 ms headless on CI.
- **Tests**: one GUT test per Accept line. Port the three scripted players' simplest case (released, heat 0) and assert a loss between 1 s and 10 s.
- **Bump**: minor.

### 7. Grey-box playable
- **Build**: `src/game/run_controller.gd` running the sim at a fixed 120 Hz with an accumulator and render interpolation; `src/view/` drawing the plate profile and the goo polygon in flat colours; mouse and touch grab per GDD 4.2 (grab point fixed at press, release anywhere including outside the window); `R` or click after a loss restarts within one frame; world-to-screen mapping per Sim spec "World".
- **Accept**: plays from drop to loss to restart with mouse; mouse-up outside the window releases the grab (no stuck grab); the sim receives input only through `SimInput`; frame time stays under 16.7 ms on the CI runner or the session machine.
- **Tests**: GUT tests for the accumulator (N ms of frames produce the right number of ticks; a long frame is clamped to 8 ticks) and for the screen-to-world mapping.
- **Bump**: minor.

### 8. Playtest build on GitHub Pages
- **Build**: Web export preset (threads off); workflow that exports the web build on every push to `main` and deploys it to GitHub Pages; the page shows the version. Verify current action versions and the export-template download location.
- **Accept**: after merge the game loads and is playable at the Pages URL; the URL is in `README.md` and in the Claude project overview doc; export presets contain no credentials.
- **Human first**: Pages must be enabled (section 2). If it is not, prepare the PR and ask.
- **Bump**: minor.

### 9. Heat ramp and invariant tests
- **Build**: `src/game/heat.gd` (heat = time / cap, stage = multiplier step) feeding drag, size and wobble into the sim per the Sim spec ramp table; `src/sim/bots.gd` with the `released` and `frozen` scripted players.
- **Accept (the design invariant)**: for the default parameters, at heat 0, over 10 seeds: `released` loses within 10 s and `frozen` loses within 20 s, every seed. At the cap the run ends as a perfect run. These thresholds are design constants.
- **Tests**: GUT tests for the invariant, the ramp end points, and the cap.
- **Bump**: minor.

### 10. Bot players and difficulty report
- **Build**: the PD bot from the reference sim in `bots.gd` with three presets (novice: delay 0.35 s, noise 0.05; average: 0.25 s, 0.03; expert: 0.12 s, 0.01); a headless script `scripts/sim_report.sh` that prints median, min and max survival per preset over 10 seeds for a given `SimParams`/kit.
- **Accept**: report runs headless in under 2 minutes; ordering holds (median novice < average < expert); expert median is under the cap; the report output for the default kit is pasted into the PR description and into ARCHITECTURE.md "Tuning".
- **Tests**: GUT test for the ordering with 5 seeds. Numeric bands are added only after item 12 (see there).
- **Note**: bots are steadier than people. They are a regression guard, not a measure of fun.
- **Bump**: minor.

### 11. Live tuning panel
- **Build**: a debug overlay (toggle with F1, excluded from release exports) with a slider for every `SimParams` value, buttons for "reset to default", "copy as text" and "set heat" (jump to 0, 0.25, 0.5, 0.75), and a readout of heat, goo local x, tilt and contact count.
- **Accept**: changing a slider affects the running sim on the next tick; "copy as text" produces lines that can be pasted into the tuning table; the panel is absent in release builds (test asserts the feature flag).
- **Bump**: minor.

### 12. Fun gate (Human)
- **Prepare**: make sure the Pages build is current; give the user the URL and this checklist: Is tilting by grab-and-drag understandable without instructions? Does the goo read as goo? How long did the first five runs last? Is the first 10 seconds too hard or too easy? Does it get harder in a way you can feel? Would you play again? Ask for the tuning-panel text if they changed values.
- **After feedback**: apply tuning in PATCH PRs. When the user says "go", run `scripts/sim_report.sh`, then add GUT tests asserting each bot preset's median stays within +/-25% of the approved values, and record them in ARCHITECTURE.md "Tuning". From then on any tuning change must update those bands deliberately, in the same PR, with the reason.
- If the answer is "adjust" in a way that changes the design, update the GDD first and re-plan affected items.

### 13. Run state machine
- **Build**: states Ready -> Dropping -> Playing -> Lost | Perfect -> ScoreCard -> Ready; goo drops from a seeded x within the middle third; timer and heat start on first contact; 0.4 s slow-motion on loss; retry input accepted as soon as the score card appears; pause when the window loses focus, resume on click.
- **Accept**: from loss to controllable next run takes under 1 s; no input reaches the sim outside Playing; pause freezes sim time exactly (state hash unchanged while paused).
- **Tests**: GUT tests for every transition and the pause invariant.
- **Bump**: minor.

### 14. Scoring logic
- **Build**: `src/game/scoring.gd`, pure logic fed by sim state each tick: survival points, multiplier from heat stage, edge rider, hang time, close call, perfect-run bonus, per GDD section 5.
- **Accept**: a scripted 180 s run with no bonuses scores exactly 6,300 + 2,000; each bonus triggers only under its GDD condition; score is an integer and never decreases.
- **Tests**: GUT tests per rule, including boundaries (exactly at a stage change, exactly at the edge zone).
- **Bump**: minor.

### 15. HUD and score card
- **Build**: in-run HUD (score, multiplier, heat meter); score card (score, best, "new best" state, breakdown by source, retry hint; reward and shop entry are added by item 20). All text through `tr()`.
- **Accept**: readable at 1280x720 and 1920x1080; the heat meter and multiplier never rely on colour alone; no text overlaps at any stage.
- **Bump**: minor.

### 16. Save data
- **Build**: `src/game/save_data.gd`: one JSON file in `user://` with a schema version, best score, lifetime score, settings. Items 19 and 52 extend it (wallet, owned awards, selected kit, stars) through migrations. Write to a temp file then rename. Load tolerates a missing, empty, corrupt or newer-version file (falls back to defaults, keeps a `.bak`, never crashes).
- **Accept**: all the failure cases above are handled; the game is fully playable when saving is impossible (browser storage blocked) and tells the player once, unobtrusively.
- **Tests**: GUT tests for round trip, each failure case, and a migration from schema 1 to a dummy schema 2.
- **Bump**: minor.

### 17. Pickup spawner and collection
- **Build**: seeded spawner per GDD section 6 (interval, lifetime, low and high lanes, at least 1 unit from the goo, rim positions weighted toward score pickups); collection when the goo polygon overlaps the pickup circle; pickup definitions as resources in `src/data/pickups/`.
- **Accept**: same seed gives the same spawn sequence; never more than 2 pickups at once; nothing spawns outside the reachable area or during non-Playing states.
- **Tests**: GUT tests for determinism, spacing, overlap detection (inside, touching, outside).
- **Bump**: minor.

### 18. Six powerups
- **Build**: powerups as data: each is a set of multipliers on `SimParams` or scoring, with a duration; a modifier stack that applies and removes them cleanly; HUD timer rings. Firm Up, Shrink, Score Orb, Double, Slow-Mo, Rim Guard per GDD section 6.
- **Accept**: after any sequence of powerups expires, effective parameters equal the base parameters exactly; picking up an active powerup refreshes its timer and does not stack its effect; Slow-Mo scales sim time, not heat or score rate per real second (document the choice in the GDD if you find a reason to change it).
- **Tests**: GUT tests per powerup, the stack-restores-exactly property with random sequences, and the invariant test from item 9 re-run with each timed powerup forced permanently on, recorded in the PR for information (powerups are temporary, so this is not a pass/fail line).
- **Bump**: minor.

### 19. Prestige awards: kit system, Drops currency, unlock rules
- **Before starting**: ask the user whether the unlock method (GDD 7.4, section 9 question 5) is decided. If not, build the Drops default below; the design must make swapping it cheap.
- **Build**: award pieces as resources in `src/data/awards/` (three slots per GDD 7.3), applied as parameter modifiers before a run; `src/game/progression.gd` with an `UnlockRule` interface and one implementation, `DropsUnlockRule` (cost per award from a data file); Drops payout function (from score, active modifiers' reward bonus, and first-time challenge stars); wallet and owned awards stored through save data (extend the schema with a migration).
- **Accept (invariant for every kit)**: for **every** combination of plate shape x plate mod x goo trait, the item 9 invariant holds (`released` within 10 s, `frozen` within 20 s, heat 0, 5 seeds). Each award increases the average bot's median survival compared with the default piece (so it really is easier). Replacing `DropsUnlockRule` with a test double needs no change outside `progression.gd` and its data. Drops can never go negative; an award cannot be bought twice.
- **Tests**: a GUT test that enumerates all combinations; a test per award for the "really easier" line; payout, purchase and boundary tests; save migration test.
- **Bump**: minor.

### 20. Prestige shop, kit select, reward on the score card
- **Build**: score card shows Drops earned this session and what is now affordable; prestige shop (from the score card and the menu) to buy awards; pre-run kit select (three slots, unowned awards show their cost); selection saved.
- **Accept**: usable with mouse only and with keyboard/gamepad focus only; an unowned award can never be equipped, including by editing the save file (validated on load); from the score card, retry is still one input and never blocked by the shop.
- **Tests**: GUT tests for selection validation and the affordable-list logic.
- **Bump**: minor.

### 21. Mid-run events
- **Before starting**: confirm with the user that events are still wanted after the fun gate.
- **Build**: per GDD 4.7: Gust, Sliding Pivot, Goo Rain; each announced 2 s ahead with an icon and sound hook; first event no earlier than 45 s; seeded schedule.
- **Accept**: the invariant still holds during each event; with events on, the average bot's median survival drops by no more than 30% versus events off.
- **Tests**: determinism of the schedule; one GUT test per event's effect on parameters.
- **Bump**: minor.

### 22. Content gate (Human)
- **Prepare**: Pages build; `scripts/sim_report.sh` output for every award combination and every challenge level; ask the user for their own scores, Drops earned per session, and where they got stuck. Propose award costs so that the first award is affordable within about five sessions, and level goals so that later levels need awards. Apply in a PATCH PR after the user agrees.

### 23. Goo rendering
- **Build**: smooth closed outline from the particle ring (Catmull-Rom or Chaikin), a fill shader with gloss and rim light, colour driven by heat (cool to hot), eyes that look along the velocity and widen near the rim, a "balled up" look while Firm Up is active. Compatibility-renderer shaders only.
- **Accept**: the view reads sim state and never writes to it (the determinism test from item 6 passes with the view attached); no visible seams or self-overlap in a 180 s bot run (check frames at 0, 60, 120, 170 s); works in the web build.
- **Bump**: minor.

### 24. Plate and background art, particles, reduced motion
- **Build**: plate, pivot and background as vector art or code-drawn shapes; drip and splat particles; light screen shake on impacts; a reduced-motion setting that turns shake and background motion off. Record every third-party asset and its licence in `assets/CREDITS.md`.
- **Accept**: goo and pickups remain the highest-contrast things on screen; reduced motion removes all shake; no asset without a recorded licence.
- **Bump**: minor.

### 25. Audio
- **Human first**: where the sounds and music come from (section 2). Until decided, build the system with clearly named placeholder files.
- **Build**: audio buses (Master, Music, SFX); squelch tied to goo speed and impacts; pickup, powerup, close-call and loss sounds; music in layers that add with the heat stage; audio starts only after the first user input (browser rule); volumes saved.
- **Accept**: no sound before first input in the web build; no clipping with all layers active; every file listed in `assets/CREDITS.md`.
- **Bump**: minor.

### 26. Menus, settings, onboarding hint, translatable strings
- **Build**: title, pause and settings screens (volumes, fullscreen, reduced motion, toggle-grab, language); a first-run hint that animates a hand grabbing and dragging the plate, shown until the player's first successful grab; every visible string in a translation CSV (English only for now).
- **Accept**: a test fails if any UI script contains a user-visible string literal not passed through `tr()`; settings persist; the game is fully operable without reading any text.
- **Bump**: minor.

### 27. Alternate inputs
- **Build**: per GDD 4.2: gamepad (left and right triggers press their rim down with analogue force; left stick as an alternative), keyboard (left/right with force ramping over 0.15 s), toggle-grab for mouse and touch. All inputs produce the same `SimInput` or an equivalent torque path defined in the Sim spec; menus navigable by gamepad.
- **Accept**: a full run including menus and kit select is possible on gamepad only and on keyboard only; the invariant tests pass unchanged.
- **Tests**: GUT tests mapping each device's input to the expected torque.
- **Bump**: minor.

### 28. Presentation gate (Human)
- **Prepare**: Pages build and a list of what changed since the fun gate; ask about readability, charm of the goo, audio mix, menu clarity.

### 29. Release builds
- **Build**: export presets for Web, Windows, Linux and macOS (check that no preset contains credentials); a workflow that builds all targets when a version tag is created and attaches them as workflow artifacts; in-game version label; debug tools excluded.
- **Accept**: all targets build in CI from a clean checkout; the web build still deploys to Pages; build outputs are not committed.
- **Bump**: minor.

### 30. itch.io release
- **Human first**: itch.io page and `BUTLER_API_KEY` secret (section 2).
- **Build**: workflow step that pushes each build to its butler channel (`html5`, `windows`, `linux`, `mac`) with the version from `VERSION`; page text and screenshots prepared in `store/itch/`.
- **Accept**: the key is read only from the secret and never printed; the user confirms the page plays in the browser.
- **Bump**: minor.

### 31. PlatformService and Steam integration
- **Human first**: Steamworks account, app ID, achievements and the two leaderboards created in Steamworks (section 2).
- **Build**: `src/platform/platform_service.gd` (interface), `null_platform.gd` (web and itch), `steam_platform.gd` using the current GodotSteam release for the pinned Godot version: achievements (list in GDD section 10), Classic and Open leaderboards, cloud save for the save file. Steam code is only loaded in Steam builds.
- **Accept**: the web export contains no Steam library; with Steam absent or offline the game runs normally; a freeplay run with no awards and no modifiers posts to Classic, any other freeplay run to Open; the app ID is not committed (`steam_appid.txt` stays ignored).
- **Tests**: GUT tests against a fake `PlatformService` for every call site.
- **Bump**: minor.

### 32. Steam Deck pass
- **Build**: check and fix 1280x800 layout, minimum text size, controller glyphs, default controller configuration, suspend/resume. Look up Valve's current Deck compatibility criteria and list each one with pass/fail in the PR.
- **Accept**: every criterion you can test is listed with its result; those needing hardware are listed for the user.
- **Bump**: minor or patch depending on the changes.

### 33. Steam store page and build upload (Human, AI prepares)
- **Prepare**: store description, feature list and tags in `store/steam/`; screenshots captured from the game at required sizes (look up the current list of required images and sizes); a SteamPipe upload script that reads credentials from the environment. The user does the uploads, images approval and submissions. Check Valve's current lead times for page and build review and tell the user.

### 34. Release gate (Human)
- **Prepare**: a release checklist in the PR: all gates passed, all store builds from the same tag, CHANGELOG reads well as patch notes, credits complete, save data survives an update from the previous version. Ask whether this release is 1.0.0.

### 51. Challenge modifiers and freeplay modifier select
- **Build**: modifiers as resources in `src/data/modifiers/` per GDD 7.2, going through the same modifier stack as awards and powerups; each has a reward bonus used by the Drops payout; a freeplay pre-run panel to toggle them; active modifiers shown on the HUD and score card. Windy, Sliding Pivot and Goo Rain are included only if item 21 is done; otherwise leave them out and note it here.
- **Accept**: every modifier lowers the average bot's median survival compared with no modifier (so it really is harder); the item 9 invariant still holds with any single modifier and with all of them together; a run with any modifier or award posts to the Open board, never Classic (assert on the flag that item 31 will read).
- **Tests**: a GUT test per modifier for the "really harder" line; stack-restores-exactly with awards + modifiers + powerups mixed.
- **Bump**: minor.

### 52. Challenge levels: ladder, goals, stars, level select
- **Build**: levels as resources in `src/data/levels/` (modifier set, goal type and value, three star thresholds, seed); goal types: survive, score, collect pickups, close calls; run controller ends a level on goal reached or loss; level select screen with stars and lock state; stars saved; first-time stars pay Drops. Ship about 20 levels with increasing difficulty; mark the later ones `awards_expected` with a recommended kit.
- **Accept**: the ladder order is enforced (also against an edited save file); for every level, the expert bot with the recommended kit reaches at least 1 star in most of 10 seeds (the level is possible); for every `awards_expected` level, the average bot's success rate with the recommended kit is at least 30 percentage points higher than with no awards; no level lasts longer than 90 s.
- **Tests**: GUT tests for each goal type, star thresholds, lock rules, and the bot lines above (may run in a separate, slower CI job).
- **Bump**: minor.

## 5. Ideas (unscheduled) and rejected

| # | Item | State | Notes |
|---|------|-------|-------|
| 35 | Daily challenge with a fixed seed | open | Cheap because the sim is seeded |
| 36 | Replay or ghost of the best run | open | Record `SimInput` per tick; exact playback is only guaranteed on the same platform |
| 37 | Hazard pickups (grease, growth) | open | After item 22 |
| 38 | Challenge kits: harder plates with a score multiplier | rejected | Superseded: built as challenge modifiers in item 51 |
| 39 | Cosmetics bought with Drops or unlocked by lifetime score | open | Something to spend on after all awards are owned |
| 40 | Mobile store release | open | Touch already works in the web build |
| 41 | Steam demo / festival build | open | The web build already serves as a demo on itch.io |
| 42 | Small always-on-top "desk toy" window mode | open | |
| 43 | Cosmetic drips from goo overhanging the rim | open | Visual only; could fold into item 24 |
| 44 | Save export/import as a text code | open | Helps browser players whose storage gets cleared |
| 45 | After each run, pick one of three bonuses for the next run | rejected | User clarified: bonuses are permanent prestige awards (GDD section 7) |
| 46 | 3D plate with two-axis tilt | rejected | Much larger scope; side-on reads better. Reopen if GDD question 2 says otherwise |
| 47 | Goo built from engine rigid bodies and joints | rejected | Jittery, hard to tune, not deterministic |
| 48 | Goo loses mass through drips, mass acts as health | rejected | Brief says falling off is the loss; a gradual loss blurs it |
| 49 | Online leaderboard shared by itch.io and Steam | rejected | Needs a server and cheat protection; Steam leaderboards cover Steam |
| 50 | Goo that splits into several blobs | rejected | Large simulation cost for unclear gain; revisit only after release |
