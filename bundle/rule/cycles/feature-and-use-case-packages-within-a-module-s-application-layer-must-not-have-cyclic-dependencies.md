---
type: Rule
id: DCA-CYC-005
title: Feature and use case packages within a module's application layer must not have cyclic dependencies
rule: "The packages directly below a module's application package are its features (application.<feature>.<usecase>) or, in a flat layout, its use cases (application.<usecase>). A feature is an optional, domain-named group of related use cases; it may depend on another feature in one direction, but a cycle between two of them means the grouping does not carry its weight - the shared concept belongs in application.shared, in the domain, or in one of the two. application.shared is the context-wide port package and is not a slice. The rule does not infer bounded contexts or aggregate ownership from the packages it slices."
constraint: Feature and use case packages within a module's application layer must not have cyclic dependencies.
enforced_by: "CycleRules#DCA-CYC-005"
status: enforced
rule_set: cycles
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/CycleRules.java
tags: [cycles, archunit]
---

```java
DcaRule.of(
    "DCA-CYC-005",
    "Feature and use case packages within a module's application layer must not have cyclic"
        + " dependencies",
    "The packages directly below a module's application package are its features"
        + " (application.<feature>.<usecase>) or, in a flat layout, its use cases"
        + " (application.<usecase>). A feature is an optional, domain-named group of related"
        + " use cases; it may depend on another feature in one direction, but a cycle between"
        + " two of them means the grouping does not carry its weight - the shared concept"
        + " belongs in application.shared, in the domain, or in one of the two. application.shared"
        + " is the context-wide port package and is not a slice. The rule does not infer bounded"
        + " contexts or aggregate ownership from the packages it slices",
    arch ->
        slices()
            .assignedFrom(applicationChildSlices(arch, layout))
            .should()
            .beFreeOfCycles()
            .allowEmptyShould(true))
```
