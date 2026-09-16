# Source-faithfulness proposal — `problem:clay-poincare`

Status: **normalization proposal only**. This file does not perform canonical admission and does not assert that a Lean proof exists.

## Frozen mathematical target

> Every closed, simply connected topological 3-manifold is homeomorphic to the standard 3-sphere S³.

The proposed JSON contract freezes exactly this topological statement. It excludes smooth-only replacements, special cases, finite verification, conditional geometrization statements, and any use of the desired conclusion as an axiom.

## Authoritative source mapping

1. Clay Mathematics Institute, Poincaré Conjecture page: https://www.claymath.org/millennium/poincare-conjecture/
2. Clay Mathematics Institute, official problem description by John Milnor: https://www.claymath.org/wp-content/uploads/2022/02/MPPc.pdf

Milnor's official description asks whether a compact three-dimensional manifold in which the relevant closed curves contract must be homeomorphic to S³ and immediately identifies the standard formulation as: every simply connected closed 3-manifold is homeomorphic to the 3-sphere. The current Clay page identifies the Poincaré conjecture as the three-dimensional sphere being characterized by simple connectivity and records its resolution by Perelman.

The source status `Solved` is historical/source metadata. It is not placed in the ProblemContract as a mathematical Result.

## Quantifier and object audit

- Universal object: an arbitrary closed, simply connected topological 3-manifold `M`.
- Existential witness: a homeomorphism `h : M ≃ S³`.
- `closed`: compact and without boundary.
- `3-manifold`: Hausdorff and locally homeomorphic to `R^3`.
- `simply connected`: path connected with all based loops null-homotopic (equivalently, trivial fundamental group in the connected setting).
- `S³`: the unit sphere in `R^4`.
- Conclusion strength: homeomorphism.

No differentiable, PL, Riemannian, triangulation, orientability, or finite-fundamental-group hypothesis is added to the frozen theorem statement.

## Lean target-layer correspondence

For the pinned Mathlib revision used by the existing Lean verification probe (`db584cd6d46c92f209a44c0f1c829460d327499d`), the upstream file

`Mathlib/Geometry/Manifold/PoincareConjecture.lean`

contains the statement-only declaration labeled by Mathlib itself as the 3-dimensional topological Poincaré conjecture:

```lean
proof_wanted SimplyConnectedSpace.nonempty_homeomorph_sphere_three
    [T2Space M] [ChartedSpace ℝ³ M] [SimplyConnectedSpace M] [CompactSpace M] :
    Nonempty (M ≃ₜ 𝕊³)
```

Statement mapping:

- `T2Space M` — Hausdorff separation;
- `ChartedSpace ℝ³ M` — topological 3-manifold charts modeled on Euclidean 3-space, hence the boundaryless local model required by the frozen statement;
- `SimplyConnectedSpace M` — simple connectivity;
- `CompactSpace M` — compactness, completing the closed-manifold condition;
- `Nonempty (M ≃ₜ 𝕊³)` — existence of a homeomorphism to the standard 3-sphere.

This upstream `proof_wanted` is used only as a statement-identity reference. It must never be imported or treated as proof evidence for the final theorem.

## Smooth/topological boundary

Mathlib also lists a separate smooth theorem with an additional `IsManifold ... ∞ M` hypothesis and a diffeomorphism conclusion. That smooth statement is not an acceptable replacement for this contract. A future proof route may formalize a topological-to-smooth bridge (for example through 3-manifold smoothing/triangulation results) only as an explicitly proved dependency; the final theorem must retain the topological hypotheses and homeomorphism conclusion above.

## Boundary and adversarial checks

- Empty/vacuous space: excluded by simple connectivity as formalized in Mathlib, which entails path-connected/nonempty behavior; final Lean statement should preserve the exact class semantics.
- Boundary: manifolds with boundary are outside the target; using Euclidean-space `ChartedSpace` rather than a half-space model preserves this boundary.
- Dimension: fixed to 3; generalized Poincaré statements in other dimensions are outside scope.
- Homology sphere: insufficient; no substitution of homology-sphere hypotheses is allowed.
- Finite fundamental group: too broad for the exact target and not substituted for simple connectivity.
- Homotopy equivalence: weaker than the required conclusion and not accepted as closure.
- Diffeomorphism: stronger only after extra smooth structure; cannot narrow the input class.

## Remaining admission checks

An independent admission reviewer/importer should still verify:

1. source provenance and the exact Clay source wording;
2. duplicate identity against any internal canonical object;
3. the project convention for `closed`, `topological 3-manifold`, and `allowed_axioms`;
4. that the canonical record uses the frozen statement without source-status leakage;
5. that downstream provisioning copies the accepted canonical JSON byte-for-byte/digest-for-digest into `vibemathing/problem-clay-poincare` and then creates the admitted Attempt/Route/ObligationGraph packet.

Proposal assessment: **statement-faithful candidate, pending independent canonical admission**.
