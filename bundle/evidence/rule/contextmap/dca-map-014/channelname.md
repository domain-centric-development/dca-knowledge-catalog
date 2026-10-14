---
type: Reference
title: "Every allowed dependency of a module declaration must be backed by an actual code dependency — `channelName`"
tags: [reference]
evidence_for: "/rule/contextmap/dca-map-014.md#channelname"
---

[Full node and context](/rule/contextmap/dca-map-014.md#channelname). This is an evidence excerpt; retain the parent selection and caveats.

### `channelName`

```java
private static String channelName(DcaArchitecture arch, Upstream.Consumes channel) {
  return arch.layout().channelSubpackage(channel);
}
```
