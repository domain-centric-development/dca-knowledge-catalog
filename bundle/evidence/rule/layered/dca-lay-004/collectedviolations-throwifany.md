---
type: Reference
title: "Transaction boundaries belong to the application layer — `CollectedViolations.throwIfAny`"
tags: [reference]
evidence_for: "/rule/layered/dca-lay-004.md#collectedviolationsthrowifany"
---

[Full node and context](/rule/layered/dca-lay-004.md#collectedviolationsthrowifany). This is an evidence excerpt; retain the parent selection and caveats.

### `CollectedViolations.throwIfAny`

```java
/**
   * Throws the collected violations as one {@link DcaRuleViolation}; nothing when there are none.
   */
  void throwIfAny() {
    if (!violations.isEmpty()) {
      throw new DcaRuleViolation(header, violations);
    }
  }
```
