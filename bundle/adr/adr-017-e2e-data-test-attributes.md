---
type: ADR
title: "ADR-017: Data-Test Attributes for E2E Test Selectors"
adr: 17
status: accepted
pattern: "All HTML elements interacted with in E2E tests MUST have a `data-test` attribute."
resource: ai-architecture-sample/docs/architecture/adr/adr-017-e2e-data-test-attributes.md
tags: [adr]
---

All HTML elements interacted with in E2E tests MUST have a `data-test` attribute.

**Consequences:** UI text/styling can change · Tests are more readable · Clear contract · Language-independent · Refactoring-safe · Slight template verbosity

## Decision process

- [How to write an ADR](/process/creating-an-adr.md)
