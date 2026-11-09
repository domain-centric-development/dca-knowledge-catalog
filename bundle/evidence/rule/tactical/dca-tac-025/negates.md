---
type: Reference
title: "Domain types must not hold bare primitives, strings or time types; a boolean only as a field or a predicate — `negates`"
tags: [reference]
evidence_for: "/rule/tactical/dca-tac-025.md#negates"
---

[Full node and context](/rule/tactical/dca-tac-025.md#negates). This is an evidence excerpt; retain the parent selection and caveats.

### `negates`

```java
private static boolean negates(String negated, String fact) {
  return !fact.isEmpty()
      && NEGATING_PREFIXES.stream().anyMatch(prefix -> negated.equals(prefix + fact));
}
```
