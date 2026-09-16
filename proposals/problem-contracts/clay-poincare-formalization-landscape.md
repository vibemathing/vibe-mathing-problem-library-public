# Formalization landscape audit — `problem:clay-poincare`

Status: **dependency/discovery audit for normalization and future obligation planning**. This file records observed formal-library coverage and gaps. It does not prove any Poincaré obligation and does not perform canonical admission.

## Fixed environment audited

The current isolated Lean verifier probe uses:

- Lean `4.33.0`;
- Mathlib commit `db584cd6d46c92f209a44c0f1c829460d327499d`.

The final target remains the 3-dimensional topological Poincaré statement. A smooth Ricci-flow route is relevant only through explicitly proved bridges back to that target.

## Existing reusable foundations at the pinned Mathlib revision

The pinned revision has meaningful manifold/topology infrastructure already available, including:

- charted spaces and smooth-manifold infrastructure;
- fundamental groupoid / `SimplyConnectedSpace` infrastructure;
- compactness and sigma-compactness infrastructure;
- Euclidean spaces and sphere topology/manifold instances;
- Riemannian bundle/metric infrastructure;
- path length and induced Riemannian distance infrastructure;
- covariant derivative infrastructure, including metric compatibility and torsion notions.

The exact pinned directory `Mathlib/Geometry/Manifold/Riemannian/` contains only:

- `Basic.lean`;
- `PathELength.lean`.

The exact pinned directory `Mathlib/Geometry/Manifold/VectorBundle/CovariantDerivative/` contains:

- `Basic.lean`;
- `Metric.lean`;
- `Torsion.lean`.

These are useful lower-level dependencies for differential geometry, but they are far below the analytic/geometric content of Perelman's proof.

## Important pin-specific gap: Levi-Civita construction

At the pinned commit, the path

`Mathlib/Geometry/Manifold/VectorBundle/CovariantDerivative/LeviCivita.lean`

does not exist. A later Mathlib revision contains a file with that name, so this is specifically a fixed-version limitation of the current verifier environment.

Consequences for the mission:

- a Perelman/Hamilton route on the current pin cannot assume a ready-made pinned Levi-Civita connection theorem from that later file;
- either the project must implement the needed pinned-version construction from existing covariant-derivative primitives, or a controlled toolchain upgrade must be separately proposed/audited through the repository's maintenance gates;
- a toolchain upgrade, if ever admitted, still would not supply the Ricci-flow/surgery proof by itself.

## Repository-wide searches for decisive Poincaré infrastructure

Searches of Mathlib found no implementation matching the following decisive terms/interfaces:

- `Ricci flow` / `RicciFlow`;
- Ricci curvature/tensor identifiers sufficient to state the Ricci-flow PDE;
- manifold surgery in the Hamilton/Perelman sense;
- manifold `ConnectedSum` infrastructure;
- Moise's three-dimensional smoothing theorem.

Search for `Perelman` only locates the Poincaré `proof_wanted` statement/reference material, not a proof implementation.

Search for `Moise` only finds an unrelated author surname in graph-theory code, not the 3-manifold smoothing theorem.

These search negatives are discovery evidence, not a mathematical impossibility theorem. Before implementing each missing layer, exact theorem/name searches should be repeated against the frozen dependency revision and any explicitly admitted auxiliary libraries.

## Consequence for proof-route decomposition

A faithful Ricci-flow-with-surgery route requires several large obligation families that are not currently supplied as ready-made Mathlib theorems at the pin:

1. **Riemannian differential geometry completion**
   - Levi-Civita connection at the fixed pin;
   - curvature operator / Riemann tensor;
   - Ricci tensor and scalar curvature;
   - tensor evolution and analytic identities.

2. **Ricci-flow PDE layer**
   - definition of time-dependent metrics;
   - short-time existence/uniqueness and continuation theory;
   - evolution equations and maximum-principle machinery.

3. **Perelman/Hamilton singularity control**
   - curvature pinching/canonical neighborhoods at the required strength;
   - non-collapsing/reduced-volume machinery or a formally equivalent route;
   - surgery construction and preservation of hypotheses.

4. **Finite-time extinction / topological extraction**
   - extinction theorem for the simply connected/finite-fundamental-group case;
   - reconstruction of the resulting 3-manifold topology;
   - prime/connected-sum and spherical space-form ingredients as required by the chosen proof organization.

5. **Topological-to-smooth bridge**
   - an explicit dimension-three smoothing/triangulation theorem sufficient to transfer the original topological input into the smooth route;
   - a proved bridge returning the final conclusion to homeomorphism of the original topological manifold.

The frozen target cannot be closed by turning any item above into a project axiom.

## Near-term engineering implication

The highest-value short-term Lean work is to establish a faithful, kernel-checked target/interface layer and map the missing dependency DAG precisely before attempting the enormous Ricci-flow proof body. The current isolated compiler probes are therefore testing imports and elementary target semantics one layer at a time under the exact pinned environment.

## Claim boundary

Observed:

- pinned Riemannian and covariant-derivative directory contents as listed above;
- pinned absence of the later `LeviCivita.lean` module;
- repository searches described above did not surface decisive Ricci-flow/surgery/connected-sum/Moise implementations.

Open:

- exhaustive theorem-by-theorem audit of every possible synonym/module;
- construction of the missing geometric-analysis stack;
- proof of the Poincaré theorem;
- canonical ProblemContract admission and research-obligation provisioning.
