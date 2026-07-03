---
type: Rule
title: Output Ports in application.shared must extend OutputPort
rule: Interfaces in application.shared are output ports and must extend OutputPort to be part of the port hierarchy.
constraint: Output Ports in application.shared must extend OutputPort.
enforced_by: "HexagonalArchitectureArchUnitTest#Output Ports in application.shared must extend OutputPort"
status: enforced
test_class: HexagonalArchitectureArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/HexagonalArchitectureArchUnitTest.groovy
tags: [hexagonal, archunit]
---

```groovy
expect:
classes()
  .that().resideInAPackage("..application.shared..")
  .and().areInterfaces()
  .should().beAssignableTo(OutputPort.class)
  .because("Interfaces in application.shared are output ports and must extend OutputPort to be part of the port hierarchy")
  .check(allClasses)
```

## Applies to markers

- [OutputPort](/marker/port-out/outputport.md)
