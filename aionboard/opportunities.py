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


# Customer-side framing: what a matched signal implies about who nearby
# might need work, plus the compliant next step. Conservative by design —
# no contact details are ever fabricated. Planning applicants are named
# individuals in public records: research, not prospects.
CUSTOMER_ACTIONS: dict[str, str] = {
    "electrician": "Leaflet the street or check the letting agent — never cold-call a homeowner without a verified number and TPS check.",
    "beauty": "New salon openings nearby may need subcontractors or referrals — approach the business, not its clients.",
    "nails": "New salon openings nearby may need subcontractors or referrals — approach the business, not its clients.",
    "lashes": "New salon openings nearby may need subcontractors or referrals — approach the business, not its clients.",
    "hair": "New salon openings nearby may need subcontractors or referrals — approach the business, not its clients.",
    "cleaners": "New offices and developments need contract cleaners — approach the managing agent or facilities contact.",
    "dog-groomers": "New residential areas mean new dog owners — leaflet vet-adjacent spots and parks noticeboards.",
    "gardeners-window-cleaners": "New estates mean whole streets needing rounds — canvass the street, not individuals.",
    "car-detailers": "Dealerships and garages need overflow detailers — approach the business.",
    "driving-instructors": "New schools and housing mean new learners — school gates and local boards, not DMs.",
    "weddings": "New venues need preferred suppliers — approach the venue, not couples.",
}


def match_customers(
    *,
    business_postcode: str,
    vertical: str,
    opportunities: list[dict],
    same_region_only: bool = True,
) -> list[dict]:
    """Flip the matcher: who nearby is likely to need work.

    Same scoring engine, customer-side framing. Planning applicants are
    named individuals in public records — that makes them research, not
    prospects. Contact still needs verified details, permission, and
    TPS/CTPS screening. Every match carries its compliant next step.
    """
    matches = match_for_business(
        business_postcode=business_postcode,
        vertical=vertical,
        opportunities=opportunities,
        same_region_only=same_region_only,
    )
    framed = []
    for match in matches:
        framed.append(
            {
                **match,
                "customer_read": (
                    f"Someone nearby is doing work matching {vertical} services. "
                    f"{CUSTOMER_ACTIONS.get(vertical, 'Investigate before any contact.')}"
                ),
            }
        )
    return framed


def customer_digest(business_name: str, vertical: str, matches: list[dict], limit: int = 5) -> str:
    """Plain-English customer-finding digest. Compliance warnings included."""
    lines = [
        f"# Potential customers near you — {business_name}",
        "",
        f"{len(matches)} signal(s) suggest nearby demand for {vertical} work.",
        "These are public-record signals, not permission to contact anyone.",
        "",
    ]
    for match in matches[:limit]:
        title = match.get("title") or match.get("summary") or "Untitled record"
        locality = match.get("locality", "")
        where = f" ({locality})" if locality else ""
        lines.append(f"- {title}{where} [relevance {match['score']}]")
        lines.append(f"  Next step: {match.get('customer_read', 'Investigate before any contact.')}")
    if not matches:
        lines.append("- No signals this week. We'll keep watching.")
    lines += [
        "",
        "Reply APPROVE before we act on any lead. "
        "We never contact homeowners or businesses without verified details, "
        "permission, and TPS/CTPS screening.",
    ]
    return "\n".join(lines)


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
