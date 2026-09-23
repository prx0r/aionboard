"""Lead generation tools per vertical.

Monitors multiple sources to find people who need services RIGHT NOW.
"""

import json
import os
import re
from datetime import datetime, timedelta
from pathlib import Path


# Planning application keywords per vertical
PLANNING_KEYWORDS = {
    "electrician": ["electrical", "wiring", "consumer unit", "ev charger", "solar", "pv", "rewire", "extension", "new build"],
    "builder": ["extension", "renovation", "conversion", "new build", "loft", "basement"],
    "plumber": ["plumbing", "heating", "boiler", "bathroom", "kitchen"],
    "cleaners": ["new build", "renovation", "extension"],
    "gardeners": ["landscaping", "garden", "grounds"],
}

# Social media keywords per vertical
SOCIAL_KEYWORDS = {
    "nails": ["nail tech", "nail salon", "gel nails", "acrylic nails", "nails near me", "nail art"],
    "electrician": ["electrician", "electrician near me", "need an electrician", "EV charger"],
    "dog_groomers": ["dog groomer", "grooming near me", "dog wash", "puppy groom"],
    "cleaners": ["cleaner near me", "cleaning service", "end of tenancy clean"],
    "hair": ["hairdresser", "hair salon", "balayage", "colourist", "hair near me"],
    "beauty": ["beauty salon", "facial", "waxing", "beauty near me"],
    "lashes": ["lash extensions", "lash tech", "lash lift", "lashes near me"],
    "car_detailers": ["car detail", "car valet", "ceramic coating", "mobile detailer"],
    "driving_instructors": ["driving instructor", "driving lessons", "learn to drive"],
    "gardeners": ["gardener", "garden maintenance", "lawn mowing", "window cleaner"],
    "weddings": ["wedding photographer", "wedding videographer", "wedding venues"],
}


def scan_planning_apps(powuk_path: str = "/root/powuk/data/normalized/planning_apps") -> list:
    """Scan planning applications for trade-relevant leads."""
    leads = []
    
    # Find latest date directory
    date_path = Path(powuk_path) / "2026" / "09"
    if not date_path.exists():
        return leads
    
    for day_dir in sorted(date_path.iterdir()):
        if not day_dir.is_dir():
            continue
        for jsonl_file in day_dir.glob("*.jsonl"):
            with open(jsonl_file) as f:
                for line in f:
                    try:
                        app = json.loads(line)
                        desc = app.get("description", "").lower()
                        
                        for vertical, keywords in PLANNING_KEYWORDS.items():
                            if any(kw in desc for kw in keywords):
                                leads.append({
                                    "source": "planning_app",
                                    "vertical": vertical,
                                    "reference": app.get("reference", ""),
                                    "description": app.get("description", "")[:200],
                                    "decision_date": app.get("decision-date", ""),
                                    "organisation": app.get("organisation-entity", ""),
                                })
                                break
                    except:
                        pass
    
    return leads


def scan_instagram_keywords(vertical: str, city: str) -> list:
    """Generate Instagram search queries for lead finding."""
    keywords = SOCIAL_KEYWORDS.get(vertical, [])
    queries = []
    for kw in keywords:
        queries.append(f"{kw} {city}")
        queries.append(f"{kw} near {city}")
    return queries


def calculate_pain(vertical: str, business_data: dict) -> dict:
    """Calculate how much money a business is losing from specific problems.

    IMPORTANT: All figures are HYPOTHETICAL SCENARIOS based on industry
    averages. They are NOT actual losses for this specific business unless
    the caller provides verified inputs via business_data.

    When business_data contains verified values (e.g. confirmed call volume,
    actual booking rate), those are used. Otherwise, industry defaults are
    applied and clearly labelled as assumptions.
    """
    
    pain_calculations = {
        "nails": {
            "missed_bookings": {
                "description": "Lost bookings from slow DM replies (hypothetical)",
                "formula": "enquiries_per_week * loss_rate * avg_booking_value",
                "defaults": {"enquiries_per_week": 15, "loss_rate": 0.3, "avg_booking_value": 40},
                "annual_loss": lambda d: d["enquiries_per_week"] * d["loss_rate"] * d["avg_booking_value"] * 52,
            },
            "no_shows": {
                "description": "Revenue lost to no-shows (hypothetical)",
                "formula": "appointments_per_week * no_show_rate * avg_booking_value",
                "defaults": {"appointments_per_week": 20, "no_show_rate": 0.10, "avg_booking_value": 40},
                "annual_loss": lambda d: d["appointments_per_week"] * d["no_show_rate"] * d["avg_booking_value"] * 52,
            },
        },
        "electrician": {
            "missed_calls": {
                "description": "Revenue lost from missed calls while on tools (hypothetical)",
                "formula": "calls_per_day * loss_rate * avg_job_value",
                "defaults": {"calls_per_day": 4, "loss_rate": 0.7, "avg_job_value": 250},
                "annual_loss": lambda d: d["calls_per_day"] * d["loss_rate"] * d["avg_job_value"] * 250,
            },
            "quote_followup": {
                "description": "Revenue lost from un-followed quotes (hypothetical)",
                "formula": "quotes_per_week * no_followup_rate * avg_quote_value * close_rate",
                "defaults": {"quotes_per_week": 5, "no_followup_rate": 0.5, "avg_quote_value": 500, "close_rate": 0.3},
                "annual_loss": lambda d: d["quotes_per_week"] * d["no_followup_rate"] * d["avg_quote_value"] * d["close_rate"] * 52,
            },
        },
        "dog_groomers": {
            "no_shows": {
                "description": "Revenue lost to no-shows (hypothetical)",
                "formula": "appointments_per_week * no_show_rate * avg_groom_value",
                "defaults": {"appointments_per_week": 15, "no_show_rate": 0.12, "avg_groom_value": 45},
                "annual_loss": lambda d: d["appointments_per_week"] * d["no_show_rate"] * d["avg_groom_value"] * 52,
            },
            "missed_bookings": {
                "description": "Lost bookings from slow responses (hypothetical)",
                "formula": "enquiries_per_week * loss_rate * avg_groom_value",
                "defaults": {"enquiries_per_week": 10, "loss_rate": 0.3, "avg_groom_value": 45},
                "annual_loss": lambda d: d["enquiries_per_week"] * d["loss_rate"] * d["avg_groom_value"] * 52,
            },
        },
        "cleaners": {
            "invoice_chasing": {
                "description": "Admin time spent chasing invoices (hypothetical)",
                "formula": "hours_per_week * hourly_rate * 52",
                "defaults": {"hours_per_week": 2, "hourly_rate": 25},
                "annual_loss": lambda d: d["hours_per_week"] * d["hourly_rate"] * 52,
            },
            "missed_bookings": {
                "description": "Lost recurring clients from poor communication (hypothetical)",
                "formula": "clients_per_month * loss_rate * monthly_value",
                "defaults": {"clients_per_month": 10, "loss_rate": 0.1, "monthly_value": 320},
                "annual_loss": lambda d: d["clients_per_month"] * d["loss_rate"] * d["monthly_value"] * 12,
            },
        },
    }
    
    calc = pain_calculations.get(vertical, {})
    results = {}
    
    for problem, config in calc.items():
        # Merge defaults with any verified business_data overrides
        params = dict(config["defaults"])
        verified_overrides = []
        for key in params:
            if key in business_data and business_data[key] is not None:
                params[key] = business_data[key]
                verified_overrides.append(key)

        annual = config["annual_loss"](params)
        monthly = annual / 12
        weekly = annual / 52

        # Determine if figures are verified or hypothetical
        is_verified = len(verified_overrides) == len(params)
        label = "verified" if is_verified else "hypothetical (industry averages)"
        
        results[problem] = {
            "description": config["description"],
            "annual_loss": round(annual),
            "monthly_loss": round(monthly),
            "weekly_loss": round(weekly),
            "assumptions": params,
            "verified_inputs": verified_overrides,
            "data_quality": label,
        }
    
    return results


def format_pain_summary(vertical: str, business_name: str) -> str:
    """Format pain calculation as a message to send to the business.

    All figures are clearly labelled as hypothetical industry averages.
    """
    pain = calculate_pain(vertical, {})
    
    if not pain:
        return f"Hi {business_name}, we help businesses like yours save time and find more customers. Want to see how?"
    
    lines = [f"Hi {business_name},"]
    lines.append("")
    lines.append("Based on industry averages for businesses like yours, here's what you MIGHT be losing:")
    lines.append("")
    
    total_annual = 0
    for problem, data in pain.items():
        lines.append(f"• {data['description']}: ~£{data['annual_loss']:,}/year")
        total_annual += data['annual_loss']
    
    lines.append("")
    lines.append(f"That's ~£{total_annual:,}/year in potential lost revenue (based on industry averages).")
    lines.append("")
    lines.append("These are estimates — your actual numbers may vary. Want to see how we can help reduce these losses?")
    lines.append("")
    lines.append("Free 7-day trial, no commitment.")
    
    return "\n".join(lines)


if __name__ == "__main__":
    # Test pain calculations
    print("=== PAIN CALCULATIONS ===\n")
    
    for vertical in ["nails", "electrician", "dog_groomers", "cleaners"]:
        print(f"--- {vertical.upper()} ---")
        pain = calculate_pain(vertical, {})
        for problem, data in pain.items():
            print(f"  {data['description']}")
            print(f"    Annual: £{data['annual_loss']:,}")
            print(f"    Monthly: £{data['monthly_loss']:,}")
            print(f"    Weekly: £{data['weekly_loss']:,}")
        print()
    
    # Test pain summary message
    print("=== SAMPLE PAIN MESSAGE (nails) ===\n")
    print(format_pain_summary("nails", "Yulia Hamilton Nails"))
