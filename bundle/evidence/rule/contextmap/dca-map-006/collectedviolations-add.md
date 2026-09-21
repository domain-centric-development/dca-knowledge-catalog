---
type: Reference
title: "Upstream declarations and the module declaration's allowed dependencies must agree — `CollectedViolations.add`"
tags: [reference]
evidence_for: "/rule/contextmap/dca-map-006.md#collectedviolationsadd"
---

[Full node and context](/rule/contextmap/dca-map-006.md#collectedviolationsadd). This is an evidence excerpt; retain the parent selection and caveats.

### `CollectedViolations.add`

```java
/** Records one violation. */
  void add(String violation) {
    violations.add(Objects.requireNonNull(violation, "violation"));
  }
```
