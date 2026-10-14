---
type: Reference
title: "GET handlers must not drive an input port that takes a command — `IntraClassCalls.reachableFrom`"
tags: [reference]
evidence_for: "/rule/hexagonal/dca-hex-014.md#intraclasscallsreachablefrom"
---

[Full node and context](/rule/hexagonal/dca-hex-014.md#intraclasscallsreachablefrom). This is an evidence excerpt; retain the parent selection and caveats.

### `IntraClassCalls.reachableFrom`

```java
/** The unit itself and every unit it reaches through calls within the class. */
  Set<JavaCodeUnit> reachableFrom(JavaCodeUnit unit) {
    return closure(unit, callees);
  }
```
