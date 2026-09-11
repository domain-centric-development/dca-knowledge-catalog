---
type: Decision
title: Keep a context in the modulith or extract it to a service
tags: [decision, strategic, modulith, bounded-context, migration, integration-event, events]
review: draft
owner: DCA catalog maintainers
evidence: [/guide/spring-modulith/what-is-spring-modulith.md, /guide/spring-modulith/module-communication.md, /guide/deployment-patterns/service-decomposition.md, /marker/strategic/boundedcontext.md, /marker/strategic/openhostservice.md, /marker/tactical/integrationevent.md, /guide/deployment-patterns/migration-path.md, /guide/deployment-patterns/deployment-pattern-comparison.md]
---

A bounded context lives inside your modular monolith. The fork is whether to **keep it there** or **extract it into its own deployable service**. Extraction buys independent scaling, technology, and release cycles — and charges you distributed complexity: network failure, eventual consistency, and operational overhead. The mistake almost everyone makes is extracting before the boundary is proven, so the default is to keep, and the interesting question is *what must be true first*.

## The discriminator

Ask, in order:

1. **Is the boundary already clean inside the modulith?** Extraction only works if the context already communicates through its Open Host Service and integration events, owns its own data, and shares no database with its neighbors. If cross-context calls are still direct method calls or a shared schema, **keep it and fix the coupling first** — extraction won't fix a boundary that isn't there.
2. **Is there a concrete pressure to extract?** A real need — this context must scale independently, wants a different tech stack, has a different release cadence, or is owned by a separate team — justifies **extraction**. "Microservices are the goal" does not; that is the anti-pattern of starting distributed before the domain boundaries are understood.
3. **Can the consumers tolerate the network?** Once extracted, every previously in-process call becomes a remote call subject to latency and failure, and previously atomic reactions become eventually consistent. If the interaction demanded immediate consistency across the boundary, that boundary probably isn't ready to become a wire.
4. **Is the team mature enough for distribution?** Distributed systems add operational and consistency burden. If the team can't yet carry it, **keep the modulith** and extract later.

## Options

### Keep it in the modulith

The context stays a Spring Modulith module: its own package boundary, in-process Open Host Service for synchronous reads, `@ApplicationModuleListener` for in-process event reactions. You still get isolation and independent evolution *in code* without any network. Because the consumer depends only on its own output port, the adapter — not the use case — is the only thing that changes on a later extraction.

- **When:** the default for new work and for any context whose boundary or team isn't yet ready; immediate consistency needed across the boundary; small or single team.
- Ground: [What is Spring Modulith](/guide/spring-modulith/what-is-spring-modulith.md) · [Module Communication](/guide/spring-modulith/module-communication.md)

### Extract it to a service

Promote the context to its own deployable. Synchronous reads move from the in-process OHS to a REST OHS; in-process events move to integration events over a broker with a transactional outbox. The context must own its data and expose only versioned contracts.

- **When:** a proven need for independent scaling, technology, release cadence, or team ownership — *and* the boundary is already event-based with its own data.
- Ground: [Service Decomposition](/guide/deployment-patterns/service-decomposition.md) · cross-boundary events: [Publish a cross-context event](/recipe/publish-a-cross-context-event.md)

**Default:** **start as a modular monolith and extract only when a pain point emerges.** The recommended evolution is one service per context first, then extract the highest-value context when its needs diverge, then more as needed — multi-service decomposition *within* one context is rarely warranted. What must be true before you extract: event-based coupling through the OHS and integration events, and the context owning its own data. If those aren't true yet, the work is to establish them inside the modulith, not to extract.

## Anchors

- Markers: [@BoundedContext](/marker/strategic/boundedcontext.md) · [@OpenHostService](/marker/strategic/openhostservice.md) · [IntegrationEvent](/marker/tactical/integrationevent.md)
- Guide: [Service Decomposition](/guide/deployment-patterns/service-decomposition.md) · [Migration Path](/guide/deployment-patterns/migration-path.md) · [Deployment Pattern Comparison](/guide/deployment-patterns/deployment-pattern-comparison.md) · [Self-Contained Systems (SCS)](/guide/deployment-patterns/self-contained-systems-scs.md) · [Module Communication](/guide/spring-modulith/module-communication.md) · [Event-Driven Architecture in Spring Modulith](/guide/spring-modulith/event-driven-architecture-in-spring-modulith.md) · [Java package structure](/guide/package-structure.md) · [Dependency structure](/guide/dependency-structure.md)
- Recipes: [Publish a cross-context event](/recipe/publish-a-cross-context-event.md)
- Related decisions: [Cross-context communication](/decision/cross-context-communication.md) · [Event delivery: sync, async, and when you need an outbox](/decision/event-delivery-sync-async-and-outbox.md)
