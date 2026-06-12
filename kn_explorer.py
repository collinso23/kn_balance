"""
kn_explorer.py — Complete graphs on a circle: visualizer + analysis toolkit.

Companion artifact to kn_edge_class_balance.md ("Navigating Conceptual Space").
Extends the original animate_complete_graphs() with:

  1. Edge-class taxonomy: adjacent / antipodal / inner
  2. Isolation modes (the inversion stress test from the paper, §3.3)
  3. A stats table for any range of n (verifies the balance theorem, §3.5)
  4. The original animation, preserved

Usage:
  python kn_explorer.py --stats 3 20          # print edge-class table
  python kn_explorer.py --show 6              # static K_6, all classes colored
  python kn_explorer.py --show 6 --mode noanti    # inversion test panel
  python kn_explorer.py --animate 3 12        # original animation, class-colored
  python kn_explorer.py --inversion 6         # 3-panel stress test for one n
  python kn_explorer.py --animate-inversion 3 12  # animated 3-panel stress test
  python kn_explorer.py --animate 3 12 --smooth   # smooth morphing between n values
  python kn_explorer.py --animate-inversion 3 12 --smooth --save morph.gif
  python kn_explorer.py --show 8 --random-colors  # random color per edge
"""

import argparse
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter, FFMpegWriter
from matplotlib.collections import LineCollection
from matplotlib.colors import to_rgba, hsv_to_rgb

# ---------------------------------------------------------------- taxonomy

def classify_edge(i, j, n):
    """Classify edge (i, j) of K_n on a circle: 'adjacent', 'antipodal', or 'inner'."""
    diff = abs(i - j)
    if diff == 1 or diff == n - 1:
        return "adjacent"
    if n % 2 == 0 and diff == n // 2:
        return "antipodal"
    return "inner"


def edge_counts(n):
    """Closed-form edge-class counts for K_n. Returns dict."""
    total = n * (n - 1) // 2
    adjacent = n
    antipodal = n // 2 if n % 2 == 0 else 0
    inner = total - adjacent - antipodal
    crossings = n * (n - 1) * (n - 2) * (n - 3) // 24  # C(n,4)
    return {
        "n": n, "total": total, "adjacent": adjacent,
        "antipodal": antipodal, "inner": inner, "crossings": crossings,
        "balanced": inner == adjacent,
    }


def verify_counts(n):
    """Cross-check closed forms against brute-force enumeration."""
    counts = {"adjacent": 0, "antipodal": 0, "inner": 0}
    for i in range(n):
        for j in range(i + 1, n):
            counts[classify_edge(i, j, n)] += 1
    cf = edge_counts(n)
    assert counts["adjacent"] == cf["adjacent"], f"adjacent mismatch at n={n}"
    assert counts["antipodal"] == cf["antipodal"], f"antipodal mismatch at n={n}"
    assert counts["inner"] == cf["inner"], f"inner mismatch at n={n}"
    return True


# ---------------------------------------------------------------- drawing

STYLE = {
    "adjacent":  dict(color="#888780", linewidth=0.8, alpha=0.55),
    "inner":     dict(color="#534AB7", linewidth=1.6, alpha=0.80),
    "antipodal": dict(color="#0F6E56", linewidth=2.4, alpha=0.95),
}

MODES = {
    "full":     lambda c: True,
    "noanti":   lambda c: c != "antipodal",
    "antionly": lambda c: c == "antipodal",
    "adjonly":  lambda c: c == "adjacent",
    "inneronly": lambda c: c == "inner",
}


def kn_title(n):
    """Default panel title: class counts plus the balance flag."""
    c = edge_counts(n)
    flag = "  [BALANCED]" if c["balanced"] else ""
    return f"K_{n}  adj={c['adjacent']} anti={c['antipodal']} inner={c['inner']}{flag}"


_random_color_rng = np.random.default_rng()
_random_color_cache = {}


def random_edge_color(i, j):
    """Random RGB for edge (i, j): a fresh palette each run, but cached so an
    edge keeps its color across frames, panels, and morph transitions.
    HSV-sampled to avoid the muddy/near-black colors uniform RGB produces."""
    if (i, j) not in _random_color_cache:
        hsv = (_random_color_rng.random(),
               0.55 + 0.35 * _random_color_rng.random(),
               0.65 + 0.30 * _random_color_rng.random())
        _random_color_cache[(i, j)] = tuple(hsv_to_rgb(hsv))
    return _random_color_cache[(i, j)]


def draw_kn(ax, n, mode="full", title=None, random_colors=False):
    """Draw K_n on ax with edge-class coloring, filtered by mode."""
    keep = MODES[mode]
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False) - np.pi / 2
    xs, ys = np.cos(angles), np.sin(angles)

    for i in range(n):
        for j in range(i + 1, n):
            cls = classify_edge(i, j, n)
            if keep(cls):
                style = STYLE[cls]
                if random_colors:
                    style = {**style, "color": random_edge_color(i, j)}
                ax.plot([xs[i], xs[j]], [ys[i], ys[j]], **style)

    ax.scatter(xs, ys, s=50, color="#534AB7", zorder=3)
    ax.set_aspect("equal")
    ax.axis("off")
    if title is None:
        title = kn_title(n)
    ax.set_title(title, fontsize=10)


# ---------------------------------------------------------------- morphing

CLASS_RGBA = {cls: to_rgba(s["color"], s["alpha"]) for cls, s in STYLE.items()}
CLASS_LW = {cls: s["linewidth"] for cls, s in STYLE.items()}
VERTEX_RGBA = to_rgba("#534AB7")

MORPH_HOLD = 8    # default frames held at each integer n
MORPH_STEPS = 14  # default frames per K_n -> K_{n+1} transition


def _smoothstep(t):
    return t * t * (3.0 - 2.0 * t)


def morph_frame(n, t, mode="full", random_colors=False):
    """Segments, per-edge RGBA/linewidths, and vertex data for the K_n -> K_{n+1}
    morph at time t in [0, 1).

    Vertex k sits at angle 2*pi*k/(n + t): t=0 is exactly K_n (the extra vertex
    coincides with vertex 0), t -> 1 approaches K_{n+1}, so the new vertex buds
    off the top and every other vertex glides to its new slot. Edges whose class
    differs between the two graphs crossfade styles; edges incident to the
    budding vertex fade in with t. Mode filtering folds into alpha, so filtered
    classes dissolve rather than pop.
    """
    keep = MODES[mode]
    m = n if t <= 0 else n + 1
    angles = 2 * np.pi * np.arange(m) / (n + t) - np.pi / 2
    xs, ys = np.cos(angles), np.sin(angles)

    segs, colors, lws = [], [], []
    for i in range(m):
        for j in range(i + 1, m):
            if t <= 0:
                cls = classify_edge(i, j, n)
                if not keep(cls):
                    continue
                rgba, lw = CLASS_RGBA[cls], CLASS_LW[cls]
            elif j == n:  # budding vertex's edges: fade in
                cls = classify_edge(i, j, n + 1)
                r, g, b, a = CLASS_RGBA[cls]
                rgba, lw = (r, g, b, a * t * keep(cls)), CLASS_LW[cls]
            else:  # crossfade between the K_n and K_{n+1} classifications
                c0, c1 = classify_edge(i, j, n), classify_edge(i, j, n + 1)
                (r0, g0, b0, a0), (r1, g1, b1, a1) = CLASS_RGBA[c0], CLASS_RGBA[c1]
                u = 1.0 - t
                rgba = (u * r0 + t * r1, u * g0 + t * g1, u * b0 + t * b1,
                        u * a0 * keep(c0) + t * a1 * keep(c1))
                lw = u * CLASS_LW[c0] + t * CLASS_LW[c1]
            if rgba[3] < 0.01:
                continue
            if random_colors:  # fixed per-edge hue; only alpha follows the class logic
                rgba = (*random_edge_color(i, j), rgba[3])
            segs.append([(xs[i], ys[i]), (xs[j], ys[j])])
            colors.append(rgba)
            lws.append(lw)

    verts = np.column_stack([xs, ys])
    vcolors = [VERTEX_RGBA] * m
    if t > 0:
        r, g, b, a = VERTEX_RGBA
        vcolors[n] = (r, g, b, a * t)
    return segs, colors, lws, verts, vcolors


def _morph_schedule(n_min, n_max, hold, steps):
    """(n, t) frame schedule: hold each K_n, ease into K_{n+1}, then ping-pong
    back down so the repeating loop has no jump cut."""
    forward = []
    for n in range(n_min, n_max):
        forward += [(n, 0.0)] * hold
        forward += [(n, _smoothstep(k / steps)) for k in range(1, steps)]
    forward += [(n_max, 0.0)] * hold
    backward = forward[::-1]
    if hold and len(backward) > 2 * hold:
        backward = backward[hold:-hold]  # avoid double-length pauses at the turnarounds
    return forward + backward


def _make_morph_panel(ax):
    """Persistent artists for one morph panel; frames update data, never clear."""
    ax.set_xlim(-1.15, 1.15)
    ax.set_ylim(-1.15, 1.15)
    ax.set_aspect("equal")
    ax.axis("off")
    lc = LineCollection([])
    ax.add_collection(lc)
    pts = ax.scatter([], [], s=50, zorder=3)
    return lc, pts


def _apply_morph_frame(ax, lc, pts, n, t, mode="full", label=None, random_colors=False):
    segs, colors, lws, verts, vcolors = morph_frame(n, t, mode, random_colors)
    lc.set_segments(segs)
    lc.set_colors(colors)
    lc.set_linewidths(lws)
    pts.set_offsets(verts)
    pts.set_facecolors(vcolors)
    if label is not None:
        title = f"{label} (n={n})" if t <= 0 else f"{label} (n={n}→{n + 1})"
    else:
        title = kn_title(n) if t <= 0 else f"K_{n} → K_{n + 1}"
    ax.set_title(title, fontsize=10)


def _morph_animation(fig, panels, n_min, n_max, interval, hold, steps,
                     random_colors=False):
    """Drive one or more (ax, mode, label) panels through the morph schedule."""
    artists = [_make_morph_panel(ax) for ax, _, _ in panels]
    schedule = _morph_schedule(n_min, n_max, hold, steps) or [(n_min, 0.0)]

    def update(frame):
        n, t = schedule[frame % len(schedule)]
        for (ax, mode, label), (lc, pts) in zip(panels, artists):
            _apply_morph_frame(ax, lc, pts, n, t, mode, label, random_colors)

    return FuncAnimation(fig, update, frames=len(schedule),
                         interval=interval, repeat=True)


def _save_or_show(anim, save, interval):
    """Show the animation window, or export it when --save was given."""
    if save is None:
        plt.show()
        return
    fps = max(1, round(1000 / interval))
    writer = (PillowWriter(fps=fps) if save.lower().endswith(".gif")
              else FFMpegWriter(fps=fps))
    try:
        anim.save(save, writer=writer, dpi=100)
    except (FileNotFoundError, RuntimeError) as e:
        print(f"Could not save {save}: {e}\n"
              "If ffmpeg is missing, try a .gif filename (uses Pillow instead).")
        return
    print(f"Saved {save} ({fps} fps)")


# ---------------------------------------------------------------- commands

def cmd_stats(n_min, n_max):
    """Print the edge-class table. Balance rows marked. Verifies brute force."""
    hdr = f"{'n':>3} {'total':>6} {'adjacent':>9} {'antipodal':>10} {'inner':>6} {'C(n,4)':>8}  balance"
    print(hdr)
    print("-" * len(hdr))
    for n in range(n_min, n_max + 1):
        verify_counts(n)
        c = edge_counts(n)
        mark = "<== inner = adjacent" if c["balanced"] else ""
        print(f"{c['n']:>3} {c['total']:>6} {c['adjacent']:>9} "
              f"{c['antipodal']:>10} {c['inner']:>6} {c['crossings']:>8}  {mark}")
    balanced = [n for n in range(3, 10_001) if edge_counts(n)["balanced"]]
    result = "PASS — only n=5 (odd), n=6 (even)" if balanced == [5, 6] else "FAIL"
    print(f"\nTheorem scan n=3..10000: balanced at {balanced}  ({result})")


def cmd_show(n, mode, random_colors=False):
    fig, ax = plt.subplots(figsize=(6, 6))
    draw_kn(ax, n, mode, random_colors=random_colors)
    plt.show()


INVERSION_PANELS = [
    ("full", "full K_n"),
    ("noanti", "antipodal removed"),
    ("antionly", "antipodal only"),
]
INVERSION_SUPTITLE = "Inversion stress test: is antipodality the mechanism?"


def cmd_inversion(n, random_colors=False):
    """The §3.3 stress test: full / antipodal-removed / antipodal-only."""
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.5))
    for ax, (mode, label) in zip(axes, INVERSION_PANELS):
        draw_kn(ax, n, mode, title=f"{label} (n={n})", random_colors=random_colors)
    fig.suptitle(INVERSION_SUPTITLE, fontsize=11)
    plt.tight_layout()
    plt.show()


def cmd_animate_inversion(n_min, n_max, interval=600, smooth=False, save=None,
                          hold=MORPH_HOLD, steps=MORPH_STEPS, random_colors=False):
    """Animated §3.3 stress test: the three panels evolve side by side over n."""
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.5))
    fig.suptitle(INVERSION_SUPTITLE, fontsize=11)
    panels = [(ax, mode, label) for ax, (mode, label) in zip(axes, INVERSION_PANELS)]

    if smooth:
        anim = _morph_animation(fig, panels, n_min, n_max, interval, hold, steps,
                                random_colors)
    else:
        def update(frame):
            n = n_min + (frame % (n_max - n_min + 1))
            for ax, mode, label in panels:
                ax.clear()
                draw_kn(ax, n, mode, title=f"{label} (n={n})",
                        random_colors=random_colors)

        anim = FuncAnimation(fig, update, frames=n_max - n_min + 1,
                             interval=interval, repeat=True)
    plt.tight_layout()
    _save_or_show(anim, save, interval)
    return anim


def cmd_animate(n_min, n_max, interval=600, smooth=False, save=None,
                hold=MORPH_HOLD, steps=MORPH_STEPS, random_colors=False):
    """The original animation, upgraded with edge-class coloring."""
    fig, ax = plt.subplots(figsize=(6, 6))

    if smooth:
        anim = _morph_animation(fig, [(ax, "full", None)], n_min, n_max,
                                interval, hold, steps, random_colors)
    else:
        def update(frame):
            n = n_min + (frame % (n_max - n_min + 1))
            ax.clear()
            draw_kn(ax, n, random_colors=random_colors)

        anim = FuncAnimation(fig, update, frames=n_max - n_min + 1,
                             interval=interval, repeat=True)
    _save_or_show(anim, save, interval)
    return anim


# ---------------------------------------------------------------- main

def main():
    p = argparse.ArgumentParser(description="K_n edge-class explorer")
    p.add_argument("--stats", nargs=2, type=int, metavar=("MIN", "MAX"),
                   help="print edge-class table for n in [MIN, MAX]")
    p.add_argument("--show", type=int, metavar="N", help="static K_N")
    p.add_argument("--mode", default="full", choices=list(MODES),
                   help="edge filter for --show (default: full)")
    p.add_argument("--inversion", type=int, metavar="N",
                   help="3-panel inversion stress test for K_N")
    p.add_argument("--animate", nargs=2, type=int, metavar=("MIN", "MAX"),
                   help="animate K_MIN through K_MAX")
    p.add_argument("--animate-inversion", nargs=2, type=int, metavar=("MIN", "MAX"),
                   help="animated 3-panel inversion test for K_MIN through K_MAX")
    p.add_argument("--smooth", action="store_true",
                   help="morph continuously between n values "
                        "(with --animate/--animate-inversion)")
    p.add_argument("--save", metavar="FILE",
                   help="save the animation to FILE (.gif or .mp4) instead of showing it")
    p.add_argument("--interval", type=int, default=None, metavar="MS",
                   help="animation frame interval in ms (default: 600, or 40 with "
                        "--smooth; only applies with --animate/--animate-inversion)")
    p.add_argument("--hold", type=int, default=None, metavar="FRAMES",
                   help=f"frames held at each n with --smooth (default: {MORPH_HOLD})")
    p.add_argument("--steps", type=int, default=None, metavar="FRAMES",
                   help=f"frames per morph transition with --smooth (default: {MORPH_STEPS})")
    p.add_argument("--random-colors", action="store_true",
                   help="give every edge its own random color (instead of the "
                        "class palette); new palette each run")
    args = p.parse_args()

    animating = bool(args.animate or args.animate_inversion)
    if args.interval is not None and not animating:
        p.error("--interval only applies with --animate or --animate-inversion")
    if (args.smooth or args.save) and not animating:
        p.error("--smooth/--save only apply with --animate or --animate-inversion")
    if (args.hold is not None or args.steps is not None) and not args.smooth:
        p.error("--hold/--steps only apply with --smooth")
    if args.steps is not None and args.steps < 1:
        p.error("--steps must be >= 1")
    if args.hold is not None and args.hold < 0:
        p.error("--hold must be >= 0")
    if args.random_colors and not (animating or args.show or args.inversion):
        p.error("--random-colors only applies with "
                "--show/--inversion/--animate/--animate-inversion")

    anim_kwargs = dict(
        interval=args.interval or (40 if args.smooth else 600),
        smooth=args.smooth,
        save=args.save,
        hold=args.hold if args.hold is not None else MORPH_HOLD,
        steps=args.steps if args.steps is not None else MORPH_STEPS,
        random_colors=args.random_colors,
    )

    try:
        if args.stats:
            cmd_stats(*args.stats)
        elif args.show:
            cmd_show(args.show, args.mode, random_colors=args.random_colors)
        elif args.inversion:
            cmd_inversion(args.inversion, random_colors=args.random_colors)
        elif args.animate:
            cmd_animate(*args.animate, **anim_kwargs)
        elif args.animate_inversion:
            cmd_animate_inversion(*args.animate_inversion, **anim_kwargs)
        else:
            cmd_stats(3, 16)  # sensible default
    except KeyboardInterrupt:
        plt.close("all")
        print("\nInterrupted.")


if __name__ == "__main__":
    main()
