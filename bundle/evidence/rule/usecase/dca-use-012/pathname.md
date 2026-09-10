---
type: Reference
title: "Use cases that save an aggregate or publish domain events must have a transaction boundary — `pathName`"
tags: [reference]
evidence_for: "/rule/usecase/dca-use-012.md#pathname"
---

[Full node and context](/rule/usecase/dca-use-012.md#pathname). This is an evidence excerpt; retain the parent selection and caveats.

### `pathName`

```java
/** {@code execute} for the unit itself, {@code execute (via persist)} when reached through it. */
  private static String pathName(JavaCodeUnit entry, JavaCodeUnit unit) {
    return entry.equals(unit) ? entry.getName() : entry.getName() + " (via " + unit.getName() + ")";
  }
```
