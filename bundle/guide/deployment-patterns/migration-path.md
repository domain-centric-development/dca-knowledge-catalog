---
type: Section
title: Migration Path
chapter: Deployment Patterns
source: guide
resource: dca-guide/topics/deployment-patterns.md
tags: [guide, section]
---

### Recommended Evolution

```mermaid
flowchart TD
    P1["<b>Phase 1 — modular monolith</b><br>where new projects start<br>clear module boundaries, events between them"]
    P2["<b>Phase 2 — extract the first SCS</b><br>when one module's needs diverge<br>highest value first, the rest stays"]
    P3["<b>Phase 3 — several SCS</b><br>driven by team structure<br>and by what actually has to scale"]
    P4["<b>Phase 4 — several services in one context</b><br>rarely needed: only for a very large context<br>with clear subdomain boundaries and a ready team"]
    P1 --> P2 --> P3 --> P4
```

**Anti-Pattern:** Starting with microservices before understanding domain boundaries.

**Best Practice:** Start simple (modular monolith), extract services when pain points emerge.

> **Implementation Note:** Spring Modulith provides excellent support for Phase 1 (modular monolith) with clear extraction paths to Phase 2. See [Spring Modulith Implementation](/guide/spring-modulith.md).
