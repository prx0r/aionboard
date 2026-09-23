# Car detailer intake form

> The entry point. If we can't define intake as a form, the unit isn't clear enough.

## The form (5 fields)

```
1. Business name + postcode
2. Phone number + email
3. Services offered (checkboxes)
4. Current booking method
5. Upload your price book (photo or PDF)
```

### Field 1: Business name + postcode

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| Business name | text | yes | As the customer wants it displayed |
| Postcode | text | yes | Used for service-area matching and geographic intel |

### Field 2: Phone number + email

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| Phone | phone | yes | Primary contact; must be TPS-screened before any outbound call |
| Email | email | yes | For handover, support, and booking confirmations |

### Field 3: Services offered

Checkboxes. Customer ticks what they do:

- [ ] Exterior wash and wax
- [ ] Maintenance wash (regular upkeep)
- [ ] Interior valet
- [ ] Full detail (interior + exterior)
- [ ] Machine polishing / paint correction
- [ ] Ceramic coating
- [ ] Paint protection film (PPF)
- [ ] Headlight restoration
- [ ] Engine bay cleaning
- [ ] Leather cleaning and conditioning
- [ ] Odour removal
- [ ] Pet hair removal
- [ ] Fleet / commercial vehicles
- [ ] Other (text field)

**Why this matters:** The AI only references services the customer actually offers. Never promise a service that isn't in this list. The rulebook (RULEBOOK.md #28) says: "AI promises results that require specialist equipment" — this field prevents it.

### Field 4: Current booking method

Dropdown or radio:

- Fresha
- Calendly
- Square Appointments
- Google Calendar
- WhatsApp only
- Phone calls only
- Instagram DMs only
- Mix of the above (text field: "which ones?")
- Nothing — I manage manually

**Why this matters:** This determines the onboarding recipe. Square user gets deposit and payment-link setup. WhatsApp-only user gets quick-reply and photo-request setup. The onboarding engine (onboarding.py) uses this to select tasks.

### Field 5: Upload your price book

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| Price book | file (image or PDF) | yes | Photo of printed price list, screenshot of digital prices, or PDF |

**Why this matters:** The AI quotes from the customer's own prices. Never invent prices. The rulebook (RULEBOOK.md #20) says: "Price book doesn't differentiate by vehicle size" — this field plus structured price tiers prevents it.

If the customer doesn't have a price book, stop. Help them create one first. The onboarding cannot proceed without approved prices.

---

## What happens after intake

1. **Import to CRM** (`crm.py`): business name, postcode, phone, email, services, booking tool. Provenance: intake-form.
2. **Select recipe** (`onboarding.py`): booking tool → which tasks apply.
3. **Generate quote draft** from uploaded price book, structured by vehicle size. Owner approves before any send.
4. **Schedule onboarding session** (1 hour, live training + setup).

## Intake rules

- No passwords collected at intake. Ever.
- No payment taken at intake. Payment is after onboarding session.
- Customer can withdraw at any point. Data deleted per DATA_POLICY.md.
- All data is customer-owned. We are processor, not controller, for their client data.

### Optional: Add-ons interested in

- [ ] Website + AI Chatbot (£199)
- [ ] Google Business Profile Optimisation (£99)
- [ ] AI Visibility Package (£149)
- [ ] Social Media Bio Optimisation (£49)
- [ ] Full Digital Footprint Audit (£79)
- [ ] Not sure — include in consultation
