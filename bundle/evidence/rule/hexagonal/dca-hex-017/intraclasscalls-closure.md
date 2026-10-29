---
type: Reference
title: "Event listeners that drive an input port must run after the commit in their own transaction — `IntraClassCalls.closure`"
tags: [reference]
evidence_for: "/rule/hexagonal/dca-hex-017.md#intraclasscallsclosure"
---

[Full node and context](/rule/hexagonal/dca-hex-017.md#intraclasscallsclosure). This is an evidence excerpt; retain the parent selection and caveats.

### `IntraClassCalls.closure`

```java
private static Set<JavaCodeUnit> closure(
    JavaCodeUnit start, Map<JavaCodeUnit, Set<JavaCodeUnit>> edges) {
  Set<JavaCodeUnit> reached = new LinkedHashSet<>();
  Deque<JavaCodeUnit> pending = new ArrayDeque<>();
  pending.add(start);
  while (!pending.isEmpty()) {
    JavaCodeUnit current = pending.remove();
    if (reached.add(current)) {
      pending.addAll(edges.getOrDefault(current, Set.of()));
    }
  }
  return reached;
}
```
