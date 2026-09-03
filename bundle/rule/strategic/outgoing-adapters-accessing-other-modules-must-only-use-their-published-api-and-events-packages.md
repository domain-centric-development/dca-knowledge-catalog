---
type: Rule
id: DCA-STR-006
title: Outgoing adapters accessing other modules must only use their published api/ and events/ packages
rule: "Cross-module communication goes through the target's published api/ (synchronous) and events/ (asynchronous) packages - DCA's in-process contract convention, package names rather than framework annotations - never through its domain, application, adapter or infrastructure packages. Selects structurally over every module that owns a DCA layer, declared as a bounded context or not."
constraint: Outgoing adapters accessing other modules must only use their published api/ and events/ packages.
enforced_by: "StrategicPatternRules#DCA-STR-006"
status: enforced
rule_set: strategic
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/StrategicPatternRules.java
tags: [strategic, archunit]
---

```java
DcaRule.check(
    "DCA-STR-006",
    "Outgoing adapters accessing other modules must only use their published api/ and events/"
        + " packages",
    "Cross-module communication goes through the target's published api/ (synchronous) and"
        + " events/ (asynchronous) packages - DCA's in-process contract convention, package"
        + " names rather than framework annotations - never through its domain, application,"
        + " adapter or infrastructure packages. Selects structurally over every module that owns"
        + " a DCA layer, declared as a bounded context or not",
    arch -> {
      List<ArchRule> perModule = new ArrayList<>();
      for (String source : arch.isolatedModuleRoots()) {
        String[] foreign = arch.moduleRootPatternsExcluding(source);
        if (foreign.length == 0) {
          continue;
        }
        String[] published = arch.publishedPackagePatternsExcluding(source);
        perModule.add(
            noClasses()
                .that()
                .resideInAPackage(layout.outgoingAdapterPattern(source))
                .should()
                .dependOnClassesThat(
                    resideInAnyPackage(foreign).and(not(resideInAnyPackage(published))))
                .allowEmptyShould(true)
                .because(
                    "Outgoing adapters in module '"
                        + arch.contextName(source)
                        + "' must not access another module's internals - use its api/ or"
                        + " events/ packages instead"));
      }
      CollectedViolations.check(perModule, arch.classes());
    })
```
