# GEO_OPPORTUNITIES.md

> How "your assistant finds opportunities near you" actually works: powuk signals, matched by postcode area, delivered as an approval-gated digest.

## The pitch (honest version)

> "Each week, your assistant checks planning applications, public procurement, and labour demand in your area — and shows you the ones relevant to your trade. You approve before we contact anyone."

What it is: keyword + postcode-area matching over public datasets. What it isn't: confirmed jobs, guaranteed leads, or automatic outreach.

## Signal sources (all from powuk)

| Source | Records | Geographic field | What it tells us |
|--------|---------|------------------|------------------|
| `planning_apps` | ~5,000 | Description text + local-authority entity | Where building work is coming |
| `contracts_finder` | ~5,000 | Buyer locality + postcode (OCDS) | Who is buying trade services |
| `ons_labour` | ~175,000 | Region × SOC | Where hiring demand is hot |
| `ch_capacity` | ~10,000 electrical | Postcode → outward area | Business density per area (184 areas) |
| `refcom` | ~11,000 | Postcode | Certified HVAC capacity per area |
| `gov_grants` | ~50 | Programme scope | Funding that drives demand (e.g. electrification) |

## Per-vertical signal map

| Vertical | Planning keywords | Procurement signals | Labour signals |
|----------|-------------------|---------------------|----------------|
| Electrician | extension, rewire, EV charger, solar/PV, conversion, new build | CPV 453 (installation), facilities contracts | Electrician SOC demand by region |
| Nails/Lashes/Hair | salon, change of use, shopfront, retail | None typical — social discovery instead | Beauty SOC demand by region |
| Cleaners | office, commercial, residential development | Facilities/cleaning contracts | Cleaning SOC demand |
| Dog groomers | pet, veterinary, residential development | None typical — referral-led | Pet-care demand |
| Gardeners/Window | garden, landscape, estate, new build | Grounds-maintenance contracts | Horticulture demand |
| Car detailers | car park, dealership, garage | Fleet contracts (rare) | Motor-trade demand |
| Driving instructors | school, residential development | None typical | Instructor demand |
| Weddings | hotel, venue, barn conversion | Events contracts (rare) | Hospitality demand |

Full keyword lists live in `aionboard/opportunities.py` (`OPPORTUNITY_KEYWORDS`). Matching is conservative by design: a false positive wastes a tradesperson's morning.

## How matching works

```
Business postcode → outward area (e.g. M1)
        ↓
Filter signals to the same area
        ↓
Score by keyword hits per vertical
        ↓
Sort highest first, cap at 5
        ↓
Render digest with score + locality + date
        ↓
Customer replies APPROVE before any contact
```

Implemented and tested in `aionboard/opportunities.py` (`match_for_business`, `digest`). Unmatched records are dropped, never silently included. Records without postcodes skip the region filter rather than failing.

## The Muse angle

When a customer asks their assistant "anything good near me this week?", the flow is:

1. Assistant reads the customer's postcode area and vertical from their profile.
2. Assistant runs `match_for_business` over the latest signals.
3. Assistant presents the digest — scores, localities, dates.
4. Customer taps APPROVE on individual leads or ignores them.
5. Nothing is contacted, quoted, or booked without a separate approval.

This works identically on ChatGPT (Developer Mode + MCP), Muse (connector when eligible), or plain email digest. The digest is the product; the assistant is the interface.

## Limits (stated to customers)

- Signals are public records, not confirmed jobs. A planning approval for an extension does not mean the homeowner wants your quote.
- Keyword matching misses things and occasionally misfires. The score is relevance, not certainty.
- Coverage depends on source freshness. Stale sources produce stale digests — check `data/health/` equivalents before promising coverage.
- Opportunity alerts are a separately-priced, separately-consented service. Buying setup never subscribes anyone.
