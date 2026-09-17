---
type: Reference
title: "Anti-Corruption Layer: upstream contract types must stay inside the matching adapter — `CollectedViolations.isEmpty`"
tags: [reference]
evidence_for: "/rule/contextmap/dca-map-008.md#collectedviolationsisempty"
---

[Full node and context](/rule/contextmap/dca-map-008.md#collectedviolationsisempty). This is an evidence excerpt; retain the parent selection and caveats.

### `CollectedViolations.isEmpty`

```java
boolean isEmpty() {
  return violations.isEmpty();
}
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `boundedContextPackages()`, `classes()`, `contextName()`, `layout()`, `packageAnnotations()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
