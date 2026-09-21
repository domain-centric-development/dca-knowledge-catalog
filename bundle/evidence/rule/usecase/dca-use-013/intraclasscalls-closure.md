---
type: Reference
title: "Declaratively transactional use cases must not call remote-capable output ports — `IntraClassCalls.closure`"
tags: [reference]
evidence_for: "/rule/usecase/dca-use-013.md#intraclasscallsclosure"
---

[Full node and context](/rule/usecase/dca-use-013.md#intraclasscallsclosure). This is an evidence excerpt; retain the parent selection and caveats.

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

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allApplicationPatterns()`, `layout()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
