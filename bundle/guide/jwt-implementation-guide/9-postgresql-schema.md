---
type: Section
title: 9. PostgreSQL Schema
chapter: JWT Implementation Guide
source: guide
resource: implementing-domain-centric-architecture/jwt-implementation-guide.md
tags: [guide, section]
---

### 9.1 `login_attempts` Table

```sql
CREATE TABLE login_attempts (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email           VARCHAR(255)  NOT NULL,
    ip_address      INET          NOT NULL,
    attempted_at    TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    success         BOOLEAN       NOT NULL,
    failure_reason  VARCHAR(100)            -- 'WRONG_PASSWORD', 'ACCOUNT_SUSPENDED', 'NOT_FOUND'
);

CREATE INDEX idx_login_attempts_email_time
    ON login_attempts (email, attempted_at DESC) WHERE success = FALSE;

CREATE INDEX idx_login_attempts_ip_time
    ON login_attempts (ip_address, attempted_at DESC) WHERE success = FALSE;
```

**Why PostgreSQL over Redis:**
- Audit data must survive restarts and be queryable for forensics
- SQL window queries (`COUNT(*) OVER (PARTITION BY email ORDER BY attempted_at)`) simplify rate-limit calculations
- No sub-millisecond latency required for a login endpoint
- No extra infrastructure to operate

**Row retention:** 90 days. Purge via scheduled job (`DELETE FROM login_attempts WHERE attempted_at < NOW() - INTERVAL '90 days'`) or time-based partitioning.

### 9.2 `refresh_tokens` Table

```sql
CREATE TABLE refresh_tokens (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    token_hash          VARCHAR(64)   NOT NULL UNIQUE,   -- SHA-256 hex of raw token
    user_id             VARCHAR(36)   NOT NULL,
    email               VARCHAR(255)  NOT NULL,
    issued_at           TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    expires_at          TIMESTAMPTZ   NOT NULL,          -- sliding; reset on rotation
    last_rotated_at     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    absolute_expires_at TIMESTAMPTZ   NOT NULL,          -- hard limit; never updated
    device_hint         VARCHAR(255),                    -- User-Agent substring
    ip_address          INET,
    revoked             BOOLEAN       NOT NULL DEFAULT FALSE,
    revoked_at          TIMESTAMPTZ,
    revoked_reason      VARCHAR(100)                     -- 'LOGOUT', 'SUSPICIOUS', 'ACCOUNT_SUSPENDED'
);

CREATE UNIQUE INDEX idx_refresh_tokens_hash    ON refresh_tokens (token_hash);
CREATE INDEX        idx_refresh_tokens_user_id ON refresh_tokens (user_id) WHERE revoked = FALSE;
```

**Critical:** Never store the raw token value. Only store `SHA-256(rawToken)` as a hex string. The raw value must exist only in memory during processing and in the `HttpOnly` cookie on the client.

---
