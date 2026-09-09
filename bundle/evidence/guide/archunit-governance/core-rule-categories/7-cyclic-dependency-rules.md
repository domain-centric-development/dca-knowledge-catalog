---
type: Reference
title: Core Rule Categories — 7. Cyclic Dependency Rules
tags: [reference]
evidence_for: "/guide/archunit-governance/core-rule-categories.md#7-cyclic-dependency-rules"
---

[Full node and context](/guide/archunit-governance/core-rule-categories.md#7-cyclic-dependency-rules). This is an evidence excerpt; retain the parent selection and caveats.

### 7. Cyclic Dependency Rules

Detect and prevent circular dependencies.

```java
@ArchTest
static final ArchRule no_cycles_in_packages =
    slices()
        .matching("com.company.project.(*)..")
        .should().beFreeOfCycles()
        .because("Cyclic dependencies make code hard to understand and maintain");

@ArchTest
static final ArchRule no_cycles_between_bounded_contexts =
    slices()
        .matching("com.company.project.(*).(*)..")   // every context, not a fixed list
        .should().beFreeOfCycles()
        .because("Bounded contexts should not have cyclic dependencies");

// Inside one context: the packages directly below application/ — the features in a grouped layout
// (application/{feature}/{usecase}), the use cases in a flat one — must not depend on each other in
// a circle. application/shared is the context-wide port package and is not a slice. Catalog: DCA-CYC-005.
@ArchTest
static final ArchRule no_cycles_between_features =
    slices()
        .matching("com.company.project.order.application.(*)..")
        .ignoreDependency(alwaysTrue(), resideInAPackage("..application.shared.."))
        .should().beFreeOfCycles()
        .because("A cycle between two features means the grouping does not carry its weight");
```

A second structural rule keeps the feature level legible: within one module the use-case packages use *one*
depth — all `application.<usecase>` or all `application.<feature>.<usecase>` — never a mixture, and never a
use case directly in `application` or nested deeper than a feature (`DCA-USE-014`). Both rules check package
shape only; they infer nothing about bounded contexts or aggregate ownership.
