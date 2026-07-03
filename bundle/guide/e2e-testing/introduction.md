---
type: Section
title: Introduction
chapter: E2E Testing for Domain-Centric Architecture
source: guide
resource: implementing-domain-centric-architecture/e2e-testing.md
tags: [guide, section]
---

E2E tests verify the complete user journey through your application. In domain-centric architecture, E2E tests sit at the top of the testing pyramid—few in number but critical for validating full-stack behavior.

**When to use E2E tests:**
- Critical user flows (checkout, authentication)
- Cross-bounded context interactions
- Smoke tests for deployments

**When NOT to use E2E tests:**
- Testing domain logic (use unit tests)
- Testing use case orchestration (use application tests)
- Testing every edge case (slow and brittle)

---
