---
type: Reference
title: "Use cases that save an aggregate must publish its domain events — `EventFreeAggregate.repository`"
tags: [reference]
evidence_for: "/rule/usecase/dca-use-009.md#eventfreeaggregaterepository"
---

[Full node and context](/rule/usecase/dca-use-009.md#eventfreeaggregaterepository). This is an evidence excerpt; retain the parent selection and caveats.

### `EventFreeAggregate.repository`

```java
static boolean repository(JavaClass repository, DcaArchitecture arch) {
  Type aggregate;
  try {
    aggregate = aggregate(repository.reflect(), Map.of());
  } catch (LinkageError | RuntimeException failure) {
    return false;
  }
  if (!(aggregate instanceof Class<?> concrete) || concrete.isInterface()) return false;
  Map<String, JavaClass> scanned = new HashMap<>();
  arch.classes().forEach(c -> scanned.put(c.getName(), c));
  JavaClass current = scanned.get(concrete.getName());
  if (current == null) return false;
  while (current != null && !platform(current.getName())) {
    if (!scanned.containsKey(current.getName())
        || !noRegistration(current, scanned, new HashSet<>())) return false;
    current = current.getRawSuperclass().orElse(null);
  }
  return true;
}
```
