---
type: Reference
title: "Every allowed dependency of a module declaration must be backed by an actual code dependency — `CollectedViolations.withoutHeader`"
tags: [reference]
evidence_for: "/rule/contextmap/dca-map-014.md#collectedviolationswithoutheader"
---

[Full node and context](/rule/contextmap/dca-map-014.md#collectedviolationswithoutheader). This is an evidence excerpt; retain the parent selection and caveats.

### `CollectedViolations.withoutHeader`

```java
/** A collector whose report is the bare list of violations. */
  static CollectedViolations withoutHeader() {
    return new CollectedViolations("");
  }
```
