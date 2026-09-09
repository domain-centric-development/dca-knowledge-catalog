---
type: Reference
title: "Use cases that save an aggregate must publish its domain events — `IntraClassCalls.entryPointsOf`"
tags: [reference]
evidence_for: "/rule/usecase/dca-use-009.md#intraclasscallsentrypointsof"
---

[Full node and context](/rule/usecase/dca-use-009.md#intraclasscallsentrypointsof). This is an evidence excerpt; retain the parent selection and caveats.

### `IntraClassCalls.entryPointsOf`

```java
/**
   * The paths a unit can be entered on: those of its (transitive) callers - the unit itself
   * included - that are entry points. A unit is an entry point when it can be called from outside
   * the class (any code unit that is not private, synthetic or a bridge - a public method stays an
   * entry point even when another method of the class also calls it) or when no unit of the class
   * calls it. When the unit is reached only from within a cycle of private helpers, so that no
   * caller qualifies, the unit itself is taken as the entry point.
   */
  Set<JavaCodeUnit> entryPointsOf(JavaCodeUnit unit) {
    Set<JavaCodeUnit> roots = new LinkedHashSet<>();
    for (JavaCodeUnit caller : callersOf(unit)) {
      if (isEntryPoint(caller)) {
        roots.add(caller);
      }
    }
    if (roots.isEmpty()) {
      roots.add(unit);
    }
    return roots;
  }
```
