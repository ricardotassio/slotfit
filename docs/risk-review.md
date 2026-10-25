# Threat, safety and evidence-integrity review

## Scope

This review covers the local synthetic POC. It is not a production healthcare
threat model and does not authorize public hosting or real data.

| Risk | Current mitigation | Residual boundary |
|---|---|---|
| Real identity or health data enters the POC | No patient/contact schema; fixtures are visibly synthetic; SECURITY.md prohibits real data | Free-form rationale could still be misused; a shared deployment needs data-loss controls and authentication |
| SQL injection | Pydantic length/pattern validation and parameterized SQLite statements | Validation is not authorization; a networked service needs identity, tenant and rate controls |
| Stored/reflected XSS | Review text is not rendered; Vue escapes interpolated fixture values | Any future review-history screen needs explicit output-encoding tests and CSP |
| Duplicate review event | Database unique constraint, transaction, winner comparison and two-connection test | SQLite serializes local writes; multi-user contention requires a PostgreSQL adapter and integration tests |
| Mutation of audit history | Database triggers reject update/delete; API exposes no such routes | Anyone with filesystem access can replace the database; production needs access control, backup and tamper-evident storage |
| Denial of service | Only bounded fixtures are exposed; solver has deterministic and wall limits; review fields are size-limited | No rate limiting exists; bind only to loopback |
| External action by mistake | No messaging/booking client exists; every response/event says `automatic_action` or `external_action: none` | Adding any integration requires a new safety review and explicit authorization |
| Presentation bias | Baseline-first neutral controls, equal styling, separate metrics, table fallback and visible no-go | Human interpretation can still anchor; user research is required before consequential use |
| Audit-label leakage | Operational slices never enter decision scenarios; metamorphic tests cover IDs/order | New features must preserve the decision/audit boundary |
| Benchmark leakage and p-hacking | Development/calibration/final registries are separated; S7 stayed closed after no-go | A new hypothesis requires fresh registries; current development seeds cannot become independent evidence |
| Unsupported public claims | Bilingual drafts include synthetic/no-go/no-external-action language; tests enforce those disclosures | Editing after export can bypass repository tests; use the publication checklist |
| Dependency or CI compromise | Exact Python/npm lockfiles, read-only CI token and no CI secrets/services | GitHub Actions use version tags; future hardening can pin reviewed full commit SHAs |
| Local database disclosure | Database is Git-ignored and contains only synthetic references | Filesystem permissions inherit the host; do not sync or share a database containing inappropriate text |

## Security conclusions

The controls are proportionate for a loopback, single-user, synthetic demo. They
are not sufficient for public hosting, PHI/PII, multi-tenancy, clinical workflow or
automatic action. The first safe step toward those contexts is a new architecture
and threat review—not an environment-variable change.

## Evidence-integrity conclusion

The terminal no-go is part of the safety story. V4 missed the fixed guardrail by
0.80 percentage point, and S7 remained closed. Changing the threshold or running
the held-out set anyway would be an integrity failure even though the code works.
