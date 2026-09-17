---
type: Reference
title: "Transaction boundaries belong to the application layer — `CollectedViolations.withoutHeader`"
tags: [reference]
evidence_for: "/rule/layered/dca-lay-004.md#collectedviolationswithoutheader"
---

[Full node and context](/rule/layered/dca-lay-004.md#collectedviolationswithoutheader). This is an evidence excerpt; retain the parent selection and caveats.

### `CollectedViolations.withoutHeader`

```java
/** A collector whose report is the bare list of violations. */
  static CollectedViolations withoutHeader() {
    return new CollectedViolations("");
  }
```
