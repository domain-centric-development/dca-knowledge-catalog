---
type: Reference
title: RULES — TESTING RULES
tags: [reference]
evidence_for: "/guide/readme/rules.md#testing-rules"
---

[Full node and context](/guide/readme/rules.md#testing-rules). This is an evidence excerpt; retain the parent selection and caveats.

### TESTING RULES

- Domain tested in isolation (unit tests)
- Domain tests require no infrastructure
- Domain tests require no frameworks
- Use cases tested with port mocks
- Use cases tested in isolation
- Adapters tested with integration tests
- Full system tested with acceptance tests
- Test pyramid: many unit, fewer integration, few E2E
