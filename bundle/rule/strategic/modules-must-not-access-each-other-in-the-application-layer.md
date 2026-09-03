---
type: Rule
id: DCA-STR-003
title: Modules must not access each other in the application layer
rule: "An application layer talks to other modules through its own output ports, implemented by adapters - never directly. Selects structurally over every module that owns a DCA layer, declared as a bounded context or not: an undeclared module must not be able to escape isolation by staying off the context map."
constraint: Modules must not access each other in the application layer.
enforced_by: "StrategicPatternRules#DCA-STR-003"
status: enforced
rule_set: strategic
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/StrategicPatternRules.java
tags: [strategic, archunit]
---

```java
DcaRule.check(
    "DCA-STR-003",
    "Modules must not access each other in the application layer",
    "An application layer talks to other modules through its own output ports, implemented by"
        + " adapters - never directly. Selects structurally over every module that owns a DCA"
        + " layer, declared as a bounded context or not: an undeclared module must not be able"
        + " to escape isolation by staying off the context map",
    arch -> {
      List<ArchRule> perModule = new ArrayList<>();
      for (String source : arch.isolatedModuleRoots()) {
        String[] forbidden = arch.moduleRootPatternsExcluding(source);
        if (forbidden.length == 0) {
          continue;
        }
        // dependOnClassesThat, not accessClassesThat: "access" is a method call or field
        // access, so a field, parameter or record component of a foreign type slips past it.
        perModule.add(
            noClasses()
                .that()
                .resideInAPackage(layout.applicationPattern(source))
                .should()
                .dependOnClassesThat()
                .resideInAnyPackage(forbidden)
                .allowEmptyShould(true)
                .because(
                    "The application layer of module '"
                        + arch.contextName(source)
                        + "' must not access other modules directly - define output ports and"
                        + " use adapters instead"));
      }
      CollectedViolations.check(perModule, arch.classes());
    })
```
