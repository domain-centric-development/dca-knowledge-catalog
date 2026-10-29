---
type: Reference
title: "Event listeners that drive an input port must run after the commit in their own transaction — `AnnotationRoles.isMetaAnnotatedWithAny`"
tags: [reference]
evidence_for: "/rule/hexagonal/dca-hex-017.md#annotationrolesismetaannotatedwithany"
---

[Full node and context](/rule/hexagonal/dca-hex-017.md#annotationrolesismetaannotatedwithany). This is an evidence excerpt; retain the parent selection and caveats.

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
