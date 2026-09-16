# Lean target audit — `problem:clay-poincare`

Status: **normalization/formalization-target audit only**. This note records a faithful Lean target and compiler-probe evidence. It does not claim a proof of the Poincaré conjecture and does not perform canonical admission.

## Frozen target

The mathematical target remains:

> Every closed, simply connected topological 3-manifold is homeomorphic to the standard 3-sphere `S³`.

No smooth-only replacement, finite verification, conditional theorem, homology-sphere substitute, or new mathematical axiom is accepted as closure.

## Pinned Lean reference

The isolated verifier probe currently available in `vibemathing/vibe-mathing-cn-public` uses:

- Lean `4.33.0`;
- Mathlib commit `db584cd6d46c92f209a44c0f1c829460d327499d`.

At that exact Mathlib commit, `Mathlib/Geometry/Manifold/PoincareConjecture.lean` contains the statement-only declaration:

```lean
proof_wanted SimplyConnectedSpace.nonempty_homeomorph_sphere_three
    [T2Space M] [ChartedSpace ℝ³ M] [SimplyConnectedSpace M] [CompactSpace M] :
    Nonempty (M ≃ₜ 𝕊³)
```

This declaration is useful only for statement correspondence. `proof_wanted` is not proof evidence and cannot be used to satisfy the final theorem.

## Statement-faithfulness audit

The class assumptions above match the frozen topological target at the intended level:

- `T2Space M` gives the Hausdorff separation convention for manifolds.
- `ChartedSpace (EuclideanSpace ℝ (Fin 3)) M` supplies boundaryless local Euclidean 3-dimensional charts.
- `SimplyConnectedSpace M` supplies simple connectivity.
- `CompactSpace M` supplies compactness.
- `Nonempty (M ≃ₜ 𝕊³)` is existence of a homeomorphism to the standard unit 3-sphere.

### Second-countability subtlety

`ChartedSpace` itself does **not** include second countability. At the pinned Mathlib revision this does not create a gap for the compact target:

1. `CompactSpace.sigmaCompact` provides `SigmaCompactSpace M` from `[CompactSpace M]` in `Mathlib/Topology/Compactness/SigmaCompact.lean`.
2. `ChartedSpace.secondCountable_of_sigmaCompact` proves `SecondCountableTopology M` from `[SecondCountableTopology H] [SigmaCompactSpace M]` in `Mathlib/Geometry/Manifold/ChartedSpace.lean`.
3. The Euclidean model `H = EuclideanSpace ℝ (Fin 3)` has the standard second-countable topology.

Therefore, for this compact Euclidean-charted target, the usual second-countability manifold convention is derivable even though it is not an explicit assumption in the upstream `proof_wanted` statement. This should be retained as a statement-faithfulness lemma/check in the eventual Lean target layer.

### Boundary convention

The chart model is Euclidean 3-space rather than a Euclidean half-space. Thus the target is the boundaryless 3-manifold version required by the classical Poincaré conjecture.

## Existing isolated compiler probe

Temporary non-merge PR:

- repository: `vibemathing/vibe-mathing-cn-public`;
- PR: `#8` — `test: Poincaré target-layer elaboration under pinned Lean`;
- final observed head: `7cba8628b2fd75dce5c4b9a1a017da1e1c2d9a23`;
- workflow run: `35118596970`.

The final probe contains only the topological target layer plus elementary consequences of simple connectivity and a homeomorphism-composition helper. It deliberately removed the smooth sphere-manifold instance import to reduce the dependency/memory footprint.

Observed workflow state:

- `validate` job: **success**;
- `production-loop` job: **failure**;
- failure occurred in the existing `lean-e2e` verifier when the bounded Lean subprocess terminated with signal `6`;
- the verifier imposes an `8192 MB` hard memory ceiling and runs `lean -j1` directly on the fixture;
- no successful kernel elaboration receipt was obtained for the appended Poincaré payload.

This receipt must be read narrowly: it identifies a verifier/resource-envelope failure. It does not establish that the candidate Lean declarations are correct or incorrect.

## Next formalization checkpoints after canonical admission

1. Create the target repository theorem with the exact topological assumptions and homeomorphism conclusion.
2. Kernel-check the target layer under the repository's fixed Lean/Mathlib revision.
3. Add an explicit second-countability derivation/audit so the encoded manifold convention is transparent.
4. Audit `#print axioms` for every theorem introduced by this project; reject `sorry`, `admit`, project-added axioms, and use of the Mathlib `proof_wanted` declaration as proof.
5. Decompose the actual proof into explicit obligations. The decisive missing mathematics remains the Perelman/Hamilton Ricci-flow-with-surgery chain (or a formally complete equivalent route), plus any topological-to-smooth bridge used by that route.
6. Preserve the final theorem at the topological/homeomorphism level even if intermediate mathematics is smooth.

## Evidence boundary

Verified here:

- the exact pinned Mathlib target declaration exists;
- the compact charted target derives the standard second-countability convention through existing pinned Mathlib lemmas;
- the isolated CI probe reached the fixed Lean verifier and failed under its bounded runtime with signal `6`.

Still open:

- successful kernel elaboration of the current Poincaré target payload;
- all substantive Poincaré proof obligations;
- axiom/trust audit of a future complete proof;
- independent clean-environment verification;
- canonical ProblemContract admission and downstream Attempt/Route/Obligation provisioning.
