# Lean target audit — `problem:clay-poincare`

Status: **normalization/formalization-target audit only**. This note records a faithful Lean target and compiler-probe evidence. It does not claim a proof of the Poincaré conjecture and does not perform canonical admission.

## Frozen target

The mathematical target remains:

> Every closed, simply connected topological 3-manifold is homeomorphic to the standard 3-sphere `S³`.

No smooth-only replacement, finite verification, conditional theorem, homology-sphere substitute, or new mathematical axiom is accepted as closure.

## Pinned Lean reference

The isolated verifier probe in `vibemathing/vibe-mathing-cn-public` uses:

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

## Isolated compiler-probe history

Temporary non-merge PR:

- repository: `vibemathing/vibe-mathing-cn-public`;
- PR: `#8` — `test: Poincaré target-layer elaboration under pinned Lean`;
- branch: `tmp-poincare-target-elab-20260916`.

The PR is a disposable verifier probe and must not be merged as mathematical content.

### Earlier broad target-layer probe

An earlier head imported the simple-connectivity, Euclidean-space, charted-space, and sphere-related target dependencies together and appended the topological target layer. Workflow run `35118596970` failed in `lean-e2e`: the bounded Lean subprocess terminated with signal `6` under the verifier's `8192 MB` hard memory ceiling. This receipt did not distinguish an import/resource problem from a declaration problem.

### Reduced simple-connectivity probe — kernel success

The branch was then reduced to isolate the `SimplyConnectedSpace` dependency. Current observed head:

- commit `ceb15dbb5b49a8262be90948a880c83e8d879e20`;
- CI workflow run `35124484438` (`CI` run #35);
- `production-loop`: **success**;
- `validate`: **success**;
- production-loop maturity audit: `100/100 PASS`;
- `lean-e2e`: **PASS**, exit code `0`.

The reduced Lean source imports `Mathlib.AlgebraicTopology.FundamentalGroupoid.SimplyConnected` and kernel-checks these project declarations:

```lean
theorem pathConnectedSpace_of_simplyConnected
    (M : Type*) [TopologicalSpace M] [SimplyConnectedSpace M] :
    PathConnectedSpace M := by
  infer_instance

theorem nonempty_of_simplyConnected
    (M : Type*) [TopologicalSpace M] [SimplyConnectedSpace M] :
    Nonempty M := by
  exact (inferInstance : PathConnectedSpace M).nonempty

theorem fundamentalGroup_subsingleton_of_simplyConnected
    (M : Type*) [TopologicalSpace M] [SimplyConnectedSpace M] (x : M) :
    Subsingleton (FundamentalGroup M x) := by
  infer_instance
```

`AxiomAudit.lean` invokes `#print axioms` on all three declarations and the bounded axiom-audit Lean process exits successfully. The current verifier only exposes a coarse `axiom_clean` check in its receipt and the CI summary does not surface each declaration's printed axiom list, so this note does **not** upgrade that to a per-declaration zero-axiom claim.

The fixed verifier implementation at the PR base runs Lean with `-j1`, timeout `600s`, output cap `2,000,000` bytes, and an `8192 MB` hard memory ceiling.

### Interpretation

The successful reduced probe is real kernel evidence for the simple-connectivity interface and the three helper declarations above. It is not evidence for the Poincaré conclusion. The difference between the earlier broad failure and the reduced success strongly localizes the current compiler blocker to the heavier target dependency/import combination rather than the basic `SimplyConnectedSpace` layer.

## Next formalization checkpoints after canonical admission

1. Re-introduce the target dependencies incrementally (`EuclideanSpace`, charted-space interface, sphere subtype/homeomorphism) and keep the smallest passing import set.
2. Kernel-check the exact target proposition under the repository's fixed Lean/Mathlib revision without importing or invoking the upstream `proof_wanted` as proof.
3. Add an explicit second-countability derivation/audit so the encoded manifold convention is transparent.
4. Strengthen the axiom audit to obtain per-declaration auditable output for project theorems; reject `sorry`, `admit`, project-added axioms, and proof-wanted shortcuts.
5. Decompose the actual proof into explicit obligations. The decisive missing mathematics remains the Perelman/Hamilton Ricci-flow-with-surgery chain (or a formally complete equivalent route), plus any topological-to-smooth bridge used by that route.
6. Preserve the final theorem at the topological/homeomorphism level even if intermediate mathematics is smooth.

## Evidence boundary

Verified here:

- the exact pinned Mathlib target declaration exists as a statement reference;
- the compact charted target derives the standard second-countability convention through existing pinned Mathlib lemmas;
- the reduced simple-connectivity probe kernel-checks under Lean `4.33.0` / Mathlib `db584cd6...` with both CI jobs passing;
- the three helper declarations above compile in that fixed environment.

Still open:

- successful kernel elaboration of the full topological Poincaré target layer under the bounded verifier;
- per-declaration zero-axiom receipt for the new helpers;
- all substantive Poincaré proof obligations;
- axiom/trust audit of a future complete proof;
- independent clean-environment verification;
- canonical ProblemContract admission and downstream Attempt/Route/Obligation provisioning.
