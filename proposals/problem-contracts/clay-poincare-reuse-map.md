# Candidate reuse map — same-pin Poincaré infrastructure

Status: **candidate dependency map**. The entries below identify exact external declarations and executable audit surfaces worth independently reproducing after canonical admission. They are not admitted dependencies or proof evidence yet.

External source frozen for this map:

- repository: `Arthur742Ramos/lean-poincare-formalization-plan`;
- commit: `d37c5d8433226cf29809dc3fa398f165f4c81625`;
- license: Apache-2.0;
- Lean: `4.33.0`;
- Mathlib: `db584cd6d46c92f209a44c0f1c829460d327499d`.

The Lean/Mathlib pair exactly matches the isolated verifier environment currently used for our target-layer probes.

## 1. Levi-Civita / static curvature layer

The external project provides its own pinned-version file

`curvature/PoincareCurvature/Geometry/Manifold/VectorBundle/CovariantDerivative/LeviCivita.lean`

because the pinned raw Mathlib revision does not contain the later Mathlib `LeviCivita.lean` module.

The source imports the project's connection-existence, Riemannian-section and metric-compatibility layers plus pinned Mathlib primitives, and states that it constructs Levi-Civita connections by the standard correction formula and proves uniqueness.

Candidate declarations visible in the repository's verification/submission surface include:

- `PoincareCurvature.Palomar.exists_contMDiffLeviCivitaConnection`;
- `CovariantDerivative.IsLeviCivita`;
- curvature/Ricci/scalar-curvature comparison theorems under `IsLeviCivita`.

These should be audited before any attempt to reconstruct the same layer locally.

## 2. Explicit audited geometric-transport theorem surface

`curvature/scripts/verify-palomar.sh` freezes six theorem names as its expected geometric transport surface:

- `PoincareCurvature.Palomar.curvatureAux_pullbackCovariantDerivative`;
- `PoincareCurvature.Palomar.curvatureAux_pullbackCovariantDerivative_apply`;
- `PoincareCurvature.Palomar.torsion_pullbackCovariantDerivative`;
- `PoincareCurvature.Palomar.isTorsionFree_pullbackCovariantDerivative`;
- `PoincareCurvature.Palomar.isMetricCompatibleTangent_pullbackCovariantDerivative`;
- `PoincareCurvature.Palomar.isLeviCivita_pullbackCovariantDerivative`.

The same script freezes an auditable definition surface including:

- `CovariantDerivative.along`;
- `CovariantDerivative.curvatureAux`;
- tangent pushforward/pullback definitions for `RicciFlow.SmoothSelfDiffeomorph2`;
- pullback of covariant derivatives;
- torsion-free, metric-compatible and Levi-Civita predicates.

This is directly relevant to the diffeomorphism/gauge machinery used by a Ricci–DeTurck proof route.

## 3. What the external verification script actually checks

At the frozen commit, `curvature/scripts/verify-palomar.sh`:

1. verifies that the Mathlib manifest is pinned to `db584cd6d46c92f209a44c0f1c829460d327499d`;
2. checks source/package shape and Apache-2.0 license identity;
3. confirms `Challenge.lean` imports only Mathlib and contains exactly seven deliberate challenge holes;
4. rejects `sorry`/`admit` in `Solution.lean`;
5. rejects locally declared `axiom` or `unsafe` declarations in `Solution.lean`;
6. scans every `PoincareCurvature/**/*.lean` source file for locally declared `axiom`/`unsafe` and for `sorryAx`;
7. checks the source dependency closures of Challenge and Solution;
8. runs `lake build` and `lake build Challenge Solution`;
9. elaborates Challenge and Solution;
10. runs `#print axioms` on the six geometric-transport theorems listed above;
11. restricts the comparator's permitted axiom vocabulary to `propext`, `Quot.sound`, and `Classical.choice`.

Important boundary: the existence of this script is strong reproducibility metadata. We have not independently executed this external script in a clean environment during the current mission, so its checks remain a reproducible verification plan until replayed.

## 4. Current true frontier in the external program

The repository's authoritative Point-4 audit targets an unconditional theorem producing `IntrinsicLocalExistenceUniquenessFamily` for general compact manifolds. The audit requires:

- zero configured cheat tokens in the library;
- a successful full `lake build`;
- an unconditional target without restricted special-case or assumed chart/closure binders;
- axioms limited to `propext`, `Classical.choice`, `Quot.sound`;
- an elaborated target type faithful to the Point-4 package.

At the frozen commit the target is absent, so Point 4 remains **OPEN**. This is the earliest large missing dependency in that program's Ricci-flow route.

## 5. Mission integration order

Once `problem:clay-poincare` becomes canonically admitted, a low-duplication route is:

1. independently replay the external static-curvature / Levi-Civita package build at the frozen commit;
2. capture exact theorem types and `#print axioms` output for the subset we intend to use;
3. decide through the target repository's allowed dependency mechanism whether to pin the auxiliary repository or vendor selected Apache-2.0 modules with immutable provenance;
4. reuse only independently verified theorem surfaces;
5. focus new formalization effort at the first real missing dependency rather than re-proving already checked static geometry;
6. keep Point 4 and every Perelman layer after it as explicit open obligations.

## Claim boundary

This map identifies high-value reusable code and an executable external audit design. It does not certify the external code, does not add a dependency to the target repository, and does not claim any Poincaré proof obligation closed.
