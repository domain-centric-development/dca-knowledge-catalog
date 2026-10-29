---
type: Reference
title: "GET handlers must not drive an input port that takes a command — `TypeInspection.inputTypes`"
tags: [reference]
evidence_for: "/rule/hexagonal/dca-hex-014.md#typeinspectioninputtypes"
---

[Full node and context](/rule/hexagonal/dca-hex-014.md#typeinspectioninputtypes). This is an evidence excerpt; retain the parent selection and caveats.

### `TypeInspection.inputTypes`

```java
/**
   * The types an operation takes as its input: the raw parameter types of every public instance
   * method the type declares or inherits from an interface assignable to the input-port role, and
   * every type a type argument of such an interface involves ({@code UseCase<PlaceOrderCommand,
   * PlaceOrderResult>} yields both). Called on an input port or on a class implementing one. Bridge
   * and synthetic methods are left out; an erased {@code Object} parameter is left out too.
   */
  static Set<JavaClass> inputTypes(JavaClass type, DescribedPredicate<JavaClass> inputPortRole) {
    Set<JavaClass> inputs = new LinkedHashSet<>();
    collectInputs(type, inputPortRole, inputs, new HashSet<>());
    inputs.removeIf(input -> input.getName().equals(OBJECT));
    return inputs;
  }
```
