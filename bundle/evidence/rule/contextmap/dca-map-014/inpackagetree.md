---
type: Reference
title: "Every allowed dependency of a module declaration must be backed by an actual code dependency — `inPackageTree`"
tags: [reference]
evidence_for: "/rule/contextmap/dca-map-014.md#inpackagetree"
---

[Full node and context](/rule/contextmap/dca-map-014.md#inpackagetree). This is an evidence excerpt; retain the parent selection and caveats.

### `inPackageTree`

```java
private static boolean inPackageTree(String packageName, String root) {
  return DcaArchitecture.inPackageTree(packageName, root);
}
```
