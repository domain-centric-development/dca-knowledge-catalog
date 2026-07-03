---
type: Guide
title: JWT Implementation Guide
source: guide
resource: implementing-domain-centric-architecture/jwt-implementation-guide.md
tags: [guide, guide]
---

Reference guide for JWT-based authentication in a multiservice e-commerce platform. Covers token design, login state management, PostgreSQL-backed security infrastructure, cookie strategy, and customer tracking.

## Sections

- [1. Introduction and Scope](/guide/jwt-implementation-guide/1-introduction-and-scope.md)
- [2. Core Concepts: Two Separate Concerns](/guide/jwt-implementation-guide/2-core-concepts-two-separate-concerns.md)
- [3. Token Types and Their Roles](/guide/jwt-implementation-guide/3-token-types-and-their-roles.md)
- [4. Token Lifetime Strategy](/guide/jwt-implementation-guide/4-token-lifetime-strategy.md)
- [5. Asymmetric Signing (ES256) for Multiservice](/guide/jwt-implementation-guide/5-asymmetric-signing-es256-for-multiservice.md)
- [6. JWT Claims Design](/guide/jwt-implementation-guide/6-jwt-claims-design.md)
- [7. Cookie Requirements](/guide/jwt-implementation-guide/7-cookie-requirements.md)
- [8. CSRF Protection](/guide/jwt-implementation-guide/8-csrf-protection.md)
- [9. PostgreSQL Schema](/guide/jwt-implementation-guide/9-postgresql-schema.md)
- [10. Brute-Force Protection and Login Attempt Tracking](/guide/jwt-implementation-guide/10-brute-force-protection-and-login-attempt-tracking.md)
- [11. Account Status and Login Flow](/guide/jwt-implementation-guide/11-account-status-and-login-flow.md)
- [12. Refresh Token Rotation Flow](/guide/jwt-implementation-guide/12-refresh-token-rotation-flow.md)
- [13. Customer Tracking: Visitor Identity After Logout](/guide/jwt-implementation-guide/13-customer-tracking-visitor-identity-after-logout.md)
- [14. Architecture Placement (DCA Pattern)](/guide/jwt-implementation-guide/14-architecture-placement-dca-pattern.md)
- [15. Must-Haves Checklist](/guide/jwt-implementation-guide/15-must-haves-checklist.md)
- [16. Optional Enhancements](/guide/jwt-implementation-guide/16-optional-enhancements.md)
- [17. Related Documents](/guide/jwt-implementation-guide/17-related-documents.md)
