---
type: Reference
title: "Query use cases must not write or publish — `TypeInspection.takesInputEndingWith`"
tags: [reference]
evidence_for: "/rule/usecase/dca-use-019.md#typeinspectiontakesinputendingwith"
---

[Full node and context](/rule/usecase/dca-use-019.md#typeinspectiontakesinputendingwith). This is an evidence excerpt; retain the parent selection and caveats.

### `TypeInspection.takesInputEndingWith`

```java
/** Whether one of the operation's input types has a simple name ending with the suffix. */
  static boolean takesInputEndingWith(JavaClass type, String inputPortRole, String suffix) {
    return inputTypes(type, inputPortRole).stream()
        .anyMatch(input -> input.getSimpleName().endsWith(suffix));
  }
```
