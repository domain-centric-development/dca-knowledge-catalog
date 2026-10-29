---
type: Reference
title: "Domain types must not hold bare primitives, strings or time types — `implementsBuildingBlock`"
tags: [reference]
evidence_for: "/rule/tactical/dca-tac-025.md#implementsbuildingblock"
---

[Full node and context](/rule/tactical/dca-tac-025.md#implementsbuildingblock). This is an evidence excerpt; retain the parent selection and caveats.

### `implementsBuildingBlock`

```java
/** Whether a building block the type implements declares a method of this name and arity. */
  private static boolean implementsBuildingBlock(
      JavaClass type, JavaMethod method, Set<String> buildingBlocks) {
    List<JavaClass> supertypes = new ArrayList<>(type.getAllRawInterfaces());
    supertypes.addAll(type.getAllRawSuperclasses());
    return supertypes.stream()
        .filter(s -> buildingBlocks.contains(s.getName()))
        .flatMap(s -> s.getMethods().stream())
        .anyMatch(
            m ->
                m.getName().equals(method.getName())
                    && m.getRawParameterTypes().size() == method.getRawParameterTypes().size());
  }
```
