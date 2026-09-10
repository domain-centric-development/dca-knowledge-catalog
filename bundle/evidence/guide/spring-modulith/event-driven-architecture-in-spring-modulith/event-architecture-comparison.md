---
type: Reference
title: Event-Driven Architecture in Spring Modulith — Event Architecture Comparison
tags: [reference]
evidence_for: "/guide/spring-modulith/event-driven-architecture-in-spring-modulith.md#event-architecture-comparison"
---

[Full node and context](/guide/spring-modulith/event-driven-architecture-in-spring-modulith.md#event-architecture-comparison). This is an evidence excerpt; retain the parent selection and caveats.

### Event Architecture Comparison

| Aspect | Domain Event | Integration Event |
|--------|--------------|-------------------|
| **Scope** | Within module | Across modules |
| **Package** | `internal/domain/event/` | `events/` (published) |
| **Marker** | Optional `DomainEvent` | `implements Externalized` ⭐ |
| **Serialization** | Not required | Required |
| **Versioning** | Not required | Required |
| **Delivery** | Sync (in-tx) *or* async (registry-backed) | Async, externalized via registry |
| **Persistence** | Only when delivered async (registry) | Yes (Event Publication Registry) |
| **Retry** | Resubmission supported for registry-backed listeners | Configure bounded retries, backoff and manual replay |
| **Visibility** | Private to module | Public to all modules |

> **Delivery mode is orthogonal to event type.** Persistence and retry come from
> **asynchronous, registry-backed delivery** — not from an event being "integration".
> A domain event handled by a synchronous listener runs in the publishing transaction and
> needs neither. A domain event handled by an **async** `@ApplicationModuleListener` is
> persisted in the registry and redelivered at-least-once — the same durable, in-process
> transactional-outbox guarantee, still **without leaving the module**. The integration
> event differs only in that its async delivery is *externalized* to a broker.
