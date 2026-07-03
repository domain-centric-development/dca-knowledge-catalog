---
type: Section
title: "Adoption Path (Tiers)"
chapter: ArchUnit Governance for Domain-Centric Architecture
source: guide
resource: implementing-domain-centric-architecture/archunit-governance.md
tags: [guide, section]
---

Introduce rules in tiers, ordered by how statically verifiable and how settled each rule is — not all at once.

### Tier 1 — Enforce Immediately

Fully static, high consensus, no project-specific conventions needed:

- Dependencies point inward; domain layer is framework-free
- No package cycles
- Bounded-context isolation (no direct cross-context imports)
- Aggregates reference other aggregates by ID only
- Repository interface/implementation split (interface in application, implementation in adapter)
- Transactions only in the application layer
- Value-object immutability
- Controllers never reach repositories directly

### Tier 2 — Needs Project Conventions

Verifiable only after the team agrees on marker interfaces/annotations and a package contract:

- DTO boundaries (adapters do not leak domain objects outward)
- Published-language / integration-event rules
- No public setters in domain classes
- No injected repositories or services inside aggregates
- Event shape and publishing rules
- Naming conventions

### Tier 3 — Warning-Level Fitness Functions

Trends to observe, not pass/fail gates — report instead of failing the build:

- Component size (classes per context or package)
- Coupling metrics: instability, abstractness, distance from the main sequence (ArchUnit metrics API, `com.tngtech.archunit.library.metrics`)
- Naming heuristics (e.g., flagging `*Manager` or `*Util` classes in the domain)

### Not Statically Testable

Some rules cannot be expressed as static checks at all. They belong in ADRs and review checklists:

- Aggregates designed around true invariants, not data convenience
- One aggregate modified per transaction
- Saga / process-manager design
- Pattern selection per context (domain model vs transaction script) — see [Context-Specific Rule Sets](#context-specific-rule-sets)

---

## Related markers

- [Repository<T, ID>](/marker/port-out/repository.md)
