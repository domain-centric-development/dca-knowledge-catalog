---
type: Reference
title: "Use cases that save an aggregate must publish its domain events — `useCases`"
tags: [reference]
evidence_for: "/rule/usecase/dca-use-009.md#usecases"
---

[Full node and context](/rule/usecase/dca-use-009.md#usecases). This is an evidence excerpt; retain the parent selection and caveats.

### `useCases`

```java
/**
   * The documented use-case selection: a non-interface class in an application package that either
   * carries the configured use-case suffix or implements the input-port role.
   *
   * <p>Spelled inline, ArchUnit joins {@code and}/{@code or} left to right, so {@code
   * resideInAnyPackage(app).and().haveSimpleNameEndingWith(suffix).or().areAssignableTo(port)
   * .and().areNotInterfaces()} reads {@code ((inApplication ∧ suffix) ∨ isInputPort) ∧ ¬interface}
   * and selects every input-port implementation anywhere, adapters included — which is neither what
   * the rule texts say nor what the .NET twin does.
   */
  private static DescribedPredicate<JavaClass> useCases(DcaArchitecture arch, DcaLayout layout) {
    DescribedPredicate<JavaClass> inApplication =
        JavaClass.Predicates.resideInAnyPackage(arch.allApplicationPatterns());
    DescribedPredicate<JavaClass> named =
        JavaClass.Predicates.simpleNameEndingWith(layout.useCaseSuffix());
    DescribedPredicate<JavaClass> port =
        JavaClass.Predicates.assignableTo(arch.layout().markers().inputPort());
    return inApplication
        .and(named.or(port))
        .and(DescribedPredicate.not(JavaClass.Predicates.INTERFACES))
        .as(
            "non-interface classes in an application package that implement the input port or end"
                + " with \"%s\"",
            layout.useCaseSuffix());
  }
```
