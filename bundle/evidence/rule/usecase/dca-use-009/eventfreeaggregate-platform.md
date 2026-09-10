---
type: Reference
title: "Use cases that save an aggregate must publish its domain events — `EventFreeAggregate.platform`"
tags: [reference]
evidence_for: "/rule/usecase/dca-use-009.md#eventfreeaggregateplatform"
---

[Full node and context](/rule/usecase/dca-use-009.md#eventfreeaggregateplatform). This is an evidence excerpt; retain the parent selection and caveats.

### `EventFreeAggregate.platform`

```java
private static boolean platform(String name) {
  return name.startsWith("java.") || name.startsWith("dev.domaincentric.dca.buildingblocks.");
}
```
