# Source cross-check — `problem:clay-poincare`

Status: **source-faithfulness support for normalization review**. This note does not admit a ProblemContract and does not assert a new proof.

## Direct topological statement

Primary source:

- John Milnor, *The Poincaré Conjecture*, Clay Mathematics Institute official problem description: https://www.claymath.org/wp-content/uploads/2022/06/poincare.pdf

Milnor formulates Poincaré's question for a compact three-dimensional manifold whose closed curves contract and then identifies the standard modern hypothesis as the statement that every simply connected closed 3-manifold is homeomorphic to the 3-sphere.

This supports the proposed contract's topological conclusion `homeomorphic to S³` and its universal quantification over closed simply connected 3-manifolds.

Secondary Clay landing page:

- https://www.claymath.org/millennium/poincare-conjecture/

The current Clay page describes the problem as characterizing the 3-sphere among simply connected 3-manifolds and records the historical solution by Perelman. The page's `Solved` status is source/history metadata and must not be copied into the repository's mathematical Result layer.

## Smooth proof literature and the bridge back to topology

Clay monograph:

- John Morgan and Gang Tian, *Ricci Flow and the Poincaré Conjecture*: https://www.claymath.org/library/monographs/cmim03.pdf

The monograph presents the theorem in smooth form: a closed smooth simply connected 3-manifold is diffeomorphic to `S³`. Its introduction also records the classical dimension-three smoothing fact that every topological 3-manifold admits a differentiable structure and that topological homeomorphism classification and smooth diffeomorphism classification agree in dimension three.

This has two consequences for the formalization contract:

1. A smooth Ricci-flow proof route can be mathematically relevant to the frozen topological theorem only if the topological-to-smooth bridge is represented by explicit proved dependencies.
2. The final Lean theorem must quantify over the original topological input class and conclude a homeomorphism. A theorem requiring an extra smooth-manifold hypothesis is an intermediate result, not closure of the frozen target.

## Proof-route evidence from the Clay monograph

The same Clay resource describes the proof architecture at a high level:

- Ricci flow with surgery exists through the required evolution;
- singularities are controlled using Perelman/Hamilton geometric analysis;
- for the relevant finite-fundamental-group case, Ricci flow with surgery becomes extinct in finite time;
- the Poincaré conclusion follows as a special case.

For Lean planning this means that a faithful Perelman/Hamilton route requires substantially more than a final topological lemma. The main obligation families include analytic Ricci-flow infrastructure, surgery/singularity control, finite-time extinction, 3-manifold topology reconstruction, and the dimension-three smoothing/topological bridge where smooth methods are used.

No item in this list is considered proved in the target repository merely because it is stated in the literature.

## Contract-level exclusions confirmed by the sources

The normalization proposal should reject the following substitutions:

- a 2-dimensional sphere-classification theorem;
- a generalized Poincaré theorem in another dimension;
- a theorem only for already-smooth inputs unless the topological bridge is separately proved;
- a finite-fundamental-group space-form theorem used as the final statement;
- a homology-sphere criterion;
- finite computation or bounded case checking;
- an invocation of Perelman's theorem, geometrization, Moise smoothing, or any equivalent decisive result as a newly introduced unproved axiom.

## Admission-review conclusion

The proposed ProblemContract statement

> Every closed, simply connected topological 3-manifold is homeomorphic to the standard 3-sphere `S³`.

is supported by the direct Clay/Milnor problem description. Morgan–Tian supports use of a smooth proof route only with an explicit dimension-three bridge and preserves the requirement that the repository's final theorem close the original topological/homeomorphism statement.
