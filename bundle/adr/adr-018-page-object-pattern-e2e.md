---
type: ADR
title: "ADR-018: Page Object Pattern for E2E Tests"
adr: 18
status: accepted
pattern: All E2E tests MUST use Page Objects to encapsulate page-specific selectors and interactions.
resource: ai-architecture-sample/docs/architecture/adr/adr-018-page-object-pattern-e2e.md
tags: [adr]
---

All E2E tests MUST use Page Objects to encapsulate page-specific selectors and interactions.

**Consequences:** Selectors centralized · Tests are shorter · Business-readable · Type-safe navigation · Reusable components · Initial overhead · Maintenance of page objects

## Decision process

- [How to write an ADR](/process/creating-an-adr.md)
