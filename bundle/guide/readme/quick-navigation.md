---
type: Section
title: Quick Navigation
chapter: Domain-Centric Architecture
source: guide
resource: implementing-domain-centric-architecture/README.md
tags: [guide, section]
---

### New to Domain-Centric Architecture?
| Step | Section | Description |
|------|---------|-------------|
| 1 | [Key Points](#key-points) | Core concepts and benefits |
| 2 | [Four Layers](#key-points) | Layer diagram and dependency flow |
| 3 | [Use Case Pattern](#use-case-pattern-with-input-ports) | Application layer organization |
| 4 | [Reference Implementation](https://github.com/chbloemer/ai-architecture-sample) | Working code examples |

### Ready to Implement?
- **[Java Package Structure](#java-package-structure)** - Copy-paste templates
- **[Spring Modulith](/guide/spring-modulith.md)** - Framework implementation guide
- **[ArchUnit Governance](/guide/archunit-governance.md)** - Enforce rules automatically

### Deep Dive Topics
| Topic | Guide | When to Read |
|-------|-------|--------------|
| Clean Architecture comparison | [clean-architecture-comparison.md](/guide/clean-architecture-comparison.md) | Understand differences |
| Deployment strategies | [deployment-patterns.md](/guide/deployment-patterns.md) | Planning production |
| Team organization | [team-topologies.md](/guide/team-topologies.md) | Scaling teams |
| Architecture decisions | [adr-template.md](/process/creating-an-adr.md) | Documenting choices |
| E2E Testing | [e2e-testing.md](/guide/e2e-testing.md) | Browser-based testing |
| Quick lookup | [architecture-reference-guide.md](/guide/architecture-reference-guide.md) | Already know DCA, need quick reference |

### Cross-Context Integration Patterns
| Pattern | Section | When to Use |
|---------|---------|-------------|
| Open Host Service | [OHS Pattern](#open-host-service-pattern) | Exposing context API to consumers |
| Composite Adapter | [Composite Adapter](#composite-adapter-pattern) | Aggregating data from multiple OHS |
| Resolver | [Resolver Pattern](#resolver-pattern) | Domain logic needing fresh external data |
| Enriched Read Model | [Enriched Read Model](#enriched-read-model-pattern) | Comparing persisted vs current data |
| Factory Assembly | [Factory for Cross-Context](#factory-for-cross-context-assembly) | Assembling complex domain objects |

---

## Related markers

- [Factory](/marker/tactical/factory.md)
