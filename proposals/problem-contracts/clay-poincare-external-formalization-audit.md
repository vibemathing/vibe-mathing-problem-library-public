# External Lean formalization audit — `problem:clay-poincare`

Status: **discovery/dependency audit only**. External repositories are untrusted research inputs until their exact source, theorem statements, dependency pins, build receipts, and axioms are independently checked. No external project is admitted here as proof of the Poincaré conjecture.

## 1. Rejected as a closure source: `gobbleyourdong/open_problems`

Repository inspected:

- `https://github.com/gobbleyourdong/open_problems`
- Poincaré folder: `math/poincare_conjecture/lean/`

The repository's human status table labels its Poincaré campaign `SOLVED (12/12)`, but direct source inspection shows that the Lean files do not encode or prove the frozen Poincaré theorem.

### Statement-faithfulness failures

`math/poincare_conjecture/lean/RicciFlow.lean` contains:

```lean
def SimplyConnected (M : Type*) : Prop := sorry

def PoincareConjecture : Prop :=
  ∀ M : Type*,
    SimplyConnected M → True
```

Thus the displayed `PoincareConjecture` does not conclude a homeomorphism to `S³`, does not require a topological 3-manifold structure, and depends on a live `sorry` in its simple-connectivity placeholder.

The same file also replaces decisive topological claims by trivial propositions, for example:

```lean
theorem bonnet_myers_finite_pi1 : True := trivial
theorem connected_sum_spheres_is_sphere : True := trivial
```

and ends the proof-structure theorem in `True`.

`SurgerySurvival.lean` likewise packages structural geometric assertions as scalar/placeholder propositions, including:

```lean
def SurgeryIsLocal : Prop := True
...
theorem poincare_complete_outline : True := trivial
```

The proved real inequalities in these files may be valid elementary lemmas, but they do not supply the missing Ricci-flow, surgery, extinction, or three-manifold topology theorems.

### Disposition

This project is **not reusable as Poincaré closure evidence** under the mission's assurance boundary. Its “12/12”/“SOLVED” metadata is not imported. Any future reuse must be restricted to individually audited elementary lemmas whose exact statements are useful independently of the placeholder architecture.

## 2. Promising same-pin auxiliary source: `Arthur742Ramos/lean-poincare-formalization-plan`

Repository inspected at:

- repository: `https://github.com/Arthur742Ramos/lean-poincare-formalization-plan`
- audited master head: `d37c5d8433226cf29809dc3fa398f165f4c81625`
- license: Apache-2.0

This project explicitly states that the Poincaré conjecture is **not yet formalized** there. Its current status page separates proved/supporting/conditional/open/future milestones and keeps the general Ricci-flow local existence-and-uniqueness milestone open.

### Exact toolchain compatibility

Its main `curvature/` project pins exactly the same environment currently used by our isolated verifier probe:

- `curvature/lean-toolchain`: `leanprover/lean4:v4.33.0`;
- `curvature/lakefile.toml`: Mathlib `db584cd6d46c92f209a44c0f1c829460d327499d`.

The project also depends locally on its sibling `HamiltonIveyReaction` package.

This exact pin match materially lowers integration risk compared with importing a library built against another Mathlib revision. It does not by itself establish trust or compatibility with the target repository's future dependency policy.

### Reported milestone boundary

The repository's current status authority reports:

1. Riemannian curvature — **Proved**;
2. curvature identities and existence — **Proved**;
3. time-dependent geometry — **Proved**;
4. Ricci-flow local existence and uniqueness — **Open**;
5–15 — downstream/future, with supporting results in some layers.

For Point 4 it defines an executable audit with five hard gates:

- no `sorry`/`admit`/locally declared `axiom`/other configured escape tokens in the library source;
- `lake build` succeeds;
- an unconditional general compact-manifold target theorem exists;
- `#print axioms` is limited to the accepted foundational axioms (`propext`, `Classical.choice`, `Quot.sound`);
- the elaborated target type carries no hidden restrictive binders.

At the current documented frontier, the unconditional target is absent, so Point 4 remains open. This honesty is consistent with our mission boundary.

### Concrete reusable surface observed

`curvature/PoincareCurvature.lean` imports a substantial library of proof-bearing infrastructure, including modules for:

- matrix/tensor smoothness and inverse derivatives;
- continuous/smooth vector-bundle sections;
- curvature, sectional curvature, Bianchi and contracted-Bianchi identities;
- Ricci norms, raised Ricci, connection/scalar Laplacians and maximum-principle support;
- time-dependent covariant-derivative geometry;
- metric inverse variation and scalar-curvature evolution;
- Hamilton–Ivey spectrum/support/reaction-related infrastructure;
- Ricci–DeTurck reaction assembly;
- Euclidean heat/Duhamel/Schauder and tensor-heat analytic PDE infrastructure;
- finite-atlas localization and reconstruction machinery.

This directly addresses lower-level gaps absent from the pinned raw Mathlib.

### Caveats still requiring independent verification

- `curvature/Challenge.lean` intentionally contains `sorry`; it is not the library proof surface and must never be imported as evidence.
- Search results that mention “sorry-free” in comments are not a substitute for running the project's lexical audit and build on a frozen commit.
- The current master push has successful documentation workflow evidence, but a documentation workflow is not a clean build receipt for the full `curvature/` library.
- Milestones 1–3 should remain **candidate reusable dependencies** until exact target theorem names, source files, clean build receipts, and `#print axioms` outputs are independently reproduced or otherwise verified.
- Point 4 remains open even in this external project; later Perelman layers remain far from a complete Poincaré proof.

## 3. Integration decision for this mission

After canonical admission of `problem:clay-poincare`, the preferred dependency strategy should be evaluated in this order:

1. audit the exact reusable modules/theorems from `Arthur742Ramos/lean-poincare-formalization-plan` at a frozen commit;
2. reproduce their build/axiom receipts in an independent clean environment on the same Lean/Mathlib pin;
3. check repository policy for adding an auxiliary dependency or vendoring licensed source with provenance;
4. reuse verified milestones 1–3 rather than reimplementing them from raw Mathlib when statement and trust checks pass;
5. take the true frontier as the first missing unconditional dependency, currently general compact-manifold Ricci-flow local existence/uniqueness in that program;
6. keep every later surgery/extinction/topological bridge as explicit open obligations until genuinely proved.

## Claim boundary

This audit establishes only source-level facts and a promising dependency candidate. It does not certify the external library, does not admit it into the target repository, and does not reduce the final assurance requirements for the Poincaré theorem.
