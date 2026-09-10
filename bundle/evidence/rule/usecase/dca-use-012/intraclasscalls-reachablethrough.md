---
type: Reference
title: "Use cases that save an aggregate or publish domain events must have a transaction boundary — `IntraClassCalls.reachableThrough`"
tags: [reference]
evidence_for: "/rule/usecase/dca-use-012.md#intraclasscallsreachablethrough"
---

[Full node and context](/rule/usecase/dca-use-012.md#intraclasscallsreachablethrough). This is an evidence excerpt; retain the parent selection and caveats.

### `IntraClassCalls.reachableThrough`

```java
/**
   * The units reachable from {@code start} on routes that pass only through units satisfying {@code
   * through} - {@code start} included, and only if it satisfies it too. A unit that fails the
   * predicate is not entered, so nothing behind it is reached on that route (it may still be
   * reached on another). Cycle-safe.
   */
  Set<JavaCodeUnit> reachableThrough(JavaCodeUnit start, Predicate<JavaCodeUnit> through) {
    Set<JavaCodeUnit> reached = new LinkedHashSet<>();
    Deque<JavaCodeUnit> pending = new ArrayDeque<>();
    pending.add(start);
    while (!pending.isEmpty()) {
      JavaCodeUnit current = pending.remove();
      if (through.test(current) && reached.add(current)) {
        pending.addAll(callees.getOrDefault(current, Set.of()));
      }
    }
    return reached;
  }
```
