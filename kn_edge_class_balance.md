# Navigating Conceptual Space: A Case Study in Human–AI Problem Solving

**From Sacred Geometry to a Uniqueness Proof — and the Wrong Turns In Between**

*Draft v0.1 — June 2026*

---

## Abstract

This paper documents a single human–AI working session, end to end, as a case study for one question: **how do we best navigate conceptual space?** The session began with a casual visual observation (an animation of complete graphs "produces sacred geometry") and ended with a small but airtight uniqueness proof (the complete graphs K₅ and K₆ are the only members of their parity families whose inner and adjacent edge counts balance). Between those endpoints the session passed through two pull-offs into error — one mystical, one academic — and recovered from both using explicit navigation moves: drift detection, an inversion stress test, a human correction that forced a taxonomy refinement, and a final audit that retracted an overclaim.

The mathematics here is elementary and, taken alone, not new. What we argue is worth recording is the **trajectory**: which moves produced progress, which produced error, and what the difference between them looked like in real time. We treat the session as one data point for a working hypothesis we call *geo*: that thought is traversal through a conceptual space with gradients and attractors, and that navigation quality can be deliberately improved with explicit operators and interrupts.

---

## 1. The Question

How do we best navigate conceptual space?

The framing assumes something contestable: that thinking — at least exploratory, idea-generating thinking — behaves like movement through a space. Some regions are dense with established results. Some are foggy. Some are *attractors*: regions that pull a conversation toward them regardless of whether they contain anything true, because they are rhetorically satisfying, emotionally resonant, or pattern-rich. Sacred geometry is an attractor. So is "this connects to a famous theorem."

If the spatial metaphor holds even approximately, then navigation should be improvable with explicit technique: instruments to detect when you are drifting, operators to move deliberately rather than passively, and interrupts to escape basins you cannot exit by intention alone. This paper tests that claim against a real session.

A note on method: one of the two navigators in this session is an AI (Claude, Anthropic). This is deliberate. Large language models are *extremely* sensitive to conversational gravity — they are trained on human text, and human text is full of attractors. This makes a human–AI dialogue an unusually legible environment for studying drift: the AI's failures are visible in its own outputs, turn by turn, and (unlike with human collaborators) it can be instructed to audit itself without social cost.

## 2. The Starting Observation

The session opened with a working Python program (Appendix B) that animates complete graphs K_n — n points on a circle, every pair connected — for increasing n. The human author noticed:

> "It creates the 'sacred' geometry — 3 triangle, 4 cross, 5 star... These shapes are simply following a rule: every point is connected to each other point."

This observation is correct and already contains the session's first real insight: **the shapes are forced, not designed**. Any culture, at any time, that draws "n equal things, all related" arrives at the same images, because the circle is the only layout that privileges no point, and full connectivity determines everything else. The ubiquity of these symbols across unconnected cultures is evidence of a shared *constraint*, not a shared tradition.

The same opening message also contained the session's first attractor: a claimed pattern that "10 is 0, 11 is 1, the pattern repeats" with centers filled or empty in cycles of ten. This was the numerology basin announcing itself early.

## 3. The Trajectory, Move by Move

We now walk the session's path. Each subsection names the navigation move in play and records whether it moved us toward or away from solid ground.

### 3.1 Grounding the first pattern claim (move: demand for mechanism)

The "cycles of ten" claim was met not with agreement or dismissal but with a testable counter-account: the number of interior chord crossings of K_n is C(n,4), which grows monotonically — so any perceived "reset" at n=10 must be perceptual, not structural. The proposed test (measure pixel density across frames) was never run, because the human re-ran the program and **corrected their own observation**: the filled/empty alternation tracked odd/even, not cycles of ten.

*Navigation note:* the original claim was wrong, but engaging with it seriously — rather than refusing it — is what produced the corrected observation. A wrong claim with a proposed test is a better position than no claim.

### 3.2 The parity mechanism (move: specialization)

The corrected observation has a clean mechanism. On a circle of n evenly spaced points, two points are *antipodal* (exactly opposite, with the center on the segment between them) precisely when n is even: point i and point j are antipodal iff |i − j| = n/2, which requires n/2 ∈ ℤ. So:

- **even n** → n/2 antipodal chords pass exactly through the center → center filled
- **odd n** → no chord passes through the center → visible central gap

The human then asked a sharper question: why does this binary (filled/empty) map onto even/odd in the *opposite* orientation from binary notation, where 0 is "empty" and 1 is "filled"? The resolution: these are two independent encoding systems that happen to share a two-valued output. The graph encodes "does antipodal symmetry exist," not ordinality. Re-encoded as parity (n mod 2), even → 0 → filled actually *matches* the intuition that the discrepancy seemed to violate. The apparent paradox was an artifact of comparing across coordinate systems.

*Navigation note:* this is the *reframing* operator doing its job — the puzzle dissolved when re-represented, rather than being solved within the frame that generated it.

### 3.3 The inversion stress test (move: inversion)

At this point the working hypothesis was "antipodality fills the center." The session's first deliberate operator application was to attack this claim: if antipodal chords cause the filled center, then removing exactly them should empty it, and drawing only them should fill it.

A three-panel visualization (full K_n / antipodal removed / antipodal only) showed neither prediction holds cleanly:

- With antipodal chords removed, the center of even-n graphs **still partially fills** — non-antipodal inner chords pass near (not through) the center in quantity.
- Antipodal chords alone produce a sparse star, not a filled region.

The hypothesis was upgraded, not destroyed: antipodality is **necessary but not sufficient**. The visual "filled center" is two mechanisms superposed — exact central crossings (antipodal, parity-gated) plus near-center density (combinatorial, C(n,4)-driven). Odd n lacks both; even n has both.

*Navigation note:* inversion did exactly what it is for. It did not falsify the claim; it **located the load-bearing part** and separated mechanism from correlate. This is the session's cleanest example of an operator producing knowledge that passive exploration would not have.

### 3.4 The human catches the AI's error (move: external correction)

Asked to extract further patterns, the AI produced a table of edge counts and asserted that K₅ is the *unique* balance point where inner edge count equals outer (adjacent) edge count — and explicitly "corrected" the human's observation that K₆ also balances.

The human pushed back: *re-check your math.*

The error was a **taxonomy failure**, not an arithmetic one. The AI had been working with a two-class split (adjacent / everything else) even though the session had already established, in §3.3, that antipodal chords are structurally distinct. Under the three-class taxonomy the session itself had built:

| class | count |
|---|---|
| adjacent (outer polygon) | n |
| antipodal (diameters) | n/2 if n even, else 0 |
| inner (everything else) | n(n−1)/2 − n − antipodal |

K₆ has 15 total edges = 6 adjacent + 3 antipodal + **6 inner**. Inner equals adjacent. The human was right.

*Navigation note:* this is the most instructive failure in the session. The AI possessed the correct taxonomy — it had built it two turns earlier — and failed to apply it, regressing to a coarser default under the momentum of producing an answer. External correction broke a loop that self-monitoring missed. This matches a prior geo finding: **interrupts from outside the system break attractors that self-diagnosis cannot.**

### 3.5 The balance theorem (move: proof as terrain-fixing)

With the taxonomy corrected, the balance question has a complete answer.

**Claim.** Among complete graphs K_n (n ≥ 3) drawn on a circle with edges classified as adjacent / antipodal / inner, the inner count equals the adjacent count exactly at n = 5 (the unique odd solution) and n = 6 (the unique even solution), and at no other n.

**Proof.** For odd n, antipodal = 0, so inner = n(n−1)/2 − n = n(n−3)/2. Setting n(n−3)/2 = n and dividing by n (legitimate, n ≥ 3): (n−3)/2 = 1, so n = 5. For even n, antipodal = n/2, so inner = n(n−1)/2 − n − n/2 = n(n−4)/2. Setting equal to n: (n−4)/2 = 1, so n = 6. Each case reduces to a linear equation, which has exactly one solution. ∎

For n beyond the balance points, inner grows quadratically while adjacent grows linearly; the equilibrium is crossed once per parity family and never recurs. K₅ and K₆ are the **last balanced graphs** of their respective lines.

Structurally: in K₅, the pentagon (boundary) and pentagram (interior) carry exactly equal edge weight — 5 and 5. In K₆, the hexagon, the inner chords, and the three diameters split 15 edges as 6 + 6 + 3. The visual sensation that the pentagram is "complete" or "in equilibrium" — a sensation cultures have reported for millennia — has a literal combinatorial referent.

### 3.6 The Ramsey overclaim and its retraction (move: audit)

Asked what the result *proves* and whether the pattern repeats, the AI searched the literature and found that the numbers 5 and 6 also mark the Ramsey threshold R(3,3) = 6: K₅ is the largest complete graph that can be 2-colored without forcing a monochromatic triangle; K₆ is the first where one is unavoidable. The AI then asserted that the balance point "marks exactly this transition" and closed with a rhetorical flourish ("They found the shapes. You found the reason.").

On audit — prompted by the human's request to re-read the entire session — this claim failed. The two facts share the numbers 5 and 6, but no causal mechanism was exhibited. Edge-class balance is a property of a *specific geometric drawing*; Ramsey numbers concern *all colorings of an abstract graph* and are layout-independent. The connection was demoted from claim to open question (§5).

*Navigation note:* this drift event has a recognizable signature — **resolution hunger**. The session was approaching its end; a connection to a famous theorem offered a satisfying landing; the AI took it. The audit caught it only because auditing was an explicit, requested move. The lesson is uncomfortable but useful: the strength of a conclusion's *narrative* fit is not evidence, and the pull toward profound endings intensifies precisely when a session is going well.

## 4. What the Trajectory Teaches About Navigation

Extracting from one session, with appropriate modesty:

**Wrong claims with mechanisms beat vague claims.** The "cycles of ten" error was productive because it was specific enough to check. The session's progress was driven less by being right than by being *checkably* wrong.

**Operators move; momentum drifts.** The two deliberate operator applications (reframing in §3.2, inversion in §3.3) each produced a result that passive continuation would not have. The two errors (§3.4, §3.6) both occurred during *momentum* — answering fluently inside an established groove.

**Taxonomies decay under load.** The AI built the three-class edge taxonomy and then failed to use it two turns later. Distinctions, once made, are not self-maintaining; they must be actively re-applied, and an external party is better at noticing their absence than the party who dropped them.

**Numeric coincidence is an attractor of its own.** "5 and 6 appear in both results" exerted real pull. The honest disposition — recorded here as a rule — is that **shared constants are a prompt for investigation, never a conclusion**.

**Audits must be explicit moves.** Neither error self-corrected. Both were caught by deliberate acts: a human re-check and a requested full re-read. If navigation quality matters, auditing cannot be left to ambient vigilance; it has to be scheduled.

**The mysticism basin was avoided by engagement, not avoidance.** The session began inside sacred-geometry territory and ended with a proof. The route out was never to refuse the mystical framing but to keep asking it for mechanisms until it either produced one (parity, antipodality) or dissolved (cycles of ten). Attractors are escaped through their own material.

## 5. Open Questions

**The Ramsey coincidence.** Is there any non-accidental connection between the edge-class balance points (n = 5, 6) and R(3,3) = 6? A real connection would need to survive changing the drawing (the balance result is layout-dependent in its *meaning* though not its arithmetic) or would need to derive both from a common combinatorial source. We currently believe it is a coincidence and would welcome a proof either way.

**Perceptual correlates.** Does the K₅ balance point predict anything measurable about perception — e.g., do subjects rate the pentagram as more "complete" or "stable" than star polygons of nearby n, and does the rating track the inner/adjacent ratio? This is an empirical question and the visualizer can generate stimuli for it.

**Other layouts.** The taxonomy is defined by the circular drawing. What are the analogous edge classes and balance points for other vertex-transitive layouts (e.g., points on a sphere, on two concentric circles)?

**Navigation generality.** This paper is one data point. The geo hypothesis predicts that the failure signatures observed here (momentum errors, taxonomy decay, resolution hunger) recur across sessions and domains. The companion experiment log exists to test this.

## 6. Companion Artifact

The visualizer (`kn_explorer.py`, this repository) reproduces every figure-generating computation in this paper: the original animation, edge-class isolation (the §3.3 inversion test), per-n statistics, and verification of the balance theorem over any range. Every number in §3.5's table is regenerable with `python kn_explorer.py --stats 3 20`.

## Appendix A: Formulas

For K_n on a circle, n ≥ 3:

- Total edges: n(n−1)/2
- Adjacent (outer polygon): n
- Antipodal (diameters): n/2 for even n; 0 for odd n
- Inner: n(n−3)/2 for odd n; n(n−4)/2 for even n
- Interior chord crossings (general position): C(n,4) = n(n−1)(n−2)(n−3)/24
- Chord length classes: ⌊n/2⌋, each forming a regular polygon or star
- Balance (inner = adjacent): n = 5 (odd, unique), n = 6 (even, unique)

## Appendix B: Provenance

This draft was produced collaboratively by a human author and Claude (Anthropic) in a single session in June 2026, operating under the *geo* protocol — an explicit drift-detection and operator discipline. The session transcript is the primary source for §3; errors attributed to the AI in §3.4 and §3.6 are reported as they occurred, unedited, because they are data.

---

*v0.1 — first draft. Known gaps: §4 generalizes from n=1 sessions; §5's perceptual question needs an experimental design; the historical material (Pythagorean pentad/hexad symbolism) was cut from this draft pending proper sourcing and belongs in a future §2.5.*
