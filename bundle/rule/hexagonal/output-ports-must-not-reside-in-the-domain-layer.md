---
type: Rule
title: Output ports must not reside in the domain layer
rule: "output ports (Repository, Store, OutputPort) are an application-layer concern and must live in application/shared/, not domain/."
constraint: Output ports must not reside in the domain layer.
enforced_by: "HexagonalArchitectureArchUnitTest#Output ports must not reside in the domain layer"
status: enforced
test_class: HexagonalArchitectureArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/HexagonalArchitectureArchUnitTest.groovy
tags: [hexagonal, archunit]
---

```groovy
expect:
// Repository/Store/OutputPort interfaces belong to the application layer (application/shared/),
// never to domain/ - the domain must stay port-free and framework-free. This catches the case
// where a *Repository is declared next to the aggregate in domain.model instead of being moved
// to application.shared, which the rule above cannot detect on its own since it only scopes
// application.shared and silently passes when the port isn't there at all.
noClasses()
  .that().areAssignableTo(OUTPUT_PORT_MARKER)
  .and().areInterfaces()
  .should().resideInAPackage(DOMAIN_PACKAGE)
  .because("output ports (Repository, Store, OutputPort) are an application-layer concern and must live in application/shared/, not domain/")
  .allowEmptyShould(true)
  .check(allClasses)
```

## Applies to markers

- [OutputPort](/marker/port-out/outputport.md)
- [Repository<T, ID>](/marker/port-out/repository.md)
