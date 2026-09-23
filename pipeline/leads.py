"""Wire powuk leads into the outreach pipeline."""

import csv
import json
import os
from datetime import datetime


def import_planning_leads(db_conn, csv_path: str) -> int:
    """Import planning application leads into pipeline."""
    count = 0
    with open(csv_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            desc = row.get('description', '')
            
            # Determine which vertical this lead is for
            vertical = None
            desc_lower = desc.lower()
            if any(w in desc_lower for w in ['electrical', 'wiring', 'consumer unit', 'ev charger']):
                vertical = 'electrician'
            elif any(w in desc_lower for w in ['plumbing', 'heating', 'boiler', 'gas']):
                vertical = 'plumber'
            elif any(w in desc_lower for w in ['extension', 'renovation', 'conversion', 'new build']):
                vertical = 'builder'
            elif any(w in desc_lower for w in ['roofing', 'roof']):
                vertical = 'roofer'
            elif any(w in desc_lower for w in ['insulation', 'glazing', 'window']):
                vertical = 'installer'
            
            if not vertical:
                vertical = 'general'
            
            # Extract location from description
            location = ''
            if 'manchester' in desc_lower:
                location = 'Manchester'
            elif 'birmingham' in desc_lower:
                location = 'Birmingham'
            elif 'london' in desc_lower:
                location = 'London'
            elif 'leeds' in desc_lower:
                location = 'Leeds'
            elif 'liverpool' in desc_lower:
                location = 'Liverpool'
            
            # Create lead record
            lead_data = {
                'vertical': vertical,
                'city': location or 'UK',
                'business_name': f"Planning App: {row.get('reference', 'Unknown')[:50]}",
                'phone': '',
                'address': '',
                'rating': 0,
                'review_count': 0,
                'website': '',
                'email': '',
                'services': f"Planning application: {desc[:100]}",
                'description': desc,
                'company_number': '',
                'company_name': '',
                'company_status': '',
                'incorporation_date': '',
                'sic_codes': '',
                'registered_address': '',
                'director_name': '',
                'director_role': '',
                'source': 'planning_app',
                'source_query': row.get('reference', ''),
            }
            
            # Insert into prospects table
            db_conn.execute("""
                INSERT OR IGNORE INTO prospects 
                (vertical, city, business_name, phone, address, rating, review_count, 
                 website, email, services, description, company_number, company_name,
                 company_status, incorporation_date, sic_codes, registered_address,
                 director_name, director_role, source, source_query)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                lead_data['vertical'], lead_data['city'], lead_data['business_name'],
                lead_data['phone'], lead_data['address'], lead_data['rating'],
                lead_data['review_count'], lead_data['website'], lead_data['email'],
                lead_data['services'], lead_data['description'], lead_data['company_number'],
                lead_data['company_name'], lead_data['company_status'],
                lead_data['incorporation_date'], lead_data['sic_codes'],
                lead_data['registered_address'], lead_data['director_name'],
                lead_data['director_role'], lead_data['source'], lead_data['source_query']
            ))
            count += 1
    
    db_conn.commit()
    return count


def import_contract_leads(db_conn, csv_path: str) -> int:
    """Import procurement contract leads into pipeline."""
    count = 0
    with open(csv_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            title = row.get('title', '')
            buyer = row.get('buyer_name', '')
            email = row.get('buyer_email', '')
            value = row.get('value', 0)
            
            # Determine vertical from contract title
            vertical = 'general'
            title_lower = title.lower()
            if any(w in title_lower for w in ['electrical', 'installation', 'maintenance']):
                vertical = 'electrician'
            elif any(w in title_lower for w in ['cleaning', 'clean']):
                vertical = 'cleaners'
            elif any(w in title_lower for w in ['landscap', 'garden', 'grounds']):
                vertical = 'gardeners'
            elif any(w in title_lower for w in ['pest control']):
                vertical = 'pest_control'
            
            # Create lead record
            lead_data = {
                'vertical': vertical,
                'city': 'UK',
                'business_name': f"Contract: {buyer[:50]}",
                'phone': '',
                'address': '',
                'rating': 0,
                'review_count': 0,
                'website': '',
                'email': email,
                'services': f"Contract: {title[:100]} (Value: £{float(value):,.0f})",
                'description': row.get('description', ''),
                'company_number': '',
                'company_name': buyer,
                'company_status': 'active',
                'incorporation_date': '',
                'sic_codes': '',
                'registered_address': '',
                'director_name': '',
                'director_role': '',
                'source': 'contract',
                'source_query': title[:100],
            }
            
            db_conn.execute("""
                INSERT OR IGNORE INTO prospects 
                (vertical, city, business_name, phone, address, rating, review_count, 
                 website, email, services, description, company_number, company_name,
                 company_status, incorporation_date, sic_codes, registered_address,
                 director_name, director_role, source, source_query)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                lead_data['vertical'], lead_data['city'], lead_data['business_name'],
                lead_data['phone'], lead_data['address'], lead_data['rating'],
                lead_data['review_count'], lead_data['website'], lead_data['email'],
                lead_data['services'], lead_data['description'], lead_data['company_number'],
                lead_data['company_name'], lead_data['company_status'],
                lead_data['incorporation_date'], lead_data['sic_codes'],
                lead_data['registered_address'], lead_data['director_name'],
                lead_data['director_role'], lead_data['source'], lead_data['source_query']
            ))
            count += 1
    
    db_conn.commit()
    return count


def get_lead_stats(db_conn) -> dict:
    """Get statistics about leads in the pipeline."""
    stats = {}
    
    # Total leads
    stats['total'] = db_conn.execute("SELECT COUNT(*) FROM prospects").fetchone()[0]
    
    # By source
    for row in db_conn.execute("SELECT source, COUNT(*) as count FROM prospects GROUP BY source"):
        stats[f"source_{row['source']}"] = row['count']
    
    # By vertical
    for row in db_conn.execute("SELECT vertical, COUNT(*) as count FROM prospects GROUP BY vertical"):
        stats[f"vertical_{row['vertical']}"] = row['count']
    
    # By stage
    for row in db_conn.execute("SELECT stage, COUNT(*) as count FROM prospects GROUP BY stage"):
        stats[f"stage_{row['stage']}"] = row['count']
    
    # With email
    stats['with_email'] = db_conn.execute("SELECT COUNT(*) FROM prospects WHERE email IS NOT NULL AND email != ''").fetchone()[0]
    
    # With phone
    stats['with_phone'] = db_conn.execute("SELECT COUNT(*) FROM prospects WHERE phone IS NOT NULL AND phone != ''").fetchone()[0]
    
    return stats


if __name__ == "__main__":
    from pipeline.db import get_db, init_db
    
    init_db()
    db = get_db()
    
    # Import planning leads
    planning_path = "data/leads/planning_apps.csv"
    if os.path.exists(planning_path):
        count = import_planning_leads(db, planning_path)
        print(f"Imported {count} planning leads")
    
    # Import contract leads
    contracts_path = "data/leads/contracts.csv"
    if os.path.exists(contracts_path):
        count = import_contract_leads(db, contracts_path)
        print(f"Imported {count} contract leads")
    
    # Stats
    stats = get_lead_stats(db)
    print(f"\nPipeline stats:")
    for k, v in stats.items():
        print(f"  {k}: {v}")
    
    db.close()
