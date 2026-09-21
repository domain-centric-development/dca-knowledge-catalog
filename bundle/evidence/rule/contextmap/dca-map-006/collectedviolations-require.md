---
type: Reference
title: "Upstream declarations and the module declaration's allowed dependencies must agree — `CollectedViolations.require`"
tags: [reference]
evidence_for: "/rule/contextmap/dca-map-006.md#collectedviolationsrequire"
---

[Full node and context](/rule/contextmap/dca-map-006.md#collectedviolationsrequire). This is an evidence excerpt; retain the parent selection and caveats.

### `CollectedViolations.require`

```java
/** Records the violation unless the condition holds. */
  void require(boolean condition, String violation) {
    if (!condition) {
      add(violation);
    }
  }
```
