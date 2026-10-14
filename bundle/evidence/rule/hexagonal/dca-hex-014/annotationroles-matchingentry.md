---
type: Reference
title: "GET handlers must not drive an input port that takes a command — `AnnotationRoles.matchingEntry`"
tags: [reference]
evidence_for: "/rule/hexagonal/dca-hex-014.md#annotationrolesmatchingentry"
---

[Full node and context](/rule/hexagonal/dca-hex-014.md#annotationrolesmatchingentry). This is an evidence excerpt; retain the parent selection and caveats.

### `AnnotationRoles.matchingEntry`

```java
/**
   * The first entry of the role the code unit carries, directly or as a meta-annotation, or {@code
   * null}. An entry {@code <annotation>#<attribute>=<value>} matches an annotation of that type
   * whose attribute holds the value - an enum constant of that name, or that string, compared
   * ignoring case; a plain entry matches the annotation type alone.
   */
  static String matchingEntry(JavaCodeUnit unit, List<String> role) {
    for (String entry : role) {
      int hash = entry.indexOf('#');
      if (hash < 0) {
        if (unit.isMetaAnnotatedWith(entry)) {
          return entry;
        }
        continue;
      }
      String type = entry.substring(0, hash);
      String[] attribute = entry.substring(hash + 1).split("=", 2);
      if (carries(unit.getAnnotations(), type, attribute[0], attribute[1], new HashSet<>())) {
        return entry;
      }
    }
    return null;
  }
```
