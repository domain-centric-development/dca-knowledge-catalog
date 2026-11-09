---
type: Reference
title: "Domain types must not hold bare primitives, strings or time types; a boolean only as a field or a predicate — `normalisedConstant`"
tags: [reference]
evidence_for: "/rule/tactical/dca-tac-025.md#normalisedconstant"
---

[Full node and context](/rule/tactical/dca-tac-025.md#normalisedconstant). This is an evidence excerpt; retain the parent selection and caveats.

### `normalisedConstant`

```java
private static String normalisedConstant(String name) {
  return name.replace("_", "").toLowerCase(java.util.Locale.ROOT);
}
```
