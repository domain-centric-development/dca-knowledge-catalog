---
type: Reference
title: "Anti-Corruption Layer: upstream contract types must stay inside the matching adapter — `packagesByName`"
tags: [reference]
evidence_for: "/rule/contextmap/dca-map-008.md#packagesbyname"
---

[Full node and context](/rule/contextmap/dca-map-008.md#packagesbyname). This is an evidence excerpt; retain the parent selection and caveats.

### `packagesByName`

```java
private static Map<String, String> packagesByName(DcaArchitecture arch) {
  Map<String, String> byName = new LinkedHashMap<>();
  arch.boundedContextPackages().forEach(p -> byName.put(arch.contextName(p), p));
  return byName;
}
```
