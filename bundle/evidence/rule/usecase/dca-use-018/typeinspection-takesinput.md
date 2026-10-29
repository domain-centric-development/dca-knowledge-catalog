---
type: Reference
title: "In a module grouped by feature, incoming adapters must drive the commands of one feature only — `TypeInspection.takesInput`"
tags: [reference]
evidence_for: "/rule/usecase/dca-use-018.md#typeinspectiontakesinput"
---

[Full node and context](/rule/usecase/dca-use-018.md#typeinspectiontakesinput). This is an evidence excerpt; retain the parent selection and caveats.

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
