---
type: Reference
title: "Diagnostic: closed use-case results without a case marked as a refusal — `TypeInspection.collectInputs`"
tags: [reference]
evidence_for: "/rule/errors/dca-err-008.md#typeinspectioncollectinputs"
---

[Full node and context](/rule/errors/dca-err-008.md#typeinspectioncollectinputs). This is an evidence excerpt; retain the parent selection and caveats.

### `TypeInspection.collectInputs`

```java
private static void collectInputs(
    JavaClass type,
    DescribedPredicate<JavaClass> inputPortRole,
    Set<JavaClass> inputs,
    Set<JavaClass> visited) {
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
    if (!inputPortRole.test(erasure)) {
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
      .filter(inputPortRole)
      .ifPresent(superclass -> collectInputs(superclass, inputPortRole, inputs, visited));
}
```
