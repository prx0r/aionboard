"""Tests for the knowledge graph and demo chatbot."""

import json
import unittest

from aionboard.graph import answer_text, ask, build_graph
from aionboard.website import (
    build_knowledge_bundle,
    render_chat_page,
    write_chat_page,
)


class GraphTests(unittest.TestCase):
    def setUp(self):
        self.graph = build_graph()

    def test_graph_has_nodes_and_edges(self):
        self.assertGreater(len(self.graph["nodes"]), 100)
        self.assertGreater(len(self.graph["edges"]), 100)

    def test_every_vertical_present(self):
        verticals = {
            node["id"]
            for node in self.graph["nodes"].values()
            if node["kind"] == "vertical"
        }
        for expected in ("electrician", "nails", "beauty", "cleaners"):
            self.assertIn(expected, verticals)

    def test_regulations_present(self):
        kinds = {
            node["kind"]
            for node in self.graph["nodes"].values()
            if node["kind"] == "regulation"
        }
        self.assertTrue(kinds)

    def test_ask_returns_cited_results(self):
        results = ask(self.graph, "nail no-shows deposits")
        self.assertTrue(results)
        for result in results:
            self.assertIn("source", result)
            self.assertIn("text", result)

    def test_ask_empty_or_unknown_returns_nothing(self):
        self.assertEqual(ask(self.graph, ""), [])
        self.assertEqual(ask(self.graph, "zzzqqq unknown"), [])

    def test_answer_admits_ignorance(self):
        text = answer_text([])
        self.assertIn("don't have verified information", text)

    def test_answer_cites_sources(self):
        text = answer_text(ask(self.graph, "MTD thresholds"))
        self.assertIn("source:", text)
        self.assertIn("MTD", text)


class ChatPageTests(unittest.TestCase):
    def test_chat_page_marks_demo_status(self):
        html = render_chat_page()
        self.assertIn("Demo assistant", html)
        self.assertIn("cannot access your accounts", html)
        self.assertIn("No live AI, no account access", html)

    def test_chat_page_makes_no_guarantees(self):
        html = render_chat_page()
        for forbidden in (
            "appear in ChatGPT",
            "guaranteed placement",
            "live AI receptionist",
            "grants Meta Muse access",
        ):
            self.assertNotIn(forbidden, html)

    def test_knowledge_bundle_matches_graph(self):
        import tempfile
        import os

        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "knowledge.json")
            build_knowledge_bundle(path)
            with open(path, encoding="utf-8") as handle:
                bundle = json.load(handle)
            graph = build_graph()
            self.assertEqual(len(bundle), len(graph["nodes"]))
            kinds = {node["kind"] for node in bundle}
            self.assertTrue({"vertical", "pain", "tool", "regulation"} <= kinds)


if __name__ == "__main__":
    unittest.main(verbosity=2)
