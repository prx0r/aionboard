"""Target profiles — who the assistant serves.

A target is one business: identity, trade, service area, qualifications,
services offered, and price-book reference. Built from aionboard CRM
business records (businesses.py), never from guesses.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class TargetProfile:
    """Everything the assistant knows about its business."""

    business_id: str
    business_name: str
    vertical: str  # electrician, plumber, cleaner, ...
    postcode: str  # outward code enough, e.g. "M14"
    services: list[str] = field(default_factory=list)
    qualifications: list[str] = field(default_factory=list)
    price_book_ref: str = ""
    team_size: int = 1
    areas_served: list[str] = field(default_factory=list)

    def system_identity(self) -> str:
        """Identity block embedded in the assistant system prompt."""
        lines = [
            f"You serve {self.business_name} ({self.business_id}), "
            f"a {self.vertical} business based in {self.postcode}.",
        ]
        if self.services:
            lines.append(f"Services: {', '.join(self.services)}.")
        if self.qualifications:
            lines.append(f"Qualifications: {', '.join(self.qualifications)}.")
        if self.areas_served:
            lines.append(f"Areas served: {', '.join(self.areas_served)}.")
        if self.price_book_ref:
            lines.append(
                "Quote only from the approved price book "
                f"({self.price_book_ref}). Never invent prices."
            )
        return " ".join(lines)


def profile_from_business(record: dict) -> TargetProfile:
    """Build a profile from a CRM business record.

    Unknown fields stay empty — the assistant must say what it doesn't
    know, never fill gaps with guesses.
    """
    return TargetProfile(
        business_id=record.get("business_id", ""),
        business_name=record.get("name", record.get("business_name", "")),
        vertical=record.get("vertical", ""),
        postcode=record.get("postcode", record.get("outward_code", "")),
        services=list(record.get("services", [])),
        qualifications=list(record.get("qualifications", [])),
        price_book_ref=record.get("price_book_ref", ""),
        team_size=int(record.get("team_size", 1) or 1),
        areas_served=list(record.get("areas_served", [])),
    )
