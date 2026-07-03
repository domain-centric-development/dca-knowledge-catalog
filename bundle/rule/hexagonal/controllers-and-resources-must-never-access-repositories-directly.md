---
type: Rule
title: Controllers and Resources must never access repositories directly
rule: "Controllers must go through use cases (input ports), never directly to repositories."
constraint: Controllers and Resources must never access repositories directly.
enforced_by: "HexagonalArchitectureArchUnitTest#Controllers and Resources must never access repositories directly"
status: enforced
test_class: HexagonalArchitectureArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/HexagonalArchitectureArchUnitTest.groovy
tags: [hexagonal, archunit]
---

```groovy
expect:
// Incoming web adapters drive the application through input ports (use cases) only.
// Direct repository access would bypass the application layer and its
// transaction/authorization/orchestration responsibilities.
noClasses()
  .that().haveSimpleNameEndingWith("Controller")
  .or().haveSimpleNameEndingWith(REST_CONTROLLER_SUFFIX)
  .should().dependOnClassesThat().areAssignableTo(REPOSITORY_MARKER)
  .because("Controllers must go through use cases (input ports), never directly to repositories")
  .allowEmptyShould(true)
  .check(allClasses)
```

## Applies to markers

- [Repository<T, ID>](/marker/port-out/repository.md)
