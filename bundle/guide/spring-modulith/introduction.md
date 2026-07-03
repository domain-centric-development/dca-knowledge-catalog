---
type: Section
title: Introduction
chapter: Spring Modulith Implementation
source: guide
resource: implementing-domain-centric-architecture/spring-modulith.md
tags: [guide, section]
---

Spring Modulith is a framework for building **modular monolithic applications** with Spring Boot. It implements the [Domain-Centric Architecture](./README.md) patterns while providing:

- **Module Verification** - Enforces architectural boundaries at compile/test time
- **Event-Based Communication** - Application Events between modules
- **Documentation** - Auto-generates module documentation
- **Observability** - Built-in module metrics and tracing
- **Integration Testing** - Test modules in isolation
- **Event Publication Registry** - Guaranteed event delivery

**Mapping:**
```
Spring Modulith Module = Bounded Context (from DDD)
                       = Domain-Centric Architecture Package Structure
```

> **Note:** For core bounded context and layer concepts, see [Domain-Centric Architecture](./README.md).
