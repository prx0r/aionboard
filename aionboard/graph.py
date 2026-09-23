"""Queryable knowledge graph for AI Onboard.

Loads vertical packs (manifests + profiles) and the regulations registry
into one in-memory graph: verticals -> pains -> tools, verticals ->
regulations, verticals -> packages. Powers grounded answers for the demo
chatbot and any future assistant: every answer cites its source nodes,
and nothing is invented.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
VERTICALS_ROOT = REPO_ROOT / "verticals"
REGISTRY_PATH = REPO_ROOT / "regulations" / "registry.json"

_TOKEN_PATTERN = re.compile(r"[a-z0-9]+")


def _tokens(text: str) -> set[str]:
    return set(_TOKEN_PATTERN.findall(text.lower()))


def build_graph() -> dict:
    """Build nodes and edges from vertical packs + regulations registry."""
    nodes: dict[str, dict] = {}
    edges: list[dict] = []

    with open(REGISTRY_PATH, encoding="utf-8") as handle:
        regulations = json.load(handle)["rules"]
    for rule in regulations:
        node_id = f"regulation:{rule['id']}"
        nodes[node_id] = {
            "kind": "regulation",
            "id": rule["id"],
            "text": f"{rule['law']}. {rule.get('detail', '')}",
            "source": "regulations/registry.json",
        }

    for manifest_path in sorted(VERTICALS_ROOT.glob("*/manifest.json")):
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        profile = json.loads((manifest_path.parent / "profile.json").read_text(encoding="utf-8"))
        vertical = manifest["vertical"]
        vnode = f"vertical:{vertical}"
        nodes[vnode] = {
            "kind": "vertical",
            "id": vertical,
            "text": f"{manifest.get('display_name', vertical)}: {profile['onboarding_difficulty']['level']} onboarding difficulty.",
            "source": f"verticals/{vertical}/manifest.json",
        }
        for mapping in profile.get("pain_mappings", []):
            pnode = f"pain:{mapping['pain_id']}"
            if pnode not in nodes:
                nodes[pnode] = {
                    "kind": "pain",
                    "id": mapping["pain_id"],
                    "text": f"{mapping['pain_name']} ({mapping['category']}, {mapping['verification']}).",
                    "source": f"verticals/{vertical}/profile.json",
                }
            edges.append({"from": vnode, "to": pnode, "relation": "has_pain"})
            for tool in mapping.get("current_stack", []):
                tnode = f"tool:{tool.lower()}"
                if tnode not in nodes:
                    nodes[tnode] = {
                        "kind": "tool",
                        "id": tool,
                        "text": f"{tool}: existing software to integrate or import, never replace unnecessarily.",
                        "source": f"verticals/{vertical}/profile.json",
                    }
                edges.append({"from": pnode, "to": tnode, "relation": "addressed_with"})
        for legal in profile.get("legal", []):
            rnode = f"regulation:{legal['id']}"
            if rnode in nodes:
                edges.append({"from": vnode, "to": rnode, "relation": "must_consider"})

    return {"nodes": nodes, "edges": edges}


def ask(graph: dict, question: str, limit: int = 5) -> list[dict]:
    """Keyword retrieval over graph nodes. Deterministic, no generation.

    Returns matching nodes with sources, best first. Empty question or
    no overlap returns an empty list — never a fabricated answer.
    """
    query_tokens = _tokens(question or "")
    query_tokens -= {"what", "how", "does", "do", "is", "are", "the", "a", "an", "to", "for", "my", "i", "it"}
    if not query_tokens:
        return []
    scored = []
    for node_id, node in graph["nodes"].items():
        node_tokens = _tokens(node["id"] + " " + node["text"])
        overlap = query_tokens & node_tokens
        if overlap:
            scored.append((len(overlap), node_id))
    scored.sort(key=lambda item: (-item[0], item[1]))
    return [graph["nodes"][node_id] for _, node_id in scored[:limit]]


def answer_text(results: list[dict]) -> str:
    """Render retrieved nodes as a cited answer. Admits ignorance honestly."""
    if not results:
        return (
            "I don't have verified information on that yet. "
            "Ask about a specific trade, pain point, tool, or regulation — "
            "for example 'nail no-shows' or 'MTD thresholds'."
        )
    lines = ["Here's what our research covers:"]
    for result in results:
        lines.append(f"- [{result['kind']}] {result['text']} (source: {result['source']})")
    return "\n".join(lines)
