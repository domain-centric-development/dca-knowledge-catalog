---
type: Reference
title: "Every allowed dependency of a module declaration must be backed by an actual code dependency — `moduleAnnotationTypes`"
tags: [reference]
evidence_for: "/rule/contextmap/dca-map-014.md#moduleannotationtypes"
---

[Full node and context](/rule/contextmap/dca-map-014.md#moduleannotationtypes). This is an evidence excerpt; retain the parent selection and caveats.

### `moduleAnnotationTypes`

```java
private List<Class<? extends Annotation>> moduleAnnotationTypes() {
  List<Class<? extends Annotation>> types = new ArrayList<>();
  for (String name : layout.frameworkAnnotations().moduleDeclaration()) {
    try {
      Class<?> type = Class.forName(name, false, Thread.currentThread().getContextClassLoader());
      if (type.isAnnotation()) {
        types.add((Class<? extends Annotation>) type);
      }
    } catch (ClassNotFoundException e) {
      // not on the class path - a declaration the project does not use
    }
  }
  return types;
}
```
