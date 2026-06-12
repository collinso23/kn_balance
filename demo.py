"""
demo.py — guided demo of the kn-balance paper, built on kn_explorer.

Walks the trajectory of kn_edge_class_balance.md point by point, regenerating
every figure the argument rests on: the forced "sacred geometry" shapes, the
parity mechanism, the inversion stress test, the K_5/K_6 balance theorem, and
the Ramsey retraction.

Usage:
  python demo.py            # write all assets to demo/ (referenced by DEMO.md)
  python demo.py --tour     # live tour: narrative + figures (close window to advance)
"""

import argparse
import math
import os
import textwrap

import matplotlib.pyplot as plt

import kn_explorer as ke

OUT_DIR = "demo"
GIF_INTERVAL = 40  # ms per frame for morph animations


def _finish(fig, out, name, anim=None):
    """Tour mode (out=None): show the figure. Asset mode: save it into out/."""
    if out is None:
        plt.show()
    elif anim is not None:
        ke._save_or_show(anim, os.path.join(out, name), GIF_INTERVAL)
    else:
        path = os.path.join(out, name)
        fig.savefig(path, dpi=110, bbox_inches="tight")
        print(f"Saved {path}")
    plt.close(fig)


def _equalize(ax, color="#534AB7", lw=1.6, alpha=0.85):
    """Uniform edge styling for figures that assert *equal counts* — the
    class styling (faint gray vs bold purple) would visually contradict
    the equality the figure exists to show."""
    for line in ax.lines:
        line.set(color=color, linewidth=lw, alpha=alpha)


def _gap_circle(ax, radius):
    ax.add_patch(plt.Circle((0, 0), radius, fill=False, linestyle="--",
                            edgecolor="#C2402A", linewidth=1.3))


# ---------------------------------------------------------------- scenes

def scene_forced_shapes(out):
    fig, ax = plt.subplots(figsize=(6, 6))
    anim = ke._morph_animation(fig, [(ax, "full", None)], 3, 10,
                               GIF_INTERVAL, ke.MORPH_HOLD, ke.MORPH_STEPS)
    _finish(fig, out, "01_forced_shapes.gif", anim=anim)


def scene_parity(out):
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.5))
    ke.draw_kn(axes[0], 7, title="K_7 — odd: no chord through the center")
    ke.draw_kn(axes[1], 8, title="K_8 — even: center filled")
    ke.draw_kn(axes[2], 8, mode="antionly", title="K_8 — the 4 antipodal diameters")
    fig.suptitle("§3.2  Antipodality is parity-gated: |i−j| = n/2 needs even n",
                 fontsize=11)
    plt.tight_layout()
    _finish(fig, out, "02_parity_mechanism.png")


def scene_inversion_static(out):
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.5))
    for ax, (mode, label) in zip(axes, ke.INVERSION_PANELS):
        ke.draw_kn(ax, 8, mode, title=f"{label} (n=8)")
    fig.suptitle("§3.3  " + ke.INVERSION_SUPTITLE, fontsize=11)
    plt.tight_layout()
    _finish(fig, out, "03_inversion_test.png")


def scene_inversion_morph(out):
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.5))
    fig.suptitle("§3.3  " + ke.INVERSION_SUPTITLE, fontsize=11)
    panels = [(ax, m, l) for ax, (m, l) in zip(axes, ke.INVERSION_PANELS)]
    anim = ke._morph_animation(fig, panels, 4, 9,
                               GIF_INTERVAL, ke.MORPH_HOLD, ke.MORPH_STEPS)
    plt.tight_layout()
    _finish(fig, out, "04_inversion_morph.gif", anim=anim)


def scene_gap_law(out):
    fig, axes = plt.subplots(1, 2, figsize=(11, 5.5))
    gap7, hole8 = math.sin(math.pi / 14), math.sin(math.pi / 8)
    ke.draw_kn(axes[0], 7, title=f"K_7 — predicted gap radius sin(π/14) ≈ {gap7:.2f}")
    _gap_circle(axes[0], gap7)
    ke.draw_kn(axes[1], 8, mode="noanti",
               title=f"K_8 − diameters — predicted hole sin(π/8) ≈ {hole8:.2f}")
    _gap_circle(axes[1], hole8)
    fig.suptitle("Appendix A: the gap law — a class-k chord sits at cos(πk/n) "
                 "from the center", fontsize=11)
    plt.tight_layout()
    _finish(fig, out, "05_gap_law.png")


def scene_balance(out):
    ke.cmd_stats(3, 12)
    print()
    fig, axes = plt.subplots(1, 2, figsize=(11, 5.5))
    ke.draw_kn(axes[0], 5)
    ke.draw_kn(axes[1], 6)
    fig.suptitle("§3.5  The only balanced K_n: 5 (odd family) and 6 (even family)",
                 fontsize=11)
    plt.tight_layout()
    _finish(fig, out, "06_balance_points.png")


def scene_pentagon_pentagram(out):
    fig, axes = plt.subplots(1, 2, figsize=(11, 5.5))
    ke.draw_kn(axes[0], 5, mode="adjonly", title="pentagon: the 5 adjacent edges")
    ke.draw_kn(axes[1], 5, mode="inneronly", title="pentagram: the 5 inner edges")
    for ax in axes:
        _equalize(ax)
    fig.suptitle("§3.5  K_5 splits its boundary and interior 5 + 5", fontsize=11)
    plt.tight_layout()
    _finish(fig, out, "07_pentagon_pentagram.png")


def scene_k6_decomposition(out):
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.5))
    ke.draw_kn(axes[0], 6, mode="adjonly", title="hexagon: 6 adjacent edges")
    ke.draw_kn(axes[1], 6, mode="inneronly", title="inner: 6 edges")
    ke.draw_kn(axes[2], 6, mode="antionly", title="diameters: 3 edges")
    _equalize(axes[0])
    _equalize(axes[1])
    fig.suptitle("§3.5  K_6 splits 15 edges as 6 + 6 + 3 — inner equals adjacent",
                 fontsize=11)
    plt.tight_layout()
    _finish(fig, out, "08_k6_decomposition.png")


def scene_random_palette(out):
    # Seeded so reruns reproduce the committed GIF byte-for-byte instead of
    # bloating git history with a fresh 2 MB palette every regeneration.
    ke.seed_random_colors(56)
    fig, ax = plt.subplots(figsize=(6, 6))
    anim = ke._morph_animation(fig, [(ax, "full", None)], 4, 8,
                               GIF_INTERVAL, ke.MORPH_HOLD, ke.MORPH_STEPS,
                               random_colors=True)
    _finish(fig, out, "09_random_palette.gif", anim=anim)


SCENES = [
    ("The forced shapes (section 2)",
     """
     The session began with an animation of K_n for rising n and the remark
     that it "creates the sacred geometry" - 3 triangle, 4 cross, 5 star.
     The first real insight: these shapes are forced, not designed. A circle
     is the only layout that privileges no point, and full connectivity
     determines everything else, so every culture that draws "n equal
     things, all related" arrives at the same images. Watch the forms grow
     out of each other.
     """,
     scene_forced_shapes),

    ("The parity mechanism (sections 3.1-3.2)",
     """
     The opening also carried the first error: a claimed "cycles of ten"
     pattern in the filled/empty centers. Engaging with it (not dismissing
     it) led to the corrected observation - the alternation tracks odd/even.
     Mechanism: points i and j are antipodal exactly when |i - j| = n/2,
     which requires even n. Even n puts n/2 diameters through the exact
     center; odd n leaves a visible gap.
     """,
     scene_parity),

    ("The inversion stress test (section 3.3)",
     """
     Hypothesis at this point: "antipodality fills the center." The
     inversion operator attacks it: remove exactly the antipodal chords -
     the center should empty. At n = 8 it largely does: the middle panel
     has an open central hole. The original session read this panel as
     "still partially fills"; the v0.2 gap law shows that reading belongs
     to the large-n regime, where the hole shrinks like pi/n and
     near-center crossing density (C(n,4)-driven) climbs. The conclusion
     stands either way: antipodality is necessary but not sufficient, and
     the filled center is two mechanisms superposed - exact central
     crossings plus near-center density.
     """,
     scene_inversion_static),

    ("The inversion test, animated",
     """
     The same three panels morphing over n = 4..9. In the right panel the
     diameters dissolve and reappear as parity flips - the parity gate of
     section 3.2, watched in real time.
     """,
     scene_inversion_morph),

    ("The gap law (v0.2 addendum, Appendix A)",
     """
     A chord connecting points k steps apart sits at distance cos(pi*k/n)
     from the center, so the empty region is predictable exactly: odd-n
     gap radius sin(pi/(2n)), and with diameters removed from even K_n, a
     hole of radius sin(pi/n) - at small n roughly twice the gap of the
     odd neighbors. The dashed circles are the predictions; the renderings
     fill everything outside them. This formula did to section 3.3 what
     section 3.3 did to section 3.2.
     """,
     scene_gap_law),

    ("The balance theorem (sections 3.4-3.5)",
     """
     Asked for more patterns, the AI claimed K_5 was the unique point where
     inner edges equal adjacent edges - and "corrected" the human's report
     that K_6 balances too. The human pushed back: re-check your math. The
     error was taxonomy decay: the AI had built the three-class split
     (adjacent / antipodal / inner) two turns earlier and failed to apply
     it. Under the correct taxonomy K_6 = 6 + 3 + 6: inner equals adjacent.
     The human was right. The theorem: for odd n, inner = adjacent forces
     n = 5; for even n it forces n = 6. One linear equation per parity
     family, one solution each, never again. See the [BALANCED] rows above.
     """,
     scene_balance),

    ("Pentagon equals pentagram (section 3.5)",
     """
     What balance means structurally: in K_5 the boundary pentagon and the
     interior pentagram carry exactly equal edge weight, 5 and 5. The
     sensation - reported across cultures for millennia - that the
     pentagram is "complete" or "in equilibrium" has a literal
     combinatorial referent. Both panels are drawn with identical styling
     because the point is the equality.
     """,
     scene_pentagon_pentagram),

    ("The K_6 decomposition (section 3.5)",
     """
     The even balance point has the same structural reading: K_6 splits
     its 15 edges as hexagon 6 + inner 6 + diameters 3. Inner equals
     adjacent here too - the hexagram is the even family's last balanced
     graph, with the three diameters as the parity surplus the odd family
     never has.
     """,
     scene_k6_decomposition),

    ("The Ramsey overclaim and the open questions (sections 3.6, 5)",
     """
     Near the end, the AI found that 5 and 6 also mark the Ramsey threshold
     R(3,3) = 6 and declared the balance point "marks exactly this
     transition." On an explicitly requested audit, the claim failed: edge-
     class balance belongs to a specific geometric drawing; Ramsey numbers
     are layout-independent. Shared constants are a prompt for
     investigation, never a conclusion. The connection was demoted to an
     open question, alongside: perceptual correlates of the K_5 balance
     point, analogous taxonomies for other layouts, and whether these
     failure signatures (momentum errors, taxonomy decay, resolution
     hunger) recur across sessions.
     """,
     None),

    ("Coda: the companion toolkit (section 6)",
     """
     Every figure above is regenerable from kn_explorer.py - stats tables,
     static class views, the inversion panels, smooth morphs, GIF export,
     and a per-edge random palette (shown here) for generating
     perception-study stimuli for the open question in section 5.
     """,
     scene_random_palette),
]


def main():
    p = argparse.ArgumentParser(description="Guided demo of the kn-balance paper")
    p.add_argument("--tour", action="store_true",
                   help="interactive tour (close each window to advance) "
                        "instead of writing assets to demo/")
    args = p.parse_args()

    out = None if args.tour else OUT_DIR
    if out is not None:
        os.makedirs(out, exist_ok=True)

    for i, (title, narrative, fn) in enumerate(SCENES, 1):
        print(f"\n{'=' * 72}\n[{i}/{len(SCENES)}] {title}\n{'=' * 72}")
        print(textwrap.fill(" ".join(narrative.split()), width=72))
        print()
        if fn is not None:
            fn(out)
        elif args.tour:
            input("(press Enter to continue)")

    if out is not None:
        print(f"\nAll assets written to {out}/ — open DEMO.md for the walkthrough.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        plt.close("all")
        print("\nInterrupted.")
