---
type: Rule
id: DCA-CYC-002
title: Application Layer must not have cyclic dependencies
rule: Application services should have clear boundaries and no cycles.
constraint: Application Layer must not have cyclic dependencies.
enforced_by: "CycleRules#DCA-CYC-002"
status: enforced
rule_set: cycles
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/CycleRules.java
tags: [cycles, archunit]
---

```java
DcaRule.of(
    "DCA-CYC-002",
    "Application Layer must not have cyclic dependencies",
    "Application services should have clear boundaries and no cycles",
    arch ->
        slices()
            .assignedFrom(
                moduleLayerSlices(arch, root -> root + "." + layout.applicationSubpackage()))
            .should()
            .beFreeOfCycles()
            .allowEmptyShould(true))
```
