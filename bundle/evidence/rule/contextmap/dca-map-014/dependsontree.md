---
type: Reference
title: "Every allowed dependency of a module declaration must be backed by an actual code dependency — `dependsOnTree`"
tags: [reference]
evidence_for: "/rule/contextmap/dca-map-014.md#dependsontree"
---

[Full node and context](/rule/contextmap/dca-map-014.md#dependsontree). This is an evidence excerpt; retain the parent selection and caveats.

### `dependsOnTree`

```java
/** Whether a class below {@code source} depends directly on a class below {@code target}. */
  private static boolean dependsOnTree(DcaArchitecture arch, String source, String target) {
    for (JavaClass javaClass : arch.classes()) {
      if (!inPackageTree(javaClass.getPackageName(), source)) {
        continue;
      }
      for (Dependency dep : javaClass.getDirectDependenciesFromSelf()) {
        if (inPackageTree(dep.getTargetClass().getPackageName(), target)) {
          return true;
        }
      }
    }
    return false;
  }
```
