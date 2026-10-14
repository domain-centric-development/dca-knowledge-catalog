---
type: Reference
title: "Every allowed dependency of a module declaration must be backed by an actual code dependency — `plannedEdges`"
tags: [reference]
evidence_for: "/rule/contextmap/dca-map-014.md#plannededges"
---

[Full node and context](/rule/contextmap/dca-map-014.md#plannededges). This is an evidence excerpt; retain the parent selection and caveats.

### `plannedEdges`

```java
/** The edges 'context :: channel' of the context's PLANNED @Upstream declarations. */
  private static Set<String> plannedEdges(DcaArchitecture arch, String contextPackage) {
    Set<String> edges = new LinkedHashSet<>();
    for (Upstream u : arch.packageAnnotations(contextPackage, Upstream.class)) {
      if (u.status() != Upstream.Status.PLANNED) {
        continue;
      }
      for (Upstream.Consumes channel : u.via()) {
        edges.add(u.context() + " :: " + channelName(arch, channel));
      }
    }
    return edges;
  }
```
