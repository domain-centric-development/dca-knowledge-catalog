---
type: Reference
title: DcaArchitecture — Construction and access
tags: [reference]
evidence_for: "/reference/architecture.md#construction-and-access"
---

[Full node and context](/reference/architecture.md#construction-and-access). This is an evidence excerpt; retain the parent selection and caveats.

### Construction and access

#### `static DcaArchitecture load(DcaLayout layout)`

Imports all production classes below the layout's base package, using the class path of the
calling test.

Jars and archives are imported as well, because `importPackages` already restricts the
result to the base package: in a multi-module build the other modules reach the test class path
as jars, and excluding those would leave their contexts undiscovered while every rule still
reported success. A project whose base package is also shipped by a third-party artifact
narrows the import with `load(DcaLayout,`.

Test code is excluded, the architecture test itself included.

#### `static DcaArchitecture load(DcaLayout layout, ImportOption... importOptions)`

Imports the base package under the given import options instead of the defaults — for a class
path the defaults read too broadly, such as a third-party artifact that ships the project's own
base package (`ImportOption.Predefined.DO_NOT_INCLUDE_JARS` keeps it out, at the price of
the sibling modules of a multi-module build).

#### `static DcaArchitecture of(DcaLayout layout, JavaClasses classes)`

Wraps already imported classes — for tests and custom importers.

#### `DcaLayout layout()`

#### `JavaClasses classes()`
