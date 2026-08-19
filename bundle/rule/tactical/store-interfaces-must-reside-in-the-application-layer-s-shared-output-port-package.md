---
type: Rule
title: Store interfaces must reside in the application layer's shared output-port package
rule: "Store interfaces are output ports in the application layer (Hexagonal Architecture)."
constraint: Store interfaces must reside in the application layer's shared output-port package.
enforced_by: "DddTacticalPatternsArchUnitTest#Store interfaces must reside in the application layer's shared output-port package"
status: enforced
test_class: DddTacticalPatternsArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/DddTacticalPatternsArchUnitTest.groovy
tags: [tactical, archunit]
---

```groovy
expect:
// Same placement as Repository: a Store is an output port, so it is declared where the
// application layer owns its contracts, not where an adapter implements them.
classes()
  .that().areInterfaces()
  .and().areAssignableTo(Store.class)
  .and().doNotHaveSimpleName("Store")
  .should().resideInAPackage(SHARED_OUTPUT_PORT_PACKAGE)
  .because("Store interfaces are output ports in the application layer (Hexagonal Architecture)")
  .allowEmptyShould(true)
  .check(allClasses)
```

## Applies to markers

- [Repository<T, ID>](/marker/port-out/repository.md)
- [Store](/marker/port-out/store.md)
