---
type: Rule
title: Repository interfaces must reside in the application layer's shared output-port package
rule: "Repository interfaces are output ports in the application layer (Hexagonal Architecture)."
constraint: Repository interfaces must reside in the application layer's shared output-port package.
enforced_by: "DddTacticalPatternsArchUnitTest#Repository interfaces must reside in the application layer's shared output-port package"
status: enforced
test_class: DddTacticalPatternsArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/DddTacticalPatternsArchUnitTest.groovy
tags: [tactical, archunit]
---

```groovy
expect:
// areAssignableTo, not implement: ArchUnit's implement() matches non-interfaces only, so
// implement(Repository) AND areInterfaces() is an empty subject set for any codebase.
classes()
  .that().areInterfaces()
  .and().areAssignableTo(Repository.class)
  .and().doNotHaveSimpleName("Repository")
  .should().resideInAPackage(SHARED_OUTPUT_PORT_PACKAGE)
  .because("Repository interfaces are output ports in the application layer (Hexagonal Architecture)")
  .allowEmptyShould(true)
  .check(allClasses)
```

## Applies to markers

- [Repository<T, ID>](/marker/port-out/repository.md)
