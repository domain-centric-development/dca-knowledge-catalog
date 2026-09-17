---
type: Reference
title: "Anti-Corruption Layer: upstream contract types must stay inside the matching adapter — `CollectedViolations.withoutHeader`"
tags: [reference]
evidence_for: "/rule/contextmap/dca-map-008.md#collectedviolationswithoutheader"
---

[Full node and context](/rule/contextmap/dca-map-008.md#collectedviolationswithoutheader). This is an evidence excerpt; retain the parent selection and caveats.

### `CollectedViolations.withoutHeader`

```java
/** A collector whose report is the bare list of violations. */
  static CollectedViolations withoutHeader() {
    return new CollectedViolations("");
  }
```
