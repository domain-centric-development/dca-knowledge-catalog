---
type: Reference
title: "Diagnostic: incoming adapter packages that drive a use case without translating its failures — `TypeInspection.outputTypes`"
tags: [reference]
evidence_for: "/rule/errors/dca-err-006.md#typeinspectionoutputtypes"
---

[Full node and context](/rule/errors/dca-err-006.md#typeinspectionoutputtypes). This is an evidence excerpt; retain the parent selection and caveats.

### `TypeInspection.outputTypes`

```java
/**
   * The types an operation may answer with: the raw return types of every public instance method
   * the type declares or inherits, and every type a type argument of an interface assignable to the
   * input-port role involves ({@code UseCase<PlaceOrderCommand, PlaceOrderResult>} yields both —
   * the caller filters). An erased {@code Object} or {@code void} is left out.
   */
  static Set<JavaClass> outputTypes(JavaClass type, DescribedPredicate<JavaClass> inputPortRole) {
    Set<JavaClass> outputs = new LinkedHashSet<>();
    for (JavaMethod method : type.getMethods()) {
      Set<JavaModifier> modifiers = method.getModifiers();
      if (modifiers.contains(JavaModifier.PUBLIC)
          && !modifiers.contains(JavaModifier.STATIC)
          && !modifiers.contains(JavaModifier.BRIDGE)
          && !modifiers.contains(JavaModifier.SYNTHETIC)) {
        outputs.add(method.getRawReturnType());
      }
    }
    Set<JavaClass> inputs = new LinkedHashSet<>();
    collectInputs(type, inputPortRole, inputs, new HashSet<>());
    outputs.addAll(inputs);
    outputs.removeIf(output -> output.getName().equals(OBJECT) || output.getName().equals("void"));
    return outputs;
  }
```
