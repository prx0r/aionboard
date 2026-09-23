# Vertical packs

Repeatable per-industry structure. Electrician is the first pilot pack; beauty and the nine `targets.md` niches reuse the same skeleton.

Pattern:

```text
verticals/
  _template/
  electrician/
  beauty/
  nails/
  lashes/
  hair/
  dog-groomers/
  cleaners/
  gardeners-window-cleaners/
  car-detailers/
  driving-instructors/
  weddings/
```

Each vertical pack contains:

- `manifest.json`: machine-readable identity, status, subdomains, and source pointers.
- `profile.json`: structured pains, stack, onboarding difficulty, legal, UK opportunities, finance, tax, and agent readiness.
- `README.md`: pilot scope and evidence state.
- `PAINS.md`: top verified research pains, not measured customer outcomes.
- `STACK.md`: existing customer software; integrate or import, do not replace unnecessarily.
- `CAMPAIGN.md`: narrow paid pilot campaign.
- `DISCOVERY.md`: portable AI-assistant discovery checklist.
- `INSTALL.md`: manual-first installation checklist reference.

Rules:

1. Point to upstream research where possible; do not duplicate entire external repositories.
2. Mark every number as research, pilot estimate, or measured outcome.
3. Do not invent case-study results.
4. Keep customer PII out of this public repository.
5. Live voice, website builds, Meta production access, and custom integrations are separate deliverables unless explicitly included in `OFFER.md`.
