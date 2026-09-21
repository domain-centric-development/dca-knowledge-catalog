---
type: Reference
title: "Use cases that save an aggregate must publish its domain events — `EventFreeAggregate.platform`"
tags: [reference]
evidence_for: "/rule/usecase/dca-use-009.md#eventfreeaggregateplatform"
---

[Full node and context](/rule/usecase/dca-use-009.md#eventfreeaggregateplatform). This is an evidence excerpt; retain the parent selection and caveats.

### `EventFreeAggregate.platform`

```java
/**
   * A type the walk does not enter: the platform's own, or one of the vocabulary's - a marker and
   * the base classes beside it register no event. Derived from the configured roles, so a project's
   * own vocabulary stops the walk where the library's does.
   */
  private static boolean platform(String name, DcaMarkers markers) {
    return name.startsWith("java.")
        || markers.declaresTypesIn(name.substring(0, Math.max(name.lastIndexOf('.'), 0)));
  }
```
