#!/usr/bin/env python3
"""Reference prototype of the Slime Balance simulation (plate + soft-body goo).

Not shipped. It exists to (1) prove the algorithm in ARCHITECTURE.md works,
(2) give starting parameter values, (3) serve as the reference when porting to
GDScript. Pure standard library. Coordinates: x right, y DOWN, pivot at origin.
Plate angle theta > 0 means the right rim is lower.

Usage: python3 tools/reference_sim.py            # prints the scenario report (about a minute)
       python3 tools/reference_sim.py --check    # fast design-invariant check, exit 1 on failure
"""
import math, random, sys

P = dict(
    dt=1 / 120, iters=4, g=9.8,
    # plate
    W=3.0, crown=0.20, thick=0.30, inertia=6.0, ang_damp=1.5, theta_max=0.70,
    lip=0.0,            # raised rim height (kit pieces / Rim Guard)
    # grab spring
    k_grab=60.0, c_grab=8.0, f_max=80.0,
    # goo
    n=28, mass=1.0, r0=0.70, fill=0.65, firmness=0.0, edge_stiff=1.0,
    # ramp over heat h in [0,1]  (h = t / cap)
    cap=180.0, drag0=2.0, drag1=0.1, size0=1.0, size1=1.5, wob0=1.0, wob1=9.0,
    lose_margin=0.75,
)

def lerp(a, b, t): return a + (b - a) * t

class Sim:
    def __init__(s, p=P, seed=1, drop_x=0.0, heat_fixed=None):
        s.p = dict(p); s.rng = random.Random(seed)
        s.t = 0.0; s.theta = 0.0; s.omega = 0.0; s.goo_torque = 0.0
        s.heat_fixed = heat_fixed
        n = s.p['n']; r = s.p['r0']
        s.rest = [(r * math.cos(2 * math.pi * i / n), r * math.sin(2 * math.pi * i / n)) for i in range(n)]
        cy = -s.p['crown'] - r - 0.05
        s.pos = [(drop_x + x, cy + y) for x, y in s.rest]
        s.vel = [(0.0, 0.0)] * n
        s.ph = [s.rng.uniform(0, 6.28) for _ in range(3)]
        s.lost = False; s.contacts = 0

    # --- plate helpers -------------------------------------------------
    def heat(s): return s.heat_fixed if s.heat_fixed is not None else min(1.0, s.t / s.p['cap'])
    def surf(s, x):
        p = s.p; u = x / p['W']
        y = -p['crown'] * (1 - u * u)
        if p['lip'] > 0 and abs(u) > 0.92: y -= p['lip'] * (abs(u) - 0.92) / 0.08
        return y
    def slope(s, x): return (s.surf(x + 1e-3) - s.surf(x - 1e-3)) / 2e-3
    def to_world(s, q):
        c, sn = math.cos(s.theta), math.sin(s.theta); return (q[0] * c - q[1] * sn, q[0] * sn + q[1] * c)
    def to_local(s, w):
        c, sn = math.cos(s.theta), math.sin(s.theta); return (w[0] * c + w[1] * sn, -w[0] * sn + w[1] * c)
    def centroid(s):
        n = len(s.pos); return (sum(a for a, _ in s.pos) / n, sum(b for _, b in s.pos) / n)
    def centroid_vel(s):
        n = len(s.vel); return (sum(a for a, _ in s.vel) / n, sum(b for _, b in s.vel) / n)

    # --- one tick ------------------------------------------------------
    def step(s, grabbing=False, grab_x=0.0, cursor=(0.0, 0.0)):
        p = s.p; dt = p['dt']; h = s.heat(); n = p['n']
        drag = lerp(p['drag0'], p['drag1'], h) * p.get('drag_mul', 1.0)
        size = lerp(p['size0'], p['size1'], h) * p.get('size_mul', 1.0)
        wob = lerp(p['wob0'], p['wob1'], h)
        # 1. plate: grab spring + goo reaction (from previous tick) + damping
        tau = s.goo_torque - p['ang_damp'] * s.omega
        if grabbing:
            gx = max(-p['W'], min(p['W'], grab_x))
            r = s.to_world((gx, s.surf(gx)))
            vg = (-r[1] * s.omega, r[0] * s.omega)
            f = (p['k_grab'] * (cursor[0] - r[0]) - p['c_grab'] * vg[0],
                 p['k_grab'] * (cursor[1] - r[1]) - p['c_grab'] * vg[1])
            m = math.hypot(*f)
            if m > p['f_max']: f = (f[0] * p['f_max'] / m, f[1] * p['f_max'] / m)
            tau += r[0] * f[1] - r[1] * f[0]
        s.omega += tau / p['inertia'] * dt
        s.theta += s.omega * dt
        if abs(s.theta) > p['theta_max']:
            s.theta = math.copysign(p['theta_max'], s.theta); s.omega = 0.0
        # 2. goo: external forces, predict
        ax = wob * (math.sin(1.3 * s.t + s.ph[0]) + 0.6 * math.sin(2.9 * s.t + s.ph[1]) + 0.3 * math.sin(6.1 * s.t + s.ph[2])) / 1.9
        ax += p.get('wind', 0.0)
        old = s.pos
        pos = [(x + (vx + ax * dt) * dt, y + (vy + p['g'] * dt) * dt) for (x, y), (vx, vy) in zip(old, s.vel)]
        coll = [[0.0, 0.0] for _ in range(n)]; hit = [None] * n
        L0 = 2 * p['r0'] * size * math.sin(math.pi / n)
        a_target = p['fill'] * math.pi * (p['r0'] * size) ** 2
        for _ in range(p['iters']):
            # 2a. skin: neighbour distance
            for i in range(n):
                j = (i + 1) % n
                dx = pos[j][0] - pos[i][0]; dy = pos[j][1] - pos[i][1]; d = math.hypot(dx, dy) or 1e-9
                c = 0.5 * p['edge_stiff'] * (d - L0) / d
                pos[i] = (pos[i][0] + dx * c, pos[i][1] + dy * c); pos[j] = (pos[j][0] - dx * c, pos[j][1] - dy * c)
            # 2b. volume: polygon area
            area = 0.5 * sum(pos[i][0] * pos[(i + 1) % n][1] - pos[(i + 1) % n][0] * pos[i][1] for i in range(n))
            grads = []
            for i in range(n):
                a, b = pos[(i - 1) % n], pos[(i + 1) % n]
                grads.append((0.5 * (b[1] - a[1]), 0.5 * (a[0] - b[0])))
            den = sum(gx * gx + gy * gy for gx, gy in grads) or 1e-9
            lam = -(area - a_target) / den
            pos = [(x + lam * gx, y + lam * gy) for (x, y), (gx, gy) in zip(pos, grads)]
            # 2c. firmness: shape matching to the rest circle
            k = p['firmness'] * p.get('firm_mul', 1.0)
            if k > 0:
                cx = sum(x for x, _ in pos) / n; cy = sum(y for _, y in pos) / n
                sa = sb = 0.0
                for (x, y), (qx, qy) in zip(pos, s.rest):
                    sa += qx * (x - cx) + qy * (y - cy); sb += qx * (y - cy) - qy * (x - cx)
                phi = math.atan2(sb, sa); c_, s_ = math.cos(phi), math.sin(phi)
                pos = [(x + k * (cx + size * (qx * c_ - qy * s_) - x), y + k * (cy + size * (qx * s_ + qy * c_) - y))
                       for (x, y), (qx, qy) in zip(pos, s.rest)]
            # 2d. plate collision (one-sided, from above, within the slab thickness)
            for i in range(n):
                q = s.to_local(pos[i])
                if abs(q[0]) <= p['W']:
                    ys = s.surf(q[0]); d = q[1] - ys
                    if 0 < d <= p['thick']:
                        w = s.to_world((q[0], ys))
                        coll[i][0] += w[0] - pos[i][0]; coll[i][1] += w[1] - pos[i][1]
                        pos[i] = w; hit[i] = q[0]
        # 3. velocities, viscous contact drag, reaction torque on the plate
        mi = p['mass'] / n; torque = 0.0; vel = []; s.contacts = 0
        for i in range(n):
            vx = (pos[i][0] - old[i][0]) / dt; vy = (pos[i][1] - old[i][1]) / dt
            if hit[i] is not None:
                s.contacts += 1
                r = pos[i]; sl = s.slope(hit[i]); ln = math.hypot(1, sl)
                tl = s.to_world((1 / ln, sl / ln))                     # surface tangent (world)
                vp = (-r[1] * s.omega, r[0] * s.omega)                 # plate velocity at contact
                vt = (vx - vp[0]) * tl[0] + (vy - vp[1]) * tl[1]
                dv = vt * (math.exp(-drag * dt) - 1.0)                 # viscous: no static friction
                vx += dv * tl[0]; vy += dv * tl[1]
                jx = mi * (coll[i][0] / dt + dv * tl[0]); jy = mi * (coll[i][1] / dt + dv * tl[1])
                torque += -(r[0] * jy - r[1] * jx) / dt                # plate gets -J
            vel.append((vx, vy))
        s.pos, s.vel, s.goo_torque = pos, vel, torque
        s.t += dt
        # 4. lose check: centroid below the lower rim
        rl = s.to_world((-p['W'], s.surf(-p['W']))); rr = s.to_world((p['W'], s.surf(p['W'])))
        if s.centroid()[1] > max(rl[1], rr[1]) + p['lose_margin']: s.lost = True
        return s.lost

# --- scripted players ---------------------------------------------------
def run_released(seed=1, heat=None, p=P, limit=60):
    s = Sim(p, seed, heat_fixed=heat)
    while not s.lost and s.t < limit: s.step()
    return s.t

def run_frozen(seed=1, heat=None, p=P, limit=60, grab_x=2.0, settle=1.5):
    """Player holds the plate level and never moves the cursor again."""
    s = Sim(p, seed, heat_fixed=heat); cur = (grab_x, s.surf(grab_x))
    while not s.lost and s.t < limit: s.step(True, grab_x, cur)
    return s.t

def run_bot(seed=1, delay=0.2, noise=0.0, p=P, limit=None, kp=0.35, kd=0.30, grab_x=2.5, heat=None):
    """PD controller that sees the goo `delay` seconds late: a proxy for a human."""
    s = Sim(p, seed, heat_fixed=heat); rng = random.Random(seed * 7919); hist = []
    limit = limit or p['cap']
    while not s.lost and s.t < limit:
        c = s.to_local(s.centroid()); v = s.to_local(s.centroid_vel())
        hist.append((c[0], v[0])); k = max(0, len(hist) - 1 - int(delay / p['dt'])); x, vx = hist[k]
        target = max(-0.5, min(0.5, -(kp * x + kd * vx) + rng.gauss(0, noise)))
        cs, sn = math.cos(target), math.sin(target); y = s.surf(grab_x)
        s.step(True, grab_x, (grab_x * cs - y * sn, grab_x * sn + y * cs))
    return s.t

def med(xs): xs = sorted(xs); return xs[len(xs) // 2]

def check():
    """Design invariant at heat 0: hands off loses within 10 s, frozen hand within 20 s."""
    ok = True
    for seed in (1, 2, 3):
        a = run_released(seed, 0.0); b = run_frozen(seed, 0.0)
        print('seed %d: released %.1f s (limit 10), frozen %.1f s (limit 20)' % (seed, a, b))
        ok = ok and a <= 10.0 and b <= 20.0
    return ok

if __name__ == '__main__':
    if '--check' in sys.argv:
        sys.exit(0 if check() else 1)
    seeds = range(1, 8)
    print('released, heat 0   : median %.1f s' % med([run_released(i, 0.0) for i in seeds]))
    print('frozen,   heat 0   : median %.1f s' % med([run_frozen(i, 0.0) for i in seeds]))
    print('frozen,   heat 0.5 : median %.1f s' % med([run_frozen(i, 0.5) for i in seeds]))
    for name, d, nz in (('novice', 0.35, 0.05), ('average', 0.25, 0.03), ('expert', 0.12, 0.01)):
        ts = [run_bot(i, d, nz) for i in seeds]
        print('bot %-8s delay %.2f: median %.0f s  (min %.0f, max %.0f)' % (name, d, med(ts), min(ts), max(ts)))
