---
type: Reference
title: "Anti-Corruption Layer: upstream contract types must stay inside the matching adapter — `CollectedViolations.add`"
tags: [reference]
evidence_for: "/rule/contextmap/dca-map-008.md#collectedviolationsadd"
---

[Full node and context](/rule/contextmap/dca-map-008.md#collectedviolationsadd). This is an evidence excerpt; retain the parent selection and caveats.

### `CollectedViolations.add`

```java
/** Records one violation. */
  void add(String violation) {
    violations.add(Objects.requireNonNull(violation, "violation"));
  }
```
