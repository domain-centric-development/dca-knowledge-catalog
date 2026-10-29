---
type: Reference
title: "Event listeners that drive an input port must run after the commit in their own transaction — `AnnotationRoles.listenerEntry`"
tags: [reference]
evidence_for: "/rule/hexagonal/dca-hex-017.md#annotationroleslistenerentry"
---

[Full node and context](/rule/hexagonal/dca-hex-017.md#annotationroleslistenerentry). This is an evidence excerpt; retain the parent selection and caveats.

### `AnnotationRoles.listenerEntry`

```java
/**
   * The first entry of the role a listener method carries - on the method itself, as {@link
   * #matchingEntry} reads it, or on one of its parameters, where a framework such as CDI puts the
   * observer annotation and its phase. On a parameter, a plain entry matches the annotation type,
   * directly or as a meta-annotation, and an entry {@code <annotation>#<attribute>=<value>} matches
   * when the parameter's annotation of that type holds the value; the declaring class plays no
   * part. {@code null} when neither does.
   */
  static String listenerEntry(JavaCodeUnit unit, List<String> role) {
    String onMethod = matchingEntry(unit, role);
    if (onMethod != null) {
      return onMethod;
    }
    for (JavaParameter parameter : unit.getParameters()) {
      for (String entry : role) {
        int hash = entry.indexOf('#');
        if (hash < 0) {
          if (parameter.isMetaAnnotatedWith(entry)) {
            return entry;
          }
          continue;
        }
        String type = entry.substring(0, hash);
        String[] attribute = entry.substring(hash + 1).split("=", 2);
        Set<String> values = new HashSet<>();
        if (!collect(parameter.getAnnotations(), type, attribute[0], values, new HashSet<>())) {
          continue;
        }
        boolean matches =
            attribute[1].isEmpty()
                ? values.isEmpty()
                : values.stream().anyMatch(v -> v.equalsIgnoreCase(attribute[1]));
        if (matches) {
          return entry;
        }
      }
    }
    return null;
  }
```
