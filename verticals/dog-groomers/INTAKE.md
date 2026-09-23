# Dog groomer intake form

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

- [ ] Full groom (bath, cut, blow-dry)
- [ ] Puppy's first groom
- [ ] Bath and brush only
- [ ] Nail trimming
- [ ] Teeth cleaning
- [ ] De-shedding treatment
- [ ] Hand-stripping
- [ ] Flea treatment bath
- [ ] Sanitary trim
- [ ] Ear cleaning
- [ ] Cat grooming
- [ ] Mobile grooming (van-based)
- [ ] Other (text field)

**Why this matters:** The AI only references services the groomer actually offers. Never promise a service that isn't in this list. The rulebook (RULEBOOK.md #34) says: "AI promises a service the groomer doesn't offer" — this field prevents it.

### Field 4: Current booking method

Dropdown or radio:

- Time To Pet
- TendPets
- PetBooker
- GroomGo
- Booksy
- Rover
- Wag
- Google Calendar
- WhatsApp only
- Phone calls only
- Mix of the above (text field: "which ones?")
- Nothing — I manage manually

**Why this matters:** This determines the onboarding recipe. Time To Pet user gets pet-record + waiting-list setup. Rover user gets direct-migration workflow. WhatsApp-only user gets quick-reply + booking-link setup.

### Field 5: Upload your price book

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| Price book | file (image or PDF) | yes | Photo of printed price list, screenshot of digital prices, or PDF |

**Why this matters:** The AI quotes from the groomer's own prices. Never invent prices. The rulebook (RULEBOOK.md #27) says: "Price varies by dog size but booking tool doesn't capture size" — this field plus size-based pricing prevents it.

If the customer doesn't have a price book, stop. Help them create one first. The onboarding cannot proceed without approved prices.

---

## What happens after intake

1. **Import to CRM** (`crm.py`): business name, postcode, phone, email, services, booking tool. Provenance: intake-form.
2. **Select recipe** (`onboarding.py`): booking tool → which tasks apply.
3. **Generate quote draft** from uploaded price book. Owner approves before any send.
4. **Schedule onboarding session** (1 hour, live training + setup).

## Intake rules

- No passwords collected at intake. Ever.
- No payment taken at intake. Payment is after onboarding session.
- Customer can withdraw at any point. Data deleted per DATA_POLICY.md.
- All data is customer-owned. We are processor, not controller, for their client data.
- Pet medical and behaviour data is collected during onboarding, not intake — it requires owner consent and detail.
