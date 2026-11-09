---
type: Reference
title: "The repository of an owned aggregate declares a lookup by the aggregate's id and the owner's id — `TypeInspection.typeArgument`"
tags: [reference]
evidence_for: "/rule/tactical/dca-tac-026.md#typeinspectiontypeargument"
---

[Full node and context](/rule/tactical/dca-tac-026.md#typeinspectiontypeargument). This is an evidence excerpt; retain the parent selection and caveats.

### `TypeInspection.typeArgument`

```java
/**
   * The type argument at {@code index} that a type binds on the given marker, through its
   * interfaces, the interfaces they extend and its superclasses; a type variable of an intermediate
   * type is substituted by the argument the type binds for it. Empty where the marker is used raw
   * or not at all.
   */
  static Optional<JavaType> typeArgument(JavaClass type, String markerName, int index) {
    List<JavaType> candidates = new ArrayList<>(type.getInterfaces());
    type.getSuperclass().ifPresent(candidates::add);
    for (JavaType candidate : candidates) {
      JavaClass erasure = candidate.toErasure();
      if (erasure.getName().equals(markerName)) {
        if (candidate instanceof JavaParameterizedType parameterized
            && parameterized.getActualTypeArguments().size() > index) {
          return Optional.of(parameterized.getActualTypeArguments().get(index));
        }
        return Optional.empty();
      }
      if (!erasure.isAssignableTo(markerName)) {
        continue;
      }
      Optional<JavaType> inherited = typeArgument(erasure, markerName, index);
      if (inherited.isPresent()
          && inherited.get() instanceof JavaTypeVariable<?> variable
          && candidate instanceof JavaParameterizedType parameterized) {
        List<? extends JavaTypeVariable<?>> parameters = erasure.getTypeParameters();
        for (int i = 0; i < parameters.size(); i++) {
          if (parameters.get(i).getName().equals(variable.getName())
              && parameterized.getActualTypeArguments().size() > i) {
            return Optional.of(parameterized.getActualTypeArguments().get(i));
          }
        }
      }
      if (inherited.isPresent()) {
        return inherited;
      }
    }
    return Optional.empty();
  }
```
