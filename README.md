# Vibe Mathing Web Problem Library (public)

This is the public problem discovery and ProblemContract catalog for the Web GPT + GitHub plugin solution.

It is one of only two total repository kinds:

1. problem library;
2. problem research template.

Concrete research happens in separately named `problem-<slug>` repositories generated from the matching-visibility template. This library does not store Attempts, EvidenceLinks, Results, or Solution views.

Start with `AGENTS.md`, `LIBRARY_PROFILE.json`, `LIBRARY_SNAPSHOT.json`, and `CATALOG.md`.

Current counts are machine-derived in `LIBRARY_SNAPSHOT.json`. Source observations and draft contracts are never research-eligible. Only an exact `active` record in `problem-library/records/canonical-problems.jsonl` may be provisioned into a concrete problem repository.

Run:

```bash
python3 -m pip install --require-hashes -r requirements-problem-library.txt
make check
```
