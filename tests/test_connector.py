"""Tests for the Muse connector pack and customer dashboard mock."""

import json
import unittest
from pathlib import Path

from aionboard.website import render_dashboard, write_dashboard

REPO_ROOT = Path(__file__).resolve().parents[1]


class ConnectorTests(unittest.TestCase):
    def setUp(self):
        with open(REPO_ROOT / "connector" / "manifest.json", encoding="utf-8") as handle:
            self.manifest = json.load(handle)

    def test_connector_is_draft(self):
        self.assertEqual(self.manifest["status"], "draft-not-submitted")

    def test_capabilities_mirror_mcp_contract(self):
        with open(REPO_ROOT / "mcp" / "tools.json", encoding="utf-8") as handle:
            contract = json.load(handle)
        contract_names = {tool["name"] for tool in contract["tools"]}
        for capability in self.manifest["capabilities"]:
            kindered = {
                "business_lookup": "vertical_lookup",
                "pain_lookup": "pain_lookup",
                "install_status": "install_status",
                "opportunity_digest": None,  # new in connector, add to MCP next
                "draft_quote": "draft_quote",
            }
            expected = kindered.get(capability["name"])
            if expected is not None:
                self.assertIn(expected, contract_names)

    def test_no_placement_promises(self):
        text = json.dumps(self.manifest)
        for forbidden in ("will appear in", "guaranteed ranking", "guaranteed recommendations"):
            self.assertNotIn(forbidden, text)
        # The honest disclaimer must be present.
        self.assertIn("No guaranteed placement", text)

    def test_limitations_admit_platform_reality(self):
        limitations = " ".join(self.manifest["limitations"])
        self.assertIn("US-only", limitations)


class DashboardTests(unittest.TestCase):
    def test_dashboard_labels_demo_data(self):
        html = render_dashboard()
        self.assertIn("Demo layout", html)
        self.assertIn("DEMO DATA", html)
        self.assertIn("fictional", html.lower())

    def test_dashboard_covers_manage_areas(self):
        html = render_dashboard()
        for section in (
            "Installation status",
            "Support window",
            "Opportunities near you",
            "Your buddy",
            "Add-ons",
        ):
            self.assertIn(section, html)

    def test_dashboard_makes_no_guarantees(self):
        html = render_dashboard()
        for forbidden in (
            "appear in ChatGPT",
            "guaranteed to appear",
            "confirmed jobs",
        ):
            self.assertNotIn(forbidden, html)
        # Signals framing must be present wherever opportunities appear.
        self.assertIn("signal, not a confirmed job", html)

    def test_dashboard_links_back(self):
        html = render_dashboard()
        self.assertIn("index.html", html)
        self.assertIn("chat.html", html)

    def test_dashboard_writes_to_disk(self):
        import os
        import tempfile

        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "dashboard.html")
            self.assertEqual(write_dashboard(path), path)
            self.assertTrue(os.path.isfile(path))


if __name__ == "__main__":
    unittest.main(verbosity=2)
