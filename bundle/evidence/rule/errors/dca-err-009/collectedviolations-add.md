---
type: Reference
title: "A domain exception is constructed only in the domain layer — `CollectedViolations.add`"
tags: [reference]
evidence_for: "/rule/errors/dca-err-009.md#collectedviolationsadd"
---

[Full node and context](/rule/errors/dca-err-009.md#collectedviolationsadd). This is an evidence excerpt; retain the parent selection and caveats.

### `CollectedViolations.add`

```java
/** Records one violation. */
  void add(String violation) {
    violations.add(Objects.requireNonNull(violation, "violation"));
  }
```
