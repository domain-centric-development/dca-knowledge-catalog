---
type: Reference
title: "Domain types must not hold bare primitives, strings or time types — `buildingBlockTypes`"
tags: [reference]
evidence_for: "/rule/tactical/dca-tac-025.md#buildingblocktypes"
---

[Full node and context](/rule/tactical/dca-tac-025.md#buildingblocktypes). This is an evidence excerpt; retain the parent selection and caveats.

### `buildingBlockTypes`

```java
/** The type names of every building block the layout names. */
  private static Set<String> buildingBlockTypes(DcaMarkers markers) {
    return Set.of(
        markers.aggregateRoot(),
        markers.entity(),
        markers.value(),
        markers.id(),
        markers.domainEvent(),
        markers.integrationEvent(),
        markers.domainService(),
        markers.factory(),
        markers.specification(),
        markers.domainException(),
        markers.outputPort(),
        markers.repository(),
        markers.store());
  }
```
