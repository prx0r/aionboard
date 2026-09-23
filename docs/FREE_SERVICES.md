# Free services for sole traders (via MCP)

> Every service below is free, needs no API key, and is wrapped as a
> read-only MCP tool (`mcp/tools.json`, no approval needed). Verified live
> September 2026. If one dies, the module degrades to "unknown", never to
> a guess.

## The stack (total cost: £0)

| Tool | Source | Trade use |
|------|--------|-----------|
| `postcode_lookup` | postcodes.io | Validate customer postcode; outward-code matching for local jobs; coords for routing |
| `bank_holiday_check` | gov.uk bank-holidays.json | Surcharge days, availability, "are we working Monday?" |
| `weather_outlook` | Open-Meteo | Go/no-go outdoor work (gardeners, roofers, window cleaners, landscapers, solar installers) |
| `daylight_hours` | sunrise-sunset.org | How many jobs fit today; stop booking evening work in December |
| `job_clustering` | local math (haversine) | Group jobs into van rounds; rough drive-time estimates |

## Per-trade recipes

- **Gardeners / window cleaners / landscapers / roofers / solar:** weather + daylight every morning. Rain ≥50% → offer the customer a swap day before they cancel on you.
- **Electricians / plumbers / heating:** postcode validation on every enquiry (catches typos that send vans wrong), bank-holiday surcharge logic, job clustering for multi-visit days.
- **Cleaners / dog groomers / beauty:** bank holidays for availability + clustering for round density.
- **All:** outward-code matching joins directly to the powuk opportunity feed (same area logic).

## Rules

1. Free services are shared infrastructure — cache aggressively, timeout fast (15s), never hammer.
2. Estimates are labeled estimates (drive times, rain probability). Confirm with maps/people before promising.
3. If a service is down, say "unknown", never substitute a guess.
4. Anything needing a key (FreeAgent, Companies House, supplier APIs) lives behind OAuth + approval tiers, not here.

## What this is not

- Not navigation (no turn-by-turn; customer uses their maps app).
- Not a weather guarantee (probabilities, not promises).
- Not lead data (that comes from powuk signals with consent rules).
