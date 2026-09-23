"""Geographic opportunity matching.

Turns powuk-type signals (planning applications, procurement contracts,
labour demand) into per-business opportunity digests. Powers the pitch:
"your assistant finds opportunities near you."

Matching is keyword + region based and explicitly approximate. A match is
a lead to investigate, never a confirmed job.
"""

from __future__ import annotations

from .crm import parse_region

# Vertical -> keywords matched against planning descriptions and tender titles.
# Kept conservative: a false positive wastes a tradesperson's time.
OPPORTUNITY_KEYWORDS: dict[str, tuple[str, ...]] = {
    "electrician": (
        "installation",
        "extension",
        "rewire",
        "consumer unit",
        "fuse box",
        "ev charger",
        "electric vehicle charging",
        "solar",
        "photovoltaic",
        "pv installation",
        "refurbishment",
        "conversion",
        "new build",
        "commercial",
        "electrical",
    ),
    "beauty": (
        "salon",
        "beauty",
        "change of use",
        "shopfront",
        "retail",
        "high street",
    ),
    "nails": (
        "salon",
        "beauty",
        "change of use",
        "shopfront",
        "retail",
        "high street",
    ),
    "lashes": (
        "salon",
        "beauty",
        "change of use",
        "shopfront",
        "retail",
    ),
    "hair": (
        "salon",
        "barber",
        "beauty",
        "change of use",
        "shopfront",
        "retail",
        "high street",
    ),
    "cleaners": (
        "office",
        "commercial",
        "residential development",
        "new build",
        "end of tenancy",
        "student accommodation",
    ),
    "dog-groomers": (
        "pet",
        "veterinary",
        "kennel",
        "cattery",
        "residential development",
        "commercial",
    ),
    "gardeners-window-cleaners": (
        "garden",
        "landscap",
        "residential",
        "estate",
        "new build",
        "commercial",
    ),
    "car-detailers": (
        "car park",
        "dealership",
        "mot centre",
        "garage",
        "commercial",
    ),
    "driving-instructors": (
        "school",
        "college",
        "residential development",
        "new town",
    ),
    "weddings": (
        "hotel",
        "venue",
        "wedding",
        "events space",
        "barn conversion",
    ),
}

# CPV codes relevant to trades (Contracts Finder classification scheme).
TRADE_CPV_PREFIXES = ("453", "454", "455", "093", "311", "316")


def score_opportunity(record: dict, vertical: str) -> int:
    """Count keyword hits. Zero means no match. Case-insensitive."""
    keywords = OPPORTUNITY_KEYWORDS.get(vertical, ())
    if not keywords:
        return 0
    text = " ".join(
        str(record.get(field, ""))
        for field in ("title", "description", "summary")
    ).lower()
    return sum(1 for keyword in keywords if keyword in text)


def same_area(postcode_a: str, postcode_b: str) -> bool:
    """Same outward-code area counts as local. Approximate by design."""
    area_a = parse_region(postcode_a)
    area_b = parse_region(postcode_b)
    return bool(area_a) and area_a == area_b


def match_for_business(
    *,
    business_postcode: str,
    vertical: str,
    opportunities: list[dict],
    same_region_only: bool = True,
) -> list[dict]:
    """Return matched opportunities sorted by score, highest first.

    Each result carries its score and match reason. Unmatched records
    are dropped, never silently included.
    """
    matches = []
    for record in opportunities:
        score = score_opportunity(record, vertical)
        if score <= 0:
            continue
        record_postcode = str(record.get("postcode", ""))
        if same_region_only and record_postcode and not same_area(
            business_postcode, record_postcode
        ):
            continue
        matches.append({**record, "score": score})
    matches.sort(key=lambda item: item["score"], reverse=True)
    return matches


def digest(business_name: str, vertical: str, matches: list[dict], limit: int = 5) -> str:
    """Plain-English digest a customer can read. States limits honestly."""
    lines = [
        f"# Weekly opportunities near you — {business_name}",
        "",
        f"{len(matches)} potential lead(s) matched for {vertical} work.",
        "These are signals to investigate, not confirmed jobs.",
        "",
    ]
    for match in matches[:limit]:
        title = match.get("title") or match.get("summary") or "Untitled record"
        locality = match.get("locality", "")
        date = match.get("date", "")
        where = f" ({locality})" if locality else ""
        when = f" — {date}" if date else ""
        lines.append(f"- {title}{where}{when} [relevance {match['score']}]")
    if not matches:
        lines.append("- No matches this week. We'll keep watching.")
    lines += [
        "",
        "Reply APPROVE before we contact anyone on your behalf. "
        "We never chase leads without your tap.",
    ]
    return "\n".join(lines)
