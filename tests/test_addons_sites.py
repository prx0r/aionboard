"""Tests for addons, customer sites, identity, cloudflare tracker."""

import sqlite3
import tempfile
import unittest
from pathlib import Path

from aionboard.addons import (
    ADDONS,
    activate_addon,
    active_addons,
    consent_addon,
    init_addon_tables,
    offer_addon,
)
from aionboard.assistant import TargetProfile
from aionboard.cloudflare import STEPS, init_cloudflare_tables, set_step, status
from aionboard.sites import (
    AgentIdentity,
    CustomerSite,
    render_customer_site,
    site_from_profile,
    write_customer_site,
)


def _db():
    conn = sqlite3.connect(":memory:")
    init_addon_tables(conn)
    init_cloudflare_tables(conn)
    return conn


class TestAddons(unittest.TestCase):
    def test_catalog_shape(self):
        for aid, a in ADDONS.items():
            for k in ("name", "price", "description", "consent"):
                self.assertIn(k, a, aid)

    def test_consent_before_activation(self):
        conn = _db()
        offer_addon(conn, "b1", "lead_alerts")
        blocked = activate_addon(conn, "b1", "lead_alerts")
        self.assertIn("error", blocked)
        consent_addon(conn, "b1", "lead_alerts")
        ok = activate_addon(conn, "b1", "lead_alerts")
        self.assertEqual(ok["state"], "active")
        self.assertEqual(active_addons(conn, "b1"), ["lead_alerts"])
        conn.close()

    def test_unknown_addon(self):
        conn = _db()
        self.assertIn("error", offer_addon(conn, "b1", "nope"))
        conn.close()


class TestSites(unittest.TestCase):
    def _site(self):
        return CustomerSite(
            business_name="Test <Sparks>",
            vertical="electrician",
            postcode="M14",
            services=["rewire", "EV chargers"],
            areas=["M14", "M20"],
            hours="Mon–Fri 8–6",
            phone="07123 456789",
            email="hi@test.example",
            identity=AgentIdentity(name="Sparky",
                                   greeting="How can I help?"))

    def test_escapes_html(self):
        html = render_customer_site(self._site())
        self.assertNotIn("<Sparks>", html)
        self.assertIn("Test &lt;Sparks&gt;", html)
        self.assertIn("Sparky", html)
        self.assertIn("owner", html.lower())

    def test_writes_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = write_customer_site(self._site(), str(Path(tmp) / "i.html"))
            self.assertTrue(Path(p).exists())

    def test_from_profile_uses_identity(self):
        prof = TargetProfile(
            business_id="b", business_name="N", vertical="electrician",
            postcode="M14", assistant_name="Volt",
            assistant_personality="Calm.", assistant_greeting="Yo.")
        site = site_from_profile(prof, record={"phone": "071"})
        self.assertEqual(site.identity.name, "Volt")
        self.assertIn("Volt", render_customer_site(site))
        self.assertIn("071", render_customer_site(site))

    def test_profile_defaults_unchanged(self):
        prof = TargetProfile(business_id="b", business_name="N",
                             vertical="e", postcode="M1")
        self.assertEqual(prof.assistant_name, "Buddy")
        self.assertIn("Buddy", prof.system_identity())


class TestCloudflare(unittest.TestCase):
    def test_steps_lifecycle(self):
        conn = _db()
        st = status(conn, "b1")
        self.assertFalse(st["complete"])
        self.assertIn("ownership", st["ownership_note"].lower())
        bad = set_step(conn, "b1", "nope", "done")
        self.assertIn("error", bad)
        set_step(conn, "b1", "dns", "done", "TXT verified")
        for s in STEPS:
            set_step(conn, "b1", s, "done")
        self.assertTrue(status(conn, "b1")["complete"])
        conn.close()


if __name__ == "__main__":
    unittest.main()
