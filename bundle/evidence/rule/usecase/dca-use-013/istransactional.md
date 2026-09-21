---
type: Reference
title: "Declaratively transactional use cases must not call remote-capable output ports — `isTransactional`"
tags: [reference]
evidence_for: "/rule/usecase/dca-use-013.md#istransactional"
---

[Full node and context](/rule/usecase/dca-use-013.md#istransactional). This is an evidence excerpt; retain the parent selection and caveats.

### `isTransactional`

```java
/**
   * Whether the unit may run inside declared transaction metadata: the class is annotated, the unit
   * is, or a unit that reaches it through calls within the class is. Used where one covered path is
   * enough to matter (a remote call inside a transaction).
   */
  private static boolean isTransactional(
      JavaClass item, JavaCodeUnit unit, IntraClassCalls calls, List<String> transactional) {
    return AnnotationRoles.isMetaAnnotatedWithAny(item, transactional)
        || calls.callersOf(unit).stream()
            .anyMatch(u -> AnnotationRoles.isMetaAnnotatedWithAny(u, transactional));
  }
```
