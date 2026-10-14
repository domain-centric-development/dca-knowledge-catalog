---
type: Reference
title: "Every allowed dependency of a module declaration must be backed by an actual code dependency — `CollectedViolations.add`"
tags: [reference]
evidence_for: "/rule/contextmap/dca-map-014.md#collectedviolationsadd"
---

[Full node and context](/rule/contextmap/dca-map-014.md#collectedviolationsadd). This is an evidence excerpt; retain the parent selection and caveats.

### `CollectedViolations.add`

```java
/** Records one violation. */
  void add(String violation) {
    violations.add(Objects.requireNonNull(violation, "violation"));
  }
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `boundedContextPackages()`, `classes()`, `contextName()`, `layout()`, `moduleRoots()`, `packageAnnotation()`, `packageAnnotations()`, `sharedKernelPackage()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
