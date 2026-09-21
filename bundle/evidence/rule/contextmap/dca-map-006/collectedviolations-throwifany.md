---
type: Reference
title: "Upstream declarations and the module declaration's allowed dependencies must agree — `CollectedViolations.throwIfAny`"
tags: [reference]
evidence_for: "/rule/contextmap/dca-map-006.md#collectedviolationsthrowifany"
---

[Full node and context](/rule/contextmap/dca-map-006.md#collectedviolationsthrowifany). This is an evidence excerpt; retain the parent selection and caveats.

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
