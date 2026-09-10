---
type: Reference
title: "Use cases that save an aggregate or publish domain events must have a transaction boundary — `IntraClassCalls.closure`"
tags: [reference]
evidence_for: "/rule/usecase/dca-use-012.md#intraclasscallsclosure"
---

[Full node and context](/rule/usecase/dca-use-012.md#intraclasscallsclosure). This is an evidence excerpt; retain the parent selection and caveats.

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

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allApplicationPatterns()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
