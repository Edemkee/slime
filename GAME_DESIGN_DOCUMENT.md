# Slime Balance - Game Design Document

Working title. Numbers are starting values for tuning, not commitments.

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
3. Difficulty ramps continuously (slipperier, bigger, wobblier goo).
4. Goo falls off (or the timer cap is reached) -> score, best score, unlock progress.
5. Unlocks earned by best score offer an easier kit -> retry.

## 3. Presentation and camera

- **2D, side-on, single screen.** Gravity points to the bottom of the screen. The plate is seen edge-on, balanced on a pivot (a stick, a finger, a waiter's hand).
- Reasoning: side-on makes "tilt toward where I drag" and "goo falls down the screen" read instantly, keeps the physics one-dimensional enough to tune well, and plays the same with mouse, touch and trackpad.

## 4. Mechanics

### 4.1 Plate
- A rigid body pinned at its centre to a pivot. It has mass and rotational inertia, light angular damping, and **no restoring spring**: left alone it tips whichever way the goo's weight pushes it.
- Top surface is slightly **crowned** (convex), so even a perfectly level plate sheds goo.
- Tilt is limited to about +/-40 degrees.

### 4.2 Controls
- **Press** on the plate to grab that point. **Drag**: a spring pulls the grabbed point toward the cursor, applying torque. **Release**: the plate is free again.
- Grabbing further from the pivot gives more leverage; quick flicks can toss the goo into the air (an advanced skill used to reach high pickups).
- Touch works the same. Gamepad (stick = torque) is a later idea.

### 4.3 Goo
- A light, soft-bodied blob: it flattens, stretches, sloshes and overhangs the rim.
- **Viscous, not sticky**: its grip on the plate is drag proportional to sliding speed, with no static friction. On any slope, however small, it creeps. It never "parks".
- It has a small idle wobble (it is a little bit alive), which knocks it off any knife-edge balance.

### 4.4 The "no stable point" rule
Three things together guarantee there is no resting state:
1. Plate on a free pivot: goo off-centre tips the plate toward itself (positive feedback).
2. Crowned surface plus viscous-only grip: the only equilibrium is the exact top of the crown, and it is unstable.
3. Idle wobble and the difficulty ramp push the goo off that point.

**Design invariant (automated test):** for every plate/goo combination in the game, a simulation with the cursor held still (or released) must end in a loss within 20 seconds. No unlock or powerup may break this.

### 4.5 Lose condition
- The goo's centre of mass drops below the plate's rim line and it is no longer supported -> run ends. Brief slow-motion on the fall, then the score card. Retry with one click or key.

### 4.6 Difficulty ramp and session cap
- Over the run: goo drag falls, goo slowly swells, wobble grows, occasional gusts push the goo sideways later on.
- Target lengths: first-time players 15-30 s, typical 45-90 s, experts approach the cap.
- **Hard cap at 3:00**: the goo pops in a celebratory "perfect run" finish with a large bonus. (Cap length is an open question, see section 9.)

## 5. Scoring

- **Survival**: 10 points per second x multiplier. The multiplier steps up every 30 s (x1 to x6).
- **Edge rider**: small bonus trickle while the goo is in the outer fifth of the plate. Risk pays.
- **Pickups**: see below. Score orbs are worth 100 x current multiplier.
- **Perfect run**: +2,000 at the cap.
- Rough ceiling: about 6,300 from survival alone, 10,000-12,000 with pickups and bonuses.

## 6. Pickups and powerups

Pickups float just above the plate (reach by sliding) or higher up (reach by tossing). They appear every 6-10 s, stay about 5 s, and are collected when the goo touches them. Effects are temporary and shown as a draining ring on the HUD. Each has a distinct shape and colour, so they read without relying on colour alone.

| Pickup | Effect | Duration |
|---|---|---|
| Firm Up | Goo hardens: drag x3, less slosh | 7 s |
| Shrink | Goo size -30% | 8 s |
| Score Orb | +100 x multiplier, instantly | - |
| Double | Score x2 | 8 s |
| Slow-Mo | Time runs at 70% | 5 s |
| Rim Guard | Temporary raised rim on both edges | 6 s |

Pickups near the rim are worth more often than pickups in the centre. Hazard pickups (e.g. extra-slippery "grease") are an open idea for later.

## 7. Progression: unlocks from best score

Reaching a best-score threshold permanently unlocks a kit piece. Before a run the player picks one **plate shape**, one **plate mod** and one **goo trait**. All make the game easier; none removes the instability (section 4.4).

| Best score | Unlock | Slot | Effect |
|---|---|---|---|
| 500 | Tacky Goo | Goo trait | +25% base drag |
| 1,200 | Wide Platter | Plate shape | +15% width |
| 2,200 | Heavy Plate | Plate mod | 2x rotational inertia: tips more slowly |
| 3,500 | Rimmed Plate | Plate shape | Low lip at both edges: buys time, overflows as the goo swells |
| 5,000 | Compact Goo | Goo trait | Starts 20% smaller |
| 7,000 | Gentle Crown | Plate shape | Flatter crown: slower creep |
| 9,000 | Lucky Goo | Goo trait | Pickups appear more often and last longer |
| Perfect run | Golden Goo | Cosmetic | Bragging rights |

- The first unlock should land within a player's first few minutes (500 is roughly a 40 s run).
- Because easier kits inflate scores, leaderboards are split: **Classic** (default kit only) and **Open** (any kit).
- Thresholds will be re-tuned from playtest score distributions.

## 8. Art and audio direction (brief)

- Bright, clean, flat-shaded 2D. The goo is a glossy translucent blob with simple eyes that look where it is sliding and panic near the rim.
- Squash-and-stretch on everything. Screen shake and particles kept light; a reduced-motion option.
- Audio: wet squelches tied to goo speed and impacts, a rising musical tension layer as the multiplier climbs, a satisfying "splat" on loss.

## 9. Open questions

1. **Session cap**: the brief said "at maximum minutes long" without a number. Assumed 3:00.
2. **2D side-on** was assumed from "goo wants to go towards the bottom of the screen". A 3D two-axis tilting plate is a different, larger game.
3. **Business model**: free on itch.io and a small price on Steam, or free on both?
4. Hard cap with a "perfect run" ending, or an endless run where the ramp alone makes survival past the cap impossible?

## 10. Design decision log

| Date | Decision | Reason |
|---|---|---|
| 2026-11-14 | 2D side-on view, one tilt axis | Matches the brief's gravity and drag description; small scope; same controls on mouse and touch |
| 2026-11-14 | Plate on a free pivot, crowned surface, viscous-only goo grip | Guarantees no stable point by construction |
| 2026-11-14 | "Loses within 20 s with no input" is a tested invariant for every kit | Keeps unlocks and powerups from accidentally creating a safe state |
| 2026-11-14 | Grab-and-drag applies a spring force, not a direct angle | Plate must obey physics; gives weight, leverage and the toss skill |
| 2026-11-14 | Hard session cap at 3:00 with a perfect-run bonus (assumed) | Brief requires a maximum session length |
| 2026-11-14 | Unlocks at best-score thresholds; three kit slots | Brief: endgame bonuses that ease plate shape, plate properties, goo properties |
| 2026-11-14 | Split leaderboards: Classic and Open | Easier kits would otherwise make scores incomparable |
