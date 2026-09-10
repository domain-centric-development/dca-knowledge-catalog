---
type: Template
title: "Factory skeleton (complex aggregate creation in the domain) — Java"
parent: /template/factory.md
tags: [template, domain, factory]
review: draft
owner: DCA catalog maintainers
evidence: [/marker/tactical/factory.md, /rule/advanced/dca-adv-013.md, /rule/advanced/dca-adv-014.md, /rule/advanced/dca-adv-015.md, /rule/advanced/dca-adv-016.md, /guide/readme/elements.md, /guide/architecture-reference-guide/framework-annotations-rules.md]
applies_to: [java]
framework: [spring]
---

The Java code of [Factory skeleton (complex aggregate creation in the domain)](/template/factory.md). The prose, the evidence and what
governs it stay in that node; this file carries the skeleton only.

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
