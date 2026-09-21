---
type: Reference
title: "Upstream declarations and the module declaration's allowed dependencies must agree — `carriesModuleDeclaration`"
tags: [reference]
evidence_for: "/rule/contextmap/dca-map-006.md#carriesmoduledeclaration"
---

[Full node and context](/rule/contextmap/dca-map-006.md#carriesmoduledeclaration). This is an evidence excerpt; retain the parent selection and caveats.

### `carriesModuleDeclaration`

```java
/** Whether the package carries at least one of the configured module declarations. */
  private static boolean carriesModuleDeclaration(
      DcaArchitecture arch, String pkg, List<Class<? extends Annotation>> moduleAnnotations) {
    return moduleAnnotations.stream()
        .anyMatch(annotation -> arch.packageAnnotation(pkg, annotation).isPresent());
  }
```
