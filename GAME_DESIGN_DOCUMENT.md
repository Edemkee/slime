# Slime Balance - Game Design Document

Working title. Numbers are starting values for tuning, not commitments. Technical detail (algorithm, parameters) lives in ARCHITECTURE.md.

## 1. Vision

- **Pitch**: A blob of slippery goo lands on a plate. Keep it there. You can't, not forever, but you can last longer than last time.
- **Genre**: One-screen physics arcade / score attack.
- **Session**: Under 3 minutes, restart in under a second. "One more go" is the whole game.
- **Target player**: Anyone with a mouse and two spare minutes; score chasers who like mastering a wobbly physics toy.
- **Platforms**: itch.io (HTML5 in the browser, plus downloads) and Steam (Windows, Linux/Steam Deck, macOS if signing is practical).
- **Pillars**
  1. *Always falling*: there is never a safe position. Stop paying attention and you lose.
  2. *The goo is the star*: it must look and feel like a living gel. Funny to watch, readable to play.
  3. *Instant retry*: death to next attempt in under one second.

## 2. Core loop

1. Goo drops onto the plate.
2. Player grabs the plate and tilts it to keep the goo on, while steering the goo into pickups.
3. The goo heats up: slipperier, bigger, wobblier.
4. Goo falls off (or boils away at the cap) -> score, best score, reward.
5. The session pays out toward prestige awards (permanent, easier kit), which help with harder challenges -> retry.

## 3. Presentation and camera

- **2D, side-on, single screen.** Gravity points to the bottom of the screen. The plate is seen edge-on, balanced on a pivot.
- Reasoning: side-on makes "tilt toward where I drag" and "goo falls down the screen" read instantly, keeps the physics simple enough to tune well, and plays the same with mouse, touch and trackpad.

## 4. Mechanics

### 4.1 Plate
- A rigid body pinned at its centre to a pivot. It has rotational inertia, light angular damping, and **no restoring spring**: left alone it tips whichever way the goo's weight pushes it.
- Top surface is slightly **crowned** (convex), so even a level plate sheds goo.
- Tilt is limited to about +/-40 degrees.

### 4.2 Controls
- **Mouse / touch (primary)**: press on the plate to grab that point. Drag: a spring pulls the grabbed point toward the cursor, applying torque. Release: the plate is free again. Grabbing further from the pivot gives more leverage.
- **Toss**: a quick flick throws the goo into the air. An advanced skill, rewarded by "hang time" and needed for high pickups.
- **Gamepad**: left and right triggers press their side of the rim down with analogue force (like a finger on each edge). Left stick is an alternative.
- **Keyboard**: left/right keys press the rim down, force ramping up while held.
- **Toggle-grab option**: click once to grab, click again to release, for players who cannot hold a button.

### 4.3 Goo
- A light, soft-bodied blob that rests as a **puddle** (roughly three times wider than tall), sloshes, stretches and overhangs the rim.
- **Viscous, not sticky**: its grip on the plate is drag proportional to sliding speed, with no static friction. On any slope, however small, it creeps. It never "parks".
- It wobbles on its own (it is a little bit alive), which knocks it off any knife-edge balance.

### 4.4 The "no stable point" rule
Three things together guarantee there is no resting state:
1. Plate on a free pivot: goo off-centre tips the plate toward itself (positive feedback).
2. Crowned surface plus viscous-only grip: the only equilibrium is the exact top of the crown, and it is unstable.
3. The goo's own wobble and the heat ramp push it off that point.

**Design invariant (automated test)**, at the easiest moment of a run (heat 0), for every kit combination:
- hands off the plate -> loss within **10 seconds**;
- plate held but cursor never moved -> loss within **20 seconds**.

No prestige award may break this. The reference prototype measures about 3 s and 5 s for the default kit, and about 3.5 s and 6.5 s for the easiest kit combination.

### 4.5 Lose condition
- The goo's centre drops below the plate's lower rim -> run ends. Brief slow-motion on the fall, then the score card. Retry with one click or key.

### 4.6 Heat: the difficulty ramp and the session timer
- The goo **warms up** over the run. Heat goes from 0 to 1 over the session cap and drives everything: grip falls, the goo swells, the wobble grows. The goo's colour shifts from cool to hot, and a heat meter on the HUD doubles as the run timer.
- Heat has six stages; each stage raises the score multiplier by one.
- **At the cap (3:00 assumed) the goo boils off in a celebratory puff: a "perfect run"** with a large bonus. It should be rare: the reference prototype's strongest scripted player lasts about 2:35.
- Target run lengths for people: first-timers 10-30 s, typical 45-90 s, experts approach the cap. To be set at the fun gate.

### 4.7 Mid-run events (after the fun gate, if still wanted)
Short, announced 2 seconds ahead, none before 0:45:
- **Gust**: a sideways push on the goo for 3 s.
- **Sliding pivot**: the pivot drifts left and right for 8 s.
- **Goo rain**: droplets fall and merge, a growth spurt.

## 5. Scoring

All gains are multiplied by the current multiplier (x1 to x6, from the heat stage).

| Source | Points | Condition |
|---|---|---|
| Survival | 10 per second | Always while playing |
| Edge rider | +5 per second | Goo centre in the outer fifth of the plate, in contact |
| Hang time | 100 per airborne second | Awarded on landing, if airborne at least 0.4 s |
| Close call | 150 | Goo centre went past the rim and came back to the inner four fifths; 3 s cooldown |
| Score Orb | 100 | Pickup |
| Perfect run | 2,000 (not multiplied) | Reaching the cap |

Rough ceiling: 6,300 from survival alone over a full run, 10,000-12,000 with bonuses.

## 6. Pickups and powerups

Pickups float just above the plate (reach by sliding) or higher up (reach by tossing). One appears every 6-10 s, stays about 5 s, at most two at once, and is collected when the goo touches it. Effects are temporary and shown as a draining ring on the HUD. Each has a distinct shape, so they read without relying on colour.

| Pickup | Effect | Duration |
|---|---|---|
| Firm Up (ice cube) | Goo chills: grip x3 and it balls up into a firmer, rounder shape | 7 s |
| Shrink | Goo size -30% | 8 s |
| Score Orb | +100 x multiplier, instantly | - |
| Double | Score gains x2 | 8 s |
| Slow-Mo | Time runs at 70% | 5 s |
| Rim Guard | Temporary raised rim on both edges | 6 s |

Score pickups appear near the rim more often than in the centre. Powerups never stop the heat.

## 7. Modes, challenges and prestige awards

The long-term game is: **challenges make it harder, prestige awards make it easier.** Players earn awards across many short sessions and use them to beat challenges they could not beat before.

### 7.1 Modes
- **Freeplay**: the core score-attack run (sections 4-6). Before a run the player may switch on any **challenge modifiers**; each one raises the reward earned from that run.
- **Challenges**: a ladder of about 20 short levels (30-90 s each). A level is a fixed set of modifiers plus a goal: survive N seconds, reach N points, collect N pickups, or make N close calls. Each level awards up to 3 stars. A level opens when the previous one has at least 1 star.

### 7.2 Challenge modifiers (always harder)

| Modifier | Effect |
|---|---|
| Tiny Saucer | Plate width -25% |
| Greasy | Grip -40% |
| Big Goo | Goo size +30% |
| Hot Start | Run begins at heat stage 3 |
| Featherweight | Plate inertia halved: tips faster |
| Steep Crown | Crown height doubled |
| No Powerups | Only score orbs appear |
| Windy | Gusts through the whole run |
| Sliding Pivot | The pivot drifts left and right |
| Goo Rain | Droplets keep adding to the goo |

The last three are the mid-run events of 4.7 used as permanent modifiers.

### 7.3 Prestige awards (permanent, always easier)

Once unlocked, an award is owned forever. Before any run or level the player equips one **plate shape**, one **plate mod** and one **goo trait**.

| Award | Slot | Effect | Tier |
|---|---|---|---|
| Tacky Goo | Goo trait | +25% grip | 1 |
| Wide Platter | Plate shape | +15% width | 2 |
| Heavy Plate | Plate mod | 2x rotational inertia: tips more slowly | 3 |
| Rimmed Plate | Plate shape | Low lip at both edges | 4 |
| Compact Goo | Goo trait | Starts 20% smaller | 5 |
| Gentle Crown | Plate shape | Flatter crown: slower creep | 6 |
| Lucky Goo | Goo trait | Pickups appear more often and last longer | 7 |
| Golden Goo | Cosmetic | For a perfect run | - |

### 7.4 How awards are unlocked (not decided)
After every session the player should be able to make progress toward, or unlock, one or more awards. The method is open. **Working assumption so development is not blocked: a currency.**
- **Drops** are paid out on the score card after every freeplay run (from the score, increased by each active modifier) and the first time each challenge star is earned.
- Drops are spent in a **prestige shop** reachable from the score card and the menu. Cost rises with the tier. The first award should be affordable within about five sessions.
- The unlock rule is data, not code, so it can be swapped for another method (best-score thresholds, star counts, a level-up track) without rework.

### 7.5 Rules
- The "no stable point" invariant (4.4) holds for every combination of awards.
- Modifiers never make a run easier; awards never make it harder.
- Later challenge levels are tuned to be very hard with no awards and comfortable with the right ones. Checked with scripted players: the average bot's success rate on those levels must be clearly higher with awards than without.
- Leaderboards: **Classic** = freeplay with no awards and no modifiers; **Open** = freeplay with anything.

## 8. Feel, art, audio, accessibility

- Bright, clean, flat-shaded 2D. The goo is a glossy translucent blob with simple eyes that look where it is sliding and panic near the rim. Its colour is the heat.
- Squash-and-stretch on everything. Screen shake and particles kept light.
- Audio: wet squelches tied to goo speed and impacts, music that adds a layer per heat stage, a satisfying splat on loss.
- **Onboarding**: no tutorial screens. On the first run an animated hand shows grab-and-drag until the player does it.
- **Accessibility**: reduced-motion setting; no information by colour alone; toggle-grab; keyboard and gamepad play; the game is operable without reading text.

## 9. Open questions (for the user)

1. **Session cap**: the brief said "at maximum minutes long" without a number. Assumed 3:00.
2. **2D side-on** was assumed from "goo wants to go towards the bottom of the screen". A 3D two-axis tilting plate is a different, larger game.
3. **Business model**: free on itch.io and a small price on Steam, or free on both?
4. **Hard cap** with a "perfect run" ending (assumed), or an endless run where the ramp alone ends it?
5. **How are prestige awards unlocked?** Assumed: a currency (Drops) earned every session and spent in a shop (7.4). Alternatives: score thresholds, challenge stars, a level-up track.
6. **Challenges as levels, as freeplay modifiers, or both?** Assumed both: modifiers first (cheap), then the level ladder built from them.

## 10. Achievements (Steam; first list)

First Grab (finish a run) - Getting Warmer (reach heat stage 3) - Boiling Point (stage 6) - Perfect Run - Frequent Flyer (10 s total hang time in one run) - That Was Close (5 close calls in one run) - Living on the Edge (30 s of edge rider in one run) - Collector (every pickup type in one run) - Fully Kitted (all prestige awards) - Star Pupil (a star on every challenge level) - Purist (5,000 points with the default kit).

## 11. Design decision log

| Date | Decision | Reason |
|---|---|---|
| 2026-11-14 | "Endgame bonuses" are prestige awards: permanent, earned across sessions, making challenges easier | User clarification |
| 2026-11-14 | Two modes: Freeplay with optional challenge modifiers, and a Challenge level ladder | User: challenges via levels or freeplay with modifiers |
| 2026-11-14 | Unlock method left open; a Drops currency is the working assumption, with the unlock rule kept as data | User has not decided; development must not block on it |
| 2026-11-14 | Best-score unlock thresholds dropped | Replaced by prestige awards |
| 2026-11-14 | Goo rests as a puddle with zero shape stiffness; Firm Up adds stiffness so it balls up | Prototype: any constant stiffness made a rigid ball, not a gel |
| 2026-11-14 | Invariant thresholds set to 10 s (hands off) and 20 s (frozen hand) at heat 0 | Prototype measures 3 s and 5-6.5 s across kits; thresholds leave room for tuning |
| 2026-11-14 | Starting ramp: grip 2.0 -> 0.1, wobble 1.0 -> 9.0, size 1.0 -> 1.5 | Prototype: the first, gentler ramp let even a slow scripted player reach the cap |
| 2026-11-14 | Heat is the single ramp, the timer and the goo's colour | One readable idea replaces three hidden curves; gives the cap a fiction (boil-off) |
| 2026-11-14 | Style bonuses: hang time and close call added to edge rider | Rewards the toss and recoveries; gives experts more to chase than time |
| 2026-11-14 | Gamepad triggers, keyboard and toggle-grab are scheduled, not ideas | Steam Deck and accessibility need them |
| 2026-11-14 | Three human play gates (fun, content, presentation) before release | An AI session can measure the game but cannot judge how it feels |
| 2026-11-14 | Mid-run events designed but built only if still wanted after the fun gate | Avoid piling content on an unproven core |
| 2026-11-14 | 2D side-on view, one tilt axis | Matches the brief's gravity and drag description; small scope; same controls on mouse and touch |
| 2026-11-14 | Plate on a free pivot, crowned surface, viscous-only goo grip | Guarantees no stable point by construction |
| 2026-11-14 | Grab-and-drag applies a spring force, not a direct angle | Plate must obey physics; gives weight, leverage and the toss skill |
| 2026-11-14 | Hard session cap at 3:00 with a perfect-run bonus (assumed) | Brief requires a maximum session length |
| 2026-11-14 | Unlocks at best-score thresholds; three kit slots | Brief: endgame bonuses that ease plate shape, plate properties, goo properties |
| 2026-11-14 | Split leaderboards: Classic and Open | Easier kits would otherwise make scores incomparable |
