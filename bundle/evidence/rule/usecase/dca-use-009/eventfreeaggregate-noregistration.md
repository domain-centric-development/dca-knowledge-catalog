---
type: Reference
title: "Use cases that save an aggregate must publish its domain events — `EventFreeAggregate.noRegistration`"
tags: [reference]
evidence_for: "/rule/usecase/dca-use-009.md#eventfreeaggregatenoregistration"
---

[Full node and context](/rule/usecase/dca-use-009.md#eventfreeaggregatenoregistration). This is an evidence excerpt; retain the parent selection and caveats.

### `EventFreeAggregate.noRegistration`

```java
private static boolean noRegistration(
    JavaClass type, Map<String, JavaClass> scanned, Set<String> visited, DcaMarkers markers) {
  if (!visited.add(type.getName())) return true;
  for (var unit : type.getCodeUnits())
    for (var call : unit.getCallsFromSelf()) {
      var owner = call.getTargetOwner();
      if (call.getTarget().getName().equals("registerEvent")
          && owner.isAssignableTo(markers.aggregateRoot())) return false;
      if (platform(owner.getName(), markers)) continue;
      var target = scanned.get(owner.getName());
      if (target == null || !noRegistration(target, scanned, visited, markers)) return false;
    }
  return true;
}
```
