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
    if (!markers.is("value").test(type) && !markers.is("id").test(type)) {
      return false;
    }
    return instanceFieldCount(type) == 1;
  }
```
