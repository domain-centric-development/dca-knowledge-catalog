---
type: Section
title: 4. Token Lifetime Strategy
chapter: JWT Implementation Guide
source: guide
resource: implementing-domain-centric-architecture/jwt-implementation-guide.md
tags: [guide, section]
---

| Token | Lifetime | Rationale |
|-------|----------|-----------|
| Visitor JWT | 30 days | Cart business requirement; no sensitive data |
| Access JWT | 15 min | Limits blast radius; invisible with silent refresh |
| Refresh token | 30 days (sliding) | Natural re-engagement cycle |
| Absolute refresh limit | 90 days | Hard cut-off regardless of rotation frequency |

**Why the current 7-day access token lifetime is insufficient:**
- A leaked token grants a 7-day attack window with no recourse
- With HS256, a compromised signing secret invalidates all services simultaneously
- Switching to a 15-minute access token + refresh rotation costs nothing for the user and dramatically reduces risk

---
