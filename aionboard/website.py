"""Minimal pilot website content."""

from __future__ import annotations

import os

SITE_DOMAIN = "aionboard.co.uk"
BOOKING_EMAIL = "hello@aionboard.co.uk"
STANDARD_PRICE_GBP = 499


def canonical_domain() -> str:
    return f"https://{SITE_DOMAIN}"


def render_site() -> str:
    return f"""<!doctype html>
<html lang=\"en-GB\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>AI Onboard — Pilot AI Setup for UK Trades</title>
  <meta name=\"description\" content=\"Pilot AI setup for existing UK trades workflows, with training and written handover.\" />
</head>
<body>
  <main>
    <h1>AI Onboard pilot</h1>
    <p><strong>Status:</strong> pilot. No completed customer installation is claimed on this page.</p>

    <h2>Standard setup — £{STANDARD_PRICE_GBP} one-off</h2>
    <ul>
      <li>Setup for existing customer-authorized email and calendar workflows</li>
      <li>Enquiry capture using customer-approved contact details</li>
      <li>Quote drafting from a customer-approved price book</li>
      <li>Owner approval before outbound quotes, bookings, payments, or messages</li>
      <li>Google Business Profile assistance through Google’s ordinary interface</li>
      <li>Live training session</li>
      <li>Written handover</li>
      <li>Fourteen days of fixes for configured workflows</li>
    </ul>

    <h2>Not included</h2>
    <ul>
      <li>New or rebuilt website</li>
      <li>Live voice service</li>
      <li>WhatsApp, Facebook, Instagram, or Meta production integration</li>
      <li>Custom integrations</li>
      <li>Lead generation</li>
      <li>Guaranteed search, Maps, ChatGPT, or AI-assistant placement</li>
    </ul>

    <h2>Customer-owned costs</h2>
    <p>Domains, hosting, telephony, messaging, AI-model usage, software subscriptions, verification costs, and payment-processing fees remain the customer’s responsibility unless separately quoted in writing.</p>

    <h2>Book a pilot discussion</h2>
    <p>Email <a href=\"mailto:{BOOKING_EMAIL}?subject=Pilot%20installation%20request\">{BOOKING_EMAIL}</a> with your business name, postcode, current software, and the workflow you want help with.</p>

    <h2>Privacy and contact rules</h2>
    <p>We verify contact sources, record permission or legal basis, screen live marketing calls against TPS, CTPS, and our suppression list, and respect objections. Research records are not marketing permission.</p>
  </main>
</body>
</html>
"""


def write_site(path: str = "site/index.html") -> str:
    directory = os.path.dirname(os.path.abspath(path))
    os.makedirs(directory, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(render_site())
    return path
