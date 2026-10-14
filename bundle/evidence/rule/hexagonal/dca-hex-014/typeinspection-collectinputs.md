---
type: Reference
title: "GET handlers must not drive an input port that takes a command — `TypeInspection.collectInputs`"
tags: [reference]
evidence_for: "/rule/hexagonal/dca-hex-014.md#typeinspectioncollectinputs"
---

[Full node and context](/rule/hexagonal/dca-hex-014.md#typeinspectioncollectinputs). This is an evidence excerpt; retain the parent selection and caveats.

### `TypeInspection.collectInputs`

```java
private static void collectInputs(
    JavaClass type, String inputPortRole, Set<JavaClass> inputs, Set<JavaClass> visited) {
  if (!visited.add(type)) {
    return;
  }
  for (JavaMethod method : type.getMethods()) {
    Set<JavaModifier> modifiers = method.getModifiers();
    if (modifiers.contains(JavaModifier.PUBLIC)
        && !modifiers.contains(JavaModifier.STATIC)
        && !modifiers.contains(JavaModifier.BRIDGE)
        && !modifiers.contains(JavaModifier.SYNTHETIC)) {
      inputs.addAll(method.getRawParameterTypes());
    }
  }
  for (JavaType candidate : type.getInterfaces()) {
    JavaClass erasure = candidate.toErasure();
    if (!erasure.isAssignableTo(inputPortRole)) {
      continue;
    }
    if (candidate instanceof JavaParameterizedType parameterized) {
      for (JavaType argument : parameterized.getActualTypeArguments()) {
        inputs.addAll(involvedTypes(argument));
      }
    }
    collectInputs(erasure, inputPortRole, inputs, visited);
  }
  type.getRawSuperclass()
      .filter(superclass -> superclass.isAssignableTo(inputPortRole))
      .ifPresent(superclass -> collectInputs(superclass, inputPortRole, inputs, visited));
}
```
