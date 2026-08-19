---
type: Rule
title: Bounded contexts must not access each other in the domain layer
rule: "The domain layer of bounded context '<context>' must depend on nothing outside its own context and the shared kernel."
constraint: Bounded contexts must not access each other in the domain layer.
enforced_by: "DddStrategicPatternsArchUnitTest#Bounded contexts must not access each other in the domain layer"
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
// Stricter than the application-layer rule above, and deliberately without exceptions: a
// domain layer talks to its own context and the shared kernel, nothing else. Not even the
// other context's api/ — reaching an Open Host Service is the job of the application layer
// or an outgoing adapter, which have somewhere to put the translation.
//
// The shared kernel cannot appear among the forbidden targets: it carries @SharedKernel, not
// @BoundedContext, so discoverBoundedContextPackages() never returns it. That is what keeps
// Money and ProductId reachable from every context's domain without an allow-list.
contextPackages.each { sourceContext ->
  String sourceName = boundedContexts[sourceContext].name()

  List<String> otherContexts = contextPackages.findAll { it != sourceContext }
  if (!otherContexts.isEmpty()) {
    String[] forbiddenContextPatterns = otherContexts.collect { it + ".." } as String[]

    noClasses()
      .that().resideInAPackage(sourceContext + ".domain..")
      // dependOnClassesThat, not accessClassesThat: "access" is a method call or field
      // access, so a field or record component of a foreign type slips past it.
      .should().dependOnClassesThat().resideInAnyPackage(forbiddenContextPatterns)
      .allowEmptyShould(true)
      .because("The domain layer of bounded context '${sourceName}' must depend on nothing outside its own context and the shared kernel")
      .check(allClasses)
  }
}
```

## Applies to markers

- [@BoundedContext](/marker/strategic/boundedcontext.md)
- [@SharedKernel](/marker/strategic/sharedkernel.md)
