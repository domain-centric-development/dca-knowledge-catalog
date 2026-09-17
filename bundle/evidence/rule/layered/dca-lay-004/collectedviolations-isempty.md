---
type: Reference
title: "Transaction boundaries belong to the application layer — `CollectedViolations.isEmpty`"
tags: [reference]
evidence_for: "/rule/layered/dca-lay-004.md#collectedviolationsisempty"
---

[Full node and context](/rule/layered/dca-lay-004.md#collectedviolationsisempty). This is an evidence excerpt; retain the parent selection and caveats.

### `CollectedViolations.isEmpty`

```java
boolean isEmpty() {
  return violations.isEmpty();
}
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allApplicationPatterns()`, `classes()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
