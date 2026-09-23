"""Tests for booking-link verification."""

import unittest

from aionboard.verify import verify_booking_link


def fake_page(body, status=200):
    def fetch(url, timeout_seconds):
        return status, body

    return fetch


def fake_failure(exc):
    def fetch(url, timeout_seconds):
        raise exc

    return fetch


class BookingLinkTests(unittest.TestCase):
    def test_valid_link_with_services(self):
        result = verify_booking_link(
            "https://example.com/book",
            ["gel nails", "infills"],
            fetcher=fake_page("<html>Gel Nails and Infills available</html>"),
        )
        self.assertTrue(result["verified"])
        self.assertEqual(result["status"], 200)
        self.assertIn("checked_at", result)

    def test_missing_service_fails(self):
        result = verify_booking_link(
            "https://example.com/book",
            ["gel nails", "spa packages"],
            fetcher=fake_page("<html>Gel Nails only</html>"),
        )
        self.assertFalse(result["verified"])
        self.assertIn("spa packages", result["reason"])

    def test_non_200_fails(self):
        result = verify_booking_link(
            "https://example.com/gone",
            ["nails"],
            fetcher=fake_page("gone", status=404),
        )
        self.assertFalse(result["verified"])
        self.assertIn("404", result["reason"])

    def test_network_failure_names_cause(self):
        result = verify_booking_link(
            "https://example.com/book",
            ["nails"],
            fetcher=fake_failure(TimeoutError("timed out")),
        )
        self.assertFalse(result["verified"])
        self.assertIn("TimeoutError", result["reason"])

    def test_bad_url_rejected(self):
        for bad in ("", "not-a-url", "ftp://example.com/x", "javascript:alert(1)"):
            with self.subTest(url=bad):
                result = verify_booking_link(bad, ["nails"])
                self.assertFalse(result["verified"])

    def test_case_insensitive_matching(self):
        result = verify_booking_link(
            "https://example.com/book",
            ["GEL NAILS"],
            fetcher=fake_page("<html>gel nails</html>"),
        )
        self.assertTrue(result["verified"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
