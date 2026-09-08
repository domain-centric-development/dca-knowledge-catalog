# spring-modulith

- [Build Configuration](build-configuration.md) — <!-- pom.xml -->
- [Core Concepts](core-concepts.md) — com.company.ecommerce
- [Event-Driven Architecture in Spring Modulith](event-driven-architecture-in-spring-modulith.md) — Spring Modulith supports two types of events that align with Domain-Driven Design principles:
- [Introduction](introduction.md) — Spring Modulith is a framework for building **modular monolithic applications** with Spring Boot. It implements the D...
- [Module Communication](module-communication.md) — // Publisher (Order Module)
- [Module Structure](module-structure.md) — com.company.ecommerce
- [Progressive Complexity for Spring Modulith Modules](progressive-complexity-for-spring-modulith-modules.md) — When creating a Spring Modulith module (bounded context), **start with minimal structure** and add complexity only wh...
- [Shared Kernel in Spring Modulith](shared-kernel-in-spring-modulith.md) — The Shared Kernel is a **small, carefully controlled** `shared/` module containing code used across multiple modules.
- [Summary](summary.md) — 1. **Enforcing Boundaries** - Modules = Bounded Contexts with verified boundaries
- [Testing](testing.md) — Modulith's `ApplicationModules.verify()` is not an ArchUnit rule and needs `spring-modulith-core` at compile
- [What is Spring Modulith?](what-is-spring-modulith.md) — Spring Modulith enables building modular monoliths with clear boundaries between modules, making it easy to:
