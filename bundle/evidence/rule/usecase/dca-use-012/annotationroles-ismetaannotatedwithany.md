---
type: Reference
title: "Use cases that publish domain events must have a transaction boundary — `AnnotationRoles.isMetaAnnotatedWithAny`"
tags: [reference]
evidence_for: "/rule/usecase/dca-use-012.md#annotationrolesismetaannotatedwithany"
---

[Full node and context](/rule/usecase/dca-use-012.md#annotationrolesismetaannotatedwithany). This is an evidence excerpt; retain the parent selection and caveats.

### `AnnotationRoles.isMetaAnnotatedWithAny`

```java
/** Meta-annotated with any annotation of the role; false for an empty role. */
  static boolean isMetaAnnotatedWithAny(CanBeAnnotated item, List<String> role) {
    for (String fqn : role) {
      if (item.isMetaAnnotatedWith(fqn)) {
        return true;
      }
    }
    return false;
  }
```
