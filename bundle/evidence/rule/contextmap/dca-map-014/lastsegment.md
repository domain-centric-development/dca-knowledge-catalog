---
type: Reference
title: "Every allowed dependency of a module declaration must be backed by an actual code dependency — `lastSegment`"
tags: [reference]
evidence_for: "/rule/contextmap/dca-map-014.md#lastsegment"
---

[Full node and context](/rule/contextmap/dca-map-014.md#lastsegment). This is an evidence excerpt; retain the parent selection and caveats.

### `lastSegment`

```java
private static String lastSegment(String pkg) {
  return pkg.substring(pkg.lastIndexOf('.') + 1);
}
```
