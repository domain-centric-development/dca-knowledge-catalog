---
type: Reference
title: "The repository of an owned aggregate declares a lookup by the aggregate's id and the owner's id — `ownedAggregateRoots`"
tags: [reference]
evidence_for: "/rule/tactical/dca-tac-026.md#ownedaggregateroots"
---

[Full node and context](/rule/tactical/dca-tac-026.md#ownedaggregateroots). This is an evidence excerpt; retain the parent selection and caveats.

### `ownedAggregateRoots`

```java
private static List<JavaClass> ownedAggregateRoots(DcaArchitecture arch) {
  DcaMarkers markers = arch.layout().markers();
  return classesMatching(
      arch,
      c ->
          markers.is("owned").test(c)
              && markers.is("aggregateRoot").test(c)
              && !c.isInterface()
              && !c.getModifiers().contains(JavaModifier.ABSTRACT));
}
```
