# STRATEGY.md

> Honest assessment of where AI Onboard stands, what could break it, and where the money actually is.

## What's strong

1. **The data is real.** 10,000 electrical businesses with postcodes is a genuine asset. Most consultancies start with nothing.
2. **The narrow offer is right.** £499 pilot, manual-first, owner approval on everything. That survives contact with reality.
3. **The code now exists.** CRM, install state machine, demo, handover, tests — the repo went from docs-only to a verifiable core.
4. **The vertical structure is clean.** 11 packs, same schema, no invented outcomes. Easy to extend.

## What's fragile

1. **No revenue yet.** Everything is hypothesis. The most important number is still zero: paying customers.
2. **Pricing is incoherent across drafts.** `OFFER.md` is canonical (£499 pilot + £20 quickstart). Older research files float other numbers — treat those as hypotheses, never checkout prices.
3. **Scope keeps expanding.** Every session adds docs. No more architecture documents until there's a paying customer.
4. **The Muse bet is unhedged.** US-only, no UK date. The assistant-agnostic fallback must be the primary pitch now, not later.
5. **Influence is a liability until audited.** Known approval-path issues; do not put customers on it yet.
6. **Support scope will leak.** "Unlimited automated help" needs documented abuse limits before the first install, not after the first burnout.
7. **Legal advice via AI is a liability surface.** Tax thresholds, CIS rules, patch-test guidance — wrong statements acted on create exposure. Disclaimers belong in the product, and prompts must defer to accountants and established procedures.

## Security: documented vs deployed

| Layer | Control | Status |
|-------|---------|--------|
| Identity | Customer-owned accounts, OAuth only, no passwords | Documented + coded |
| Authorization | Scoped tokens, per-action approval, payload hashing | Coded, not deployed |
| Isolation | Tenant-scoped queries, disjoint refs/storage | Coded, not enforced at DB layer |
| Audit | Every tool call logged with identity + approval | Coded, no production pipeline |
| Secrets | Scan + reject in prompts, handovers, logs | Coded and tested |
| Backups | Encrypted, integrity-checked, restore-tested | Coded and tested |
| Network | Remote MCP over HTTPS, no localhost exposure | Designed, not built |
| Abuse | Rate limits, support-minute tracking, escalation | Partially coded |

A documented control that isn't running is a plan, not a control. The next security milestone is deploying the gateway with these switched on, then testing it.

## How Muse/ChatGPT actually manage each vertical

They don't manage. They assist under supervision:

| Vertical | AI does | Human always does |
|----------|---------|-------------------|
| Nails/lashes/hair | Draft replies, reminders, rebooking lists | Approve sends, set prices, patch-test decisions |
| Electrician | Draft quotes from price book, summarize enquiries | Approve quotes, safety judgments, dispatch |
| Cleaners | Schedule proposals, payment reminders, win-back lists | Approve sends, credits/refunds, hiring |
| Dog groomers | Waiting-list fill proposals, review requests | Temperament/safety calls, pricing |
| Gardeners/window | Route organization, skip/credit tracking | Safety-at-height calls, debt enforcement |
| Drivers/detailers/weddings | Enquiry triage, scheduling proposals | Pricing, contracts, creative judgment |

Platform reality:
- **ChatGPT today:** Developer Mode + remote MCP + per-action confirmation. Buildable now, gated by paid plan.
- **Muse today:** US-only. Prepare the connector submission; sell the manual workflow meanwhile.
- **Neither is the sole dependency.** The install must work with plain WhatsApp + Google Calendar + a price book.

## Onboard vs support: the actual economics

**£20 Quickstart per customer:**
```
Revenue:                        £20.00
Acquisition (enrich+call):      -£8-15  (unknown, estimated)
Delivery human time (30 min):   -£15.00 (@£30/hr)
Support human time (15 min):    -£7.50
Third-party costs:              -£0-2
                                ────────
Margin:                         -£10 to -£2.50  (LOSS)
```

**£499 Standard per customer:**
```
Revenue:                        £499.00
Acquisition:                    -£50-100
Delivery (5 hrs):               -£150-250
Support (1 hr):                 -£30-50
                                ────────
Margin:                         +£100 to +£270
```

**Conclusion:** the £20 product loses money standalone at any realistic human-time level. It only works as acquisition spend — justified by referrals at zero CAC or upsell to support/lead-gen/custom work.

Rules that follow:
1. Support minutes per customer is the single most important metric. Median over 20 minutes → kill or reprice.
2. The support window is the product. 7 days of good support converts to trust; trust converts to referrals and upsells.
3. Cap the downside. Abuse limits before the first install, not after the first burnout.
4. £499 funds the business; £20 funds growth. Don't confuse the two.

The flywheel is real but slow: onboard cheap → measure → prove → refer → upsell. Each loop takes 30–60 days. Plan cash accordingly.
