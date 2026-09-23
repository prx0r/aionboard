# DATA_POLICY.md

> How AI Onboard handles data: what we store, where it lives, how long we keep it, and how we recover it.

## Data classes

| Class | Examples | Where it lives | In git? |
|-------|----------|----------------|---------|
| Public research | Companies House records, ONS data, pain registry | `prospects_electrical.csv`, BigQuery | Yes (no PII) |
| Customer PII | Names, phones, emails, addresses | Local SQLite only | **Never** |
| Credentials | OAuth tokens, API keys, passwords | Customer-owned vaults / OS keychain | **Never** |
| Installation records | Checklists, handovers, evidence | Local SQLite + `data/handovers/` | **Never** |
| Audit logs | Tool calls, approvals, contact attempts | Local SQLite | **Never** |

## Rules

1. **Research is not permission.** A prospect record never implies marketing consent.
2. **No passwords, ever.** OAuth or customer-performed exports only.
3. **No secrets in code, docs, prompts, or handovers.** `scan_text()` rejects them.
4. **One customer, one boundary.** Credential refs and storage paths must be disjoint across clients (`assert_customer_isolation`).
5. **Failed verification is blocked, never complete.** No false-green records.

## Retention

| Data | Keep for | Then |
|------|----------|------|
| Prospect research | Until superseded by newer import | Update in place, preserve source |
| Contact attempts | 3 years (legitimate-interest evidence) | Delete on request |
| Call transcripts | 90 days (per influence kernel default) | Sweep quarterly with `confirm:true` |
| Installation handovers | Duration of customer relationship + 1 year | Delete on request |
| Suppression list | **Indefinitely** | Never delete (do-not-contact must persist) |
| Audit logs | 3 years | Delete on request unless legal hold |

## Backups

Local SQLite databases are backed up with `aionboard.backup`:

- Timestamped copy: `data/backups/crm-YYYYMMDD-HHMMSS.sqlite3`
- SHA-256 manifest alongside each backup
- Verify by restoring to a temp database and running the test suite
- Backups inherit the same access controls as live data
- Never commit backups to git

## Incident response

1. Revoke affected credentials immediately.
2. Identify scope: which clients, which records, which time window.
3. Notify affected customers within 72 hours (UK GDPR).
4. Record the incident in the audit log.
5. Fix the root cause before reconnecting anything.

## Customer rights

On request, within 30 days:

- Export everything we hold about them (handover format).
- Delete everything except the suppression record and legal-hold audit entries.
- Revoke all OAuth grants and API access.
