---
type: Reference
title: "Repositories must only exist for Aggregate Roots — `fail`"
tags: [reference]
evidence_for: "/rule/tactical/dca-tac-016.md#fail"
---

[Full node and context](/rule/tactical/dca-tac-016.md#fail). This is an evidence excerpt; retain the parent selection and caveats.

### `fail`

```java
private static void fail(String message, List<String> violations) {
  if (!violations.isEmpty()) {
    throw new DcaRuleViolation(message, violations);
  }
}
```
