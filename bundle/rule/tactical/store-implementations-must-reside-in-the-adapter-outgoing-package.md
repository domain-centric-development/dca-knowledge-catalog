---
type: Rule
title: Store implementations must reside in the adapter.outgoing package
rule: Store implementations are outgoing adapters in bounded contexts.
constraint: Store implementations must reside in the adapter.outgoing package.
enforced_by: "DddTacticalPatternsArchUnitTest#Store implementations must reside in the adapter.outgoing package"
status: enforced
test_class: DddTacticalPatternsArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/DddTacticalPatternsArchUnitTest.groovy
tags: [tactical, archunit]
---

```groovy
expect:
classes()
  .that().areNotInterfaces()
  .and().areAssignableTo(Store.class)
  .should().resideInAPackage(OUTGOING_ADAPTER_PACKAGE)
  .because("Store implementations are outgoing adapters in bounded contexts")
  .allowEmptyShould(true)
  .check(allClasses)
```

## Applies to markers

- [Store](/marker/port-out/store.md)
