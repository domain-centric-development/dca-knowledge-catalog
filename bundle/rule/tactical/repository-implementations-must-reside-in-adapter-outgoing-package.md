---
type: Rule
title: Repository Implementations must reside in adapter.outgoing package
rule: Repository implementations are outgoing adapters in bounded contexts.
constraint: Repository Implementations must reside in adapter.outgoing package.
enforced_by: "DddTacticalPatternsArchUnitTest#Repository Implementations must reside in adapter.outgoing package"
status: enforced
test_class: DddTacticalPatternsArchUnitTest
resource: dca-ecommerce-sample/src/test-architecture/groovy/de/sample/aiarchitecture/DddTacticalPatternsArchUnitTest.groovy
tags: [tactical, archunit]
---

```groovy
expect:
classes()
  .that().areNotInterfaces()
  .and().areAssignableTo(Repository.class)
  .should().resideInAPackage(OUTGOING_ADAPTER_PACKAGE)
  .because("Repository implementations are outgoing adapters in bounded contexts")
  .allowEmptyShould(true)
  .check(allClasses)
```

## Applies to markers

- [Repository<T, ID>](/marker/port-out/repository.md)
