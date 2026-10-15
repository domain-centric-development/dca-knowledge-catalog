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
   * null}. A plain entry matches the annotation type alone. An entry {@code
   * <annotation>#<attribute>=<value>} matches a code unit carrying an annotation of that type when
   * the attribute holds the value - an enum constant of that name, or that string, compared
   * ignoring case; an entry {@code <annotation>#<attribute>=} matches when the attribute holds no
   * value. The values are those of every annotation of that type on the code unit together with
   * those on its declaring class, as a framework combines a class-level and a method-level mapping;
   * the class alone makes no match.
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
      Set<String> values = new HashSet<>();
      if (!collect(unit.getAnnotations(), type, attribute[0], values, new HashSet<>())) {
        continue;
      }
      collect(unit.getOwner().getAnnotations(), type, attribute[0], values, new HashSet<>());
      boolean matches =
          attribute[1].isEmpty()
              ? values.isEmpty()
              : values.stream().anyMatch(v -> v.equalsIgnoreCase(attribute[1]));
      if (matches) {
        return entry;
      }
    }
    return null;
  }
```
