---
type: Reference
title: "Upstream declarations and the module declaration's allowed dependencies must agree — `CollectedViolations.withoutHeader`"
tags: [reference]
evidence_for: "/rule/contextmap/dca-map-006.md#collectedviolationswithoutheader"
---

[Full node and context](/rule/contextmap/dca-map-006.md#collectedviolationswithoutheader). This is an evidence excerpt; retain the parent selection and caveats.

### `CollectedViolations.withoutHeader`

```java
/** A collector whose report is the bare list of violations. */
  static CollectedViolations withoutHeader() {
    return new CollectedViolations("");
  }
```
