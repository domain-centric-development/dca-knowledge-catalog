---
type: Reference
title: "Use cases that publish domain events must have a transaction boundary — `pathIsTransactional`"
tags: [reference]
evidence_for: "/rule/usecase/dca-use-012.md#pathistransactional"
---

[Full node and context](/rule/usecase/dca-use-012.md#pathistransactional). This is an evidence excerpt; retain the parent selection and caveats.

### `pathIsTransactional`

```java
/**
   * Whether every route from {@code entry} down to {@code publisher} is covered: the class is
   * annotated, or no route reaches the publisher through units none of which carries the annotation
   * or draws an explicit boundary. A boundary on one route does not cover another route to the same
   * publisher.
   */
  private static boolean pathIsTransactional(
      JavaClass item,
      JavaCodeUnit entry,
      JavaCodeUnit publisher,
      IntraClassCalls calls,
      List<String> transactional) {
    if (AnnotationRoles.isMetaAnnotatedWithAny(item, transactional)) {
      return true;
    }
    Predicate<JavaCodeUnit> uncovered =
        unit ->
            !AnnotationRoles.isMetaAnnotatedWithAny(unit, transactional) && !callsBoundary(unit);
    return !calls.reachableThrough(entry, uncovered).contains(publisher);
  }
```
