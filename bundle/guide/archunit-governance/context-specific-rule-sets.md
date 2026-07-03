---
type: Section
title: Context-Specific Rule Sets
chapter: ArchUnit Governance for Domain-Centric Architecture
source: guide
resource: implementing-domain-centric-architecture/archunit-governance.md
tags: [guide, section]
---

Not every bounded context warrants the full rule set. A core context with a rich domain model benefits from all tactical rules; a simple supporting context (lookup data, basic admin CRUD) implemented as transaction script or active record would only fight rules written for aggregates it does not have.

**Approach:** Each context declares its pattern style in an ADR:

- **Domain-model contexts** — full tactical rule set: framework-free domain, aggregate rules, value-object immutability, domain-event immutability, etc.
- **Transaction-script contexts** — structural baseline only: layer dependencies, no package cycles, bounded-context isolation

Scope the tactical rules to the declared domain-model contexts:

```java
// Contexts that committed to a rich domain model (per ADR).
// Transaction-script contexts (e.g., backoffice) are intentionally absent.
private static final String[] DOMAIN_MODEL_CONTEXTS = {
    "..order.domain..",
    "..pricing.domain..",
    "..inventory.domain.."
};

@ArchTest
static final ArchRule value_objects_in_domain_model_contexts_are_immutable =
    classes()
        .that().resideInAnyPackage(DOMAIN_MODEL_CONTEXTS)
        .and().implement(Value.class)
        .should().haveOnlyFinalFields()
        .because("Domain-model contexts committed to immutable Value Objects (see ADR)");
```

The structural baseline (layer dependencies, cycles, context isolation) still applies to **every** context — only the tactical DDD rules are scoped.

---

## Related markers

- [Value](/marker/tactical/value.md)
