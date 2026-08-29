---
type: Rule
id: DCA-STR-003
title: "Bounded contexts must not directly access each other in application layer (except allowed dependencies)"
rule: "Application layers talk to other contexts through output ports and adapters, never directly."
constraint: "Bounded contexts must not directly access each other in application layer (except allowed dependencies)."
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
    "Bounded contexts must not directly access each other in application layer (except allowed"
        + " dependencies)",
    "Application layers talk to other contexts through output ports and adapters, never"
        + " directly",
    arch -> {
      for (Map.Entry<String, BoundedContext> source : arch.boundedContexts().entrySet()) {
        String[] forbidden = arch.boundedContextPatternsExcluding(source.getKey());
        if (forbidden.length == 0) {
          continue;
        }
        // dependOnClassesThat, not accessClassesThat: "access" is a method call or field
        // access, so a field, parameter or record component of a foreign type slips past it.
        noClasses()
            .that()
            .resideInAPackage(layout.applicationPattern(source.getKey()))
            .should()
            .dependOnClassesThat()
            .resideInAnyPackage(forbidden)
            .allowEmptyShould(true)
            .because(
                "Application layer of bounded context '"
                    + source.getValue().name()
                    + "' must not access other contexts directly - define output ports and"
                    + " use adapters instead")
            .check(arch.classes());
      }
    })
```

## Applies to markers

- [@BoundedContext](/marker/strategic/boundedcontext.md)
