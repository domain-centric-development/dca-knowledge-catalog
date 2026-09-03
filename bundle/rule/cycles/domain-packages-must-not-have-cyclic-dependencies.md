---
type: Rule
id: DCA-CYC-001
title: Domain Packages must not have cyclic dependencies
rule: "Domain model packages should have clear boundaries and no cycles (Acyclic Dependencies Principle)."
constraint: Domain Packages must not have cyclic dependencies.
enforced_by: "CycleRules#DCA-CYC-001"
status: enforced
rule_set: cycles
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/CycleRules.java
tags: [cycles, archunit]
---

```java
DcaRule.of(
    "DCA-CYC-001",
    "Domain Packages must not have cyclic dependencies",
    "Domain model packages should have clear boundaries and no cycles (Acyclic Dependencies"
        + " Principle)",
    arch ->
        slices()
            .assignedFrom(
                moduleLayerSlices(
                    arch, root -> root + "." + layout.domainSubpackage() + ".model"))
            .should()
            .beFreeOfCycles()
            .allowEmptyShould(true))
```
