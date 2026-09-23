# SOFTWARE_INTEL.md

> BigQuery + cgraphuk intelligence for the nine target niches: current pains, current software, and AI-native onboarding difficulty.

All BigQuery pain rows below exclude test records. Statistics marked `template-analysis` or `PROPOSED` are research hypotheses, not measured customer outcomes. Statistics marked `verified-2026` still need customer-level validation before use in sales material.

## Capability baseline

From `drop.capabilities`, ordered by implementation effort:

| Capability | Autonomy | Effort | Industries |
|---|---:|---:|---|
| Lapse Detector | 5 | 5d | barber, beauty, cleaning, petcare, tutor |
| Round Ledger | 5 | 5d | window_cleaner, cleaning |
| Tax Sweeper | 5 | 5d | gig_driver, bookkeeping |
| Review Engine | 4 | 5d | restaurant, hotel, beauty, barber |
| No-Show Protector | 5 | 7d | barber, beauty, restaurant, hotel |
| Quote Follower | 4 | 7d | electrician, builder, hvac, garage |
| Channel P&L | 5 | 10d | restaurant, hotel |
| Compliance Dashboard | 4 | 10d | electrician, hvac, builder, care, vet |
| Direct Migration | 4 | 10d | petcare, restaurant, hotel, barber |
| Voice Agent | 5 | 14d | electrician, builder, hvac, garage |

Readiness observations in `drop.graph_observations` are template-derived, not customer-measured. Treat `readiness.*` as onboarding hypotheses.

## Muse / ChatGPT / connector posture

- Meta Muse is US-only with no confirmed UK date. Do not sell native Muse voice, Muse access, or a Muse connector as included.
- OpenMuse is a separate open-source project. It does not grant Meta access.
- ChatGPT has no guaranteed business listing or placement. Optimize accuracy, accessibility, structured data, reviews, directories, and Bing indexing instead.
- Keep the customer’s existing phone number unless they explicitly request a change.
- Production WhatsApp, Meta, voice, payment, calendar, and booking integrations require customer-owned accounts, explicit authorization, verification, and supplier-paid costs.
- Owner approval remains required before quotes, bookings, deposits, payments, contracts, and outbound customer messages.

---

## 1. Nails — `verticals/nails/`

Parent research: beauty.

### Pains

| Pain | Evidence | Verification | Autonomy | Agent action pattern |
|---|---|---|---:|---|
| PP-002: calls go to voicemail during treatments; major beauty platforms lack AI reception | 0/5 platforms offer voice/SMS/WhatsApp AI reception | VERIFIED | 5 | Answer, book, confirm by SMS |
| PP-008: empty room and staffed hours, no revenue | 8% bookings lost; deposits cut no-shows 57% | VERIFIED | 5 | Send deposit request |
| PP-038: prepaid packages expire unworked; new money walks away | No stat; prepaid leakage | PROPOSED | 4 | Send package-expiry reminders |
| PP-037: lapsed regulars never win-backed | No stat; cheapest revenue hypothesis | PROPOSED | 5 | Send rebooking SMS |
| PP-060: reviews never answered or leveraged | No stat | PROPOSED | 4 | Respond and request reviews |
| PP-014: Booksy Boost and Fresha new-client cuts | Booksy 30% Boost; Fresha 20% new-client cut | VERIFIED | 4 | Track channel mix and migrate repeats |
| PP-015: salon SaaS add-on creep | Vagaro base to add-on stack | VERIFIED | 3 | Compare net software cost |

### Current stack to integrate, not replace

Booksy, Fresha, Square Appointments, GlossGenius, Vagaro, Mangomint, Mindbody, Pabau for clinical-adjacent work, Phorest, customer exports, Stripe/Square payments.

### AI-native onboarding difficulty: Easy

Why: message-first enquiries, repeatable services, deposits, reminders, reviews, and portfolio proof. Keep the existing booking platform. Add booking-link hygiene, quick replies, deposit rules, reminder workflow, rebooking workflow, and review workflow.

---

## 2. Lashes and brows — `verticals/lashes/`

Parent research: beauty.

### Pains

Same beauty pain set as nails, plus stronger safety weight:

| Pain | Evidence | Verification | Autonomy |
|---|---|---|---:|
| PP-002: missed inbound during treatments | Category-wide AI-reception gap | VERIFIED | 5 |
| PP-008: no-shows on staffed rooms | 8% bookings lost; deposits cut no-shows 57% | VERIFIED | 5 |
| PP-038: package and course leakage | Prepaid expiry hypothesis | PROPOSED | 4 |
| PP-037: lapsed clients never win-backed | Repeat-demand hypothesis | PROPOSED | 5 |
| PP-060: reviews never answered or leveraged | No stat | PROPOSED | 4 |
| PP-014/PP-015: marketplace and SaaS tax | Booksy/Fresha/Vagaro pricing research | VERIFIED | 4/3 |

Safety addition: patch-test and allergy records must precede relevant treatments. This is a compliance and liability workflow, not an autonomous decision.

### Current stack

Same beauty stack as nails. Phorest, Vagaro, Fresha, Booksy, Square Appointments, GlossGenius, Mangomint, customer exports.

### AI-native onboarding difficulty: Easy

Why: same booking/deposit/reminder mechanics as nails, with one extra mandatory safety workflow. Do not automate allergy judgments.

---

## 3. Mobile hairdressers and braiders — `verticals/hair/`

Parent research: beauty, with service-area adaptation.

### Pains

| Pain | Evidence | Verification | Autonomy |
|---|---|---|---:|
| PP-002: missed inbound during appointments | Category-wide AI-reception gap | VERIFIED | 5 |
| PP-008: no-shows on staffed time | 8% bookings lost; deposits cut no-shows 57% | VERIFIED | 5 |
| PP-038: package and repeat leakage | Prepaid expiry hypothesis | PROPOSED | 4 |
| PP-037: lapsed clients never win-backed | Repeat-demand hypothesis | PROPOSED | 5 |
| PP-060: reviews never answered or leveraged | No stat | PROPOSED | 4 |
| PP-014/PP-015: marketplace and SaaS tax | Booksy/Fresha/Vagaro pricing research | VERIFIED | 4/3 |

Mobile-specific gaps: service-area ambiguity, travel cost handling, portfolio organization, and colour patch-test rules.

### Current stack

Booksy, Fresha, Square Appointments, Google Calendar, Stripe/Square payments, Instagram/Facebook portfolios, customer exports.

### AI-native onboarding difficulty: Easy

Why: portable booking, service-area profile, social portfolio, reminders, deposits, rebooking, and reviews. Travel pricing must remain explicit and owner-approved.

---

## 4. Dog groomers — `verticals/dog-groomers/`

Parent research: petcare.

### Pains

| Pain | Evidence | Verification | Autonomy |
|---|---|---|---:|
| PP-013: Rover ~20%, Wag ~40% marketplace tax | Steepest marketplace tax in the template set | VERIFIED | 5 |
| PP-067: 40% Wag bleed with flat-subscription alternative | Rover/Wag fee research | VERIFIED | 5 |
| PP-043: lapsed owners never re-engaged | Dogs need recurring walks/grooms; scheduling-failure hypothesis | PROPOSED | 5 |
| PP-065: single visits where grouping would work; route sprawl | No stat | PROPOSED | 3 |
| PP-079: proof-of-service records never reviewed | Trust-product hypothesis | PROPOSED | 5 |

### Current stack to integrate, not replace

Time To Pet, Dog Walker Central, TendPets, Rover, Wag, PetBacker/BorrowMyDoggy, DBS/Cliverton/NarpsUK trust records, Google Calendar, customer-owned payments.

### AI-native onboarding difficulty: Easy–Medium

Why Easy: recurring appointments, reminders, waiting lists, reviews, and direct-repeat migration are highly automatable.

Why Medium: pet medical/behavior records, temperament grouping, incident protocols, and insurance/accountability boundaries need human control. Do not automate safety judgments.

---

## 5. Domestic cleaners — `verticals/cleaners/`

Parent research: cleaning.

### Pains

| Pain | Evidence | Verification | Autonomy |
|---|---|---|---:|
| PP-039: paused/cancelled plans never win-backed | 5–10 recoverable clients/month hypothesis | PROPOSED | 5 |
| PP-025: travel, parking, materials, deep-clean extras unbilled | Fixed-price margin hypothesis | PROPOSED | 3 |
| PP-073: missed direct debits never chased | No stat | PROPOSED | 5 |
| PP-078: before/after photos never posted | Marketing hypothesis | PROPOSED | 5 |
| PP-064: fortnightly/3-week/4-week cadence poorly supported | Cadence-gap research | VERIFIED | 4 |
| PP-061: first cleans priced as standard cleans | 2–3x work hypothesis | PROPOSED | 3 |
| PP-017/PP-047: per-user SaaS scaling versus flat UK pricing | Jobber versus ProCleanerUK pricing research | VERIFIED | 3 |

### Current stack to integrate, not replace

ZenMaid, BookingKoala, Launch27, ConvertLabs, Cleenie, ProCleanerUK, Swept, Jobber, Google Calendar, GoCardless/Stripe payments, customer exports.

### AI-native onboarding difficulty: Easy

Why: recurring plans, reminders, payment chasing, win-back, photo proof, and reviews are highly automatable. Keep owner approval for pricing changes, refunds, credits, and payment actions.

---

## 6. Gardeners and window cleaners — `verticals/gardeners-window-cleaners/`

Parent research: window_cleaner, with an explicit gardener gap.

### Pains

| Pain | Evidence | Verification | Autonomy |
|---|---|---|---:|
| PP-024: unbilled cleans, verbal credits, unchased missed debits | Round-economics hypothesis | PROPOSED | 5 |
| PP-066: paper round book is a single point of failure | Density-pattern hypothesis | PROPOSED | 4 |
| PP-073: missed direct debits never chased | No stat | PROPOSED | 5 |
| PP-061: first cleans priced as standard cleans | 2–3x work hypothesis | PROPOSED | 3 |

Gardener-specific seasonal work, access, waste removal, equipment, and weather disruption still need dedicated discovery. Do not present window-cleaner evidence as gardener evidence.

### Current stack

Cleaner Planner, Work Planner, Manage My Round, Squeegee/George/Aworka, GoCardless, Google Calendar, customer exports. Gardener tooling must be discovered per customer.

### AI-native onboarding difficulty: Easy for window rounds; Medium for gardeners

Why: round ledgers, skip/credit/debt tracking, reminders, and reviews are highly automatable. Gardening adds weather, access, waste, equipment, and seasonal variability.

---

## 7. Mobile car detailers — `verticals/car-detailers/`

Status: research stub. No dedicated upstream teardown, campaign, voice profile, or BigQuery vertical was found.

### Discovery hypotheses

- Photo-led quote requests need complete vehicle, location, condition, and timing details.
- Approval boundaries matter more than automation speed.
- Travel and weather compete with scheduling.
- Repeat services need explicit offers.
- Portfolio and reviews matter, but do not invent results.

### Current stack

Discover per customer. Likely: phone/SMS/WhatsApp, Instagram/TikTok DMs, Google Calendar, Stripe/Square payments, Google Business Profile, customer exports.

### AI-native onboarding difficulty: Medium

Why: photo intake and scheduling are automatable, but condition assessment, pricing variation, travel, weather, and approval boundaries need human control. Do not automate condition judgments or final prices.

---

## 8. Driving instructors — `verticals/driving-instructors/`

Status: research stub. No dedicated upstream teardown, campaign, voice profile, or BigQuery vertical was found. Do not reuse tutor research as proof.

### Discovery hypotheses

- Enquiries arrive across phone, SMS, social, directories, and referrals.
- Lesson scheduling competes with cancellations and waiting-list demand.
- Progress records live in notebooks, messages, or memory.
- Reviews and referrals are inconsistently collected.
- Regulatory, insurance, vehicle, and safeguarding obligations vary by instructor.

### Current stack

Discover per instructor. Likely: phone/SMS/WhatsApp, Google Calendar, instructor directories, Google Business Profile, customer-owned payments.

### AI-native onboarding difficulty: Medium

Why: scheduling, waiting lists, reminders, and progress administration are automatable. Regulatory, insurance, safeguarding, and test-readiness judgments are not.

---

## 9. Wedding photographers and makeup artists — `verticals/weddings/`

Status: partial. Makeup work can use beauty research. Wedding-photography assets are missing.

### Pains

Makeup-specific pains use the beauty set above: missed inbound, no-shows, package leakage, lapsed clients, reviews, marketplace/SaaS tax.

Photography-specific items are discovery hypotheses:

- Incomplete dates, venues, party sizes, packages, and budgets.
- Availability changes faster than manual calendars and marketplace profiles.
- Proposals, deposits, contracts, and payment schedules need careful approval.
- Portfolio proof is scattered.
- Reviews are influential but inconsistently collected.

### Current stack

Makeup: Booksy, Fresha, Square Appointments, GlossGenius, Vagaro, Mangomint, Phorest, customer exports. Photography tooling must be discovered per supplier.

### AI-native onboarding difficulty: Medium

Why: enquiry qualification, availability, proposals, deposits, contracts, preparation, and reviews are automatable. Creative judgment, event-day decisions, and contract terms need human control.

---

## Cross-niche onboarding order

1. Nails, lashes, and mobile hair first: message-first intake, deposits, reminders, rebooking, reviews, and portfolio proof.
2. Cleaners and dog groomers next: recurring schedules, waiting lists, payment chasing, win-back, and direct-repeat migration.
3. Gardeners/window cleaners next: round ledgers, skip/credit/debt discipline, reminders, and reviews.
4. Car detailers, driving instructors, and wedding photography only after dedicated discovery validates unit economics, delivery time, support load, and repeatability.
