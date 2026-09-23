"""Tests for aionboard.localinfo — all network mocked."""

import unittest
from unittest import mock

from aionboard.localinfo import (
    cluster_by_proximity,
    daylight_hours,
    haversine_km,
    is_bank_holiday,
    outward_code,
    postcode_lookup,
    rain_risk_days,
    travel_estimate,
    weather_forecast,
)


class TestPostcodes(unittest.TestCase):
    def test_outward_local(self):
        self.assertEqual(outward_code("M14 5TQ"), "M14")
        self.assertEqual(outward_code("m1 2ab"), "M1")
        self.assertEqual(outward_code(""), "")

    def test_lookup_mocked(self):
        payload = {"status": 200, "result": {
            "postcode": "M14 5TQ", "latitude": 53.45, "longitude": -2.22,
            "region": "North West", "admin_district": "Manchester",
            "parliamentary_constituency": "Manchester Central",
            "country": "England"}}
        with mock.patch("aionboard.localinfo.postcodes.get_json",
                        return_value=payload):
            r = postcode_lookup("M14 5TQ")
        self.assertEqual(r["outward_code"], "M14")
        self.assertEqual(r["region"], "North West")

    def test_lookup_not_found(self):
        with mock.patch("aionboard.localinfo.postcodes.get_json",
                        return_value={"status": 404}):
            with self.assertRaises(RuntimeError):
                postcode_lookup("ZZ9 9ZZ")


class TestHolidays(unittest.TestCase):
    HOL = {"england-and-wales": {"events": [
        {"title": "Christmas Day", "date": "2026-12-25"},
        {"title": "Boxing Day", "date": "2026-12-26"}]}}

    def test_is_holiday(self):
        with mock.patch("aionboard.localinfo.holidays.get_json",
                        return_value=self.HOL):
            self.assertTrue(is_bank_holiday("2026-12-25")["is_holiday"])
            self.assertFalse(is_bank_holiday("2026-12-24")["is_holiday"])

    def test_next_holiday(self):
        from aionboard.localinfo import next_holiday
        with mock.patch("aionboard.localinfo.holidays.get_json",
                        return_value=self.HOL):
            self.assertEqual(
                next_holiday("2026-12-01")["title"], "Christmas Day")

    def test_bad_division(self):
        from aionboard.localinfo import bank_holidays
        with self.assertRaises(ValueError):
            bank_holidays("atlantis")


class TestWeather(unittest.TestCase):
    def test_forecast_shape(self):
        payload = {"daily": {"time": ["2026-09-24", "2026-09-25"],
                             "temperature_2m_max": [17.0, 15.0],
                             "precipitation_probability_max": [80, 10]}}
        with mock.patch("aionboard.localinfo.weather.get_json",
                        return_value=payload):
            days = weather_forecast(53.45, -2.27, days=2)
            risky = rain_risk_days(53.45, -2.27, threshold_pct=50, days=2)
        self.assertEqual(len(days), 2)
        self.assertEqual(len(risky), 1)
        self.assertEqual(risky[0]["date"], "2026-09-24")


class TestDaylight(unittest.TestCase):
    def test_hours(self):
        payload = {"results": {"sunrise": "2026-09-23T05:55:06+00:00",
                               "sunset": "2026-09-23T18:07:45+00:00",
                               "day_length": 43959}}
        with mock.patch("aionboard.localinfo.daylight.get_json",
                        return_value=payload):
            d = daylight_hours(53.45, -2.27)
        self.assertAlmostEqual(d["daylight_hours"], 12.2, places=1)


class TestDistance(unittest.TestCase):
    def test_haversine(self):
        # Manchester ~ Liverpool, straight line
        km = haversine_km(53.4808, -2.2426, 53.4106, -2.9779)
        self.assertTrue(40 < km < 60, km)

    def test_travel_estimate(self):
        t = travel_estimate(15.0)
        self.assertEqual(t["drive_minutes"], 30)
        self.assertIn("Estimate", t["note"])

    def test_clustering(self):
        jobs = [
            {"id": "a", "latitude": 53.48, "longitude": -2.24},
            {"id": "b", "latitude": 53.49, "longitude": -2.25},
            {"id": "c", "latitude": 53.41, "longitude": -2.98},
        ]
        clusters = cluster_by_proximity(jobs, max_km=8.0)
        self.assertEqual(len(clusters), 2)
        self.assertEqual({len(c) for c in clusters}, {1, 2})


if __name__ == "__main__":
    unittest.main()
