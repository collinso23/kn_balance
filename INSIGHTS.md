# Insights from the demo-building session (June 2026)

Working notes behind the v0.2 addenda to [the paper](kn_edge_class_balance.md).
Each item is self-contained: derivation first, then what it changes, then where
it leads. Numbers verified against `kn_explorer.py` geometry.

## 1. The chord–center distance formula

For n points evenly spaced on the unit circle, a chord connecting two points
k steps apart subtends a central angle of 2πk/n. The perpendicular from the
center bisects the chord, so the distance from center to chord is the cosine
of half the subtended angle:

> **d(k, n) = cos(πk/n)**

Two sanity checks: k = n/2 (even n) gives cos(π/2) = 0 — diameters pass through
the center exactly, recovering §3.2's parity gate. k = 1 gives cos(π/n) → 1 —
adjacent edges hug the rim.

Every edge class in the paper's taxonomy now has a *number*, not just a label.
The taxonomy's three classes are positions in a distance spectrum: adjacent at
the maximum, antipodal at zero, inner spread between.

**Gap laws** (innermost class determines the empty region around the center):

| n | innermost k | natural gap radius | hole radius, diameters removed |
|---|---|---|---|
| 5 | 2 | sin(π/10) = 0.309 | — |
| 6 | 3 (diam.) | 0 | sin(π/6) = 0.500 |
| 7 | 3 | sin(π/14) = 0.222 | — |
| 8 | 4 (diam.) | 0 | sin(π/8) = 0.383 |
| 9 | 4 | sin(π/18) = 0.174 | — |
| 10 | 5 (diam.) | 0 | sin(π/10) = 0.309 |
| 11 | 5 | sin(π/22) = 0.142 | — |
| 12 | 6 (diam.) | 0 | sin(π/12) = 0.259 |

Odd n: innermost k = (n−1)/2, gap radius cos(π/2 − π/(2n)) = **sin(π/(2n)) ≈ π/(2n)**.
Even n with antipodals removed: innermost k = n/2 − 1, hole radius **sin(π/n)** —
roughly *twice* the odd-n gap at comparable n.

## 2. What this does to §3.3 (the inversion test)

The paper reports: "with antipodal chords removed, the center of even-n graphs
still partially fills." The formula shows this is **n-dependent**:

- At small n the opposite is closer to true. K₆ minus diameters has a central
  hole of radius 0.50 — far more open than K₅ (0.31) or K₇ (0.22). K₈ minus
  diameters (0.38) is likewise more open than either odd neighbor. At these n,
  the original inversion prediction — *removing the diameters empties the
  center* — holds rather well.
- The "partial fill" impression becomes accurate as n grows: the hole shrinks
  like π/n while near-center crossing density (C(n,4)-driven) climbs steeply.

So the inversion test's conclusion ("necessary but not sufficient") stands, but
its evidential base was the large-n regime; at small n antipodality is closer
to sufficient after all. This is the paper's own method applied one level
deeper — §3.3 separated mechanism from visual correlate qualitatively; the
formula does it exactly, and finds the qualitative summary was itself partly a
perceptual artifact. (Note the pattern: every error in the session, and now
this refinement, traces to trusting a visual impression beyond its resolution.)

## 3. The perceptual 1/n fade — an experiment design

The structural parity dichotomy is absolute (a chord through the exact center
exists or it does not), but its perceptual signal is the gap radius
sin(π/(2n)) ≈ π/(2n), which fades like 1/n: K₅'s gap is 31% of the circle's
radius; K₉₉'s is 1.6% — invisible at ordinary resolution.

Prediction: subjects' ability to classify odd vs even K_n from the rendered
image degrades on a 1/n law and collapses where the gap falls below visual
acuity for the given viewing size. That turns §5's open-ended "do ratings track
the ratio?" into a psychophysics design with a known parameter. Stimulus sets
are reproducible via `kn_explorer.py --show N --random-colors --seed S` (the
random palette also decouples "filled center" judgments from the class-color
coding).

## 4. Continuous balance (speculative)

The morph (`--smooth`) realizes the K_n family as one continuous deformation:
vertex k at angle 2πk/(n+t). During transitions, the renderer assigns each edge
*fractional* class membership — the crossfade weight (1−t)·class_n + t·class_{n+1}
is literally a fractional taxonomy. This suggests treating ν = n + t as a
continuous parameter and asking: under the natural interpolation of the class
counts, is there one balance curve whose crossings are the paper's two balance
points (ν = 5 in the odd family, ν = 6 in the even family)? The odd and even
formulas — inner = n(n−3)/2 and n(n−4)/2 — differ by exactly the antipodal
count n/2, so a fractional-antipodal interpolation might unify them. Unexplored;
the morph machinery in `kn_explorer.py` already computes the needed weights.

## 5. The distance-spectrum generalization (§5 "other layouts")

"Adjacent / antipodal / inner" sounds combinatorial but is secretly metric:
the classes are the maximum, zero, and interior of the chord–center distance
spectrum d(k, n) = cos(πk/n). That reformulation transfers where the labels do
not: for points on a sphere, two concentric circles, or any vertex-transitive
layout, compute each edge's distance from the symmetry center and classify by
the spectrum's structure. The balance question ("when does the rim class weigh
as much as the interior?") is then well-posed for every such layout. This is a
concrete attack on §5's third open question.

## 6. The morph as a proof-by-exhibition of layout-dependence

Along the deformation from K_n to K_{n+1}, edge (0, n−1) changes class —
adjacent to inner — while its endpoints never change. Class is a property of
the embedding, not the vertex pair. This is the exact fact that doomed the
Ramsey connection in §3.6 (Ramsey properties are layout-independent), now
exhibited dynamically rather than argued. It also adds texture to §4's
"taxonomies decay under load": this taxonomy isn't just operationally fragile,
it is *definitionally* unstable under deformation — there was never an
intrinsic fact about which class an edge "really" belongs to.

## Queued follow-ups

All five original follow-ups (textwrap artifact, C(n,4) phrasing,
pentagon/pentagram equal styling, K₆ decomposition panel, gap-law figure)
were completed in the demo pass of 2026-06-12. Remaining open threads are the
research directions above: the psychophysics experiment (§3), continuous
balance (§4), and the distance-spectrum generalization (§5).
