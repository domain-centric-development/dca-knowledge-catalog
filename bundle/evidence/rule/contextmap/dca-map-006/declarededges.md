---
type: Reference
title: "Upstream declarations and the module declaration's allowed dependencies must agree — `declaredEdges`"
tags: [reference]
evidence_for: "/rule/contextmap/dca-map-006.md#declarededges"
---

[Full node and context](/rule/contextmap/dca-map-006.md#declarededges). This is an evidence excerpt; retain the parent selection and caveats.

### `declaredEdges`

```java
/** All declared upstream edges of a context as "target :: channel" strings. */
  private static Set<String> declaredEdges(DcaArchitecture arch, String contextPackage) {
    Set<String> edges = new LinkedHashSet<>();
    for (Upstream u : arch.packageAnnotations(contextPackage, Upstream.class)) {
      for (Upstream.Consumes channel : u.via()) {
        edges.add(u.context() + " :: " + channelName(arch, channel));
      }
    }
    return edges;
  }
```
