---
type: Reference
title: "Repositories must only exist for Aggregate Roots — `boundAggregateArgument`"
tags: [reference]
evidence_for: "/rule/tactical/dca-tac-016.md#boundaggregateargument"
---

[Full node and context](/rule/tactical/dca-tac-016.md#boundaggregateargument). This is an evidence excerpt; retain the parent selection and caveats.

### `boundAggregateArgument`

```java
/**
   * The aggregate type a repository interface binds: the first type argument of the parameterised
   * repository marker it extends, or of an intermediate port that is itself assignable to the
   * marker. Empty when the marker is not generic, when it is used raw, or when the binding only
   * becomes concrete further up a chain that substitutes type parameters - the rule then falls back
   * to resolving the aggregate by name.
   */
  private static Optional<JavaType> boundAggregateArgument(JavaClass type, String markerName) {
    for (JavaType candidate : type.getInterfaces()) {
      JavaClass erasure = candidate.toErasure();
      boolean isMarker = erasure.getName().equals(markerName) || erasure.isAssignableTo(markerName);
      if (isMarker
          && candidate instanceof JavaParameterizedType parameterized
          && !parameterized.getActualTypeArguments().isEmpty()) {
        return Optional.of(parameterized.getActualTypeArguments().get(0));
      }
    }
    return Optional.empty();
  }
```
