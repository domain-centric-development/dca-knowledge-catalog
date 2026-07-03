---
type: Section
title: Migration Path
chapter: Deployment Patterns
source: guide
resource: implementing-domain-centric-architecture/deployment-patterns.md
tags: [guide, section]
---

### Recommended Evolution

```
Phase 1: Modular Monolith
└─ Start here for new projects
   └─ Clear module boundaries
      └─ Domain events between modules

Phase 2: Extract First SCS
└─ When one module has very different needs
   └─ Extract highest-value module first
      └─ Keep rest as monolith

Phase 3: Multiple SCS
└─ Extract additional SCS as needed
   └─ Based on team structure
      └─ Based on scaling needs

Phase 4: Multi-Service BC (rarely needed)
└─ Only when BC is very large
   └─ And subdomain boundaries are clear
      └─ And team is very mature
```

**Anti-Pattern:** Starting with microservices before understanding domain boundaries.

**Best Practice:** Start simple (modular monolith), extract services when pain points emerge.

> **Implementation Note:** Spring Modulith provides excellent support for Phase 1 (modular monolith) with clear extraction paths to Phase 2. See [Spring Modulith Implementation](./spring-modulith.md).
