---
type: Reference
title: "Domain types must not hold bare primitives, strings or time types; a boolean only as a field or a predicate — `isBoolean`"
tags: [reference]
evidence_for: "/rule/tactical/dca-tac-025.md#isboolean"
---

[Full node and context](/rule/tactical/dca-tac-025.md#isboolean). This is an evidence excerpt; retain the parent selection and caveats.

### `isBoolean`

```java
/** A boolean or its box: a yes/no fact as a field, a predicate as a return type. */
  private static boolean isBoolean(JavaClass type) {
    return type.getName().equals("boolean") || type.getName().equals("java.lang.Boolean");
  }
```
