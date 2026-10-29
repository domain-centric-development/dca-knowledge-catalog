---
type: Reference
title: "GET handlers must not drive an input port that takes a command — `TypeInspection.takesInput`"
tags: [reference]
evidence_for: "/rule/hexagonal/dca-hex-014.md#typeinspectiontakesinput"
---

[Full node and context](/rule/hexagonal/dca-hex-014.md#typeinspectiontakesinput). This is an evidence excerpt; retain the parent selection and caveats.

### `TypeInspection.takesInput`

```java
/**
   * Whether one of the operation's input types is of the given role — a command or a query, as the
   * layout's markers recognise them.
   */
  static boolean takesInput(
      JavaClass type,
      DescribedPredicate<JavaClass> inputPortRole,
      DescribedPredicate<JavaClass> input) {
    return inputTypes(type, inputPortRole).stream().anyMatch(input);
  }
```
