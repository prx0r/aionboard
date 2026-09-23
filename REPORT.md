# REPORT.md — powuk × aionboard Integration

> How POWUK's UK physical economy data powers AI Onboard's market research, prospect identification, and launch strategy.

---

## Executive Summary

POWUK has been collecting UK physical economy data for months. This data is directly useful to AI Onboard for:

1. **Prospect identification** — 10,000+ electrical businesses with postcodes, SIC codes, and company numbers
2. **Market sizing** — labour demand data, wage data, training pipeline data
3. **Geographic targeting** — regional business density, planning applications, procurement signals
4. **Competitive intelligence** — who's hiring, who's expanding, who's in which trade

This report maps relevant POWUK datasets to AI Onboard research needs. It is research and planning, not proof that the datasets are sufficient for automated prospecting or that the proposed pipeline is built.

---

## 1. The Prospect Database — Electrical Businesses

### What we have

**10,000+ active electrical businesses** from Companies House, filtered by SIC code 43210 (Electrical installation).

Each record contains:
```json
{
  "company_number": "12013809",
  "name": "WN NETWORKS LTD",
  "status": "active",
  "sic_codes": ["43210"],
  "incorporation_date": null,
  "postcode": "S5 9LG",
  "cluster": "electrical"
}
```

### What this gives AI Onboard

| Use case | How |
|----------|-----|
| Research shortlist | Company name + postcode → independently verify contact details, permission, TPS/CTPS, and suppression before any contact |
| Business age | Incorporation date → established vs new |
| Geographic targeting | Postcode → region, city, area |
| Service inference | SIC codes → what they do (electrical, HVAC, solar) |
| Growth signals | Multiple SIC codes → diversified services |

### Regional breakdown (top 20 areas)

```
BT  215 businesses  (Belfast)
NG  209 businesses  (Nottingham)
CM  197 businesses  (Chelmsford)
RM  163 businesses  (Romford)
DA  160 businesses  (Dartford)
BS  159 businesses  (Bristol)
CF  156 businesses  (Cardiff)
LE  152 businesses  (Leicester)
BN  151 businesses  (Brighton)
ME  149 businesses  (Medway)
PO  148 businesses  (Portsmouth)
NE  145 businesses  (Newcastle)
SS  142 businesses  (Southend)
PE  142 businesses  (Peterborough)
TN  134 businesses  (Tunbridge Wells)
HA  128 businesses  (Harrow)
DN  124 businesses  (Doncaster)
RG  120 businesses  (Reading)
GU  116 businesses  (Guildford)
DE  114 businesses  (Derby)
```

### What we can build

A **prospect scoring system** that ranks businesses by:
- Business age (newer = more likely to need setup)
- Geographic density (clusters = referral opportunities)
- Service diversity (more SIC codes = more complex needs)
- Company status (active, recently incorporated)

---

## 2. Labour Market Intelligence

### What we have

| Dataset | Records | What it measures |
|---------|---------|------------------|
| `ons_labour` | 175,181 | Online job adverts by SOC code × region |
| `ons_salaries` | 50,973 | Asking salaries from job adverts |
| `ons_skills` | 4,282 | Skills mentioned in job adverts |
| `ashe_wages` | 3,906 | Official wage data by region × occupation |

### How this helps AI Onboard

**For sales targeting:**
- High demand for electricians in a region → more businesses likely to invest in AI
- Rising salaries → businesses have money to spend
- Skills gaps → businesses struggling to hire → AI could help

**For product positioning:**
- If electricians are asking for "EV charger installation" skills → pitch AI for complex quoting
- If salaries are rising fast → pitch "do more with existing staff"

**For market sizing:**
- 175K job adverts × average salary = market value of electrical labour demand
- Regional breakdown → where to focus first

---

## 3. Training Pipeline Data

### What we have

| Dataset | Records | What it measures |
|---------|---------|------------------|
| `apar` | 1,424 | Apprenticeship providers (who trains) |
| `ofqual` | 10,000+ | Regulated qualifications (what they teach) |
| `dfe_apprenticeships` | BLOCKED | Apprenticeship starts/completions |

### How this helps AI Onboard

- **Training providers** → potential partners (they train electricians, we onboard their graduates)
- **Qualifications** → what skills electricians are expected to have
- **Apprenticeship data** → pipeline of new electricians entering the market

---

## 4. Procurement & Planning Signals

### What we have

| Dataset | Records | What it measures |
|---------|---------|------------------|
| `contracts_finder` | 5,000 | Public procurement contracts (OCDS) |
| `find_tender` | 50 | Higher-value procurement |
| `planning_apps` | 5,000 | Planning applications |

### How this helps AI Onboard

**For prospect identification:**
- Government procurement for electrical services → which businesses are winning contracts
- Planning applications → new construction = new electrical work = new customers for AI Onboard

**For sales intelligence:**
- "I see you won a contract with [council] — congratulations. How are you managing the admin for that?"
- "There's a lot of new building in your area — are you set up to handle the extra enquiries?"

---

## 5. Certification & Capacity Data

### What we have

| Dataset | Records | What it measures |
|---------|---------|------------------|
| `refcom` | 11,295 | F-gas certified companies |
| `evspark_trades` | 55,925 | Electrical businesses by postcode |

### How this helps AI Onboard

- **REFCOM** → HVAC businesses (plumbing/heating firms in the vision)
- **EvSpark** → historical electrical business data (deprecated but useful for calibration)

---

## 6. BigQuery Integration

### Available credentials

```
GOOGLE_CLOUD_PROJECT: project-ff2366d2-8fda-4fcb-9ba
```

### What we can do with BigQuery

| Capability | How it helps AI Onboard |
|------------|------------------------|
| Store prospect database | Queryable, shareable, API-accessible |
| Join with external datasets | Census, ONS, Companies House bulk data |
| Build dashboards | Looker Studio, Data Studio |
| API access | Serve prospect data to aionboard.co.uk |
| Historical tracking | Track how business population changes |

### Proposed BigQuery schema for AI Onboard

```sql
-- Prospect table
CREATE TABLE aionboard.prospects (
  company_number STRING,
  name STRING,
  status STRING,
  sic_codes ARRAY<STRING>,
  postcode STRING,
  region STRING,
  incorporation_date DATE,
  cluster STRING,
  score FLOAT64,
  last_contacted DATE,
  contact_status STRING,
  notes STRING
);

-- Contact attempts
CREATE TABLE aionboard.contacts (
  contact_id STRING,
  company_number STRING,
  contact_date TIMESTAMP,
  channel STRING,  -- phone, email, linkedin
  outcome STRING,  -- interested, not interested, no answer, callback
  notes STRING
);

-- Installations
CREATE TABLE aionboard.installations (
  installation_id STRING,
  company_number STRING,
  package STRING,  -- foundation, standard, premium
  price FLOAT64,
  install_date DATE,
  delivery_hours FLOAT64,
  support_requests INT64,
  satisfied BOOLEAN,
  referral BOOLEAN
);
```

---

## 7. What to Implement First

### Priority 1: Prospect export from powuk

```python
# Export electrical businesses as CSV for AI Onboard
def export_prospects():
    """
    Export electrical businesses with:
    - company_number
    - name  
    - postcode
    - region
    - sic_codes
    - status
    """
    # Read from data/normalized/ch_capacity/
    # Filter for cluster=electrical
    # Export to CSV
    # Import to BigQuery
```

### Priority 2: Regional scoring

```python
# Score regions by electrical business density
def score_regions():
    """
    For each postcode area:
    - Count of electrical businesses
    - Average business age
    - Planning application activity
    - Procurement contract activity
    
    Output: ranked list of regions for AI Onboard campaigns
    """
```

### Priority 3: Prospect enrichment

```python
# Enrich prospects with additional data
def enrich_prospect(company_number):
    """
    For each prospect, add:
    - Google Business Profile (if exists)
    - Website (if exists)
    - Phone number (from Companies House or web)
    - Services offered (from website or trade directories)
    - Growth signals (hiring, expanding, new certifications)
    """
```

### Priority 4: BigQuery pipeline

```python
# Sync powuk data to BigQuery
def sync_to_bigquery():
    """
    Daily sync:
    1. Export new/updated prospects from powuk
    2. Load to BigQuery
    3. Update scores
    4. Refresh dashboard
    """
```

---

## 8. Data Quality Notes

### What's good
- **Electrical businesses**: 10,000+ records, verified via Companies House API
- **Labour data**: 175K+ job adverts, 50K+ salary records
- **Procurement**: 5,000+ contracts with OCDS structure

### What needs work
- **Business phone numbers**: Not in Companies House data — need to enrich from Google/web
- **Business websites**: Not in Companies House data — need to enrich
- **Team size**: Not available — need to estimate from other signals
- **Existing software**: Not available — need to discover during sales calls

### What's blocked
- **nomis_supply**: Labour supply data (employment by SOC) — needs API key
- **dfe_apprenticeships**: Training pipeline — needs URL fix
- **mcs_installers**: MCS certified installers — needs data request
- **ozev_installers**: OZEV authorized installers — needs scraping

---

## 9. Integration Architecture

```
POWUK (data collection)
  │
  ├── Companies House → electrical businesses (10K+)
  ├── ONS → labour demand, salaries, skills
  ├── Training → providers, qualifications
  ├── Procurement → contracts, planning apps
  └── Certification → REFCOM, EvSpark
          │
          ▼
    BigQuery (storage + API)
          │
          ├── Prospect database
          ├── Contact tracking
          └── Installation records
          │
          ▼
    aionboard.co.uk (frontend)
          │
          ├── Prospect search
          ├── Campaign management
          └── Installation tracking
```

---

## 10. Revenue Opportunity

### Market sizing from powuk data

| Metric | Value | Source |
|--------|-------|--------|
| Electrical businesses (UK) | 10,000+ | Companies House (SIC 43210) |
| Construction SMEs (UK) | 885,000 | Vision doc |
| Sole traders using AI | 40% | Business Data Survey |
| Sole traders with integration | 18% | Business Data Survey |
| Average AI Onboard package | £499 | Vision doc |

### Planning scenarios, not targets

These calculations test arithmetic, not demand:

```
100 hypothetical installations × £499 = £49,900
```

Do not use them as revenue forecasts, conversion-rate evidence, or sales claims.

---

## 11. Next Steps

### Immediate (this week)
1. Export electrical businesses from powuk to CSV
2. Create BigQuery dataset and load prospect data
3. Build basic prospect scoring (region + business age)

### Short-term (this month)
1. Enrich prospects with Google Business Profile data
2. Build regional campaign reports
3. Create prospect search API

### Medium-term (this quarter)
1. Integrate with aionboard.co.uk
2. Track contact attempts and conversions
3. Build installation tracking system

---

*This report was generated from POWUK data collected through 2026-09-23. All data is subject to source licensing (mostly OGL).*
