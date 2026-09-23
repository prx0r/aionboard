"""Tests for the combined regulations registry."""

import json
import unittest
from datetime import date
from pathlib import Path

from aionboard import connect, init_compliance_tables, load_registry, rules_for_industry, stale_rules

REPO_ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = REPO_ROOT / "regulations" / "registry.json"

REQUIRED_KEYS = {
    "id",
    "domain",
    "jurisdiction",
    "industries",
    "law",
    "detail",
    "citation",
    "source_url",
    "basis",
    "review_date",
    "applies_when",
    "owner_action",
    "escalation",
    "source",
}
VALID_DOMAINS = {
    "ai-agent",
    "consumer",
    "data",
    "employment",
    "finance",
    "marketing",
    "security",
    "tax",
    "trade",
    "voice",
}
VALID_BASES = {"verified-2026", "well-established", "template-analysis"}

# Every vertical slug used anywhere in profiles, plus cgraphuk-only ones.
KNOWN_VERTICALS = {
    "all",
    "electrician",
    "beauty",
    "nails",
    "lashes",
    "hair",
    "cleaners",
    "dog-groomers",
    "gardeners-window-cleaners",
    "car-detailers",
    "driving-instructors",
    "weddings",
    "barber",
    "restaurant",
    "hotel",
    "builder",
    "hvac",
    "garage",
    "petcare",
    "tutor",
    "care",
    "cleaning",
    "window_cleaner",
    "gp_surgery",
    "vet",
    "medspa",
    "bookkeeping",
    "retail",
    "gig_driver",
    "funeral",
    "tree_surgeon",
    "reseller",
    "dropship",
    "msp",
    "it_helpdesk",
}


class RegistrySchemaTests(unittest.TestCase):
    def test_registry_loads_with_unique_ids(self):
        rules = load_registry()
        self.assertGreater(len(rules), 30)
        ids = [rule["id"] for rule in rules]
        self.assertEqual(len(ids), len(set(ids)))

    def test_every_entry_has_required_keys(self):
        for rule in load_registry():
            with self.subTest(rule=rule.get("id")):
                self.assertTrue(REQUIRED_KEYS <= set(rule.keys()))
                self.assertTrue(rule["industries"])

    def test_domains_and_bases_are_valid(self):
        for rule in load_registry():
            with self.subTest(rule=rule["id"]):
                self.assertIn(rule["domain"], VALID_DOMAINS)
                self.assertIn(rule["basis"], VALID_BASES)

    def test_review_dates_parse(self):
        for rule in load_registry():
            with self.subTest(rule=rule["id"]):
                date.fromisoformat(rule["review_date"])

    def test_verticals_are_known(self):
        for rule in load_registry():
            for industry in rule["industries"]:
                with self.subTest(rule=rule["id"], industry=industry):
                    self.assertIn(industry, KNOWN_VERTICALS)

    def test_design_rules_labelled_honestly(self):
        for rule in load_registry():
            if rule["basis"] == "template-analysis":
                text = (rule["law"] + rule.get("failure_mode", "")).lower()
                self.assertTrue(
                    "not legislation" in text or "design rule" in text or "platform" in text,
                    msg=f"{rule['id']} must not read as statute",
                )


class RegistryDatabaseTests(unittest.TestCase):
    def test_tables_seed_from_registry(self):
        connection = connect()
        init_compliance_tables(connection)
        count = connection.execute("SELECT COUNT(*) FROM compliance_rules").fetchone()[0]
        self.assertEqual(count, len(load_registry()))

    def test_rules_for_industry(self):
        connection = connect()
        init_compliance_tables(connection)
        nails = {r["rule_id"] for r in rules_for_industry(connection, "nails")}
        # Nails matches beauty-family rules via LIKE; MTD/VAT apply via 'all'.
        self.assertTrue(any("MTD" in r or "VAT" in r for r in nails))

    def test_stale_detection(self):
        connection = connect()
        init_compliance_tables(connection)
        self.assertEqual(stale_rules(connection, "2020-01-01"), [])
        stale = stale_rules(connection, "2030-01-01")
        self.assertEqual(len(stale), len(load_registry()))


class ProfileCrossCheckTests(unittest.TestCase):
    def test_profile_legal_ids_exist_in_registry(self):
        registry_ids = {rule["id"] for rule in load_registry()}
        verticals_root = REPO_ROOT / "verticals"
        checked = 0
        for manifest in sorted(verticals_root.glob("*/manifest.json")):
            profile_path = manifest.parent / "profile.json"
            profile = json.loads(profile_path.read_text(encoding="utf-8"))
            for entry in profile.get("legal", []):
                with self.subTest(vertical=profile["vertical"], legal=entry["id"]):
                    self.assertIn(entry["id"], registry_ids)
                    checked += 1
        self.assertGreater(checked, 20)


if __name__ == "__main__":
    unittest.main(verbosity=2)
