---
type: Reference
title: "A domain exception is constructed only in the domain layer — `CollectedViolations.withoutHeader`"
tags: [reference]
evidence_for: "/rule/errors/dca-err-009.md#collectedviolationswithoutheader"
---

[Full node and context](/rule/errors/dca-err-009.md#collectedviolationswithoutheader). This is an evidence excerpt; retain the parent selection and caveats.

### `CollectedViolations.withoutHeader`

```java
/** A collector whose report is the bare list of violations. */
  static CollectedViolations withoutHeader() {
    return new CollectedViolations("");
  }
```
