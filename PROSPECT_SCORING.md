# PROSPECT_SCORING.md

> How to rank and prioritize prospects for AI Onboard.

---

## Scoring factors

### 1. Geographic density (0-25 points)

More businesses in an area = more referral opportunities.

| Businesses in postcode area | Score |
|-----------------------------|-------|
| >200 | 25 |
| 150-200 | 20 |
| 100-150 | 15 |
| 50-100 | 10 |
| <50 | 5 |

### 2. Business age (0-25 points)

Newer businesses need more help.

| Incorporation age | Score |
|-------------------|-------|
| <1 year | 25 |
| 1-3 years | 20 |
| 3-5 years | 15 |
| 5-10 years | 10 |
| >10 years | 5 |

### 3. Service diversity (0-25 points)

More SIC codes = more complex needs.

| SIC codes | Score |
|-----------|-------|
| 4+ | 25 |
| 3 | 20 |
| 2 | 15 |
| 1 | 10 |

### 4. Growth signals (0-25 points)

Observable signs of expansion.

| Signal | Score |
|--------|-------|
| Multiple postcodes | 10 |
| Electrical installation SIC (43210) | 5 |
| Related construction SIC | 5 |
| Independently verified hiring signal | 5 |

SIC 43210 means electrical installation. It does not prove EV-charger capability. Regional labour data does not prove that an individual business is hiring.

---

## Total score interpretation

| Score | Priority | Action |
|-------|----------|--------|
| 80-100 | HOT | Verify contact source and permission, screen TPS/CTPS, then call |
| 60-79 | WARM | Verify contact source and permission this week, then call |
| 40-59 | COOL | Add to research monitoring only |
| <40 | COLD | Monitor, don't call yet |

---

## Greater Manchester prospects

Approximate regional counts from a powuk research snapshot. They are not verified call lists, customer qualifications, or marketing permissions:

| Postcode | Area | Businesses | Score |
|----------|------|------------|-------|
| M | Manchester | ~120 | HOT |
| BL | Bolton | ~45 | WARM |
| OL | Oldham | ~35 | COOL |
| SK | Stockport | ~40 | COOL |
| WA | Warrington | ~30 | COOL |
| WN | Wigan | ~25 | COLD |
| FY | Blackpool | ~20 | COLD |
| PR | Preston | ~35 | COOL |

**Recommendation:** Start with M (Manchester city centre) — highest density, most opportunities.

---

## Qualification criteria

Before calling a prospect, verify:

1. **Trading status** — Active on Companies House
2. **Website** — Does it exist? Is it outdated?
3. **Google Business Profile** — Claimed? Reviews?
4. **Phone number** — Valid? Answered?
5. **Services** — Do they match our target (EV, solar, commercial)?

---

## Prospect data structure

```json
{
  "company_number": "12013809",
  "name": "WN NETWORKS LTD",
  "postcode": "S5 9LG",
  "region": "SN",
  "sic_codes": ["43210"],
  "status": "active",
  "score": 75,
  "priority": "WARM",
  "qualifications": {
    "trading_status": true,
    "has_website": false,
    "has_gbp": true,
    "phone_valid": true,
    "services_match": true
  },
  "notes": "Website status needs independent verification before any sales claim"
}
```
