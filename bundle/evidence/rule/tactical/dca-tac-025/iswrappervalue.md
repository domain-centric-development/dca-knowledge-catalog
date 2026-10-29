---
type: Reference
title: "Domain types must not hold bare primitives, strings or time types — `isWrapperValue`"
tags: [reference]
evidence_for: "/rule/tactical/dca-tac-025.md#iswrappervalue"
---

[Full node and context](/rule/tactical/dca-tac-025.md#iswrappervalue). This is an evidence excerpt; retain the parent selection and caveats.

### `isWrapperValue`

```java
/** A value or an identifier of exactly one instance field: it wraps that field's primitive. */
  private static boolean isWrapperValue(JavaClass type, DcaMarkers markers) {
    if (!type.isAssignableTo(markers.value()) && !type.isAssignableTo(markers.id())) {
      return false;
    }
    return type.getFields().stream()
            .filter(
                f ->
                    !f.getModifiers().contains(JavaModifier.STATIC)
                        && !f.getModifiers().contains(JavaModifier.SYNTHETIC))
            .count()
        == 1;
  }
```
