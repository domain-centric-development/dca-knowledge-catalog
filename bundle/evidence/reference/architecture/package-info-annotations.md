---
type: Reference
title: DcaArchitecture — package-info annotations
tags: [reference]
evidence_for: "/reference/architecture.md#package-info-annotations"
---

[Full node and context](/reference/architecture.md#package-info-annotations). This is an evidence excerpt; retain the parent selection and caveats.

### package-info annotations

#### `<T extends Annotation> Optional<T> packageAnnotation(String packageName, Class<T> annotationType)`

A single annotation from the package's `package-info`, if present.

Read from the imported bytecode, never by loading the `package-info` class: the
classes under test need not be loadable, and an annotation retained only in the class file is
enough. For `t` and `l` the annotation looked for is the
one the layout's marker role names (`boundedContext()`, `sharedKernel()`); a project's own annotation is then answered as the library type,
its members read by name.

#### `<T extends Annotation> List<T> packageAnnotations(String packageName, Class<T> annotationType)`

All instances of a repeatable annotation from the package's `package-info` — the one
written directly and those inside its container — read from the bytecode like `packageAnnotation(String,`.
