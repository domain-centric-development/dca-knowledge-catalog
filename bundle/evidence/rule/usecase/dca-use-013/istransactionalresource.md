---
type: Reference
title: "Declaratively transactional use cases must not call remote-capable output ports — `isTransactionalResource`"
tags: [reference]
evidence_for: "/rule/usecase/dca-use-013.md#istransactionalresource"
---

[Full node and context](/rule/usecase/dca-use-013.md#istransactionalresource). This is an evidence excerpt; retain the parent selection and caveats.

### `isTransactionalResource`

```java
/**
   * Output ports that live inside the transaction; every other output port may leave the process.
   */
  private static boolean isTransactionalResource(JavaClass owner, DcaMarkers markers) {
    return owner.isAssignableTo(markers.repository())
        || owner.isAssignableTo(markers.store())
        || owner.isAssignableTo(markers.domainEventPublisher())
        || owner.isAssignableTo(markers.integrationEventPublisher());
  }
```
