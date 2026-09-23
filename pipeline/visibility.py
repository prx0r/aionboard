"""ChatGPT visibility tools per vertical.

Makes businesses show up when people ask AI assistants.

NOTE: The 'data completeness score' below measures what data WE have about
a business in our database. It does NOT measure actual Google Business
Profile status, Google ranking, or real-world visibility. Do not present
this score as 'GBP completeness' or 'Google visibility'.
"""

import json


# Schema markup templates per vertical
SCHEMA_TEMPLATES = {
    "nails": {
        "@context": "https://schema.org",
        "@type": "BeautySalon",
        "name": "{business_name}",
        "address": {"@type": "PostalAddress", "streetAddress": "{address}", "addressLocality": "{city}", "postalCode": "{postcode}"},
        "telephone": "{phone}",
        "url": "{website}",
        "openingHours": "{hours}",
        "priceRange": "{price_range}",
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Nail Services",
            "itemListElement": []
        },
    },
    "electrician": {
        "@context": "https://schema.org",
        "@type": "Electrician",
        "name": "{business_name}",
        "address": {"@type": "PostalAddress", "streetAddress": "{address}", "addressLocality": "{city}", "postalCode": "{postcode}"},
        "telephone": "{phone}",
        "url": "{website}",
        "openingHours": "{hours}",
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Electrical Services",
            "itemListElement": []
        },
    },
    "dog_groomers": {
        "@context": "https://schema.org",
        "@type": "PetStore",
        "name": "{business_name}",
        "address": {"@type": "PostalAddress", "streetAddress": "{address}", "addressLocality": "{city}", "postalCode": "{postcode}"},
        "telephone": "{phone}",
        "url": "{website}",
        "openingHours": "{hours}",
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Dog Grooming Services",
            "itemListElement": []
        },
    },
    "cleaners": {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": "{business_name}",
        "address": {"@type": "PostalAddress", "streetAddress": "{address}", "addressLocality": "{city}", "postalCode": "{postcode}"},
        "telephone": "{phone}",
        "url": "{website}",
        "openingHours": "{hours}",
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Cleaning Services",
            "itemListElement": []
        },
    },
    "hair": {
        "@context": "https://schema.org",
        "@type": "HairSalon",
        "name": "{business_name}",
        "address": {"@type": "PostalAddress", "streetAddress": "{address}", "addressLocality": "{city}", "postalCode": "{postcode}"},
        "telephone": "{phone}",
        "url": "{website}",
        "openingHours": "{hours}",
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Hair Services",
            "itemListElement": []
        },
    },
    "beauty": {
        "@context": "https://schema.org",
        "@type": "BeautySalon",
        "name": "{business_name}",
        "address": {"@type": "PostalAddress", "streetAddress": "{address}", "addressLocality": "{city}", "postalCode": "{postcode}"},
        "telephone": "{phone}",
        "url": "{website}",
        "openingHours": "{hours}",
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Beauty Services",
            "itemListElement": []
        },
    },
    "lashes": {
        "@context": "https://schema.org",
        "@type": "BeautySalon",
        "name": "{business_name}",
        "address": {"@type": "PostalAddress", "streetAddress": "{address}", "addressLocality": "{city}", "postalCode": "{postcode}"},
        "telephone": "{phone}",
        "url": "{website}",
        "openingHours": "{hours}",
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Lash Services",
            "itemListElement": []
        },
    },
    "car_detailers": {
        "@context": "https://schema.org",
        "@type": "AutomotiveBusiness",
        "name": "{business_name}",
        "address": {"@type": "PostalAddress", "streetAddress": "{address}", "addressLocality": "{city}", "postalCode": "{postcode}"},
        "telephone": "{phone}",
        "url": "{website}",
        "openingHours": "{hours}",
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Car Detailing Services",
            "itemListElement": []
        },
    },
    "driving_instructors": {
        "@context": "https://schema.org",
        "@type": "DrivingSchool",
        "name": "{business_name}",
        "address": {"@type": "PostalAddress", "streetAddress": "{address}", "addressLocality": "{city}", "postalCode": "{postcode}"},
        "telephone": "{phone}",
        "url": "{website}",
        "openingHours": "{hours}",
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Driving Lessons",
            "itemListElement": []
        },
    },
    "gardeners": {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": "{business_name}",
        "address": {"@type": "PostalAddress", "streetAddress": "{address}", "addressLocality": "{city}", "postalCode": "{postcode}"},
        "telephone": "{phone}",
        "url": "{website}",
        "openingHours": "{hours}",
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Gardening Services",
            "itemListElement": []
        },
    },
    "weddings": {
        "@context": "https://schema.org",
        "@type": "Photographer",
        "name": "{business_name}",
        "address": {"@type": "PostalAddress", "streetAddress": "{address}", "addressLocality": "{city}", "postalCode": "{postcode}"},
        "telephone": "{phone}",
        "url": "{website}",
        "openingHours": "{hours}",
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Wedding Photography Packages",
            "itemListElement": []
        },
    },
}


def generate_schema_markup(vertical: str, business_data: dict) -> str:
    """Generate schema.org markup for a business."""
    template = SCHEMA_TEMPLATES.get(vertical, SCHEMA_TEMPLATES["nails"])
    
    # Fill in template with business data
    schema = json.loads(json.dumps(template))
    
    # Replace placeholders
    schema_str = json.dumps(schema, indent=2)
    for key, value in business_data.items():
        schema_str = schema_str.replace(f"{{{key}}}", str(value))
    
    # Add services if provided
    if "services" in business_data:
        services = business_data["services"]
        if isinstance(services, str):
            services = [s.strip() for s in services.split(",")]
        
        schema = json.loads(schema_str)
        catalog = schema.get("hasOfferCatalog", {})
        items = []
        for i, service in enumerate(services):
            if isinstance(service, dict):
                items.append({
                    "@type": "Offer",
                    "name": service.get("name", ""),
                    "price": service.get("price", ""),
                    "priceCurrency": "GBP",
                })
            else:
                items.append({
                    "@type": "Offer",
                    "name": service,
                })
        catalog["itemListElement"] = items
        schema_str = json.dumps(schema, indent=2)
    
    return f'<script type="application/ld+json">\n{schema_str}\n</script>'


def generate_llms_txt(vertical: str, business_data: dict) -> str:
    """Generate llms.txt for a business (AI-readable summary)."""
    name = business_data.get("business_name", "Business")
    address = business_data.get("address", "")
    city = business_data.get("city", "")
    phone = business_data.get("phone", "")
    services = business_data.get("services", "")
    hours = business_data.get("hours", "Mon-Fri 9am-5pm")
    
    if isinstance(services, list):
        services = ", ".join([s.get("name", s) if isinstance(s, dict) else s for s in services])
    
    llms = f"""# {name}

## About
{name} is a {vertical} business in {city}.

## Contact
- Phone: {phone}
- Address: {address}
- Hours: {hours}

## Services
{services}

## How to book
Contact {phone} or visit the website to book an appointment.

## Location
{address}, {city}
"""
    
    return llms


def generate_robots_txt() -> str:
    """Generate robots.txt allowing AI crawlers."""
    return """User-agent: *
Allow: /

User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: CCBot
Allow: /

User-agent: anthropic-ai
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Applebot-Extended
Allow: /

Sitemap: /sitemap.xml
"""


def generate_visibility_checklist(vertical: str, business_data: dict) -> list:
    """Generate a checklist for improving AI visibility."""
    checklist = [
        {"item": "Schema markup added", "status": "pending", "priority": "high"},
        {"item": "llms.txt created", "status": "pending", "priority": "high"},
        {"item": "robots.txt allows AI crawlers", "status": "pending", "priority": "high"},
        {"item": "Google Business Profile complete", "status": "pending", "priority": "high"},
        {"item": "NAP consistent across platforms", "status": "pending", "priority": "high"},
        {"item": "Website has meta description", "status": "pending", "priority": "medium"},
        {"item": "Website has structured data", "status": "pending", "priority": "medium"},
        {"item": "Bing Webmaster Tools submitted", "status": "pending", "priority": "medium"},
        {"item": "Social media profiles linked", "status": "pending", "priority": "low"},
        {"item": "Reviews responded to", "status": "pending", "priority": "low"},
    ]
    
    # Pre-fill what we know
    if business_data.get("website"):
        checklist[3]["status"] = "done"
    if business_data.get("google_complete"):
        checklist[3]["status"] = "done"
    
    return checklist


def calculate_data_completeness_score(vertical: str, business_data: dict) -> dict:
    """Calculate data completeness score (0-100).

    IMPORTANT: This measures data we have in OUR database, NOT actual
    Google Business Profile completeness, Google ranking, or real-world
    online visibility. Do not present this as 'GBP score' or 'visibility'.
    """
    score = 0
    factors = []
    
    # Has website (+20)
    if business_data.get("website"):
        score += 20
        factors.append("has_website")
    
    # Has rating (+20) — means we have Google data
    if business_data.get("rating"):
        score += 20
        factors.append("has_rating_data")
    
    # Has phone number (+10)
    if business_data.get("phone"):
        score += 10
        factors.append("has_phone")
    
    # Has address (+10)
    if business_data.get("address"):
        score += 10
        factors.append("has_address")
    
    # Has reviews (+10)
    if business_data.get("reviewCount") and int(business_data.get("reviewCount", 0)) > 0:
        score += 10
        factors.append("has_reviews")
    
    # Rating above 4.0 (+10)
    if business_data.get("rating") and float(business_data.get("rating", 0)) > 4.0:
        score += 10
        factors.append("good_rating")
    
    # Has email (+5)
    if business_data.get("email"):
        score += 5
        factors.append("has_email")
    
    # Has Instagram (+5)
    if business_data.get("instagram"):
        score += 5
        factors.append("has_instagram")
    
    # Has description (+5)
    if business_data.get("description"):
        score += 5
        factors.append("has_description")
    
    # Has services listed (+5)
    if business_data.get("services"):
        score += 5
        factors.append("has_services")
    
    return {
        "score": min(score, 100),
        "factors": factors,
        "missing": [f for f in ["has_website", "has_rating_data", "has_phone", "has_address", "has_reviews", "good_rating", "has_email", "has_instagram", "has_description", "has_services"] if f not in factors],
        "_disclaimer": "This score measures data completeness in our database, NOT actual Google Business Profile status or online visibility.",
    }


# Backward-compatible alias (deprecated — use calculate_data_completeness_score)
def calculate_visibility_score(vertical: str, business_data: dict) -> dict:
    """Deprecated: use calculate_data_completeness_score instead."""
    return calculate_data_completeness_score(vertical, business_data)


if __name__ == "__main__":
    # Test schema generation
    print("=== SCHEMA MARKUP (nails) ===\n")
    schema = generate_schema_markup("nails", {
        "business_name": "Yulia Hamilton Nails",
        "address": "40 Laystall St",
        "city": "Manchester",
        "postcode": "M1 2JQ",
        "phone": "07858 358562",
        "hours": "Tue-Sat 9am-6pm",
        "services": ["Gel Manicure £35", "Acrylic Full Set £55", "Pedicure £40"],
    })
    print(schema[:500])
    
    # Test llms.txt
    print("\n=== LLMS.TXT (nails) ===\n")
    llms = generate_llms_txt("nails", {
        "business_name": "Yulia Hamilton Nails",
        "city": "Manchester",
        "address": "40 Laystall St, M1 2JQ",
        "phone": "07858 358562",
        "services": "Gel Manicure, Acrylic Full Set, Pedicure",
        "hours": "Tue-Sat 9am-6pm",
    })
    print(llms)
    
    # Test data completeness score
    print("\n=== DATA COMPLETENESS SCORE ===\n")
    score = calculate_data_completeness_score("nails", {
        "website": "https://mcrnails.co.uk",
        "rating": "4.8",
        "phone": "07858 358562",
        "address": "40 Laystall St",
        "reviewCount": "686",
        "email": "test@email.com",
        "instagram": "yh_nails",
        "description": "Manchester nail salon",
        "services": ["Gel Manicure", "Acrylic Full Set"],
    })
    print(f"Score: {score['score']}/100")
    print(f"Factors: {score['factors']}")
    print(f"Missing: {score['missing']}")
