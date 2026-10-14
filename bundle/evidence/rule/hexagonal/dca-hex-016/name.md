---
type: Reference
title: "Diagnostic: adapters that publish an enum by its member name — `name`"
tags: [reference]
evidence_for: "/rule/hexagonal/dca-hex-016.md#name"
---

[Full node and context](/rule/hexagonal/dca-hex-016.md#name). This is an evidence excerpt; retain the parent selection and caveats.

### `name`

```java
public String name() {
  return "hexagonal";
}
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allAdapterPatterns()`, `allApplicationPatterns()`, `allDomainPatterns()`, `classes()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
