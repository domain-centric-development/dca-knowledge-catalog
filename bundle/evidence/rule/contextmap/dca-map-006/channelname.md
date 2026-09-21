---
type: Reference
title: "Upstream declarations and the module declaration's allowed dependencies must agree — `channelName`"
tags: [reference]
evidence_for: "/rule/contextmap/dca-map-006.md#channelname"
---

[Full node and context](/rule/contextmap/dca-map-006.md#channelname). This is an evidence excerpt; retain the parent selection and caveats.

### `channelName`

```java
private static String channelName(DcaArchitecture arch, Upstream.Consumes channel) {
  return arch.layout().channelSubpackage(channel);
}
```
