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
      Map<String, BoundedContext> contexts = arch.boundedContexts();
      for (Map.Entry<String, BoundedContext> entry : contexts.entrySet()) {
        String contextPackage = entry.getKey();
        String[] otherContexts = arch.boundedContextPatternsExcluding(contextPackage);
        if (otherContexts.length == 0) {
          continue;
        }
        noClasses()
            .that()
            .resideInAPackage(layout.incomingAdapterPattern(contextPackage))
            .and()
            .resideOutsideOfPackage(eventConsumerPattern())
            .should()
            .dependOnClassesThat()
            .resideInAnyPackage(otherContexts)
            .allowEmptyShould(true)
            .because(
                "Incoming adapters in '"
                    + entry.getValue().name()
                    + "' must only orchestrate use cases from their own bounded context - use"
                    + " domain events for cross-context integration")
            .check(arch.classes());
      }
    })
```

## Applies to markers

- [@BoundedContext](/marker/strategic/boundedcontext.md)
