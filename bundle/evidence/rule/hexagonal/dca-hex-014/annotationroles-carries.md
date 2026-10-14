---
type: Reference
title: "GET handlers must not drive an input port that takes a command — `AnnotationRoles.carries`"
tags: [reference]
evidence_for: "/rule/hexagonal/dca-hex-014.md#annotationrolescarries"
---

[Full node and context](/rule/hexagonal/dca-hex-014.md#annotationrolescarries). This is an evidence excerpt; retain the parent selection and caveats.

### `AnnotationRoles.carries`

```java
private static boolean carries(
    Iterable<? extends JavaAnnotation<?>> annotations,
    String type,
    String attribute,
    String value,
    Set<String> visited) {
  for (JavaAnnotation<?> annotation : annotations) {
    String name = annotation.getRawType().getName();
    if (name.equals(type) && annotation.get(attribute).map(v -> holds(v, value)).orElse(false)) {
      return true;
    }
    if (visited.add(name)
        && carries(annotation.getRawType().getAnnotations(), type, attribute, value, visited)) {
      return true;
    }
  }
  return false;
}
```
