"""Tests for prospect CSV import: dedupe, provenance, no permission granted."""

import csv
import unittest
from pathlib import Path

from aionboard import connect, get_prospect, import_prospects, init_business_tables

REPO_ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = REPO_ROOT / "prospects_electrical.csv"


def read_csv_rows(limit=None):
    with open(CSV_PATH, newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
    return rows if limit is None else rows[:limit]


class ProspectImportTests(unittest.TestCase):
    def test_real_csv_imports_with_provenance(self):
        connection = connect()
        rows = read_csv_rows(limit=500)
        stats = import_prospects(
            connection,
            rows,
            source="powuk-ch_capacity",
            source_path="data/normalized/ch_capacity/2026/09/22/001226.jsonl",
        )
        self.assertEqual(stats["imported"], 500)
        self.assertEqual(stats["updated"], 0)
        prospect = get_prospect(connection, rows[0]["company_number"])
        self.assertIsNotNone(prospect)
        self.assertEqual(prospect["source"], "powuk-ch_capacity")
        self.assertIn("ch_capacity", prospect["source_path"])

    def test_reimport_updates_without_duplicates(self):
        connection = connect()
        rows = read_csv_rows(limit=200)
        first = import_prospects(
            connection, rows, source="powuk-ch_capacity", source_path="v1.jsonl"
        )
        second = import_prospects(
            connection, rows, source="powuk-ch_capacity", source_path="v2.jsonl"
        )
        self.assertEqual(first["imported"], 200)
        self.assertEqual(second["imported"], 0)
        self.assertEqual(second["updated"], 200)
        count = connection.execute("SELECT COUNT(*) FROM prospects").fetchone()[0]
        self.assertEqual(count, 200)

    def test_import_grants_no_marketing_permission(self):
        connection = connect()
        init_business_tables(connection)
        rows = read_csv_rows(limit=100)
        import_prospects(
            connection, rows, source="powuk-ch_capacity", source_path="v1.jsonl"
        )
        consents = connection.execute("SELECT COUNT(*) FROM consents").fetchone()[0]
        self.assertEqual(consents, 0)
        contacts = connection.execute("SELECT COUNT(*) FROM contacts").fetchone()[0]
        self.assertEqual(contacts, 0)

    def test_incomplete_rows_skipped_not_crash(self):
        connection = connect()
        stats = import_prospects(
            connection,
            [{"company_number": "", "name": "Missing number"}],
            source="test",
            source_path="test.csv",
        )
        self.assertEqual(stats, {"imported": 0, "updated": 0, "skipped": 1})


if __name__ == "__main__":
    unittest.main(verbosity=2)
