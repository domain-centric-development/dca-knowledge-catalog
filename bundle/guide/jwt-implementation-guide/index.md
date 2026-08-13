# jwt-implementation-guide

- [1. Introduction and Scope](1-introduction-and-scope.md) — Two concerns that must be kept separate:
- [10. Brute-Force Protection and Login Attempt Tracking](10-brute-force-protection-and-login-attempt-tracking.md) — On every login attempt: insert a row into `login_attempts` (success or failure).
- [11. Account Status and Login Flow](11-account-status-and-login-flow.md) — Always return the same generic message for unauthenticated failures:
- [12. Refresh Token Rotation Flow](12-refresh-token-rotation-flow.md) — 1. POST /auth/refresh → Browser sends Cookie: shop-refresh=<raw>
- [13. Customer Tracking: Visitor Identity After Logout](13-customer-tracking-visitor-identity-after-logout.md) — The visitor identity answers "whose cart is this", not "is this person authenticated". Those two
- [14. Architecture Placement (DCA Pattern)](14-architecture-placement-dca-pattern.md) — New ports and use cases consistent with existing patterns:
- [15. Must-Haves Checklist](15-must-haves-checklist.md) — [ ] Switch from HS256 to ES256 (asymmetric signing)
- [16. Optional Enhancements](16-optional-enhancements.md) — [ ] Multi-level authentication (soft login / full login) with loginTyp claim
- [17. Related Documents](17-related-documents.md) — 17. Related Documents
- [2. Core Concepts: Two Separate Concerns](2-core-concepts-two-separate-concerns.md) — 2. Core Concepts: Two Separate Concerns
- [3. Token Types and Their Roles](3-token-types-and-their-roles.md) — Purpose: persists an anonymous `UserId` so the shopping cart survives browser restarts without requiring an account. ...
- [4. Token Lifetime Strategy](4-token-lifetime-strategy.md) — 4. Token Lifetime Strategy
- [5. Asymmetric Signing (ES256) for Multiservice](5-asymmetric-signing-es256-for-multiservice.md) — With a shared symmetric key, any service that can verify tokens can also mint them. A compromised service exposes the...
- [6. JWT Claims Design](6-jwt-claims-design.md) — Two standards define JWT claim names:
- [7. Cookie Requirements](7-cookie-requirements.md) — Path-scoping `shop-refresh` to `/auth/refresh` means the browser only sends it to the refresh endpoint. The cookie is...
- [8. CSRF Protection](8-csrf-protection.md) — When authentication credentials are stored in cookies, browsers automatically attach them to every request — includin...
- [9. PostgreSQL Schema](9-postgresql-schema.md) — CREATE TABLE login_attempts (
