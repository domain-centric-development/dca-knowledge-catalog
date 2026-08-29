---
type: Rule
id: DCA-STR-004
title: Bounded contexts must not access each other in the domain layer
rule: "A domain layer talks to its own context and the shared kernel, nothing else — not even another context's api/."
constraint: Bounded contexts must not access each other in the domain layer.
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
    "Bounded contexts must not access each other in the domain layer",
    "A domain layer talks to its own context and the shared kernel, nothing else — not even"
        + " another context's api/",
    arch -> {
      for (Map.Entry<String, BoundedContext> source : arch.boundedContexts().entrySet()) {
        String[] forbidden = arch.boundedContextPatternsExcluding(source.getKey());
        if (forbidden.length == 0) {
          continue;
        }
        noClasses()
            .that()
            .resideInAPackage(layout.domainPattern(source.getKey()))
            .should()
            .dependOnClassesThat()
            .resideInAnyPackage(forbidden)
            .allowEmptyShould(true)
            .because(
                "The domain layer of bounded context '"
                    + source.getValue().name()
                    + "' must depend on nothing outside its own context and the shared kernel")
            .check(arch.classes());
      }
    })
```

## Applies to markers

- [@BoundedContext](/marker/strategic/boundedcontext.md)
