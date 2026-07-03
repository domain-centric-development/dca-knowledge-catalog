---
type: Section
title: 10. Brute-Force Protection and Login Attempt Tracking
chapter: JWT Implementation Guide
source: guide
resource: implementing-domain-centric-architecture/jwt-implementation-guide.md
tags: [guide, section]
---

**Current gap:** `AuthenticateAccountUseCase` logs failures to the console but stores nothing; there is no rate limiting.

### Strategy

On every login attempt: insert a row into `login_attempts` (success or failure).

Before checking credentials, count recent failures:

| Condition | Action |
|-----------|--------|
| ≥ 5 failures for this email in 15 min | Soft lock: return 429, skip credential check |
| ≥ 20 failures from this IP in 15 min | IP block: return 429 for all accounts from that IP |
| 3 soft locks for this email in 24 h | Escalate to `AccountStatus.SUSPENDED` (requires manual reactivation) |

Make thresholds configurable:

```yaml
app:
  security:
    login-attempts:
      max-per-email: 5
      max-per-ip: 20
      window-minutes: 15
```

### Application Layer Placement

Consistent with the existing output port pattern:

```
account/application/shared/
└── LoginAttemptRepository.java    -- extends OutputPort; called before + after credential check
```

`AuthenticateAccountUseCase` calls `loginAttemptRepository.record(...)` before returning. The `Account` aggregate does not know about attempt tracking — that concern belongs to the application layer.

### Soft Lock vs Hard Suspension

- **Soft lock:** Temporary, auto-expires, controlled by infrastructure policy. User can retry after the window.
- **AccountSuspended:** Business/admin decision requiring manual reactivation. Raises a domain event that triggers session revocation (see Section 10).
- Escalate to `AccountSuspended` only after repeated lockout events (e.g., 3 soft locks in 24 hours), not on the first lockout (see Section 11 for how suspended status affects the login flow).

---

## Related markers

- [OutputPort](/marker/port-out/outputport.md)
