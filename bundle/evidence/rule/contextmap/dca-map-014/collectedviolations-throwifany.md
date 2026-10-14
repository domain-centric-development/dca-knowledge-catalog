---
type: Reference
title: "Every allowed dependency of a module declaration must be backed by an actual code dependency — `CollectedViolations.throwIfAny`"
tags: [reference]
evidence_for: "/rule/contextmap/dca-map-014.md#collectedviolationsthrowifany"
---

[Full node and context](/rule/contextmap/dca-map-014.md#collectedviolationsthrowifany). This is an evidence excerpt; retain the parent selection and caveats.

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
