---
type: Reference
title: "Query use cases must not write or publish — `sideEffectOf`"
tags: [reference]
evidence_for: "/rule/usecase/dca-use-019.md#sideeffectof"
---

[Full node and context](/rule/usecase/dca-use-019.md#sideeffectof). This is an evidence excerpt; retain the parent selection and caveats.

### `sideEffectOf`

```java
/** The side effect a call has, worded for the violation, or {@code null} for a read. */
  private static String sideEffectOf(
      JavaClass owner,
      com.tngtech.archunit.core.domain.AccessTarget.MethodCallTarget target,
      DcaMarkers markers) {
    if (owner.isAssignableTo(markers.domainEventPublisher())
        || owner.isAssignableTo(markers.integrationEventPublisher())) {
      return "publishes";
    }
    boolean repository = owner.isAssignableTo(markers.repository());
    if (!repository && !owner.isAssignableTo(markers.store())) {
      return null;
    }
    boolean writes = WRITE_VERB.matcher(target.getName()).matches();
    return writes ? (repository ? "writes through a repository" : "writes to a store") : null;
  }
```
