# STACK_CAPTURE.md

> How we learn what software a business already uses — then onboard without replacing it.

## Principle

**Integrate or import. Never replace unnecessarily.**

The customer already has a phone, a booking system, a website (maybe), and accounting software (maybe). Our job is to make what they have work better, not to sell them a new stack.

## The capture flow

### Step 1: Ask (discovery call)

```
1. "What do you use for bookings?"
2. "What do you use for quotes?"
3. "What do you use for accounting?"
4. "What do you use for email and calendar?"
5. "Where do customers find you? (Google, Instagram, Checkatrade...)"
6. "What frustrates you most about your current setup?"
```

Record answers verbatim. Do not assume.

### Step 2: Classify (per tool)

| Verdict | Meaning | Action |
|---------|---------|--------|
| `integrate` | Keep it, connect to it | Configure OAuth/API/export with customer authorization |
| `import-from` | Pull data out once | Export customers, price book, history; customer keeps the tool |
| `replace` | Only with explicit customer request + written reason | Migrate data, verify, keep old system read-only for 30 days |

Default verdict is `integrate` or `import-from`. `replace` requires written customer approval and a migration plan.

### Step 3: Verify (before handover)

For each tool in the stack inventory:

- [ ] Access confirmed (customer logged in, OAuth granted, or export received)
- [ ] Data flows confirmed (test record visible in both systems)
- [ ] Owner knows how to use it (demonstrated in training)
- [ ] Recorded in handover with owner, status, and access method

An unverified tool is marked `blocked`, never `verified`.

### Step 4: Record (CRM)

Every tool goes into the `stack_items` table:

```json
{
  "company_number": "12013809",
  "tool": "Tradify",
  "category": "job management",
  "verdict": "import-from",
  "access": "customer export received 2026-09-23",
  "owner": "customer",
  "verified": true
}
```

## Per-vertical starting points

| Vertical | Ask about first |
|----------|-----------------|
| Electrician | Tradify, Fergus, Jobber, Powered Now, Xero, WhatsApp |
| Nails/Lashes/Hair | Booksy, Fresha, Square, Instagram, WhatsApp |
| Cleaners | ZenMaid, BookingKoala, Cleenie, ProCleanerUK, GoCardless |
| Dog groomers | Time To Pet, Rover, Wag, TendPets |
| Gardeners/Window | Cleaner Planner, Work Planner, GoCardless |
| Driving instructors | Calendar, WhatsApp, instructor directory |
| Weddings | Instagram, booking platform, contracts tool |

Full per-vertical intelligence lives in `verticals/<slug>/STACK.md` and `profile.json`.

## What we never do

- Never migrate a customer off working software without their written request.
- Never store their passwords. OAuth or customer-performed exports only.
- Never invent a tool they don't have.
- Never mark an integration `verified` from an API acceptance alone.
