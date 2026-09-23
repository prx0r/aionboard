# AI Onboard

One-fee AI setup for UK trades and beauty businesses. Pilot only — zero paying customers. Everything unvalidated is marked as such.

## What it does

One-off setup (£499 standard, £20 quickstart). No subscriptions. Owner approves everything. We never hold passwords.

See [OFFER.md](OFFER.md) for canonical pricing and scope.

## Quick start

```bash
# Run all 147 tests
python3 -m unittest discover -s tests -v

# Generate the static pilot site
python3 -c "from aionboard.website import write_site; print(write_site())"

# Run the fictional electrician demo
python3 -c "from aionboard.demo import run_demo; import json; print(json.dumps(run_demo(), indent=2))"
```

## Repository structure

```
aionboard/            Python package (stdlib + cryptography only)
  crm.py              Prospects, contacts, attempts, TPS checks
  onboarding.py       Package registry + recipes (11 verticals)
  buddy.py            Per-business scoped assistant
  graph.py            Knowledge graph + retrieval
  opportunities.py    Geographic opportunity matcher
  security.py         Approvals, isolation, secret scan, audit
  backup.py           Encrypted SQLite backups
  privacy.py          GDPR export/delete
  compliance.py       Regulations registry loader
  manual.py           Customer teaching manual generator
  handover.py         Handover document generator
  website.py          Static site generators (index, chat, dashboard)
  assistant/          Per-target chatbot (profiles, legislation, powuk bridge)

verticals/            11 vertical packs (8 pilot-ready, 3 research stubs)
regulations/          36-rule combined registry
tests/                147 tests
site/                 Generated static pages
mcp/                  Tool contracts (designed, not deployed)
connector/            Muse submission pack (draft, not submitted)
data/                 Local databases, handovers (gitignored)
archive/              Superseded reference docs
```

## Start here

| I need... | Read |
|-----------|------|
| **Where to start** | [AGENTS.md](AGENTS.md) — full repo map, honest status, conventions |
| **What we sell** | [OFFER.md](OFFER.md) |
| **What to do next** | [THREADS.md](THREADS.md) — open work (T1-T12) |
| **Forward plan** | [DEVPLAN_NEXT.md](DEVPLAN_NEXT.md) — phases 0-4 with kill criteria |
| **Trust model** | [TRUST_MODEL.md](TRUST_MODEL.md) — five guarantees |
| **Security design** | [SECURITY_ARCHITECTURE.md](SECURITY_ARCHITECTURE.md) |
| **Strategy** | [STRATEGY.md](STRATEGY.md) — honest economics |
| **Sales** | [SALES_PLAYBOOK.md](SALES_PLAYBOOK.md), [SALES_EMAIL_01.md](SALES_EMAIL_01.md) |
| **Marketing** | [TIKTOK_BATCH_01.md](TIKTOK_BATCH_01.md) — 5 scripts + funnel |
| **Vertical intel** | `verticals/<slug>/profile.json` (machine-readable) |
| **Regulations** | [regulations/registry.json](regulations/registry.json) |
| **Build history** | [BUILD_NOTES.md](BUILD_NOTES.md) |
| **Electrician intel** | [ELECTRICIAN_INTEL.md](ELECTRICIAN_INTEL.md) |
| **Old research** | [archive/](archive/) — superseded but useful for reference |

## Conventions

1. Tests must pass before any commit
2. No secrets in the tree
3. Docs stay honest — hypotheses marked, no invented case studies
4. Stdlib + cryptography only
5. Customer data never enters git

## License

Private. Not for distribution.
