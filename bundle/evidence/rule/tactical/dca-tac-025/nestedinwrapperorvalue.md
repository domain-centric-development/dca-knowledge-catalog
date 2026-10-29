---
type: Reference
title: "Domain types must not hold bare primitives, strings or time types — `nestedInWrapperOrValue`"
tags: [reference]
evidence_for: "/rule/tactical/dca-tac-025.md#nestedinwrapperorvalue"
---

[Full node and context](/rule/tactical/dca-tac-025.md#nestedinwrapperorvalue). This is an evidence excerpt; retain the parent selection and caveats.

### `nestedInWrapperOrValue`

```java
/**
   * A type declared inside a value or an id - the value's own error shapes, which carry the input
   * it refused. "With everything it declares" holds for its nested types too.
   */
  private static boolean nestedInWrapperOrValue(JavaClass type, DcaMarkers markers) {
    for (java.util.Optional<JavaClass> enclosing = type.getEnclosingClass();
        enclosing.isPresent();
        enclosing = enclosing.get().getEnclosingClass()) {
      if (markers.is("value").test(enclosing.get()) || markers.is("id").test(enclosing.get())) {
        return true;
      }
    }
    return false;
  }
```
