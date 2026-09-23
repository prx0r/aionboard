"""Tests for the geographic opportunity matcher."""

import unittest

from aionboard.opportunities import (
    OPPORTUNITY_KEYWORDS,
    customer_digest,
    digest,
    match_customers,
    match_for_business,
    same_area,
    score_opportunity,
)

PLANNING_RECORD = {
    "kind": "planning",
    "title": "23/00002/FUL",
    "description": "Erection of a single storey extension with PV installation to pitched roof",
    "locality": "Manchester",
    "postcode": "M1 1AA",
    "date": "2023-05-09",
}

TENDER_RECORD = {
    "kind": "procurement",
    "title": "Installation Services, Small Works and Reactive Call Outs",
    "description": "Building installation work across three campuses",
    "locality": "Gloucester",
    "postcode": "GL1 2EL",
    "date": "2026-09-21",
}

SALON_RECORD = {
    "kind": "planning",
    "title": "Change of use to beauty salon with new shopfront",
    "description": "Ground floor retail unit to beauty salon",
    "locality": "Leeds",
    "postcode": "LS1 4DY",
    "date": "2026-08-01",
}


class ScoringTests(unittest.TestCase):
    def test_electrician_matches_extension_and_pv(self):
        self.assertGreater(score_opportunity(PLANNING_RECORD, "electrician"), 0)

    def test_nails_ignores_electrical_work(self):
        self.assertEqual(score_opportunity(PLANNING_RECORD, "nails"), 0)

    def test_nails_matches_salon(self):
        self.assertGreater(score_opportunity(SALON_RECORD, "nails"), 0)

    def test_unknown_vertical_scores_zero(self):
        self.assertEqual(score_opportunity(PLANNING_RECORD, "astronaut"), 0)

    def test_case_insensitive(self):
        record = {"title": "EV CHARGER INSTALLATION", "description": ""}
        self.assertGreater(score_opportunity(record, "electrician"), 0)


class RegionTests(unittest.TestCase):
    def test_same_outward_code_is_local(self):
        self.assertTrue(same_area("M1 1AA", "M1 2AB"))

    def test_different_areas_are_not_local(self):
        self.assertFalse(same_area("M1 1AA", "GL1 2EL"))

    def test_empty_postcode_is_not_local(self):
        self.assertFalse(same_area("M1 1AA", ""))


class MatchingTests(unittest.TestCase):
    def test_region_filter_drops_distant_matches(self):
        matches = match_for_business(
            business_postcode="M1 1AA",
            vertical="electrician",
            opportunities=[PLANNING_RECORD, TENDER_RECORD],
        )
        postcodes = [m["postcode"] for m in matches]
        self.assertIn("M1 1AA", postcodes)
        self.assertNotIn("GL1 2EL", postcodes)

    def test_region_filter_can_be_disabled(self):
        matches = match_for_business(
            business_postcode="M1 1AA",
            vertical="electrician",
            opportunities=[TENDER_RECORD],
            same_region_only=False,
        )
        self.assertEqual(len(matches), 1)

    def test_sorted_by_score(self):
        weak = {"title": "Extension", "description": "", "postcode": "M1 2AB"}
        strong = {
            "title": "Extension with solar PV and EV charger",
            "description": "Full rewire and consumer unit",
            "postcode": "M1 3CD",
        }
        matches = match_for_business(
            business_postcode="M1 1AA",
            vertical="electrician",
            opportunities=[weak, strong],
        )
        self.assertGreater(matches[0]["score"], matches[1]["score"])

    def test_unmatched_records_dropped(self):
        matches = match_for_business(
            business_postcode="M1 1AA",
            vertical="electrician",
            opportunities=[SALON_RECORD],
        )
        self.assertEqual(matches, [])


class CustomerFindingTests(unittest.TestCase):
    def test_match_customers_adds_compliant_next_step(self):
        matches = match_customers(
            business_postcode="M1 1AA",
            vertical="electrician",
            opportunities=[PLANNING_RECORD],
        )
        self.assertEqual(len(matches), 1)
        self.assertIn("customer_read", matches[0])
        self.assertIn("TPS", matches[0]["customer_read"])

    def test_match_customers_empty_when_no_match(self):
        matches = match_customers(
            business_postcode="M1 1AA",
            vertical="electrician",
            opportunities=[SALON_RECORD],
        )
        self.assertEqual(matches, [])

    def test_customer_digest_warns_about_permission(self):
        matches = match_customers(
            business_postcode="M1 1AA",
            vertical="nails",
            opportunities=[SALON_RECORD],
        )
        # SALON_RECORD is Leeds, business is Manchester: filtered out.
        self.assertEqual(matches, [])
        text = customer_digest("Fictional Nails", "nails", matches)
        self.assertIn("not permission to contact", text)

    def test_customer_digest_requires_approval(self):
        local_salon = {**SALON_RECORD, "postcode": "M1 9AB"}
        matches = match_customers(
            business_postcode="M1 1AA",
            vertical="nails",
            opportunities=[local_salon],
        )
        self.assertEqual(len(matches), 1)
        text = customer_digest("Fictional Nails", "nails", matches)
        self.assertIn("Reply APPROVE", text)
        self.assertIn("verified details", text)


class DigestTests(unittest.TestCase):
    def test_digest_states_limits(self):
        text = digest("Fictional Sparks", "electrician", [])
        self.assertIn("Fictional Sparks", text)
        self.assertIn("signals to investigate, not confirmed jobs", text)
        self.assertIn("No matches this week", text)

    def test_digest_requires_approval(self):
        text = digest(
            "Fictional Sparks", "electrician", [{**PLANNING_RECORD, "score": 2}]
        )
        self.assertIn("Reply APPROVE", text)
        self.assertIn("never chase leads without your tap", text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
