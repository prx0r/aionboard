# ELECTRICIAN_INTEL.md

> Everything useful from `/root/ab` (EvSpark business), `/root/cmail` (domain/email infra), and related intelligence — adapted for AI Onboard's narrow pilot. Sources attributed; hypotheses marked.

## Source map

| Finding | Source file |
|---------|-------------|
| Sparky price book (£350 EV labour, £90 fault) | `ab/businesses/evspark/KERNEL.md` |
| EV unit economics (£892 install, £250/£180 CM, 8 jobs/mo break-even) | `ab/businesses/evspark/PLAN.md` |
| 4-segment targeting + 14-day outreach + partner terms | `ab/businesses/evspark/SPARKIES.md` |
| Labour shortage (136k, down 19.6%, <1 in 5 reach employment) | `ab/intelligence/SUPPLY.md` |
| Cluster math (~300k households → ~1.5k charger jobs/yr ≈ £1.3M) | `ab/SPARKAGENT_THESIS.md` |
| Domain + email in 8 steps (~$10/yr + $0–5/mo) | `cmail/RECIPE.md` |
| No-guarantee policy language | `ab/businesses/evspark/KERNEL.md` (`policy.ozev`) |

## Price book (sparky v2, for quote drafting)

Use as the starting template for customer price books. Every figure must be confirmed or replaced by the owner's actual rates — never quote these blind.

| Job | Labour | Typical parts |
|-----|--------|---------------|
| EV charger install | £350 | 7kW smart unit (OZEV list), 32A RCBO, SWA cable/m, mounting kit, EIC + DNO notify |
| Fault triage/diagnosis | £90 | Diagnostic visit, PCB mail-in option |
| Consumer unit replacement | £450 (v1 book) | 10-way dual-RCD board, RCBOs, labels/cert |

After-hours multiplier 1.5×. Callout covers diagnosis. Unknown job types quote a site visit, never an invented price.

## OZEV grant window (time-sensitive wedge)

- £500/socket to **31 Mar 2027**, 5 schemes, authorised-installer + approved-hardware required.
- **Eligibility is decided by OZEV, never by us.** Pre-check and submit; never guarantee approval. (Verbatim-safe policy from KERNEL.md.)
- Grant-shaped search ("OZEV installer near me") is the highest-intent demand in the vertical right now.
- Post-cliff (from Apr 2027): landlord retainers, EICR bundles, tariff-switch offers, solar/battery cross-sell.

## Four prospect segments (adapted from SPARKIES.md)

| Segment | Find them | Our pitch |
|---------|-----------|-----------|
| **Busy local spark** (2–5 staff, diary full) | NICEIC/NAPIT directory, Checkatrade, 4.5★+ Places | Overflow cover + zero admin; "you never touch paperwork" |
| **Newly qualified / 1-man band** (<3 yrs) | Training graduates, new MyBuilder profiles, Instagram starters | Leads + backend + reputation from zero |
| **EICR/landlord spark** (testing + remedial) | Letting agents, EICR-heavy profiles | EV bolt-on on visits already happening |
| **Career changer** (supervised) | Bootcamps, adult-diploma centres | Ladder + supervised hours + jobs (long-term pipeline) |

Start with exactly ONE busy-local (competence proven) plus a new-spark backup. Quality over quantity until first jobs land.

## Outreach sequence that works (adapted, lead-first)

No cold SaaS pitch exists in this plan. Every touch carries proof or books proof:

1. **Email all 50:** subject carries cluster + goods ("3 EV jobs in {town} this month — want the first free?"). Attach a sample scope pack. One ask: 10-min call. B2B to published addresses, opt-out honored, TPS-screen sole-trader mobiles before any cold call.
2. **Calls (engaged + Ltd):** 10-min script — capacity, day-rate, EV experience, Part P, area. Qualify for fit. Goal: 5 deep conversations.
3. **Warm-transfer the first TWO leads free** with full scope pack. Free means free — no contract, one line: "more where that came from."
4. **Close partner terms with ONE.** Then stop recruiting and deliver.

Funnel math (plan, not evidence): 50 → 15 replies → 5 calls → 2 trials → 1 partner. If replies <10: list or subject is wrong — fix once, then re-evaluate.

## Demand stack (in order)

1. Grant-shaped search (OZEV installer queries)
2. Marketplaces (Checkatrade/MyBuilder — rented demand, deliberate bridge)
3. Landlord/HMO direct (letters + EICR bundle — highest £/effort)
4. Organic (compatibility content: "which charger for [flat / no-driveway / 3-phase / solar]")
5. Referral + review flywheel (every job → photos → review → case page)

## Labour market context (for sales conversations, not guarantees)

- 136k qualified electricians, workforce down 19.6% since 2018; ~12k new qualifiers/yr needed.
- <1 in 5 classroom learners ever reach apprenticeship or skilled employment — training exists, jobs exist, the bridge is broken.
- Heat pumps: 9k MCS installers vs 150k needed.
- Use sparingly: supports "use existing staff more effectively" messaging. Does not prove AI Onboard delivers it.

## Onboarding infrastructure (from cmail)

- Domain + routed email: ~$10/yr domain, $0/mo inbound, ~$5/mo with outbound. 8-step recipe in `cmail/RECIPE.md` (search → buy → wire → verify → read → draft).
- Every money step needs explicit human confirm; receipts filed per run (ab standing rule: propose exact commands, wait for confirm).
- Relevance to AI Onboard: our install provisions identity the same way — domain, email, phone — then configures workflows on top. We do not rebuild what cmail already does.

## Kill conditions (adopted for our pilot)

- No qualified spark available <£250/day sustained in area → delivery breaks, hold.
- Net hardware + sundries push non-grant CM <£120/job → economics break, hold.
- CAC >£120/job for 4 consecutive weeks post-optimisation → channel break, reposition.
- Any safety incident → immediate hold, review before resume.
