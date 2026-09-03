---
type: Template
title: "Enriched domain model skeleton (read model combining aggregate + cross-context data)"
tags: [template, domain, value-object, bounded-context]
---

Domain-free skeleton for an **enriched domain model**: an immutable read model that combines one aggregate's state with fresh data fetched from *other* bounded contexts, and owns the business rules that need data from more than one context. It is a **Value Object** — it implements `Value`, lives in `{context}.domain.model/` next to the aggregate it enriches, has **no identity, no lifecycle, and raises no events**. Assembly happens through a **static factory** that takes the aggregate plus the external data; the aggregate never learns about the external concepts, so bounded-context isolation stays intact. Use this when a read must show aggregate state together with, e.g., current price (Pricing) or stock (Inventory), or must compare persisted vs. current values. Replace `{Name}` (aggregate) / `{context}` / `{basePackage}` / `{External}` (the cross-context data carrier).

## `Enriched{Name}.java` — enriched read model (domain layer)

```java
package {basePackage}.{context}.domain.model;

import {basePackage}.sharedkernel.domain.model.Money;
import dev.domaincentric.dca.buildingblocks.ddd.tactical.Value;

/**
 * Enriched read model: {Name} aggregate state + cross-context data.
 * Owns cross-context business rules (evaluation); the aggregate owns identity and mutations.
 */
public record Enriched{Name}(
    {Name}Id {name}Id,
    // fields copied from the aggregate (denormalised) …
    Money currentPrice,        // from another context (e.g. Pricing)
    int stockQuantity,         // from another context (e.g. Inventory)
    boolean isAvailable
) implements Value {

    public Enriched{Name} {
        // validate the invariants this read model must hold (non-null id, price, …)
    }

    // Factory: combine the aggregate with external data fetched via ports.
    public static Enriched{Name} from(final {Name} {name}, final {External} external) {
        return new Enriched{Name}(
            {name}.id(),
            /* {name}.someField().value(), … */
            external.currentPrice(),
            external.stockQuantity(),
            external.isAvailable());
    }

    // Cross-context business rules live here, not on the aggregate.
    public boolean canPurchase() { return isAvailable && stockQuantity > 0; }
    public boolean hasStockFor(final int quantity) { return stockQuantity >= quantity; }
}
```

The enriched model implements `Value`, so it is compared by attributes and stays
immutable. It carries **no** `@Entity`/`@Component` annotation and references no
other aggregate — the external data arrives as a plain carrier (`{External}`),
typically produced by an Open Host Service of the owning context. Keep the
responsibility split sharp: the aggregate owns identity, mutations and its own
invariants; the enriched model owns only the rules that genuinely need
cross-context data. For presentation, map it to a [ViewModel](/template/view-model.md) at the adapter edge — never expose the enriched model (with its `Money` and other domain types) to a template.

## Realizes / governed by

- Marker: [Value](/marker/tactical/value.md)
- Guide: [Enriched Read Model Pattern](/guide/readme/integration-patterns.md) · [Layer elements](/guide/readme/elements.md) · [Java package structure](/guide/readme/java-package-structure.md)
- Related template: [ViewModel](/template/view-model.md)
- Related decision: [Plain query use case or a dedicated read model](/decision/read-model-vs-domain-query.md)
