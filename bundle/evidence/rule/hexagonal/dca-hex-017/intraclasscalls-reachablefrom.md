---
type: Reference
title: "Event listeners that drive an input port must run after the commit in their own transaction — `IntraClassCalls.reachableFrom`"
tags: [reference]
evidence_for: "/rule/hexagonal/dca-hex-017.md#intraclasscallsreachablefrom"
---

[Full node and context](/rule/hexagonal/dca-hex-017.md#intraclasscallsreachablefrom). This is an evidence excerpt; retain the parent selection and caveats.

### `IntraClassCalls.reachableFrom`

```java
/** The unit itself and every unit it reaches through calls within the class. */
  Set<JavaCodeUnit> reachableFrom(JavaCodeUnit unit) {
    return closure(unit, callees);
  }
```
