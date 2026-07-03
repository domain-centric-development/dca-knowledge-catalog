---
type: Rule
title: Transaction boundaries belong to the application layer
rule: Transactions are an application-layer concern - domain and incoming adapters must not manage them.
constraint: Transaction boundaries belong to the application layer.
enforced_by: "LayeredArchitectureArchUnitTest#Transaction boundaries belong to the application layer"
status: enforced
test_class: LayeredArchitectureArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/LayeredArchitectureArchUnitTest.groovy
tags: [layered, archunit]
---

```groovy
expect:
// The use case owns the unit of work. @Transactional is allowed in the application
// layer (transaction boundary) and in outgoing persistence adapters (multi-statement
// operations that must stay atomic even when invoked outside a use-case transaction;
// with default REQUIRED propagation they join the caller's transaction).
// It is never allowed in the domain layer or in incoming adapters.
def transactionalMethods = methods()
  .that().areAnnotatedWith(Transactional.class)
  .should().beDeclaredInClassesThat().resideInAnyPackage(
    (allApplicationPatterns().toList() + ["..adapter.outgoing.."]) as String[])
  .because("Transactions are an application-layer concern - domain and incoming adapters must not manage them")
  .allowEmptyShould(true)

def transactionalClasses = classes()
  .that().areAnnotatedWith(Transactional.class)
  .should().resideInAnyPackage(
    (allApplicationPatterns().toList() + ["..adapter.outgoing.."]) as String[])
  .because("Transactions are an application-layer concern - domain and incoming adapters must not manage them")
  .allowEmptyShould(true)

transactionalMethods.check(allClasses)
transactionalClasses.check(allClasses)
```
