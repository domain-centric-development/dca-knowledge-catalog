---
type: Pitfall
title: Declarative transaction without a transaction manager
tags: [pitfall, application, use-case, events, spring, modulith]
review: draft
owner: DCA catalog maintainers
evidence: [/rule/usecase/dca-use-012.md, /marker/application/transactionboundary.md, /marker/port-out/domaineventpublisher.md, /guide/readme/elements.md, /guide/spring-modulith/event-driven-architecture-in-spring-modulith.md]
---

A Spring application in its in-memory phase — `spring-boot-starter`, `spring-modulith-starter-core`, repositories over `ConcurrentHashMap`, no data starter — with `@Transactional` on its use cases. Everything compiles, the context starts, the architecture rules are green, and no after-commit listener ever runs.

## Why it is wrong

- `@Transactional` is metadata. It needs an interceptor to create the proxy and a `PlatformTransactionManager` to open a transaction. In Spring Boot 4 the interceptor is switched on by `TransactionAutoConfiguration`, which lives in `spring-boot-transaction` — an artifact that `spring-boot-starter` and `spring-modulith-starter-core` do **not** bring. The JDBC and JPA starters bring it, together with a manager. An in-memory application has neither.
- Without them the annotation is **silently inert**: no proxy, no transaction, not one log line even at `TRACE`. `@TransactionalEventListener` and Spring Modulith's `@ApplicationModuleListener` register on the *current* transaction and are skipped when there is none — the use case succeeds, the events are cleared from the aggregate, and the other module never hears of them.
- A manager bean alone does not help: without `spring-boot-transaction` (or an explicit `@EnableTransactionManagement`) the proxy is never created. The only self-announcing variant is `@EnableTransactionManagement` *without* a manager, and even that fails at the first call, not at startup (`NoSuchBeanDefinitionException: No qualifying bean of type 'org.springframework.transaction.TransactionManager'`).
- The rule that demands the transaction boundary reads the annotation and cannot see whether a manager exists — the failure is invisible to static analysis by construction.

## What forbids it

Nothing static can. The rule below makes the *intent* explicit; the runtime configuration has to honour it:

- [Use cases that publish domain events must have a transaction boundary](/rule/usecase/dca-use-012.md)

## Do instead

Three dependencies, declared on purpose, before the first write use case:

1. `org.springframework.boot:spring-boot-transaction` — the auto-configuration that turns the annotation into a proxy.
2. A `PlatformTransactionManager` bean. Until a database arrives, a small no-op subclass of `AbstractPlatformTransactionManager` **written in the project**, in a file whose name and comment say what replaces it. Deliberately not a library class: a published no-op manager survives into production unnoticed.
3. With Modulith, `org.springframework.modulith:spring-modulith-events-api` — `@ApplicationModuleListener` itself is not in `starter-core`.

Then the `TransactionBoundary` and `DomainEventPublisher` implementations from the `dca-spring` artifact are auto-configured (the boundary once the manager exists), and a test that publishes through the boundary and asserts the after-commit listener fired pins the whole chain. For tests without Spring, `InMemoryTransactionBoundary` keeps the nesting contract.

- Related: [Publishing domain events without a transaction](/pitfall/publishing-domain-events-without-a-transaction.md) — the same silence, caused by a missing annotation instead of a missing manager
- Decision: [Declarative or explicit transaction boundary](/decision/declarative-vs-explicit-transaction-boundary.md)

## Anchors

- Rules: [Use cases that publish domain events must have a transaction boundary](/rule/usecase/dca-use-012.md)
- Markers: [TransactionBoundary](/marker/application/transactionboundary.md) · [DomainEventPublisher](/marker/port-out/domaineventpublisher.md)
- Guide: [Shared kernel and the building-block dependency](/guide/readme/elements.md) · [Event-driven architecture in Spring Modulith](/guide/spring-modulith/event-driven-architecture-in-spring-modulith.md)
- Recipe: [Bootstrap a new application](/recipe/bootstrap-a-new-application.md)
