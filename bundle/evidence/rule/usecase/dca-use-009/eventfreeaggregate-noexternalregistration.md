---
type: Reference
title: "Use cases that save an aggregate must publish its domain events — `EventFreeAggregate.noExternalRegistration`"
tags: [reference]
evidence_for: "/rule/usecase/dca-use-009.md#eventfreeaggregatenoexternalregistration"
---

[Full node and context](/rule/usecase/dca-use-009.md#eventfreeaggregatenoexternalregistration). This is an evidence excerpt; retain the parent selection and caveats.

### `EventFreeAggregate.noExternalRegistration`

```java
/**
   * A class outside the aggregate's hierarchy that registers an event on it (a same-package helper
   * reaching the protected method) is invisible from the aggregate's own code units, so every
   * scanned class is inspected: a registration whose target is the aggregate or one of its
   * supertypes disables the exemption.
   */
  private static boolean noExternalRegistration(
      Set<String> hierarchy, Map<String, JavaClass> scanned) {
    for (JavaClass type : scanned.values()) {
      if (hierarchy.contains(type.getName())) continue;
      for (var unit : type.getCodeUnits())
        for (var call : unit.getCallsFromSelf()) {
          var owner = call.getTargetOwner();
          if (call.getTarget().getName().equals("registerEvent")
              && owner.isAssignableTo(AggregateRoot.class)
              && (hierarchy.contains(owner.getName()) || platform(owner.getName()))) return false;
        }
    }
    return true;
  }
```
