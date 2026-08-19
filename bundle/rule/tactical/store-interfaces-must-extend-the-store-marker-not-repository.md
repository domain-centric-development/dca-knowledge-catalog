---
type: Rule
title: "Store interfaces must extend the Store marker, not Repository"
rule: Stores extend the Store marker; Repository is reserved for Aggregate Roots.
constraint: "Store interfaces must extend the Store marker, not Repository."
enforced_by: "DddTacticalPatternsArchUnitTest#Store interfaces must extend the Store marker, not Repository"
status: enforced
test_class: DddTacticalPatternsArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/DddTacticalPatternsArchUnitTest.groovy
tags: [tactical, archunit]
---

```groovy
expect:
// A *Store records or queries operational data that has no aggregate lifecycle. Marking one
// as a Repository is a category error: the name would promise identity-based load/save.
classes()
  .that().areInterfaces()
  .and().haveSimpleNameEndingWith("Store")
  .and().doNotHaveSimpleName("Store")
  .should().beAssignableTo(Store.class)
  .andShould().notBeAssignableTo(Repository.class)
  .because("Stores extend the Store marker; Repository is reserved for Aggregate Roots")
  .allowEmptyShould(true)
  .check(allClasses)
```

## Applies to markers

- [Repository<T, ID>](/marker/port-out/repository.md)
- [Store](/marker/port-out/store.md)
