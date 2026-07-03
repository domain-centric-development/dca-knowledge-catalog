---
type: Rule
title: "Bounded contexts must not directly access each other in application layer (except allowed dependencies)"
rule: "Application layer of bounded context '<context>' must not access other contexts directly - define output ports and use adapters instead."
constraint: "Bounded contexts must not directly access each other in application layer (except allowed dependencies)."
enforced_by: "DddStrategicPatternsArchUnitTest#Bounded contexts must not directly access each other in application layer (except allowed dependencies)"
status: enforced
test_class: DddStrategicPatternsArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/DddStrategicPatternsArchUnitTest.groovy
tags: [strategic, archunit]
---

```groovy
given:
Map<String, BoundedContext> boundedContexts = discoverBoundedContextPackages()
List<String> contextPackages = boundedContexts.keySet().toList()

expect:
// For each bounded context, verify its application layer does not access any other bounded context
// Exceptions:
// 1. Event consumers (..adapter.incoming.event..) may access other contexts' events
// 2. Allowed cross-context dependencies documented in ALLOWED_CROSS_CONTEXT_DEPENDENCIES
contextPackages.each { sourceContext ->
  String sourceName = boundedContexts[sourceContext].name()
  String sourceContextShort = extractContextName(sourceContext)

  // Get allowed target contexts for this source
  List<String> allowedTargets = ALLOWED_CROSS_CONTEXT_DEPENDENCIES.getOrDefault(sourceContextShort, [])

  // Get all other contexts, excluding allowed targets
  List<String> forbiddenContexts = contextPackages.findAll { targetContext ->
    if (targetContext == sourceContext) return false
    String targetContextShort = extractContextName(targetContext)
    return !allowedTargets.contains(targetContextShort)
  }

  if (!forbiddenContexts.isEmpty()) {
    String[] forbiddenContextPatterns = forbiddenContexts.collect { it + ".." } as String[]

    // Check application layer isolation
    // Use allowEmptyShould(true) for contexts that may not have an application layer yet
    noClasses()
      .that().resideInAPackage(sourceContext + ".application..")
      .should().accessClassesThat().resideInAnyPackage(forbiddenContextPatterns)
      .allowEmptyShould(true)
      .because("Application layer of bounded context '${sourceName}' must not access other contexts directly - define output ports and use adapters instead")
      .check(allClasses)
  }
}
```

## Applies to markers

- [@BoundedContext](/marker/strategic/boundedcontext.md)
