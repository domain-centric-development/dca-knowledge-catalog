---
type: Rule
title: Shared Kernel must not have dependencies on any bounded context
rule: "Shared Kernel must not depend on bounded context '<context>' (<context>) - Shared Kernel must be context-independent."
constraint: Shared Kernel must not have dependencies on any bounded context.
enforced_by: "DddStrategicPatternsArchUnitTest#Shared Kernel must not have dependencies on any bounded context"
status: enforced
test_class: DddStrategicPatternsArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/DddStrategicPatternsArchUnitTest.groovy
tags: [strategic, archunit]
---

```groovy
given:
String sharedKernelPackage = discoverSharedKernelPackage()
Map<String, BoundedContext> boundedContexts = discoverBoundedContextPackages()

expect:
// The Shared Kernel should be truly shared - no dependencies on specific contexts
// Dynamically check against all discovered bounded contexts
boundedContexts.each { contextPackage, annotation ->
  noClasses()
    .that().resideInAPackage(sharedKernelPackage + "..")
    .should().accessClassesThat().resideInAPackage(contextPackage + "..")
    .allowEmptyShould(true)
    .because("Shared Kernel must not depend on bounded context '${annotation.name()}' (${contextPackage}) - Shared Kernel must be context-independent")
    .check(allClasses)
}
```

## Applies to markers

- [@BoundedContext](/marker/strategic/boundedcontext.md)
