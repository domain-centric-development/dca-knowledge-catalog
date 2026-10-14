---
type: Reference
title: "GET handlers must not drive an input port that takes a command — `TypeInspection.takesInputEndingWith`"
tags: [reference]
evidence_for: "/rule/hexagonal/dca-hex-014.md#typeinspectiontakesinputendingwith"
---

[Full node and context](/rule/hexagonal/dca-hex-014.md#typeinspectiontakesinputendingwith). This is an evidence excerpt; retain the parent selection and caveats.

### `TypeInspection.takesInputEndingWith`

```java
/** Whether one of the operation's input types has a simple name ending with the suffix. */
  static boolean takesInputEndingWith(JavaClass type, String inputPortRole, String suffix) {
    return inputTypes(type, inputPortRole).stream()
        .anyMatch(input -> input.getSimpleName().endsWith(suffix));
  }
```
