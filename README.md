# kn-balance: edge-class balance in complete graphs

Draw n points on a circle and connect every pair (the complete graph K_n). The edges
split into three natural classes: **adjacent** (the outer polygon, always n),
**antipodal** (diameters, n/2 if n is even, otherwise none), and **inner** (the rest).
Inner equals adjacent at exactly two values — n = 5 and n = 6, one per parity family,
provably never again. The pentagram and hexagram, the two shapes ancient cultures
most consistently labeled "balance" and "equilibrium," are the unique equilibrium
points of this taxonomy.

## Contents

- **`kn_edge_class_balance.md`** — the paper: *From Sacred Geometry to a Uniqueness
  Proof — and the Wrong Turns In Between.* A single human–AI session traced move by
  move, from a visual observation to a small proof, through two documented errors.
- **`kn_explorer.py`** — companion visualizer and analysis toolkit. Reproduces every
  computation in the paper.

## Quick start

```bash
pip install numpy matplotlib

python kn_explorer.py --stats 3 20      # edge-class table + balance theorem check
python kn_explorer.py --inversion 6     # the 3-panel stress test from §3.3
python kn_explorer.py --show 5          # static K_5 with edge classes colored
python kn_explorer.py --animate 3 12    # the original animation
```

## Status

Paper draft v0.1. Open questions in §5 of the paper. This work originated as
session 1 of the [geo](../geo) navigation-protocol project; the session's
navigation log lives there (`geo/sessions/2026-06-10_balance/`).
