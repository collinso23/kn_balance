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
"""

import argparse
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

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


def draw_kn(ax, n, mode="full", title=None):
    """Draw K_n on ax with edge-class coloring, filtered by mode."""
    keep = MODES[mode]
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False) - np.pi / 2
    xs, ys = np.cos(angles), np.sin(angles)

    for i in range(n):
        for j in range(i + 1, n):
            cls = classify_edge(i, j, n)
            if keep(cls):
                ax.plot([xs[i], xs[j]], [ys[i], ys[j]], **STYLE[cls])

    ax.scatter(xs, ys, s=50, color="#534AB7", zorder=3)
    ax.set_aspect("equal")
    ax.axis("off")
    if title is None:
        c = edge_counts(n)
        flag = "  [BALANCED]" if c["balanced"] else ""
        title = f"K_{n}  adj={c['adjacent']} anti={c['antipodal']} inner={c['inner']}{flag}"
    ax.set_title(title, fontsize=10)


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


def cmd_show(n, mode):
    fig, ax = plt.subplots(figsize=(6, 6))
    draw_kn(ax, n, mode)
    plt.show()


INVERSION_PANELS = [
    ("full", "full K_n"),
    ("noanti", "antipodal removed"),
    ("antionly", "antipodal only"),
]
INVERSION_SUPTITLE = "Inversion stress test: is antipodality the mechanism?"


def cmd_inversion(n):
    """The §3.3 stress test: full / antipodal-removed / antipodal-only."""
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.5))
    for ax, (mode, label) in zip(axes, INVERSION_PANELS):
        draw_kn(ax, n, mode, title=f"{label} (n={n})")
    fig.suptitle(INVERSION_SUPTITLE, fontsize=11)
    plt.tight_layout()
    plt.show()


def cmd_animate_inversion(n_min, n_max, interval=600):
    """Animated §3.3 stress test: the three panels evolve side by side over n."""
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.5))
    fig.suptitle(INVERSION_SUPTITLE, fontsize=11)

    def update(frame):
        n = n_min + (frame % (n_max - n_min + 1))
        for ax, (mode, label) in zip(axes, INVERSION_PANELS):
            ax.clear()
            draw_kn(ax, n, mode, title=f"{label} (n={n})")

    anim = FuncAnimation(fig, update, frames=n_max - n_min + 1,
                         interval=interval, repeat=True)
    plt.tight_layout()
    plt.show()
    return anim


def cmd_animate(n_min, n_max, interval=600):
    """The original animation, upgraded with edge-class coloring."""
    fig, ax = plt.subplots(figsize=(6, 6))

    def update(frame):
        n = n_min + (frame % (n_max - n_min + 1))
        ax.clear()
        draw_kn(ax, n)

    anim = FuncAnimation(fig, update, frames=n_max - n_min + 1,
                         interval=interval, repeat=True)
    plt.show()
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
    p.add_argument("--interval", type=int, default=None, metavar="MS",
                   help="animation frame interval in ms (default: 600, "
                        "only applies with --animate/--animate-inversion)")
    args = p.parse_args()

    if args.interval is not None and not (args.animate or args.animate_inversion):
        p.error("--interval only applies with --animate or --animate-inversion")

    try:
        if args.stats:
            cmd_stats(*args.stats)
        elif args.show:
            cmd_show(args.show, args.mode)
        elif args.inversion:
            cmd_inversion(args.inversion)
        elif args.animate:
            cmd_animate(*args.animate, interval=args.interval or 600)
        elif args.animate_inversion:
            cmd_animate_inversion(*args.animate_inversion, interval=args.interval or 600)
        else:
            cmd_stats(3, 16)  # sensible default
    except KeyboardInterrupt:
        plt.close("all")
        print("\nInterrupted.")


if __name__ == "__main__":
    main()
