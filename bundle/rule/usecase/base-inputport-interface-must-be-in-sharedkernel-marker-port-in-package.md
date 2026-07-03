---
type: Rule
title: Base InputPort interface must be in sharedkernel marker port in package
rule: "Base InputPort interface defines the generic contract for all use cases (Hexagonal Architecture)."
constraint: Base InputPort interface must be in sharedkernel marker port in package.
enforced_by: "UseCasePatternsArchUnitTest#Base InputPort interface must be in sharedkernel marker port in package"
status: enforced
test_class: UseCasePatternsArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/UseCasePatternsArchUnitTest.groovy
tags: [usecase, archunit]
---

```groovy
expect:
classes()
  .that().areInterfaces()
  .and().haveSimpleName("InputPort")
  .should().resideInAPackage(SHAREDKERNEL_MARKER_PORT_IN_PACKAGE)
  .because("Base InputPort interface defines the generic contract for all use cases (Hexagonal Architecture)")
  .allowEmptyShould(true)
  .check(allClasses)
```

## Applies to markers

- [InputPort](/marker/port-in/inputport.md)
