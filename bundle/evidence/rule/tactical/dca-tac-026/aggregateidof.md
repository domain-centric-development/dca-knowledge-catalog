---
type: Reference
title: "The repository of an owned aggregate declares a lookup by the aggregate's id and the owner's id — `aggregateIdOf`"
tags: [reference]
evidence_for: "/rule/tactical/dca-tac-026.md#aggregateidof"
---

[Full node and context](/rule/tactical/dca-tac-026.md#aggregateidof). This is an evidence excerpt; retain the parent selection and caveats.

### `aggregateIdOf`

```java
/**
   * The aggregate's id type: the second argument of the repository's binding, else the return type
   * of the aggregate's own id().
   */
  private static Optional<JavaClass> aggregateIdOf(
      JavaClass aggregate, JavaClass repository, DcaMarkers markers) {
    Optional<JavaType> bound = TypeInspection.typeArgument(repository, markers.repository(), 1);
    if (bound.isPresent() && !(bound.get() instanceof JavaTypeVariable)) {
      return Optional.of(bound.get().toErasure());
    }
    return aggregate.getAllMethods().stream()
        .filter(m -> m.getName().equals("id") && m.getRawParameterTypes().isEmpty())
        .map(JavaMethod::getRawReturnType)
        .filter(type -> markers.is("id").test(type))
        .filter(type -> !type.getName().equals(markers.id()))
        .findFirst();
  }
```
