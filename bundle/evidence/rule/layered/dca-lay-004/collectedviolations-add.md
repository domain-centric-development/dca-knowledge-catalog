---
type: Reference
title: "Transaction boundaries belong to the application layer — `CollectedViolations.add`"
tags: [reference]
evidence_for: "/rule/layered/dca-lay-004.md#collectedviolationsadd"
---

[Full node and context](/rule/layered/dca-lay-004.md#collectedviolationsadd). This is an evidence excerpt; retain the parent selection and caveats.

### `CollectedViolations.add`

```java
/** Records one violation. */
  void add(String violation) {
    violations.add(Objects.requireNonNull(violation, "violation"));
  }
```
