---
type: Reference
title: "A domain exception is constructed only in the domain layer — `chainsTo`"
tags: [reference]
evidence_for: "/rule/errors/dca-err-009.md#chainsto"
---

[Full node and context](/rule/errors/dca-err-009.md#chainsto). This is an evidence excerpt; retain the parent selection and caveats.

### `chainsTo`

```java
/** A subclass constructor's call to its parent's constructor, or a {@code this(...)} call. */
  private static boolean chainsTo(JavaCodeUnitAccess<?> construction, JavaClass target) {
    return construction.getOrigin().isConstructor()
        && construction.getOriginOwner().isAssignableTo(target.getName());
  }
```
