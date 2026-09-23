"""Prospect ingestion from multiple sources."""

import csv
import json
import os
import subprocess
import time
import urllib.request
import urllib.parse
import base64
from datetime import datetime


def ingest_from_csv(db_conn, csv_path: str) -> int:
    """Ingest prospects from a CSV file."""
    count = 0
    with open(csv_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            data = {
                "vertical": row.get("vertical", ""),
                "city": row.get("city", ""),
                "business_name": row.get("businessName", row.get("business_name", "")),
                "phone": row.get("phone", ""),
                "address": row.get("address", ""),
                "postcode": row.get("postcode", ""),
                "rating": float(row.get("rating") or 0),
                "review_count": int(row.get("reviewCount") or row.get("review_count") or 0),
                "website": row.get("website", ""),
                "email": row.get("email", ""),
                "instagram": row.get("instagram", ""),
                "facebook": row.get("facebook", ""),
                "services": row.get("services", ""),
                "description": row.get("description", ""),
                "company_number": row.get("company_number", ""),
                "company_name": row.get("company_name", ""),
                "company_status": row.get("company_status", ""),
                "incorporation_date": row.get("incorporation_date", ""),
                "sic_codes": row.get("sic_codes", ""),
                "registered_address": row.get("registered_address", ""),
                "director_name": row.get("director_name", row.get("directors", "")),
                "director_role": row.get("director_role", ""),
                "source": row.get("source", "csv"),
                "source_query": row.get("search_query", ""),
            }
            if data["business_name"]:
                from pipeline.db import upsert_prospect
                upsert_prospect(db_conn, data)
                count += 1
    db_conn.commit()
    return count


def ingest_from_serpapi(db_conn, api_key: str, verticals: dict, cities: list) -> int:
    """Ingest prospects from SerpAPI Google Maps search."""
    from pipeline.db import upsert_prospect
    
    count = 0
    total = len(cities) * len(verticals)
    idx = 0
    
    for city in cities:
        for vertical, template in verticals.items():
            idx += 1
            query = template.format(city=city)
            print(f"[{idx}/{total}] {vertical} in {city}...", end=" ", flush=True)
            
            try:
                url = f"https://serpapi.com/search.json?engine=google_maps&q={urllib.parse.quote(query)}&api_key={api_key}&hl=en&gl=uk"
                req = urllib.request.Request(url)
                resp = urllib.request.urlopen(req, timeout=15)
                data = json.loads(resp.read())
                results = data.get("local_results", [])
                
                for r in results:
                    prospect_data = {
                        "vertical": vertical,
                        "city": city,
                        "business_name": r.get("title", ""),
                        "phone": r.get("phone", ""),
                        "address": r.get("address", ""),
                        "rating": float(r.get("rating", 0) or 0),
                        "review_count": int(r.get("reviews", 0) or 0),
                        "website": r.get("website", ""),
                        "source": "serpapi",
                        "source_query": query,
                    }
                    if prospect_data["business_name"]:
                        upsert_prospect(db_conn, prospect_data)
                        count += 1
                
                print(f"{len(results)} found")
            except Exception as e:
                print(f"ERROR: {e}")
            
            time.sleep(1)
    
    db_conn.commit()
    return count


def enrich_with_companies_house(db_conn, api_key: str, limit: int = 100) -> int:
    """Enrich prospects with Companies House data.

    Matching rules (P0-2 fix):
    - Require exact name match (case-insensitive) OR exact company_number match
    - Partial substring matches are NOT accepted
    - If no confident match, leave fields empty (don't guess)
    - Log when match is uncertain
    """
    from pipeline.db import upsert_prospect
    
    prospects = db_conn.execute(
        "SELECT id, business_name FROM prospects WHERE company_number IS NULL OR company_number='' LIMIT ?",
        (limit,)
    ).fetchall()
    
    enriched = 0
    for p in prospects:
        name = p["business_name"]
        try:
            # Search Companies House
            url = f"https://api.company-information.service.gov.uk/search/companies?q={urllib.parse.quote(name)}"
            req = urllib.request.Request(url)
            req.add_header("Authorization", f"Basic {base64.b64encode(f'{api_key}:'.encode()).decode()}")
            resp = urllib.request.urlopen(req, timeout=10)
            data = json.loads(resp.read())
            items = data.get("items", [])
            
            if items:
                # Find exact name match only — no partial matches
                best = None
                name_lower = name.lower().strip()
                for item in items:
                    item_title = (item.get("title", "") or "").lower().strip()
                    if item_title == name_lower:
                        best = item
                        break
                
                if not best:
                    # No exact match found — skip to avoid false positives
                    print(f"  [CH] No exact match for '{name}' — skipping enrichment")
                    time.sleep(0.3)
                    continue
                
                company_number = best.get("company_number", "")
                if company_number:
                    # Get full details
                    detail_url = f"https://api.company-information.service.gov.uk/company/{company_number}"
                    detail_req = urllib.request.Request(detail_url)
                    detail_req.add_header("Authorization", f"Basic {base64.b64encode(f'{api_key}:'.encode()).decode()}")
                    detail_resp = urllib.request.urlopen(detail_req, timeout=10)
                    details = json.loads(detail_resp.read())
                    
                    # Get officers
                    officer_url = f"https://api.company-information.service.gov.uk/company/{company_number}/officers"
                    officer_req = urllib.request.Request(officer_url)
                    officer_req.add_header("Authorization", f"Basic {base64.b64encode(f'{api_key}:'.encode()).decode()}")
                    officer_resp = urllib.request.urlopen(officer_req, timeout=10)
                    officers = json.loads(officer_resp.read()).get("items", [])
                    
                    # Find director
                    director_name = ""
                    director_role = ""
                    for o in officers:
                        if o.get("officer_role") == "director":
                            director_name = o.get("name", "")
                            director_role = "director"
                            break
                    
                    # Update prospect
                    db_conn.execute(
                        """UPDATE prospects SET 
                           company_number=?, company_name=?, company_status=?, 
                           incorporation_date=?, sic_codes=?, registered_address=?,
                           director_name=?, director_role=?, updated_at=?
                           WHERE id=?""",
                        (
                            company_number,
                            details.get("company_name", ""),
                            details.get("company_status", ""),
                            details.get("date_of_creation", ""),
                            ",".join(details.get("sic_codes", [])),
                            f"{details.get('registered_office_address', {}).get('address_line_1', '')} {details.get('registered_office_address', {}).get('locality', '')}".strip(),
                            director_name,
                            director_role,
                            datetime.now().isoformat(),
                            p["id"],
                        )
                    )
                    enriched += 1
            
            time.sleep(0.3)
        except Exception as e:
            pass
    
    db_conn.commit()
    return enriched


def enrich_with_website_scrape(db_conn, limit: int = 100) -> int:
    """Enrich prospects by scraping their websites."""
    import re
    
    prospects = db_conn.execute(
        "SELECT id, website FROM prospects WHERE website IS NOT NULL AND website!='' AND (email IS NULL OR email='') LIMIT ?",
        (limit,)
    ).fetchall()
    
    enriched = 0
    for p in prospects:
        url = p["website"]
        if not url or "instagram.com" in url or "facebook.com" in url:
            continue
        
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            resp = urllib.request.urlopen(req, timeout=10)
            html = resp.read().decode("utf-8", errors="ignore")
            
            updates = {}
            
            # Extract email
            emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", html)
            valid_emails = [e for e in emails if "example.com" not in e and "domain.com" not in e]
            if valid_emails:
                updates["email"] = valid_emails[0]
            
            # Extract Instagram
            instagram = re.findall(r"instagram\.com/([a-zA-Z0-9_.]+)", html)
            if instagram:
                updates["instagram"] = instagram[0]
            
            # Extract Facebook
            facebook = re.findall(r"facebook\.com/([a-zA-Z0-9_.]+)", html)
            if facebook:
                updates["facebook"] = facebook[0]
            
            # Extract description
            desc = re.findall(r'<meta\s+name="description"\s+content="([^"]*)"', html)
            if desc:
                updates["description"] = desc[0][:200]
            
            if updates:
                updates["updated_at"] = datetime.now().isoformat()
                set_clause = ", ".join(f"{k}=?" for k in updates)
                db_conn.execute(f"UPDATE prospects SET {set_clause} WHERE id=?", list(updates.values()) + [p["id"]])
                enriched += 1
            
            time.sleep(0.5)
        except:
            pass
    
    db_conn.commit()
    return enriched


def score_prospects(db_conn) -> int:
    """Score prospects based on business fit and observable gaps.

    P0-5/P0-8 fix: Separates fit (is it the right business?) from gap
    (does it need our help?). High ratings/reviews REDUCE priority —
    businesses doing well online don't need us. Businesses with gaps
    (low reviews, no website, incomplete profile) are our targets.
    """
    prospects = db_conn.execute("SELECT * FROM prospects").fetchall()
    
    scored = 0
    for p in prospects:
        fit_score = 0
        gap_score = 0
        reasons = []
        
        # === FIT SCORE: Is this the right type of business? (0-50) ===
        
        # Has phone (contactable = higher fit)
        if p["phone"]:
            fit_score += 10
            reasons.append("has_phone")
        
        # Has email (contactable)
        if p["email"]:
            fit_score += 5
            reasons.append("has_email")
        
        # Has director name (real business, not a shell)
        if p["director_name"]:
            fit_score += 10
            reasons.append("has_director")
        
        # Company is active
        if p["company_status"] == "active":
            fit_score += 10
            reasons.append("active_company")
        
        # Has address (real location)
        if p["address"]:
            fit_score += 5
            reasons.append("has_address")
        
        # Has services listed
        if p["services"]:
            fit_score += 5
            reasons.append("has_services")
        
        # Has website (contactable, established)
        if p["website"]:
            fit_score += 5
            reasons.append("has_website")
        
        # === GAP SCORE: Does this business need our help? (0-50) ===
        
        # Low reviews = big gap (invisible or struggling)
        reviews = p["review_count"] or 0
        if reviews == 0:
            gap_score += 20
            reasons.append("no_reviews")
        elif reviews < 5:
            gap_score += 15
            reasons.append("few_reviews")
        elif reviews < 20:
            gap_score += 10
            reasons.append("low_reviews")
        # 20+ reviews = no gap bonus
        
        # Low or missing rating
        rating = p["rating"] or 0
        if rating == 0:
            gap_score += 10
            reasons.append("no_rating")
        elif rating < 3.5:
            gap_score += 10
            reasons.append("low_rating")
        elif rating < 4.0:
            gap_score += 5
            reasons.append("below_4_rating")
        # 4.0+ = no gap bonus
        
        # No website = gap
        if not p["website"]:
            gap_score += 10
            reasons.append("no_website")
        
        # Incomplete profile (missing social/contact data)
        missing_fields = sum(1 for f in [p["email"], p["instagram"], p["facebook"], p["description"]] if not f)
        if missing_fields >= 3:
            gap_score += 10
            reasons.append("incomplete_profile")
        elif missing_fields >= 2:
            gap_score += 5
            reasons.append("partially_incomplete")
        
        # Combined score: fit × gap_ratio
        gap_ratio = gap_score / 50.0  # normalize to 0-1
        combined = round(fit_score * gap_ratio, 1)
        
        # Update
        db_conn.execute(
            "UPDATE prospects SET score=?, score_reasons=? WHERE id=?",
            (combined, ",".join(reasons), p["id"])
        )
        scored += 1
    
    db_conn.commit()
    return scored


if __name__ == "__main__":
    from pipeline.db import get_db, init_db
    
    init_db()
    db = get_db()
    
    # Ingest from existing CSV
    csv_path = "data/prospects/serpapi_all_verticals.csv"
    if os.path.exists(csv_path):
        count = ingest_from_csv(db, csv_path)
        print(f"Ingested {count} prospects from CSV")
    
    # Score
    scored = score_prospects(db)
    print(f"Scored {scored} prospects")
    
    # Stats
    stats = db.execute("SELECT stage, COUNT(*) FROM prospects GROUP BY stage").fetchall()
    print(f"\nPipeline stages:")
    for stage, count in stats:
        print(f"  {stage}: {count}")
    
    db.close()
