"""Prospect scoring engine for electrical businesses.

Reads powuk's normalized data (Companies House, planning applications,
contracts finder) and generates scored prospect lists.
"""

import csv
import json
import os
import re
from collections import Counter, defaultdict
from datetime import date, datetime
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_electrical_businesses(powuk_base: str = "/root/powuk") -> list[dict]:
    """Load all electrical businesses from ch_capacity JSONL files.

    Returns list of dicts with keys:
    company_number, name, status, sic_codes, incorporation_date, postcode, cluster
    """
    base = Path(powuk_base) / "data" / "normalized" / "ch_capacity"
    businesses: list[dict] = []
    for jsonl_path in sorted(base.rglob("*.jsonl")):
        with open(jsonl_path, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    continue
                businesses.append({
                    "company_number": rec.get("company_number", ""),
                    "name": rec.get("name", ""),
                    "status": rec.get("status", ""),
                    "sic_codes": rec.get("sic_codes", []),
                    "incorporation_date": rec.get("incorporation_date"),
                    "postcode": rec.get("postcode", ""),
                    "cluster": rec.get("cluster", ""),
                })
    return businesses


# ---------------------------------------------------------------------------
# Postcode density
# ---------------------------------------------------------------------------

def count_postcode_density(businesses: list[dict]) -> dict[str, int]:
    """Count businesses per postcode area (first 2 chars of postcode).

    Returns {"M": 45, "B": 32, ...}
    """
    area_counter: Counter[str] = Counter()
    for b in businesses:
        pc = (b.get("postcode") or "").strip()
        if len(pc) >= 2:
            area = pc[:2].upper()
            area_counter[area] += 1
    return dict(area_counter.most_common())


def count_full_postcode_density(businesses: list[dict]) -> dict[str, int]:
    """Count businesses per full postcode.

    Returns {"M1 1AA": 12, "B1 1BB": 8, ...}
    """
    counter: Counter[str] = Counter()
    for b in businesses:
        pc = (b.get("postcode") or "").strip()
        if pc:
            counter[pc.upper()] += 1
    return dict(counter.most_common())


# ---------------------------------------------------------------------------
# Area signals (planning + contracts)
# ---------------------------------------------------------------------------

def _extract_postcode_area(postcode: str) -> str | None:
    """Extract the first 2 characters of a UK postcode as the area code."""
    pc = (postcode or "").strip()
    if len(pc) >= 2:
        return pc[:2].upper()
    return None


def count_area_signals(powuk_base: str = "/root/powuk") -> dict[str, dict[str, int]]:
    """Count planning apps and contracts per postcode area.

    P0-4 fix: Planning apps are attributed to their actual location
    (extracted from the organisation-entity or address data), NOT spread
    across areas associated with procurement contracts. If no location
    can be determined from a planning app, it is counted in a '_unlocated'
    bucket rather than attributed to random areas.

    Returns {"GL": {"planning": 5, "contracts": 2}, ...}
    """
    signals: dict[str, dict[str, int]] = defaultdict(lambda: {"planning": 0, "contracts": 0})

    # --- Contracts finder: extract postal codes from tender items ---
    contracts_base = Path(powuk_base) / "data" / "normalized" / "contracts_finder"
    for jsonl_path in sorted(contracts_base.rglob("*.jsonl")):
        with open(jsonl_path, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    continue
                tender = rec.get("tender", {})
                for item in tender.get("items", []):
                    for addr in item.get("deliveryAddresses", []):
                        area = _extract_postcode_area(addr.get("postalCode", ""))
                        if area:
                            signals[area]["contracts"] += 1

    # --- Planning apps: count per organisation-entity, attribute to actual location ---
    planning_base = Path(powuk_base) / "data" / "normalized" / "planning_apps"
    # Try to map organisation-entities to postcode areas from contract data
    org_areas: dict[int, str] = {}

    for jsonl_path in sorted(planning_base.rglob("*.jsonl")):
        with open(jsonl_path, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    continue

                # Try to extract a postcode area from the planning app itself
                # Planning apps may have location data in various fields
                area = None

                # Check for postcode in the record
                postcode = rec.get("postcode") or rec.get("location_postcode") or ""
                if postcode:
                    area = _extract_postcode_area(postcode)

                # Check for address fields
                if not area:
                    for addr_field in ["address", "location", "site_address"]:
                        addr_val = rec.get(addr_field, "")
                        if isinstance(addr_val, str) and addr_val:
                            # Try to extract postcode from address string
                            pc_match = re.search(r'[A-Z]{1,2}\d{1,2}[A-Z]?\s*\d[A-Z]{2}', addr_val, re.IGNORECASE)
                            if pc_match:
                                area = _extract_postcode_area(pc_match.group())
                                break

                if area:
                    signals[area]["planning"] += 1
                else:
                    # No location data — count in unlocated bucket
                    signals["_unlocated"]["planning"] += 1

    return dict(signals)


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------

def score_business(
    business: dict,
    planning_count: int = 0,
    contract_count: int = 0,
    postcode_density: int = 1,
    max_density: int = 1,
) -> float:
    """Score a business 0-100 based on how well it FITS our target profile.

    This is a FIT score only — it measures whether the business is the
    right type, size, and age for our offering. It does NOT reward
    businesses for having strong online presence (that's the gap score).

    Components:
      - Status: active = continue, dissolved/other = 0 (early exit)
      - Is actual electrician: +20 if SIC 43210 (max 20 pts)
      - Business age: newer incorporation → higher (max 25 pts)
      - Postcode density: denser cluster → higher (max 15 pts)
      - SIC code diversity: more SICs → higher (max 10 pts)
      - Planning activity nearby: +15 if planning apps in area
      - Contract activity nearby: +15 if contracts in area
    """
    # Status gate
    status = (business.get("status") or "").lower().strip()
    if status != "active":
        return 0.0

    score = 0.0

    # --- Is actual electrician (max 20 pts) ---
    sic_codes = business.get("sic_codes") or []
    if "43210" in sic_codes:
        score += 20  # Electrical installation — our target
    elif any(sic.startswith("43") for sic in sic_codes):
        score += 10  # Related construction
    elif any(sic.startswith("61") for sic in sic_codes):
        score += 5   # Telecoms (related but not core)
    else:
        score += 0   # IT, energy, etc. — not our target

    # --- Business age (max 25 pts) ---
    inc_str = business.get("incorporation_date")
    if inc_str:
        try:
            inc_date = datetime.strptime(str(inc_str), "%Y-%m-%d").date()
            age_years = (date.today() - inc_date).days / 365.25
            # 0-3 years → 25 pts (new, needs setup), 3-7 → 20 pts, 7-15 → 10 pts, 15+ → 5 pts
            if age_years <= 3:
                score += 25
            elif age_years <= 7:
                score += 20
            elif age_years <= 15:
                score += 10
            else:
                score += 5
        except (ValueError, TypeError):
            pass
    else:
        # Unknown date → treat as medium age
        score += 12

    # --- Postcode density (max 15 pts) ---
    if max_density > 0:
        density_ratio = min(postcode_density / max_density, 1.0)
        score += round(density_ratio * 15, 1)

    # --- SIC code diversity (max 10 pts) ---
    num_sics = len(sic_codes)
    if num_sics >= 4:
        score += 10
    elif num_sics >= 3:
        score += 8
    elif num_sics >= 2:
        score += 5
    elif num_sics >= 1:
        score += 2

    # --- Planning activity nearby (max 15 pts) ---
    if planning_count > 0:
        score += min(planning_count / 10, 15)  # Scale by count, cap at 15

    # --- Contract activity nearby (max 15 pts) ---
    if contract_count > 0:
        score += min(contract_count / 10, 15)  # Scale by count, cap at 15

    return round(min(score, 100.0), 1)


def calculate_gap_score(business: dict) -> float:
    """Calculate how much a business NEEDS our help (0-100).

    High gap = business has weak online presence, few reviews, incomplete
    profile. These businesses benefit most from our service.

    Low gap = business is already doing well online, has lots of reviews,
    complete profile. They need us less.

    Returns 0-100 where 100 = biggest gap = highest priority.
    """
    gap = 0.0

    # --- Review count (0-35 pts) ---
    # Fewer reviews = bigger gap (business is invisible or new)
    reviews = business.get("review_count") or 0
    if reviews == 0:
        gap += 35  # No reviews at all — biggest gap
    elif reviews < 5:
        gap += 30
    elif reviews < 20:
        gap += 20
    elif reviews < 50:
        gap += 10
    # 50+ reviews = no gap bonus

    # --- Rating (0-15 pts) ---
    # Low or missing rating = bigger gap
    rating = business.get("rating") or 0
    if rating == 0:
        gap += 15  # No rating — invisible
    elif rating < 3.5:
        gap += 15  # Poor rating — needs help
    elif rating < 4.0:
        gap += 10
    elif rating < 4.5:
        gap += 5
    # 4.5+ = no gap bonus (doing well)

    # --- Website (0-20 pts) ---
    # No website = big gap
    website = business.get("website") or ""
    if not website:
        gap += 20
    elif "facebook.com" in website or "instagram.com" in website:
        # Only social media, no proper website
        gap += 10

    # --- Profile completeness (0-20 pts) ---
    # Missing data = gap
    fields_present = sum(1 for f in [
        business.get("phone"),
        business.get("email"),
        business.get("address"),
        business.get("instagram"),
        business.get("facebook"),
        business.get("description"),
        business.get("services"),
    ] if f)
    # 0 fields = 20 gap, each present field reduces gap
    gap += max(0, 20 - (fields_present * 3))

    # --- Description / services (0-10 pts) ---
    if not business.get("description"):
        gap += 5
    if not business.get("services"):
        gap += 5

    return round(min(gap, 100.0), 1)


# ---------------------------------------------------------------------------
# Prospect list generation
# ---------------------------------------------------------------------------

def generate_prospect_list(
    powuk_base: str = "/root/powuk",
    min_score: float = 50.0,
) -> list[dict]:
    """Generate a scored prospect list.

    Returns list of dicts sorted by score descending, each containing:
    company_number, name, status, sic_codes, incorporation_date, postcode,
    cluster, score, gap_score, area, planning_count, contract_count, density

    Final score = fit_score × (gap_score / 100)
    High fit + high gap = highest priority (business needs us and fits our profile).
    """
    businesses = load_electrical_businesses(powuk_base)
    if not businesses:
        return []

    area_density_map = count_postcode_density(businesses)
    full_density_map = count_full_postcode_density(businesses)
    area_signals = count_area_signals(powuk_base)

    # Find max density for normalisation (full postcode level)
    max_density = max(full_density_map.values()) if full_density_map else 1

    scored: list[dict] = []
    for b in businesses:
        pc = (b.get("postcode") or "").strip()
        area = pc[:2].upper() if len(pc) >= 2 else ""

        signals = area_signals.get(area, {"planning": 0, "contracts": 0})
        planning = signals["planning"]
        contracts = signals["contracts"]

        density = area_density_map.get(area, 0)
        full_density = full_density_map.get(pc.upper(), 0) if pc else 0

        fit = score_business(
            b,
            planning_count=planning,
            contract_count=contracts,
            postcode_density=full_density,
            max_density=max_density,
        )

        gap = calculate_gap_score(b)

        # Combined score: fit × gap_ratio
        # High fit + high gap = highest priority
        gap_ratio = gap / 100.0
        combined = round(fit * gap_ratio, 1)

        scored.append({
            "company_number": b["company_number"],
            "name": b["name"],
            "status": b["status"],
            "sic_codes": b["sic_codes"],
            "incorporation_date": b["incorporation_date"],
            "postcode": b["postcode"],
            "cluster": b["cluster"],
            "score": combined,
            "fit_score": fit,
            "gap_score": gap,
            "area": area,
            "planning_count": planning,
            "contract_count": contracts,
            "density": density,
        })

    # Deduplicate by company name (keep highest score)
    seen: dict[str, dict] = {}
    for p in scored:
        name = p["name"].strip()
        if name not in seen or p["score"] > seen[name]["score"]:
            seen[name] = p
    
    deduped = sorted(seen.values(), key=lambda x: x["score"], reverse=True)
    return [p for p in deduped if p["score"] >= min_score]


# ---------------------------------------------------------------------------
# CSV export
# ---------------------------------------------------------------------------

_CSV_FIELDS = [
    "rank",
    "company_number",
    "name",
    "status",
    "score",
    "fit_score",
    "gap_score",
    "postcode",
    "area",
    "cluster",
    "sic_codes",
    "incorporation_date",
    "planning_count",
    "contract_count",
    "density",
]


def export_csv(prospects: list[dict], output_path: str) -> str:
    """Export prospects to CSV. Returns the output path."""
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=_CSV_FIELDS, extrasaction="ignore")
        writer.writeheader()
        for i, p in enumerate(prospects, 1):
            row = {k: p.get(k, "") for k in _CSV_FIELDS}
            row["rank"] = i
            # Convert list fields to strings
            if isinstance(row.get("sic_codes"), list):
                row["sic_codes"] = "; ".join(row["sic_codes"])
            writer.writerow(row)
    return output_path


# ---------------------------------------------------------------------------
# Regional summary
# ---------------------------------------------------------------------------

def regional_summary(prospects: list[dict]) -> dict[str, dict]:
    """Summarise prospects by region.

    Returns {"M": {"count": 12, "avg_score": 73.4, "top_businesses": [...]}, ...}
    """
    regions: dict[str, list[dict]] = defaultdict(list)
    for p in prospects:
        area = p.get("area") or "unknown"
        regions[area].append(p)

    summary: dict[str, dict] = {}
    for area, items in sorted(regions.items(), key=lambda x: -len(x[1])):
        scores = [i["score"] for i in items]
        avg = round(sum(scores) / len(scores), 1) if scores else 0
        top = sorted(items, key=lambda x: x["score"], reverse=True)[:5]
        summary[area] = {
            "count": len(items),
            "avg_score": avg,
            "top_businesses": [
                {"name": t["name"], "company_number": t["company_number"], "score": t["score"]}
                for t in top
            ],
        }
    return summary


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys

    base = sys.argv[1] if len(sys.argv) > 1 else "/root/powuk"
    out = sys.argv[2] if len(sys.argv) > 2 else "/root/aionboard/data/prospects_scored.csv"
    limit = int(sys.argv[3]) if len(sys.argv) > 3 else 200

    print(f"Loading businesses from {base}...")
    all_biz = load_electrical_businesses(base)
    print(f"  Loaded {len(all_biz)} electrical businesses")

    print("Generating prospect list (min_score=50)...")
    prospects = generate_prospect_list(powuk_base=base, min_score=50.0)
    print(f"  {len(prospects)} prospects above threshold")

    # Take top N
    top = prospects[:limit]
    print(f"  Exporting top {len(top)} to {out}")
    export_csv(top, out)

    summary = regional_summary(top)
    print("\nRegional summary:")
    for area, info in list(summary.items())[:10]:
        print(f"  {area}: {info['count']} businesses, avg score {info['avg_score']}")

    print(f"\nDone. CSV written to {out}")
