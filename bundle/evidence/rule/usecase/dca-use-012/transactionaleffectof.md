---
type: Reference
title: "Use cases that save an aggregate or publish domain events must have a transaction boundary — `transactionalEffectOf`"
tags: [reference]
evidence_for: "/rule/usecase/dca-use-012.md#transactionaleffectof"
---

[Full node and context](/rule/usecase/dca-use-012.md#transactionaleffectof). This is an evidence excerpt; retain the parent selection and caveats.

### `transactionalEffectOf`

```java
/**
   * The effect of a code unit that needs a transaction, worded for the violation, or {@code null}
   * when the unit neither writes through a Repository nor publishes domain events.
   */
  private static String transactionalEffectOf(JavaCodeUnit unit) {
    boolean saves = calls(unit, Repository.class, "save");
    boolean deletes = calls(unit, Repository.class, "deleteById");
    boolean publishes = calls(unit, DomainEventPublisher.class);
    if (!saves && !deletes && !publishes) {
      return null;
    }
    List<String> effects = new ArrayList<>();
    if (saves) {
      effects.add("saves an aggregate");
    }
    if (deletes) {
      effects.add("deletes an aggregate");
    }
    if (publishes) {
      effects.add("publishes domain events");
    }
    return String.join(" and ", effects);
  }
```
