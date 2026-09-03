---
type: Rule
id: DCA-HEX-007
title: "Incoming adapters must only access their own bounded context (except event consumers and Open Host Services)"
rule: Incoming adapters must only orchestrate use cases from their own bounded context - use domain events for cross-context integration.
constraint: "Incoming adapters must only access their own bounded context (except event consumers and Open Host Services)."
enforced_by: "HexagonalRules#DCA-HEX-007"
status: enforced
rule_set: hexagonal
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/HexagonalRules.java
tags: [hexagonal, archunit]
---

```java
DcaRule.check(
    "DCA-HEX-007",
    "Incoming adapters must only access their own bounded context (except event consumers and"
        + " Open Host Services)",
    "Incoming adapters must only orchestrate use cases from their own bounded context - use"
        + " domain events for cross-context integration",
    arch -> {
      // Structural, over every module that owns a DCA layer - declared as a bounded context or
      // not - so an undeclared module can neither reach out nor be reached into.
      List<ArchRule> perModule = new ArrayList<>();
      for (String module : arch.isolatedModuleRoots()) {
        String[] otherModules = arch.moduleRootPatternsExcluding(module);
        if (otherModules.length == 0) {
          continue;
        }
        perModule.add(
            noClasses()
                .that()
                .resideInAPackage(layout.incomingAdapterPattern(module))
                .and()
                .resideOutsideOfPackage(eventConsumerPattern())
                .should()
                .dependOnClassesThat()
                .resideInAnyPackage(otherModules)
                .allowEmptyShould(true)
                .because(
                    "Incoming adapters in module '"
                        + arch.contextName(module)
                        + "' must only orchestrate use cases from their own module - use"
                        + " domain events for cross-context integration"));
      }
      CollectedViolations.check(perModule, arch.classes());
    })
```
