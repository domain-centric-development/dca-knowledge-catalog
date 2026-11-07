---
type: Reference
title: "A domain exception is constructed only in the domain layer — `CollectedViolations.isEmpty`"
tags: [reference]
evidence_for: "/rule/errors/dca-err-009.md#collectedviolationsisempty"
---

[Full node and context](/rule/errors/dca-err-009.md#collectedviolationsisempty). This is an evidence excerpt; retain the parent selection and caveats.

### `CollectedViolations.isEmpty`

```java
boolean isEmpty() {
  return violations.isEmpty();
}
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `classes()`, `inDomain()`, `layout()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
