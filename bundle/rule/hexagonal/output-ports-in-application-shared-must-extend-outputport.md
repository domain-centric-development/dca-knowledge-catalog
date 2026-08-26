---
type: Rule
title: Output Ports in application.shared must extend OutputPort
rule: Top-level interfaces in application.shared are output ports and must extend OutputPort to be part of the port hierarchy. .
constraint: Output Ports in application.shared must extend OutputPort.
enforced_by: "HexagonalArchitectureArchUnitTest#Output Ports in application.shared must extend OutputPort"
status: enforced
test_class: HexagonalArchitectureArchUnitTest
resource: dca-ecommerce-sample/src/test-architecture/groovy/de/sample/aiarchitecture/HexagonalArchitectureArchUnitTest.groovy
tags: [hexagonal, archunit]
---

```groovy
expect:
classes()
  .that().resideInAPackage("..application.shared..")
  .and().areInterfaces()
  .and().areTopLevelClasses()
  .and().haveSimpleNameNotEndingWith("package-info")
  .should().beAssignableTo(OutputPort.class)
  .because("Top-level interfaces in application.shared are output ports and must extend OutputPort to be part of the port hierarchy. " +
  "Nested interfaces (e.g. IdentityProvider.Identity) are part of their enclosing port's contract, not ports themselves")
  .check(allClasses)
```

## Applies to markers

- [OutputPort](/marker/port-out/outputport.md)
