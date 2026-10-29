---
type: Reference
title: "Domain types must not hold bare primitives, strings or time types — `instanceFieldCount`"
tags: [reference]
evidence_for: "/rule/tactical/dca-tac-025.md#instancefieldcount"
---

[Full node and context](/rule/tactical/dca-tac-025.md#instancefieldcount). This is an evidence excerpt; retain the parent selection and caveats.

### `instanceFieldCount`

```java
private static long instanceFieldCount(JavaClass type) {
  return type.getFields().stream()
      .filter(
          f ->
              !f.getModifiers().contains(JavaModifier.STATIC)
                  && !f.getModifiers().contains(JavaModifier.SYNTHETIC))
      .count();
}
```
