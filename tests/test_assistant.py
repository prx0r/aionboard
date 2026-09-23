"""Tests for aionboard.assistant — per-target chatbot package."""

import json
import sqlite3
import tempfile
import unittest
from pathlib import Path

from aionboard.assistant import (
    TargetProfile,
    build_session,
    build_system_prompt,
    grant_approval,
    is_stale,
    load_powuk_signals,
    opportunities_for_target,
    profile_from_business,
    request_approval,
    rules_for_target,
)
from aionboard.security import init_approval_tables


def _profile(**kw):
    base = {"business_id": "b1", "business_name": "Test Sparks",
            "vertical": "electrician", "postcode": "M14"}
    base.update(kw)
    return TargetProfile(**base)


class TestTargets(unittest.TestCase):
    def test_identity_block(self):
        p = _profile(services=["rewire"], qualifications=["NICEIC"])
        ident = p.system_identity()
        self.assertIn("Test Sparks", ident)
        self.assertIn("NICEIC", ident)

    def test_profile_from_sparse_record(self):
        p = profile_from_business({"business_id": "x"})
        self.assertEqual(p.business_id, "x")
        self.assertEqual(p.services, [])  # gaps stay empty, never guessed

    def test_price_book_rule(self):
        p = _profile(price_book_ref="pb-2026.pdf")
        self.assertIn("Never invent prices", p.system_identity())


class TestLegislation(unittest.TestCase):
    def _registry(self, tmp):
        reg = {"rules": [
            {"id": "R1", "industries": ["electrician"], "law": "Wiring regs",
             "detail": "Part P building work", "citation": "BS 7671",
             "review_date": "2099-01-01"},
            {"id": "R2", "industries": ["electrician"], "law": "Old rule",
             "detail": "expired", "citation": "X",
             "review_date": "2020-01-01"},
            {"id": "R3", "industries": ["plumber"], "law": "Other trade",
             "detail": "x", "citation": "Y", "review_date": "2099-01-01"},
        ]}
        p = Path(tmp) / "registry.json"
        p.write_text(json.dumps(reg))
        return p

    def test_filters_vertical_and_stale(self):
        with tempfile.TemporaryDirectory() as tmp:
            reg = self._registry(tmp)
            rules = rules_for_target("electrician", registry_path=reg)
            self.assertEqual([r["id"] for r in rules], ["R1"])

    def test_topic_filter(self):
        with tempfile.TemporaryDirectory() as tmp:
            reg = self._registry(tmp)
            self.assertEqual(len(rules_for_target(
                "electrician", topic="wiring", registry_path=reg)), 1)
            self.assertEqual(rules_for_target(
                "electrician", topic="gas", registry_path=reg), [])

    def test_stale_flag(self):
        self.assertTrue(is_stale({"review_date": "2020-01-01"}))
        self.assertFalse(is_stale({"review_date": "2099-01-01"}))
        self.assertTrue(is_stale({}))


class TestPowukBridge(unittest.TestCase):
    def _powuk(self, tmp):
        base = Path(tmp) / "powuk"
        d = base / "data" / "normalized" / "planning_apps" / "2026" / "09" / "23"
        d.mkdir(parents=True)
        (d / "120000.jsonl").write_text(
            json.dumps({"title": "Single-storey extension",
                        "description": "Extension and rewire in M14",
                        "postcode": "M14 5TQ"}) + "\n"
            + json.dumps({"title": "Dog grooming salon",
                          "description": "Change of use shopfront",
                          "postcode": "M1 2AB"}) + "\n")
        return base

    def test_load_signals(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = self._powuk(tmp)
            sigs = load_powuk_signals(base=base)
            self.assertEqual(len(sigs), 2)
            self.assertEqual(sigs[0]["_source"], "powuk/planning_apps")

    def test_missing_powuk_gives_empty(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(
                load_powuk_signals(base=Path(tmp) / "nothing"), [])

    def test_opportunities_for_electrician(self):
        with tempfile.TemporaryDirectory() as tmp:
            import aionboard.assistant.powuk_bridge as bridge
            orig = bridge.POWUK_BASE
            bridge.POWUK_BASE = self._powuk(tmp)
            try:
                opps = opportunities_for_target(_profile())
            finally:
                bridge.POWUK_BASE = orig
            self.assertTrue(any("extension" in o["title"].lower() for o in opps))

    def test_no_profile_no_opps(self):
        opps = opportunities_for_target(TargetProfile(
            business_id="x", business_name="y", vertical="", postcode=""))
        self.assertEqual(opps, [])


class TestApprovals(unittest.TestCase):
    def _conn(self):
        conn = sqlite3.connect(":memory:")
        init_approval_tables(conn)
        return conn

    def test_propose_then_grant(self):
        conn = self._conn()
        r = request_approval(conn, action="draft_quote", business_id="b1",
                             arguments={"total": 499}, evidence="price book v3")
        self.assertFalse(r["sent"])
        self.assertFalse(r["authorized"])
        self.assertTrue(r["approval_id"].startswith("apr-"))
        g = grant_approval(conn, r, approver="owner", evidence="checked")
        self.assertTrue(g["authorized"])
        conn.close()

    def test_values_redacted_in_audit(self):
        conn = self._conn()
        request_approval(conn, action="a", business_id="b1",
                         arguments={"email": "customer@example.com"})
        row = conn.execute("SELECT detail FROM audit_log").fetchone()[0]
        self.assertNotIn("customer@example.com", row)
        conn.close()


class TestAgent(unittest.TestCase):
    def test_prompt_embeds_identity(self):
        prompt = build_system_prompt(_profile())
        self.assertIn("Test Sparks", prompt)
        self.assertIn("draft, never send", prompt)

    def test_dry_run_default(self):
        res = build_session(_profile(), "Summarise today")
        self.assertTrue(res["dry_run"])
        self.assertIn("agent", res["payload"])
        self.assertIn("target", res["payload"])

    def test_execute_without_sdk_raises(self):
        import aionboard.assistant.agent as agent_mod
        if agent_mod.AGENTS_AVAILABLE and "OPENAI_API_KEY" in __import__("os").environ:
            self.skipTest("live SDK configured")
        with self.assertRaises(RuntimeError):
            build_session(_profile(), "x", execute=True)


if __name__ == "__main__":
    unittest.main()
