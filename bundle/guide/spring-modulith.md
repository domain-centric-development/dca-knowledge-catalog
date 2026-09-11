---
type: Guide
title: Spring Modulith Implementation
source: guide
resource: dca-guide/topics/spring-modulith.md
tags: [guide, guide]
---

*Practical Implementation of Domain-Centric Architecture using Spring Modulith*

> **📘 Prerequisites:** This document shows how to implement [Domain-Centric Architecture](/guide/readme.md) using Spring Modulith. Read the main document first for core patterns and rules.

> **☕ Java/Spring specific.** Everything here assumes Spring Boot and Spring Modulith. The .NET
> equivalents — project boundaries plus ArchUnitNET instead of module verification, an outbox or
> post-commit dispatch instead of `@TransactionalEventListener`, DI registration instead of component
> scan — are in [Language Mappings](/guide/language-mappings.md).

## Sections

- [Introduction](/guide/spring-modulith/introduction.md)
- [What is Spring Modulith?](/guide/spring-modulith/what-is-spring-modulith.md)
- [Core Concepts](/guide/spring-modulith/core-concepts.md)
- [Event-Driven Architecture in Spring Modulith](/guide/spring-modulith/event-driven-architecture-in-spring-modulith.md)
- [Module Structure](/guide/spring-modulith/module-structure.md)
- [Progressive Complexity for Spring Modulith Modules](/guide/spring-modulith/progressive-complexity-for-spring-modulith-modules.md)
- [Shared Kernel in Spring Modulith](/guide/spring-modulith/shared-kernel-in-spring-modulith.md)
- [Testing](/guide/spring-modulith/testing.md)
- [Module Communication](/guide/spring-modulith/module-communication.md)
- [Build Configuration](/guide/spring-modulith/build-configuration.md)
- [Summary](/guide/spring-modulith/summary.md)
