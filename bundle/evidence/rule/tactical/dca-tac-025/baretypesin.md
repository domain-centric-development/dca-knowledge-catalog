---
type: Reference
title: "Domain types must not hold bare primitives, strings or time types — `bareTypesIn`"
tags: [reference]
evidence_for: "/rule/tactical/dca-tac-025.md#baretypesin"
---

[Full node and context](/rule/tactical/dca-tac-025.md#baretypesin). This is an evidence excerpt; retain the parent selection and caveats.

### `bareTypesIn`

```java
/** The bare types a declared type involves, generic arguments included; "" when none. */
  private static String bareTypesIn(JavaType type) {
    return type.getAllInvolvedRawTypes().stream()
        .map(JavaClass::getName)
        .filter(BARE_TYPES::contains)
        .map(name -> name.substring(name.lastIndexOf('.') + 1))
        .distinct()
        .sorted()
        .collect(Collectors.joining(", "));
  }
```
