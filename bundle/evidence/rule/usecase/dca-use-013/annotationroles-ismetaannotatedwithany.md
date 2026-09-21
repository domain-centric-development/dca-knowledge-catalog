---
type: Reference
title: "Declaratively transactional use cases must not call remote-capable output ports — `AnnotationRoles.isMetaAnnotatedWithAny`"
tags: [reference]
evidence_for: "/rule/usecase/dca-use-013.md#annotationrolesismetaannotatedwithany"
---

[Full node and context](/rule/usecase/dca-use-013.md#annotationrolesismetaannotatedwithany). This is an evidence excerpt; retain the parent selection and caveats.

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
