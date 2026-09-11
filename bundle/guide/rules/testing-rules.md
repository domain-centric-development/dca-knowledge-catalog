---
type: Section
title: TESTING RULES
chapter: Rules
source: guide
resource: dca-guide/architecture/rules.md
tags: [guide, section]
---

- Domain tested in isolation (unit tests)
- Domain tests require no infrastructure
- Domain tests require no frameworks
- Use cases tested with port mocks
- Use cases tested in isolation
- Adapters tested with integration tests
- Full system tested with acceptance tests
- Test pyramid: many unit, fewer integration, few E2E
