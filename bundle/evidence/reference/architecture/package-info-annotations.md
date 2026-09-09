---
type: Reference
title: DcaArchitecture — package-info annotations
tags: [reference]
evidence_for: "/reference/architecture.md#package-info-annotations"
---

[Full node and context](/reference/architecture.md#package-info-annotations). This is an evidence excerpt; retain the parent selection and caveats.

### package-info annotations

#### `<T extends Annotation> Optional<T> packageAnnotation(String packageName, Class<T> annotationType)`

A single annotation from the package's `package-info` class, if present.

#### `<T extends Annotation> List<T> packageAnnotations(String packageName, Class<T> annotationType)`

All instances of a repeatable annotation from the package's `package-info` class.
