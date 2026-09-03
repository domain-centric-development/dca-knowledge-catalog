---
type: Rule
id: DCA-STR-004
title: Modules must not access each other in the domain layer
rule: "A domain layer talks to its own module and the shared kernel, nothing else - not even another module's api/. Selects structurally over every module that owns a DCA layer, declared as a bounded context or not."
constraint: Modules must not access each other in the domain layer.
enforced_by: "StrategicPatternRules#DCA-STR-004"
status: enforced
rule_set: strategic
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/StrategicPatternRules.java
tags: [strategic, archunit]
---

```java
DcaRule.check(
    "DCA-STR-004",
    "Modules must not access each other in the domain layer",
    "A domain layer talks to its own module and the shared kernel, nothing else - not even"
        + " another module's api/. Selects structurally over every module that owns a DCA layer,"
        + " declared as a bounded context or not",
    arch -> {
      List<ArchRule> perModule = new ArrayList<>();
      for (String source : arch.isolatedModuleRoots()) {
        String[] forbidden = arch.moduleRootPatternsExcluding(source);
        if (forbidden.length == 0) {
          continue;
        }
        perModule.add(
            noClasses()
                .that()
                .resideInAPackage(layout.domainPattern(source))
                .should()
                .dependOnClassesThat()
                .resideInAnyPackage(forbidden)
                .allowEmptyShould(true)
                .because(
                    "The domain layer of module '"
                        + arch.contextName(source)
                        + "' must depend on nothing outside its own module and the shared"
                        + " kernel"));
      }
      CollectedViolations.check(perModule, arch.classes());
    })
```
