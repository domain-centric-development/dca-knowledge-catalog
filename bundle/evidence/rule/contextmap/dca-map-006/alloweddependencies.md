---
type: Reference
title: "Upstream declarations and the module declaration's allowed dependencies must agree — `allowedDependencies`"
tags: [reference]
evidence_for: "/rule/contextmap/dca-map-006.md#alloweddependencies"
---

[Full node and context](/rule/contextmap/dca-map-006.md#alloweddependencies). This is an evidence excerpt; retain the parent selection and caveats.

### `allowedDependencies`

```java
/**
   * The {@code allowedDependencies} of every module declaration the package actually carries - a
   * package may use any of the configured declarations, and a package carrying none contributes
   * nothing.
   */
  private static List<String> allowedDependencies(
      DcaArchitecture arch, String pkg, List<Class<? extends Annotation>> moduleAnnotations) {
    List<String> allowed = new ArrayList<>();
    for (Class<? extends Annotation> moduleAnnotation : moduleAnnotations) {
      Optional<? extends Annotation> module = arch.packageAnnotation(pkg, moduleAnnotation);
      if (module.isEmpty()) {
        continue;
      }
      try {
        Method attribute = moduleAnnotation.getMethod("allowedDependencies");
        Object value = attribute.invoke(module.get());
        if (value instanceof String[]) {
          allowed.addAll(Arrays.asList((String[]) value));
        }
      } catch (ReflectiveOperationException e) {
        // a declaration without that attribute contributes nothing
      }
    }
    return allowed;
  }
```
