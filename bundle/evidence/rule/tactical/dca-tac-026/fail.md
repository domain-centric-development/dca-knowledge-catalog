---
type: Reference
title: "The repository of an owned aggregate declares a lookup by the aggregate's id and the owner's id — `fail`"
tags: [reference]
evidence_for: "/rule/tactical/dca-tac-026.md#fail"
---

[Full node and context](/rule/tactical/dca-tac-026.md#fail). This is an evidence excerpt; retain the parent selection and caveats.

### `fail`

```java
private static void fail(String message, List<String> violations) {
  if (!violations.isEmpty()) {
    throw new DcaRuleViolation(message, violations);
  }
}
```
