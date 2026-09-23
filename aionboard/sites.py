"""Personalized customer sites + agent identity.

Renders a static per-business site from the target profile: services,
areas, hours, contact, plus the assistant's identity block (name,
personality, greeting). Static HTML — no backend, no tracking, no
framework. Customer owns the domain; we hand over files.
"""

from __future__ import annotations

import html
import os
from dataclasses import dataclass, field


@dataclass
class AgentIdentity:
    """How the business's assistant appears everywhere."""

    name: str = "Buddy"
    personality: str = "Direct, friendly, no jargon."
    greeting: str = "Hi — how can I help?"
    response_style: str = "Short answers. Prices only from the price book."
    avatar_emoji: str = ""
    color: str = "#111111"


@dataclass
class CustomerSite:
    """Everything needed to render one business site."""

    business_name: str
    vertical: str
    postcode: str
    services: list[str] = field(default_factory=list)
    areas: list[str] = field(default_factory=list)
    hours: str = ""
    phone: str = ""
    email: str = ""
    identity: AgentIdentity = field(default_factory=AgentIdentity)


def _esc(s: str) -> str:
    return html.escape(s or "")


def render_customer_site(site: CustomerSite) -> str:
    """Render a complete static site for one business."""
    services = "".join(f"<li>{_esc(s)}</li>" for s in site.services)
    areas = ", ".join(_esc(a) for a in site.areas) or "Surrounding areas"
    ident = site.identity
    avatar = f"<span>{_esc(ident.avatar_emoji)}</span> " if ident.avatar_emoji else ""
    return f"""<!doctype html>
<html lang="en-GB">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{_esc(site.business_name)} — { _esc(site.vertical).title()} in {_esc(site.postcode)}</title>
  <meta name="description" content="{_esc(site.business_name)}: {', '.join(_esc(s) for s in site.services[:3])}." />
</head>
<body>
  <main>
    <h1>{_esc(site.business_name)}</h1>
    <p>{_esc(site.vertical).title()} — {_esc(site.postcode)}. { _esc(site.hours)}</p>

    <h2>Services</h2>
    <ul>{services}</ul>

    <h2>Areas covered</h2>
    <p>{areas}</p>

    <h2>Contact</h2>
    <p>{_esc(site.phone)} {_esc(site.email)}</p>

    <h2>Ask {avatar}{_esc(ident.name)}</h2>
    <p><em>{_esc(ident.greeting)}</em></p>
    <p>{_esc(ident.personality)} { _esc(ident.response_style)}</p>
    <p><small>Quotes come from our approved price list. Nothing is booked or sent without the owner's approval.</small></p>
  </main>
</body>
</html>
"""


def write_customer_site(site: CustomerSite, path: str) -> str:
    """Write the rendered site. Returns path."""
    directory = os.path.dirname(os.path.abspath(path))
    os.makedirs(directory, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(render_customer_site(site))
    return path


def site_from_profile(profile, record=None, identity=None) -> CustomerSite:
    """Build a CustomerSite from an assistant TargetProfile.

    record carries contact extras (hours, phone, email) when known.
    identity overrides the profile identity when the agent_identity
    addon is active; otherwise the profile's identity is used.
    """
    record = record or {}
    ident = identity or AgentIdentity(
        name=profile.assistant_name,
        personality=profile.assistant_personality,
        greeting=profile.assistant_greeting,
    )
    return CustomerSite(
        business_name=profile.business_name,
        vertical=profile.vertical,
        postcode=profile.postcode,
        services=list(profile.services),
        areas=list(profile.areas_served),
        hours=str(record.get("hours", "")),
        phone=str(record.get("phone", "")),
        email=str(record.get("email", "")),
        identity=ident,
    )
