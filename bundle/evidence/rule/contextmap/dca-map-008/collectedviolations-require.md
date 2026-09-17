---
type: Reference
title: "Anti-Corruption Layer: upstream contract types must stay inside the matching adapter — `CollectedViolations.require`"
tags: [reference]
evidence_for: "/rule/contextmap/dca-map-008.md#collectedviolationsrequire"
---

[Full node and context](/rule/contextmap/dca-map-008.md#collectedviolationsrequire). This is an evidence excerpt; retain the parent selection and caveats.

### `CollectedViolations.require`

```java
/** Records the violation unless the condition holds. */
  void require(boolean condition, String violation) {
    if (!condition) {
      add(violation);
    }
  }
```
