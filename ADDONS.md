# ADDONS.md

> What customers can buy after setup — each separately consented, separately priced, and only built after the pilot is validated.

## Rule zero: no overbuild

Nothing in this file is built until its trigger is met:

| Add-on | Build trigger |
|--------|---------------|
| Lead alerts | 1 verified install + measured digest accuracy |
| Ad creation | 1 funnel video driving chat visits |
| Analytics | 10+ creatives worth comparing |
| Custom dashboard backend | 5+ paying customers asking for it |
| Muse connector submission | Remote MCP live + OAuth tested + 1 verified install |

Until then, these are specs, not products.

## Add-on ladder

| Add-on | What it is | Price status |
|--------|------------|--------------|
| Lead alerts | Weekly scored opportunity digest (see `GEO_OPPORTUNITIES.md`) | Future, separate consent |
| Ad creation | TikTok slideshows from vertical pains via the aoc pipeline | Future, per-creative quote |
| Analytics | Views → chats → emails → installs per creative | Future, bundled with ads |
| Custom dashboard | Live per-customer view (mock today at `site/dashboard.html`) | Future, after 5 customers |
| Custom integrations | Bespoke workflows beyond the pilot | Separate quote, always |

## Ad creation via aoc

The aoc repo (`prx0r/aoc`) is the TikTok slideshow factory: hook → PNGs → ZIP → human approve → manual post, with creative memory tracking audience × hook × angle → leads.

Vertical-to-segment mapping (same skeletons, shared language):

| aionboard vertical | aoc segment |
|---|---|
| nails, lashes, hair, beauty | beautician, hair, lashes, nails |
| electrician | electrician |
| cleaners | cleaners |
| dog-groomers | dog_groomers |
| gardeners-window-cleaners | gardeners |
| car-detailers | car_detailers |
| driving-instructors | driving_instructors |
| weddings | weddings |

Pain points flow one way: `verticals/<slug>/profile.json` → ad angles in aoc segments. Performance flows back: winning hooks update the vertical's campaign notes. Neither repo imports the other's code.

## Lead creation and monitoring

Two directions, both approval-gated:

1. **Opportunities (work coming):** planning + procurement + labour signals, scored per vertical, digested weekly. Customer approves before any contact.
2. **Customers (who needs work):** same signals framed customer-side with compliant next steps. Planning applicants are research, never prospects.

Monitoring means: track which alerts converted, record the outcome, feed it back into scoring. No monitoring without the customer's explicit opt-in to opportunity alerts.

## Muse's role in add-ons

When eligible, Muse (or ChatGPT) becomes the interface for add-ons: "what opportunities this week?", "draft that quote", "show my ad performance". The add-ons themselves remain our code, our data, our approval gates. The assistant is the remote control, not the engine.

Until Muse reaches the UK, every add-on must also work over email, WhatsApp, or the static dashboard. No add-on may depend solely on a platform the customer cannot access.
