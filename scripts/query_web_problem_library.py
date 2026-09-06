#!/usr/bin/env python3
# Query canonical contracts, private draft proposals, or private source observations.
# Run: python3 scripts/query_web_problem_library.py --collection canonical --text graph
# Requires: Python 3; read-only and offline.
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> Iterable[dict[str, Any]]:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            value = json.loads(line)
            if not isinstance(value, dict):
                raise ValueError(f"non-object JSONL record in {path}")
            yield value


def records(collection: str) -> Iterable[dict[str, Any]]:
    if collection == "canonical":
        for value in read_jsonl(ROOT / "problem-library/records/canonical-problems.jsonl"):
            yield {**value, "_collection": "canonical", "_research_eligible": value.get("lifecycle") == "active"}
    elif collection == "drafts":
        index = read_json(ROOT / "catalog/draft-index.json")
        for item in index["records"]:
            value = read_json(ROOT / item["path"])
            yield {**value, "_collection": "draft", "_research_eligible": False}
    else:
        manifest = read_json(ROOT / "catalog/source-shards.json")
        for item in manifest["shards"]:
            for value in read_jsonl(ROOT / item["path"]):
                yield {**value, "_collection": "source_observation", "_research_eligible": False}


def text_blob(record: dict[str, Any]) -> str:
    statement = record.get("statement")
    statement_text = statement.get("text", "") if isinstance(statement, dict) else record.get("statement_excerpt", "")
    categories = record.get("categories") or record.get("msc") or []
    return "\n".join([str(record.get("title", "")), str(statement_text), " ".join(map(str, categories))]).casefold()


def main() -> int:
    parser = argparse.ArgumentParser(description="Query the Web problem library; canonical is the safe default.")
    parser.add_argument("--collection", choices=("canonical", "drafts", "sources"), default="canonical")
    parser.add_argument("--text")
    parser.add_argument("--source")
    parser.add_argument("--lifecycle", choices=("draft", "active", "withdrawn"))
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if args.limit < 1:
        parser.error("--limit must be positive")
    try:
        profile = read_json(ROOT / "LIBRARY_PROFILE.json")
        if args.collection in {"drafts", "sources"} and profile.get("visibility") != "private":
            raise ValueError(f"collection {args.collection} is unavailable in the public library")
        emitted = 0
        for record in records(args.collection):
            if args.text and args.text.casefold() not in text_blob(record):
                continue
            if args.source:
                sources = record.get("sources")
                canonical_sources = [item.get("source") for item in sources] if isinstance(sources, list) else []
                if record.get("source") != args.source and args.source not in canonical_sources:
                    continue
            if args.lifecycle and record.get("lifecycle") != args.lifecycle:
                continue
            if args.json:
                print(json.dumps(record, ensure_ascii=False, sort_keys=True))
            else:
                identity = record.get("problem_id") or record.get("id")
                print(f"{record['_collection']}\t{identity}\t{record.get('title')}\tresearch_eligible={str(record['_research_eligible']).lower()}")
            emitted += 1
            if emitted >= args.limit:
                break
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
