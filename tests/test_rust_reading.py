"""The Rust suite's rules.json reaches the rule nodes: a reading per shared id, the not-applicable reasons, and no
node for an id only the unpublished suite has."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from dca_catalog import rules

REPO_ROOT = Path(__file__).resolve().parents[2]
RUST_JSON = REPO_ROOT / rules.RUST_RULES_JSON_REL

pytestmark = pytest.mark.skipif(not RUST_JSON.exists(), reason="no dca-rust checkout beside the catalog")


def _nodes():
    return {node.frontmatter["id"]: node for node in rules.extract(REPO_ROOT) if node.frontmatter.get("type") == "Rule"}


def test_every_applicable_shared_rule_carries_a_rust_reading():
    nodes = _nodes()
    rust = {entry["id"]: entry for entry in json.loads(RUST_JSON.read_text(encoding="utf-8"))["rules"]}
    missing = [rule_id for rule_id, entry in rust.items()
               if rule_id in nodes and entry.get("status") != "n/a" and "## Rust reading" not in nodes[rule_id].body]
    assert not missing, missing


def test_a_rule_not_applicable_in_rust_names_its_reason():
    nodes = _nodes()
    rust = {entry["id"]: entry for entry in json.loads(RUST_JSON.read_text(encoding="utf-8"))["rules"]}
    for rule_id, entry in rust.items():
        if entry.get("status") == "n/a":
            assert nodes[rule_id].frontmatter["not_applicable_rust"] == entry["reason"]
            assert "rust" not in nodes[rule_id].frontmatter["implementations"]


def test_rust_counts_as_an_implementation_only_where_a_test_or_the_compiler_holds_the_rule():
    nodes = _nodes()
    rust = {entry["id"]: entry for entry in json.loads(RUST_JSON.read_text(encoding="utf-8"))["rules"]}
    for rule_id, entry in rust.items():
        if rule_id not in nodes or entry.get("status") == "n/a":
            continue
        holds = bool(entry.get("implemented")) or entry.get("category") == "compiler"
        assert ("rust" in nodes[rule_id].frontmatter["implementations"]) == holds, rule_id


def test_an_unpublished_suite_gets_no_node_for_its_own_ids():
    _, published = rules._rust_catalog(REPO_ROOT)
    rust_only = [rule_id for rule_id in _nodes() if rule_id.startswith("DCA-RS-")]
    assert published or not rust_only, rust_only
