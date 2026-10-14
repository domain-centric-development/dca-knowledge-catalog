---
type: Reference
title: "Every allowed dependency of a module declaration must be backed by an actual code dependency — `modulePackagesByName`"
tags: [reference]
evidence_for: "/rule/contextmap/dca-map-014.md#modulepackagesbyname"
---

[Full node and context](/rule/contextmap/dca-map-014.md#modulepackagesbyname). This is an evidence excerpt; retain the parent selection and caveats.

### `modulePackagesByName`

```java
/**
   * Module names as a module declaration spells them: a bounded context by its name, any module
   * root - the shared kernel included - by its last package segment.
   */
  private static Map<String, String> modulePackagesByName(DcaArchitecture arch) {
    Map<String, String> byName = new LinkedHashMap<>();
    for (String root : arch.moduleRoots()) {
      byName.putIfAbsent(lastSegment(root), root);
    }
    arch.sharedKernelPackage().ifPresent(shared -> byName.putIfAbsent(lastSegment(shared), shared));
    arch.boundedContextPackages().forEach(p -> byName.put(arch.contextName(p), p));
    return byName;
  }
```
