"""Tests for the prospect scoring engine."""

import csv
import os
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path

from aionboard.prospects import (
    calculate_gap_score,
    count_area_signals,
    count_postcode_density,
    export_csv,
    generate_prospect_list,
    load_electrical_businesses,
    regional_summary,
    score_business,
)

POWUK_BASE = "/root/powuk"


class TestLoadElectricalBusinesses(unittest.TestCase):
    def test_returns_non_empty_list(self):
        result = load_electrical_businesses(POWUK_BASE)
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

    def test_records_have_required_keys(self):
        result = load_electrical_businesses(POWUK_BASE)
        for b in result[:10]:
            for key in ("company_number", "name", "status", "sic_codes", "postcode"):
                self.assertIn(key, b)

    def test_sic_codes_are_lists(self):
        result = load_electrical_businesses(POWUK_BASE)
        for b in result[:20]:
            self.assertIsInstance(b["sic_codes"], list)


class TestScoreBusiness(unittest.TestCase):
    def test_active_business_returns_nonzero(self):
        biz = {
            "company_number": "123",
            "name": "Test Ltd",
            "status": "active",
            "sic_codes": ["43210"],
            "incorporation_date": "2020-01-01",
            "postcode": "M1 1AA",
            "cluster": "electrical",
        }
        score = score_business(biz, planning_count=0, contract_count=0)
        self.assertGreater(score, 0)

    def test_dissolved_business_returns_zero(self):
        biz = {
            "company_number": "456",
            "name": "Dead Co",
            "status": "dissolved",
            "sic_codes": ["43210"],
            "incorporation_date": "2015-06-01",
            "postcode": "B1 1BB",
            "cluster": "electrical",
        }
        score = score_business(biz)
        self.assertEqual(score, 0.0)

    def test_score_between_0_and_100(self):
        biz = {
            "company_number": "789",
            "name": "Test Active",
            "status": "active",
            "sic_codes": ["43210", "61900", "25990"],
            "incorporation_date": "2022-03-15",
            "postcode": "GL1 1AA",
            "cluster": "electrical",
        }
        score = score_business(biz, planning_count=5, contract_count=3)
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)

    def test_planning_bump(self):
        biz = {
            "company_number": "100",
            "name": "Plans Co",
            "status": "active",
            "sic_codes": ["43210"],
            "incorporation_date": "2020-01-01",
            "postcode": "M1 1AA",
            "cluster": "electrical",
        }
        without = score_business(biz, planning_count=0, contract_count=0)
        with_plan = score_business(biz, planning_count=5, contract_count=0)
        self.assertGreater(with_plan, without)

    def test_contract_bump(self):
        biz = {
            "company_number": "200",
            "name": "Contract Co",
            "status": "active",
            "sic_codes": ["43210"],
            "incorporation_date": "2020-01-01",
            "postcode": "M1 1AA",
            "cluster": "electrical",
        }
        without = score_business(biz, planning_count=0, contract_count=0)
        with_contract = score_business(biz, planning_count=0, contract_count=3)
        self.assertGreater(with_contract, without)

    def test_diverse_sics_higher_score(self):
        base_biz = {
            "company_number": "300",
            "name": "SIC Co",
            "status": "active",
            "incorporation_date": "2020-01-01",
            "postcode": "M1 1AA",
            "cluster": "electrical",
        }
        single = score_business({**base_biz, "sic_codes": ["43210"]})
        multi = score_business({**base_biz, "sic_codes": ["43210", "61900", "25990", "43999"]})
        self.assertGreater(multi, single)


class TestCountPostcodeDensity(unittest.TestCase):
    def test_returns_dict(self):
        result = count_postcode_density(load_electrical_businesses(POWUK_BASE))
        self.assertIsInstance(result, dict)
        self.assertGreater(len(result), 0)

    def test_keys_are_two_char_strings(self):
        result = count_postcode_density(load_electrical_businesses(POWUK_BASE))
        for key in result:
            self.assertEqual(len(key), 2)

    def test_values_are_integers(self):
        result = count_postcode_density(load_electrical_businesses(POWUK_BASE))
        for val in result.values():
            self.assertIsInstance(val, int)
            self.assertGreater(val, 0)


class TestCountAreaSignals(unittest.TestCase):
    def test_returns_dict(self):
        result = count_area_signals(POWUK_BASE)
        self.assertIsInstance(result, dict)
        self.assertGreater(len(result), 0)

    def test_values_have_planning_and_contracts(self):
        result = count_area_signals(POWUK_BASE)
        for area, signals in result.items():
            self.assertIn("planning", signals)
            self.assertIn("contracts", signals)


class TestGenerateProspectList(unittest.TestCase):
    def test_returns_sorted_list(self):
        result = generate_prospect_list(POWUK_BASE, min_score=0)
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        # Check sorted descending
        scores = [p["score"] for p in result]
        self.assertEqual(scores, sorted(scores, reverse=True))

    def test_min_score_filter(self):
        result = generate_prospect_list(POWUK_BASE, min_score=80)
        for p in result:
            self.assertGreaterEqual(p["score"], 80)

    def test_prospects_have_score_key(self):
        result = generate_prospect_list(POWUK_BASE, min_score=0)
        for p in result[:10]:
            self.assertIn("score", p)
            self.assertIn("area", p)
            self.assertIn("planning_count", p)
            self.assertIn("contract_count", p)


class TestExportCsv(unittest.TestCase):
    def test_creates_file(self):
        prospects = generate_prospect_list(POWUK_BASE, min_score=50)[:10]
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
            path = tmp.name
        try:
            result = export_csv(prospects, path)
            self.assertEqual(result, path)
            self.assertTrue(os.path.exists(path))
            with open(path, encoding="utf-8") as fh:
                reader = csv.DictReader(fh)
                rows = list(reader)
            self.assertEqual(len(rows), len(prospects))
            self.assertIn("score", rows[0])
            self.assertIn("company_number", rows[0])
        finally:
            os.unlink(path)

    def test_csv_has_rank_column(self):
        prospects = generate_prospect_list(POWUK_BASE, min_score=50)[:5]
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
            path = tmp.name
        try:
            export_csv(prospects, path)
            with open(path, encoding="utf-8") as fh:
                reader = csv.DictReader(fh)
                rows = list(reader)
            self.assertIn("rank", rows[0])
            self.assertEqual(rows[0]["rank"], "1")
        finally:
            os.unlink(path)


class TestRegionalSummary(unittest.TestCase):
    def test_returns_dict(self):
        prospects = generate_prospect_list(POWUK_BASE, min_score=0)
        result = regional_summary(prospects)
        self.assertIsInstance(result, dict)
        self.assertGreater(len(result), 0)

    def test_values_have_required_keys(self):
        prospects = generate_prospect_list(POWUK_BASE, min_score=0)
        result = regional_summary(prospects)
        for area, info in result.items():
            self.assertIn("count", info)
            self.assertIn("avg_score", info)
            self.assertIn("top_businesses", info)
            self.assertIsInstance(info["top_businesses"], list)

    def test_top_businesses_limited_to_five(self):
        prospects = generate_prospect_list(POWUK_BASE, min_score=0)
        result = regional_summary(prospects)
        for area, info in result.items():
            self.assertLessEqual(len(info["top_businesses"]), 5)


if __name__ == "__main__":
    unittest.main(verbosity=2)
