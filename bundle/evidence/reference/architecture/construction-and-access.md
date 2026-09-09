---
type: Reference
title: DcaArchitecture — Construction and access
tags: [reference]
evidence_for: "/reference/architecture.md#construction-and-access"
---

[Full node and context](/reference/architecture.md#construction-and-access). This is an evidence excerpt; retain the parent selection and caveats.

### Construction and access

#### `static DcaArchitecture load(DcaLayout layout)`

Imports all production classes below the layout's base package (excluding tests, jars and
archives) using the class path of the calling test.

#### `static DcaArchitecture of(DcaLayout layout, JavaClasses classes)`

Wraps already imported classes — for tests and custom importers.

#### `DcaLayout layout()`

#### `JavaClasses classes()`
