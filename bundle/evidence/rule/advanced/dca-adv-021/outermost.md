---
type: Reference
title: "Domain services are used only by the application and by other domain services — `outermost`"
tags: [reference]
evidence_for: "/rule/advanced/dca-adv-021.md#outermost"
---

[Full node and context](/rule/advanced/dca-adv-021.md#outermost). This is an evidence excerpt; retain the parent selection and caveats.

### `outermost`

```java
/** The top-level class a nested, local or anonymous class is declared in. */
  private static JavaClass outermost(JavaClass type) {
    JavaClass current = type;
    while (current.getEnclosingClass().isPresent()) {
      current = current.getEnclosingClass().get();
    }
    return current;
  }
```
