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
  private static String transactionalEffectOf(JavaCodeUnit unit, DcaMarkers markers) {
    boolean saves = calls(unit, markers.repository(), "save");
    boolean deletes = calls(unit, markers.repository(), "deleteById");
    boolean publishes = calls(unit, markers.domainEventPublisher());
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
