---
type: Section
title: STRATEGIC DESIGN RULES
chapter: Rules
source: guide
resource: dca-guide/architecture/rules.md
tags: [guide, section]
---

### Bounded Context Rules
- Each Bounded Context has own Ubiquitous Language
- Each Bounded Context has own model
- Same term can mean different things in different contexts
- Context boundaries are explicit
- Models not unified across contexts
- Teams own Bounded Contexts
- One Bounded Context per deployment unit (preferred)

> **Note:** For deployment variations including multi-service bounded contexts, see [Deployment Patterns](/guide/deployment-patterns.md)

### Context Integration Rules
- Make all context relationships explicit — declare them in code on each context's `package-info.java`
  (`@Upstream`, `@ExternalUpstream`, `@Partnership`, see [Declaring Context Relationships in Code](/guide/integration-patterns/declaring-context-relationships-in-code.md))
- Use Context Map to document relationships and each context's subdomain type (Core/Supporting/Generic);
  generate it from the declarations so it cannot drift
- Protect domain with Anti-Corruption Layer
- Shared Kernel requires team coordination
- Keep Shared Kernel small
- Upstream contexts influence downstream
- Define integration patterns clearly

### Subdomain Rules
- Focus most effort on Core Domain
- Core Domain provides competitive advantage
- Supporting Subdomains support core
- Generic Subdomains can be outsourced
- Align Bounded Contexts with Subdomains

### Pattern Selection per Subdomain

DCA's full pattern set is not mandatory for every bounded context. Apply tactical DDD where complexity warrants it — never to trivial domains. Choose per context, by subdomain type:

| Subdomain | Business Logic Pattern | Architecture | Notes |
|---|---|---|---|
| **Core** | Rich domain model (aggregates, domain events) | Ports & Adapters, optionally CQRS / event sourcing | Full DCA rule set applies |
| **Supporting** | Transaction script or active record | Simple layering | CRUD is not an anti-pattern here |
| **Generic** | Buy / adopt (SaaS, open source) | Integrate via ACL | Don't build what you can buy |

Rules:
- Each bounded context declares its chosen pattern style in an ADR
- Architecture tests activate the matching rule subset per context: domain-model contexts get the full tactical rules; transaction-script contexts only the structural baseline (layer dependencies, no cycles, context isolation) — see [ArchUnit Governance](/guide/archunit-governance.md)
- Consistency within a context matters; uniformity across contexts does not
- Reclassify when a subdomain's importance changes (supporting → core happens) and upgrade the pattern with it — this is Progressive Complexity at the strategic level

## Related mentions (heuristic)

- [@ExternalUpstream](/marker/strategic/externalupstream.md)
- [@Partnership](/marker/strategic/partnership.md)
- [@Upstream](/marker/strategic/upstream.md)
