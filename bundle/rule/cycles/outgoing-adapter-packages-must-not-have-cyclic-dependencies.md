---
type: Rule
id: DCA-CYC-003
title: Outgoing Adapter Packages must not have cyclic dependencies
rule: Outgoing adapters should have clear boundaries and no cycles.
constraint: Outgoing Adapter Packages must not have cyclic dependencies.
enforced_by: "CycleRules#DCA-CYC-003"
status: enforced
rule_set: cycles
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/CycleRules.java
tags: [cycles, archunit]
---

```java
DcaRule.of(
    "DCA-CYC-003",
    "Outgoing Adapter Packages must not have cyclic dependencies",
    "Outgoing adapters should have clear boundaries and no cycles",
    arch ->
        slices()
            .matching(
                layout.basePackage()
                    + ".(*)."
                    + layout.adapterSubpackage()
                    + "."
                    + layout.outgoingSubpackage()
                    + "..")
            .should()
            .beFreeOfCycles())
```
