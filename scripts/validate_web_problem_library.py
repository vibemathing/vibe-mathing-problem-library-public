#!/usr/bin/env python3
# Validate a standalone Web GPT problem-library repository and its visibility boundary.
# Run: python3 scripts/validate_web_problem_library.py --project-root .
# Requires: Python 3 and jsonschema; read-only and offline.
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path, PurePosixPath
from typing import Any, Iterable

from jsonschema import Draft202012Validator, FormatChecker

SNAPSHOT_EXCLUDES = {"LIBRARY_SNAPSHOT.json"}
PUBLIC_FORBIDDEN_PREFIXES = (
    "catalog/source-observations/",
    "catalog/draft-contracts/",
)
PUBLIC_FORBIDDEN_PATHS = {"catalog/source-capture-manifest.json"}
PUBLIC_PRIVATE_LOCATOR = re.compile(
    rb"\b(?:vibemathing|tradecatlabs)/[A-Za-z0-9_.-]*internal[A-Za-z0-9_.-]*\b"
)
CREDENTIAL_PATTERNS = (
    re.compile(rb"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(rb"gh[pousr]_[A-Za-z0-9]{20,}"),
    re.compile(rb"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_digest(value: Any) -> str:
    return sha256_bytes(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode())


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    values: list[dict[str, Any]] = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        value = json.loads(line)
        if not isinstance(value, dict):
            raise ValueError(f"non-object JSONL record: {path}:{number}")
        values.append(value)
    return values


def validate_instance(value: Any, schema: dict[str, Any], label: str, errors: list[str]) -> None:
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    for error in sorted(validator.iter_errors(value), key=lambda item: list(item.path))[:20]:
        errors.append(f"{label}: {error.message}")


def repository_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        if ".git" in relative.parts or "__pycache__" in relative.parts:
            continue
        if path.is_symlink():
            raise ValueError(f"symlink forbidden: {relative.as_posix()}")
        if path.is_file():
            files.append(path)
    return files


def snapshot_row(root: Path, path: Path) -> dict[str, Any]:
    relative = path.relative_to(root).as_posix()
    return {"path": relative, "bytes": path.stat().st_size, "sha256": sha256_file(path)}


def iter_shard_records(root: Path, manifest: dict[str, Any], schema: dict[str, Any], errors: list[str]) -> Iterable[dict[str, Any]]:
    digest = hashlib.sha256()
    total = 0
    ids: set[str] = set()
    for item in manifest.get("shards", []):
        relative = item.get("path")
        if not isinstance(relative, str):
            errors.append("source shard path missing")
            continue
        pure = PurePosixPath(relative)
        if pure.is_absolute() or ".." in pure.parts:
            errors.append(f"unsafe source shard path: {relative}")
            continue
        path = root / relative
        if not path.is_file() or path.is_symlink():
            errors.append(f"source shard missing: {relative}")
            continue
        data = path.read_bytes()
        digest.update(data)
        if len(data) != item.get("bytes") or sha256_bytes(data) != item.get("sha256"):
            errors.append(f"source shard digest mismatch: {relative}")
        records = read_jsonl(path)
        if len(records) != item.get("records"):
            errors.append(f"source shard count mismatch: {relative}")
        for position, record in enumerate(records, 1):
            validate_instance(record, schema, f"{relative}:{position}", errors)
            record_id = record.get("id")
            if not isinstance(record_id, str) or record_id in ids:
                errors.append(f"invalid or duplicate source observation ID: {record_id}")
            else:
                ids.add(record_id)
            total += 1
            yield record
    if total != manifest.get("record_count"):
        errors.append("source shard total does not match manifest")
    if digest.hexdigest() != manifest.get("records_sha256"):
        errors.append("source shard concatenation does not match original records digest")


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    required = {
        "AGENTS.md", "README.md", "CATALOG.md", "LIBRARY_PROFILE.json", "LIBRARY_SNAPSHOT.json",
        "Makefile", "requirements-problem-library.txt", ".github/workflows/ci.yml",
        "problem-library/records/canonical-problems.jsonl", "problem-library/records/repositories.jsonl",
        "problem-library/schema/canonical-problem.schema.json", "problem-library/schema/problem.schema.json",
        "problem-library/schema/problem-repository-record.schema.json",
        "catalog/canonical-index.json", "catalog/draft-index.json", "catalog/source-shards.json",
        "scripts/validate_web_problem_library.py", "scripts/query_web_problem_library.py",
    }
    try:
        files = repository_files(root)
    except ValueError as exc:
        return [str(exc)]
    paths = {path.relative_to(root).as_posix() for path in files}
    for relative in sorted(required - paths):
        errors.append(f"required file missing: {relative}")

    try:
        profile = read_json(root / "LIBRARY_PROFILE.json")
        snapshot = read_json(root / "LIBRARY_SNAPSHOT.json")
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return errors + [f"cannot load profile/snapshot: {exc}"]
    visibility = profile.get("visibility")
    if visibility not in {"private", "public"}:
        errors.append("profile visibility must be private or public")
    if profile.get("repository") != snapshot.get("repository") or visibility != snapshot.get("visibility"):
        errors.append("profile/snapshot repository identity mismatch")
    identity = snapshot.get("repository_identity", {})
    if identity.get("full_name") != profile.get("repository") or identity.get("visibility") != visibility:
        errors.append("snapshot verified identity does not match profile")
    binding = identity.get("binding_state")
    if binding not in {"planned", "verified"}:
        errors.append("repository identity binding must be planned or verified")
    elif binding == "verified" and (not isinstance(identity.get("database_id"), int) or not identity.get("node_id")):
        errors.append("verified repository identity requires database/node IDs")
    elif binding == "planned" and (identity.get("database_id") is not None or identity.get("node_id") is not None):
        errors.append("planned repository identity must not contain database/node IDs")
    if profile.get("role") != "problem_discovery_and_contract_admission":
        errors.append("invalid problem-library role")
    if profile.get("stores_mathematical_results") is not False:
        errors.append("problem library must not store mathematical Results")

    expected_rows = [snapshot_row(root, path) for path in files if path.relative_to(root).as_posix() not in SNAPSHOT_EXCLUDES]
    listed = snapshot.get("files")
    if listed != expected_rows:
        errors.append("snapshot file inventory differs from current tree")
    if snapshot.get("tree_sha256") != canonical_digest(expected_rows):
        errors.append("snapshot tree digest mismatch")

    try:
        canonical_schema = read_json(root / "problem-library/schema/canonical-problem.schema.json")
        source_schema = read_json(root / "problem-library/schema/problem.schema.json")
        repository_schema = read_json(root / "problem-library/schema/problem-repository-record.schema.json")
        Draft202012Validator.check_schema(canonical_schema)
        Draft202012Validator.check_schema(source_schema)
        Draft202012Validator.check_schema(repository_schema)
        canonical = read_jsonl(root / "problem-library/records/canonical-problems.jsonl")
        locators = read_jsonl(root / "problem-library/records/repositories.jsonl")
        canonical_index = read_json(root / "catalog/canonical-index.json")
        draft_index = read_json(root / "catalog/draft-index.json")
        source_manifest = read_json(root / "catalog/source-shards.json")
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        return errors + [f"cannot load library records: {exc}"]

    expected_canonical: list[dict[str, Any]] = []
    canonical_by_id: dict[str, dict[str, Any]] = {}
    for position, problem in enumerate(canonical, 1):
        validate_instance(problem, canonical_schema, f"canonical:{position}", errors)
        problem_id = problem.get("problem_id")
        if not isinstance(problem_id, str) or problem_id in canonical_by_id:
            errors.append(f"invalid or duplicate canonical problem ID: {problem_id}")
            continue
        canonical_by_id[problem_id] = problem
        slug = problem_id.split(":", 1)[-1]
        relative = f"catalog/problems/{slug}.json"
        path = root / relative
        if not path.is_file() or read_json(path) != problem:
            errors.append(f"canonical materialized record mismatch: {problem_id}")
        expected_canonical.append({
            "problem_id": problem_id,
            "lifecycle": problem.get("lifecycle"),
            "contract_sha256": canonical_digest(problem),
            "path": relative,
        })
    if canonical_index != {"schema_version": "1.0.0", "count": len(expected_canonical), "records": expected_canonical}:
        errors.append("canonical index mismatch")

    for position, locator in enumerate(locators, 1):
        validate_instance(locator, repository_schema, f"repository-locator:{position}", errors)
        problem = canonical_by_id.get(locator.get("problem_id"))
        if problem is None or locator.get("contract_sha256") != canonical_digest(problem):
            errors.append(f"repository locator is not bound to a canonical contract: {locator.get('problem_id')}")
        if visibility == "public" and locator.get("visibility") != "public":
            errors.append("public library contains non-public repository locator")

    drafts = draft_index.get("records", [])
    if draft_index.get("count") != len(drafts):
        errors.append("draft index count mismatch")
    for item in drafts:
        path = root / str(item.get("path", ""))
        if not path.is_file():
            errors.append(f"draft contract missing: {item.get('path')}")
            continue
        problem = read_json(path)
        validate_instance(problem, canonical_schema, f"draft:{item.get('path')}", errors)
        if problem.get("lifecycle") != "draft" or item.get("contract_sha256") != canonical_digest(problem):
            errors.append(f"draft contract state/digest mismatch: {item.get('path')}")

    if visibility == "private":
        if profile.get("includes_source_observations") is not True:
            errors.append("private profile must declare included source observations")
        list(iter_shard_records(root, source_manifest, source_schema, errors))
    else:
        if profile.get("includes_source_observations") is not False or source_manifest.get("record_count") != 0:
            errors.append("public profile must exclude source observations")
        if drafts:
            errors.append("public library must exclude draft ProblemContracts")
        for path in paths:
            if path in PUBLIC_FORBIDDEN_PATHS or path.startswith(PUBLIC_FORBIDDEN_PREFIXES):
                errors.append(f"public-forbidden path: {path}")

    forbidden_roots = ("research/", "result-library/", "problem-library/raw/", "problem-library/derived/")
    for path in sorted(paths):
        if path.startswith(forbidden_roots):
            errors.append(f"library contains forbidden research/raw path: {path}")
    for path in files:
        data = path.read_bytes()
        for pattern in CREDENTIAL_PATTERNS:
            if pattern.search(data):
                errors.append(f"credential-like content: {path.relative_to(root).as_posix()}")
                break
        if visibility == "public" and PUBLIC_PRIVATE_LOCATOR.search(data):
            errors.append(f"public file exposes a private repository locator: {path.relative_to(root).as_posix()}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a standalone Web problem-library repository.")
    parser.add_argument("--project-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        errors = validate(args.project_root.resolve())
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        errors = [str(exc)]
    report = {"decision": "PASS" if not errors else "BLOCK", "errors": errors}
    if args.json:
        print(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2))
    elif errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"web problem library validation: BLOCK errors={len(errors)}", file=sys.stderr)
    else:
        print("web problem library validation: PASS")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
