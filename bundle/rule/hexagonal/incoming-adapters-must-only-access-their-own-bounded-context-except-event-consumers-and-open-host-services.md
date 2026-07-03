---
type: Rule
title: "Incoming adapters must only access their own bounded context (except event consumers and Open Host Services)"
rule: "Incoming adapters in '<context>' must only orchestrate use cases from their own bounded context - use domain events for cross-context integration."
constraint: "Incoming adapters must only access their own bounded context (except event consumers and Open Host Services)."
enforced_by: "HexagonalArchitectureArchUnitTest#Incoming adapters must only access their own bounded context (except event consumers and Open Host Services)"
status: enforced
test_class: HexagonalArchitectureArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/HexagonalArchitectureArchUnitTest.groovy
tags: [hexagonal, archunit]
---

```groovy
given:
Map<String, BoundedContext> boundedContexts = discoverBoundedContextPackages()
List<String> contextPackages = boundedContexts.keySet().toList()

expect:
// Dynamically check each bounded context's incoming adapters
// They must not access any other bounded context
// Exception: Event consumers may access other contexts' integration events
// Note: Open Host Services (api/ packages) are designed to BE ACCESSED by other contexts,
// but they themselves should not access other contexts
contextPackages.each { contextPackage ->
  String contextName = boundedContexts[contextPackage].name()

  // Get all other context packages (excluding current)
  List<String> otherContexts = contextPackages.findAll { it != contextPackage }

  if (!otherContexts.isEmpty()) {
    String[] otherContextPatterns = otherContexts.collect { it + ".." } as String[]

    noClasses()
      .that().resideInAPackage("${contextPackage}.adapter.incoming..")
        .and().resideOutsideOfPackage("..adapter.incoming.event..")
      .should().accessClassesThat().resideInAnyPackage(otherContextPatterns)
      .allowEmptyShould(true)
      .because("Incoming adapters in '${contextName}' must only orchestrate use cases from their own bounded context - use domain events for cross-context integration")
      .check(allClasses)
  }
}
```

## Applies to markers

- [@BoundedContext](/marker/strategic/boundedcontext.md)
