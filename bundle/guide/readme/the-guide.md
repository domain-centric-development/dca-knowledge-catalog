---
type: Section
title: The guide
chapter: Domain-Centric Architecture
source: guide
resource: dca-guide/README.md
tags: [guide, section]
---

The architecture itself, in reading order:

| Document | What it settles |
|---|---|
| [Elements](/guide/elements.md) | The four layers and what lives in each, the use-case pattern, the building blocks the library defines |
| [Strategic Architecture](/guide/strategic-design.md) | Bounded contexts, the shared kernel, and what may enter it |
| [Repository vs. Store](/guide/repository-vs-store.md) | The two persistence-shaped output ports, and the persistence model kept separate from the aggregate |
| [Rules](/guide/rules.md) | The rule catalog in prose — per layer, per building block, per boundary |
| [Java Package Structure](/guide/package-structure.md) | Package templates, progressive complexity, features, where a custom annotation lives |
| [Dependency Structure](/guide/dependency-structure.md) | Which direction dependencies run, what an adapter may inject, how to repair a wrong one |
| [Integration Patterns](/guide/integration-patterns.md) | Open Host Service, composite adapter, enriched read model, events across contexts |
| [Quick Reference](/guide/quick-reference.md) | Placement tables and a checklist, for readers who know the style |
| [References & Further Reading](/guide/references.md) | The literature this rests on |

Deeper topics, each self-contained:

| Document | When to read it |
|---|---|
| [ArchUnit Governance](/guide/archunit-governance.md) | Enforcing the rules in a build |
| [Spring Modulith](/guide/spring-modulith.md) | Implementing contexts as modules on Spring |
| [Language Mappings](/guide/language-mappings.md) | Writing the same architecture in C#/.NET |
| [Clean Architecture Comparison](/guide/clean-architecture-comparison.md) | Understanding how this differs from Clean Architecture |
| [Deployment Patterns](/guide/deployment-patterns.md) | Self-Contained Systems, service decomposition, going to production |
| [Team Topologies](/guide/team-topologies.md) | Aligning teams with bounded contexts |
| [Domain Services with Data Dependencies](/guide/domain-services-with-data-dependencies.md) | A domain service that needs data it cannot reach |
| [E2E Testing](/guide/e2e-testing.md) | Browser tests with the Page Object pattern |
| [JWT Implementation](/guide/jwt-implementation-guide.md) | Authentication across contexts |

Process:

| Document | What it is |
|---|---|
| [Factory](/guide/factory.md) | Delivering one story: backlog contract, six stages, the gates between them |
| [ADR Template](/process/creating-an-adr.md) | Recording an architectural decision |

> **📝 Note on examples.** This guide uses generic examples (Order, Customer, Inventory) for
> clarity. Package names shown as `com.company.project.*` are placeholders; a real project uses its
> own root. The guide is written in Java; [Language Mappings](/guide/language-mappings.md)
> translates every concept to C#/.NET.

## Related mentions (heuristic)

- [Repository<T, ID>](/marker/port-out/repository.md)
- [Factory](/marker/tactical/factory.md)
