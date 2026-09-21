---
type: Reference
title: "Upstream declarations and the module declaration's allowed dependencies must agree — `moduleNames`"
tags: [reference]
evidence_for: "/rule/contextmap/dca-map-006.md#modulenames"
---

[Full node and context](/rule/contextmap/dca-map-006.md#modulenames). This is an evidence excerpt; retain the parent selection and caveats.

### `moduleNames`

```java
private static Set<String> moduleNames(DcaArchitecture arch) {
  Set<String> names = new LinkedHashSet<>();
  arch.boundedContextPackages().forEach(p -> names.add(arch.contextName(p)));
  return names;
}
```
