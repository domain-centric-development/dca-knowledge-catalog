---
type: Reference
title: "Anti-Corruption Layer: upstream contract types must stay inside the matching adapter — `channelName`"
tags: [reference]
evidence_for: "/rule/contextmap/dca-map-008.md#channelname"
---

[Full node and context](/rule/contextmap/dca-map-008.md#channelname). This is an evidence excerpt; retain the parent selection and caveats.

### `channelName`

```java
private static String channelName(DcaArchitecture arch, Upstream.Consumes channel) {
  return arch.layout().channelSubpackage(channel);
}
```
