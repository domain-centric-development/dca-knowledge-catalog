---
type: Section
title: What is Spring Modulith?
chapter: Spring Modulith Implementation
source: guide
resource: implementing-domain-centric-architecture/spring-modulith.md
tags: [guide, section]
---

Spring Modulith enables building modular monoliths with clear boundaries between modules, making it easy to:

1. **Start Simple** - Single deployment unit, simple development
2. **Enforce Boundaries** - Modules can't access each other's internals
3. **Event-Driven** - Asynchronous communication between modules
4. **Extract Services** - Easy path to microservices if needed

**Benefits over plain Spring Boot:**
- Explicit module boundaries
- Compile-time verification of dependencies
- Event-based decoupling
- Easy testing of modules in isolation
- Clear documentation of module structure
