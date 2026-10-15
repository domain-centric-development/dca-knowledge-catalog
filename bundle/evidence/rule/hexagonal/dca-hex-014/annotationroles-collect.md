---
type: Reference
title: "GET handlers must not drive an input port that takes a command — `AnnotationRoles.collect`"
tags: [reference]
evidence_for: "/rule/hexagonal/dca-hex-014.md#annotationrolescollect"
---

[Full node and context](/rule/hexagonal/dca-hex-014.md#annotationrolescollect). This is an evidence excerpt; retain the parent selection and caveats.

### `AnnotationRoles.collect`

```java
/**
   * Adds the attribute values of every annotation of the type among the annotations, directly or as
   * a meta-annotation; true when at least one such annotation was found.
   */
  private static boolean collect(
      Iterable<? extends JavaAnnotation<?>> annotations,
      String type,
      String attribute,
      Set<String> values,
      Set<String> visited) {
    boolean found = false;
    for (JavaAnnotation<?> annotation : annotations) {
      String name = annotation.getRawType().getName();
      if (name.equals(type)) {
        found = true;
        annotation.get(attribute).ifPresent(v -> addValues(v, values));
      }
      if (visited.add(name)
          && collect(annotation.getRawType().getAnnotations(), type, attribute, values, visited)) {
        found = true;
      }
    }
    return found;
  }
```
