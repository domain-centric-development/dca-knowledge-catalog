---
type: Reference
title: "A domain exception is constructed only in the domain layer — `CollectedViolations.withHeader`"
tags: [reference]
evidence_for: "/rule/errors/dca-err-009.md#collectedviolationswithheader"
---

[Full node and context](/rule/errors/dca-err-009.md#collectedviolationswithheader). This is an evidence excerpt; retain the parent selection and caveats.

### `CollectedViolations.withHeader`

```java
/** A collector whose report starts with the given statement of what the rule demands. */
  static CollectedViolations withHeader(String header) {
    return new CollectedViolations(header);
  }
```
