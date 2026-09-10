---
type: Template
title: "Factory skeleton (complex aggregate creation in the domain)"
tags: [template, domain, factory]
review: draft
owner: DCA catalog maintainers
evidence: [/marker/tactical/factory.md, /rule/advanced/dca-adv-013.md, /rule/advanced/dca-adv-014.md, /rule/advanced/dca-adv-015.md, /rule/advanced/dca-adv-016.md, /guide/readme/elements.md, /guide/architecture-reference-guide/framework-annotations-rules.md]
applies_to: [java]
framework: [spring]
---

Domain-free skeleton for a **Factory**: a domain-layer object that encapsulates complex creation of an aggregate so that every returned instance is fully formed and satisfies its invariants from the first moment. Use it when construction is multi-step, requires knowledge the aggregate doesn't own, or would otherwise force a constructor to break the aggregate's invariants. It implements the `Factory` marker, is stateless (or minimal `final` state), carries **no** Spring annotation, and lives beside the aggregate in the domain layer. For simple cases prefer a static factory method on the aggregate itself (`{Name}.of(...)`) over a separate class — see the decision link. Replace `{Name}` (aggregate) / `{name}` / `{context}` / `{basePackage}`.

## `{Name}Factory.java` — factory (domain layer)

```java
package {basePackage}.{context}.domain.{name};

import {basePackage}.{context}.domain.{name}.event.{Name}Created;
import dev.domaincentric.dca.buildingblocks.ddd.tactical.Factory;

/**
 * Factory for creating {Name} aggregates.
 *
 * <p>Encapsulates complex creation logic and guarantees all invariants hold from
 * the moment of creation. Framework-free and stateless.
 */
public final class {Name}Factory implements Factory {

    /** Creates a new {Name}, generating its identity and raising the creation event. */
    public {Name} create({ValueObject} first, {ValueObject} second) {
        final {Name}Id id = {Name}Id.generate();

        final {Name} aggregate = new {Name}(id, first, second);
        aggregate.registerEvent({Name}Created.now(id, first));
        return aggregate;
    }

    /**
     * Reconstitutes a {Name} with an existing identity — does NOT raise a creation
     * event. Use only for rebuilding from persistence or in tests.
     */
    public {Name} reconstitute({Name}Id id, {ValueObject} first, {ValueObject} second) {
        return new {Name}(id, first, second);
    }
}
```

The factory is `final`, has no `@Component`/`@Service`, and returns a valid
aggregate — never a half-built object a caller must finish. Creation raises the
aggregate's creation domain event; reconstitution (rebuild from storage) does
not, so replayed history isn't re-published. Because it is framework-free it is
constructed with plain `new` by the use case, not injected.

## Realizes / governed by

- Marker: [Factory](/marker/tactical/factory.md)
- Rules: [Factories should implement Factory Marker Interface](/rule/advanced/dca-adv-013.md) · [Factories must reside in domain package](/rule/advanced/dca-adv-014.md) · [Factories must not have Spring annotations](/rule/advanced/dca-adv-015.md) · [Factories should be stateless (only final fields for dependencies)](/rule/advanced/dca-adv-016.md)
- Guide: [Layer elements](/guide/readme/elements.md) · [Framework annotation rules](/guide/architecture-reference-guide/framework-annotations-rules.md)
- Decisions: [Factory or constructor](/decision/factory-vs-constructor.md)
- Related template: [Aggregate root](/template/aggregate-root.md)
