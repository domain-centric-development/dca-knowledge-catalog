---
type: Reference
title: "Domain types must not hold bare primitives, strings or time types — `isFailure`"
tags: [reference]
evidence_for: "/rule/tactical/dca-tac-025.md#isfailure"
---

[Full node and context](/rule/tactical/dca-tac-025.md#isfailure). This is an evidence excerpt; retain the parent selection and caveats.

### `isFailure`

```java
/** A failure reports what was refused - the raw input included - and is no value itself. */
  private static boolean isFailure(JavaClass type, DcaMarkers markers) {
    return markers.is("domainException").test(type) || markers.is("useCaseException").test(type);
  }
```
