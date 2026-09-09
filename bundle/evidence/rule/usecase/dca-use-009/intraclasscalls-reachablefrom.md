---
type: Reference
title: "Use cases that save an aggregate must publish its domain events — `IntraClassCalls.reachableFrom`"
tags: [reference]
evidence_for: "/rule/usecase/dca-use-009.md#intraclasscallsreachablefrom"
---

[Full node and context](/rule/usecase/dca-use-009.md#intraclasscallsreachablefrom). This is an evidence excerpt; retain the parent selection and caveats.

### `IntraClassCalls.reachableFrom`

```java
/** The unit itself and every unit it reaches through calls within the class. */
  Set<JavaCodeUnit> reachableFrom(JavaCodeUnit unit) {
    return closure(unit, callees);
  }
```
