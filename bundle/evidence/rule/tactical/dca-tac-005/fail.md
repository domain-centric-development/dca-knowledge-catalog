---
type: Reference
title: "Entities must not be instantiated directly from outside the aggregate — `fail`"
tags: [reference]
evidence_for: "/rule/tactical/dca-tac-005.md#fail"
---

[Full node and context](/rule/tactical/dca-tac-005.md#fail). This is an evidence excerpt; retain the parent selection and caveats.

### `fail`

```java
private static void fail(String message, List<String> violations) {
  if (!violations.isEmpty()) {
    throw new DcaRuleViolation(message, violations);
  }
}
```
