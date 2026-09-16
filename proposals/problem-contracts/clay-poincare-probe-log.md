# Poincaré Lean probe log

Purpose: append-style human-readable recovery log for disposable compiler probes run in `vibemathing/vibe-mathing-cn-public#8`. These probes test the pinned Lean/Mathlib environment and target interfaces. They do not prove the Poincaré conjecture.

Pinned environment used by the probe PR:

- Lean `4.33.0`;
- Mathlib `db584cd6d46c92f209a44c0f1c829460d327499d`;
- verifier Lean command uses `-j1`, timeout `600s`, output cap `2,000,000` bytes and hard memory ceiling `8192 MB`.

## Probe A — broad topological target layer

- head: `7cba8628b2fd75dce5c4b9a1a017da1e1c2d9a23`;
- workflow: `35118596970`;
- imports included `FundamentalGroupoid.SimplyConnected`, `PiL2`, `ChartedSpace` and a topological target layer;
- `validate`: pass;
- `production-loop`: fail;
- `lean-e2e`: bounded Lean subprocess terminated by signal `6`.

Interpretation: resource/verifier failure; no kernel-success claim for the full payload.

## Probe B — simple-connectivity core

- head: `ceb15dbb5b49a8262be90948a880c83e8d879e20`;
- workflow: `35124484438`;
- import isolated to `Mathlib.AlgebraicTopology.FundamentalGroupoid.SimplyConnected`;
- kernel-checked helpers:
  - `pathConnectedSpace_of_simplyConnected`;
  - `nonempty_of_simplyConnected`;
  - `fundamentalGroup_subsingleton_of_simplyConnected`;
- `AxiomAudit.lean` ran `#print axioms` on the helpers;
- `validate`: pass;
- `production-loop`: pass;
- `lean-e2e`: pass;
- production-loop audit: `100/100 PASS`.

Interpretation: the simple-connectivity interface and these helper proofs compile in the fixed environment. The CI summary does not expose enough per-declaration axiom text to claim a complete zero-axiom audit for them.

## Probe C — compact Euclidean-charted second countability

- head: `ba072d070d194538ebb903acc906042e737d7cc7`;
- workflow: `35125093565`;
- imports isolated to `Mathlib.Analysis.InnerProductSpace.PiL2` plus `Mathlib.Geometry.Manifold.ChartedSpace`;
- intended theorem:

```lean
abbrev Euclidean3 := EuclideanSpace ℝ (Fin 3)

theorem secondCountable_of_compact_charted
    (M : Type*) [TopologicalSpace M] [ChartedSpace Euclidean3 M] [CompactSpace M] :
    SecondCountableTopology M := by
  exact ChartedSpace.secondCountable_of_sigmaCompact Euclidean3 M
```

Observed result:

- `validate`: pass;
- `production-loop`: fail;
- `lean-e2e`: bounded Lean subprocess terminated by signal `6`;
- no Lean elaboration/type error was emitted before termination.

Interpretation: under this verifier budget, the `PiL2 + ChartedSpace` import/dependency combination is already too heavy (or otherwise triggers the same bounded-runtime abort) before a useful theorem-level diagnostic is obtained. This does not refute the theorem.

## Probe D — Euclidean-space / `PiL2` import alone

- head: `b536c1649029c03f552447adaf394f3f33692932`;
- workflow: `35125601417`;
- imports isolated to `Mathlib.Analysis.InnerProductSpace.PiL2` (plus the fixture's tiny Nat import);
- attempted declaration:

```lean
abbrev Euclidean3 := EuclideanSpace ℝ (Fin 3)

theorem euclidean3_nonempty : Nonempty Euclidean3 := by
  exact ⟨0⟩
```

Observed result:

- `validate`: pass;
- `production-loop`: fail;
- `lean-e2e`: bounded Lean subprocess terminated by signal `6` after about 16 seconds of the Lean e2e phase;
- no elaboration/type error was emitted before termination.

Interpretation: the current `8192 MB` verifier envelope cannot successfully process even this minimal `PiL2`/`EuclideanSpace` probe. The failure therefore does not originate in the `ChartedSpace.secondCountable_of_sigmaCompact` proof or in the simple-connectivity layer. The next diagnostic isolates `Mathlib.Geometry.Manifold.ChartedSpace` with a lightweight model space that avoids `PiL2`.

## Current next probe

Test `Mathlib.Geometry.Manifold.ChartedSpace` without importing `PiL2`, using a lightweight model (for example `ℝ`) and the same compact-to-second-countable interface. If that passes, retain the theorem-level charted-space interface and treat `PiL2` as a verifier-resource integration blocker. If that also terminates by signal `6`, the current verifier budget is too small for the charted-manifold target layer itself and a separate verifier-budget/transport decision will be required.
