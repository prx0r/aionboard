# Electrician rulebook

> What "correct" means for this vertical and every way the AI gets it wrong. Built from research; must be validated against real jobs and updated after every mistake caught. This is the moat.

## How to use this file

Every time we deliver work for an electrician customer and something goes wrong, add it here with the fix. After 50 jobs this list is worth more than the model. A competitor can copy our tools; they can't copy this.

---

## Missed inbound (PP-001)

| # | What goes wrong | Why it matters | Fix |
|---|----------------|----------------|-----|
| 1 | AI answers with generic greeting when customer has an emergency | Customer with a fuse board fire gets "How can I help you today?" instead of urgency triage | Detect urgency keywords (sparking, burning, no power, trip) and escalate immediately |
| 2 | Missed-call capture asks too many questions | On-site sparky can't listen to a 2-minute voicemail from the AI | Capture: name, number, job type, urgency — under 30 seconds |
| 3 | AI promises same-day attendance when diary is full | Customer expects someone at 4pm, nobody shows | Only promise callback within 1 hour, not attendance |
| 4 | After-hours message doesn't capture enough for a useful callback | Sparky calls back, has to re-ask everything | Capture: name, number, postcode, brief description, urgency |
| 5 | Enquiry labelled "booked" when it's still a quote request | Follow-up never happens, customer goes to competitor | Stages: new → quoted → approved → scheduled → completed |

## Compliance drift (PP-070)

| # | What goes wrong | Why it matters | Fix |
|---|----------------|----------------|-----|
| 6 | AI doesn't flag expired Part P registration | Notifiable work done without valid competent-person registration; customer can't get building control sign-off | Track registration expiry; block notifiable jobs if expired |
| 7 | EICR cycle not tracked per property | Landlord's 5-year EICR lapses, tenant at risk, fine | Track per-property EICR dates; remind at 6 months, 3 months, 1 month before due |
| 8 | AI quotes for notifiable work without checking registration | Sparky isn't registered, can't legally do the work, wastes everyone's time | Verify registration type before quoting notifiable domestic work |
| 9 | CDM duties not passed to contractor on domestic projects | Legal exposure if something goes wrong on site | Flag CDM obligations for jobs over notification thresholds |
| 10 | EV charger install quoted without checking OZEV eligibility | Customer expects £500/socket grant, OZEV rejects, sparky absorbs the blame | Never confirm eligibility ourselves; direct customer to OZEV checker; state grant is subject to OZEV approval |
| 11 | Compliance docs not delivered with certificate | Customer can't find their EICR or minor works cert when selling property | Include compliance doc delivery in job completion workflow |

## Quote follow-up (PP-030)

| # | What goes wrong | Why it matters | Fix |
|---|----------------|----------------|-----|
| 12 | Quote sent, no follow-up scheduled | Customer says "sounds good, let me think about it" and never comes back | Auto-schedule follow-up at 24h, 48h, 7 days — require owner approval on each |
| 13 | Follow-up tone is pushy | Customer feels pressured, goes to a different sparky | Tone: helpful, not salesy. "Just checking if you have any questions about the quote" |
| 14 | Quote expires without warning | Customer comes back 3 months later expecting same price, materials have gone up | State quote validity (30 days typical); remind before expiry |
| 15 | AI sends follow-up before owner has reviewed the quote | Draft quote has wrong price or wrong scope | Every outbound message requires owner approval |
| 16 | Multiple follow-ups to same customer without response | Customer blocks the number | Maximum 3 follow-ups; if no response, mark as cold and stop |

## Scope creep and extras (PP-019)

| # | What goes wrong | Why it matters | Fix |
|---|----------------|----------------|-----|
| 17 | Extras agreed on-site with a nod, never billed | Sparky does 2 extra hours, customer says "I thought that was included" | Record every variation on-site; price from approved rates; get customer sign-off before continuing |
| 18 | AI quotes based on description without seeing the property | Quote is £500, actual job is £900 because the consumer unit is in the loft | Require site visit or photos before firm quote for complex jobs |
| 19 | EV charger quote doesn't include DNO notification | Install can't proceed without distribution network operator approval | Include DNO notification timeline in EV quotes; note it takes 5-10 working days |
| 20 | Labour rate doesn't account for job type or property | Bathroom rewire quoted at same rate as a socket swap | Price book must have tiers: simple, intermediate, complex — linked to property and job type |

## Safety and site judgments

| # | What goes wrong | Why it matters | Fix |
|---|----------------|----------------|-----|
| 21 | AI schedules rewire without considering access | Customer's loft is full of boxes, sparky can't reach consumer unit | Ask about access constraints during intake; flag in job notes |
| 22 | Emergency callout not prioritised correctly | Sparky treats a tripped RCD the same as a sparking socket | Triage: sparking/burning = immediate; no power = same-day; intermittent = next available |
| 23 | No record of test results on completion | Customer disputes work quality, no evidence of compliance | Require test results recorded at job completion (R1+R2, insulation, RCD times) |

## Pricing and payments

| # | What goes wrong | Why it matters | Fix |
|---|----------------|----------------|-----|
| 24 | Price book outdated | AI quotes old material costs, sparky eats the difference | Verify price book monthly; flag when last updated |
| 25 | CIS deduction not accounted for on sub-contractor jobs | Subbie expects full payment, sparky has to deduct 20-30% | Flag CIS obligations; link to HMRC verification status |
| 26 | Travel charge not included for jobs outside usual area | Quoted £300, actual is £350 with travel | Include travel in quote if job is outside defined radius |
| 27 | VAT not stated on quotes for VAT-registered businesses | Customer expects £500 inc VAT, invoice is £600 | Always state whether quote is inc or ex VAT; match to registration status |

## General

| # | What goes wrong | Why it matters | Fix |
|---|----------------|----------------|-----|
| 28 | AI promises work that requires building control notification when sparky isn't registered | Customer is told the job can be done, then learns it can't | Only quote notifiable work if sparky is Part P registered or building control route is agreed |
| 29 | Handover doesn't explain how to update price book | Sparky changes material costs, AI still quotes old ones | Handover includes: "To update prices, edit [file] and tell us" |
| 30 | Support window expires but sparky still needs help | 7-day window too short for compliance-heavy vertical | Track support usage; flag if no contact by day 5 |

---

## Review cadence

- After every job: check if anything went wrong. If yes, add to this list.
- Weekly: review all entries, remove any that are no longer relevant.
- After 50 jobs: this list is the product. Protect it.
