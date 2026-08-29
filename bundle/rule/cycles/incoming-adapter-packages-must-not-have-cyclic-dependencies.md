---
type: Rule
id: DCA-CYC-004
title: Incoming Adapter Packages must not have cyclic dependencies
rule: Incoming adapters should have clear boundaries and no cycles.
constraint: Incoming Adapter Packages must not have cyclic dependencies.
enforced_by: "CycleRules#DCA-CYC-004"
status: enforced
rule_set: cycles
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/CycleRules.java
tags: [cycles, archunit]
---

```java
DcaRule.of(
    "DCA-CYC-004",
    "Incoming Adapter Packages must not have cyclic dependencies",
    "Incoming adapters should have clear boundaries and no cycles",
    arch ->
        slices()
            .matching(
                layout.basePackage()
                    + ".(*)."
                    + layout.adapterSubpackage()
                    + "."
                    + layout.incomingSubpackage()
                    + "..")
            .should()
            .beFreeOfCycles())
```
