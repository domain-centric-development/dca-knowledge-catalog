---
type: Reference
title: "Every allowed dependency of a module declaration must be backed by an actual code dependency — `CollectedViolations.require`"
tags: [reference]
evidence_for: "/rule/contextmap/dca-map-014.md#collectedviolationsrequire"
---

[Full node and context](/rule/contextmap/dca-map-014.md#collectedviolationsrequire). This is an evidence excerpt; retain the parent selection and caveats.

### `CollectedViolations.require`

```java
/** Records the violation unless the condition holds. */
  void require(boolean condition, String violation) {
    if (!condition) {
      add(violation);
    }
  }
```
