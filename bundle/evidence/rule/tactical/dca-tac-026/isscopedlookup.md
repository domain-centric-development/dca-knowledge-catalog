---
type: Reference
title: "The repository of an owned aggregate declares a lookup by the aggregate's id and the owner's id — `isScopedLookup`"
tags: [reference]
evidence_for: "/rule/tactical/dca-tac-026.md#isscopedlookup"
---

[Full node and context](/rule/tactical/dca-tac-026.md#isscopedlookup). This is an evidence excerpt; retain the parent selection and caveats.

### `isScopedLookup`

```java
private static boolean isScopedLookup(
    JavaMethod method,
    JavaClass aggregate,
    JavaClass aggregateId,
    JavaClass ownerId,
    DcaMarkers markers) {
  if (!TypeInspection.involvedTypes(method.getReturnType()).contains(aggregate)) {
    return false;
  }
  List<JavaClass> parameters = new ArrayList<>(method.getRawParameterTypes());
  if (!parameters.remove(ownerId)) {
    return false;
  }
  return parameters.stream()
      .anyMatch(
          type -> aggregateId != null ? type.equals(aggregateId) : markers.is("id").test(type));
}
```
