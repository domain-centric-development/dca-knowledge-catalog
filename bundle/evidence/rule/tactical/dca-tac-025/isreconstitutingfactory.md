---
type: Reference
title: "Domain types must not hold bare primitives, strings or time types; a boolean only as a field or a predicate — `isReconstitutingFactory`"
tags: [reference]
evidence_for: "/rule/tactical/dca-tac-025.md#isreconstitutingfactory"
---

[Full node and context](/rule/tactical/dca-tac-025.md#isreconstitutingfactory). This is an evidence excerpt; retain the parent selection and caveats.

### `isReconstitutingFactory`

```java
/**
   * The factory that rebuilds a stored object: static, returning the type that declares it, named
   * as the layout configures ({@code reconstitute}, {@code restore} by default), case ignored.
   */
  private static boolean isReconstitutingFactory(
      JavaClass type, JavaMethod method, Set<String> names) {
    return method.getModifiers().contains(JavaModifier.STATIC)
        && method.getRawReturnType().equals(type)
        && names.contains(method.getName().toLowerCase(java.util.Locale.ROOT));
  }
```
