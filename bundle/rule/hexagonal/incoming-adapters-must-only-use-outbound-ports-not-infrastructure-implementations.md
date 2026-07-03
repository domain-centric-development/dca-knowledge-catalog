---
type: Rule
title: "Incoming Adapters must only use outbound ports (not infrastructure implementations)"
rule: "Incoming adapters should only use outbound ports from sharedkernel.application.port, not infrastructure implementation details."
constraint: "Incoming Adapters must only use outbound ports (not infrastructure implementations)."
enforced_by: "HexagonalArchitectureArchUnitTest#Incoming Adapters must only use outbound ports (not infrastructure implementations)"
status: enforced
test_class: HexagonalArchitectureArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/HexagonalArchitectureArchUnitTest.groovy
tags: [hexagonal, archunit]
---

```groovy
expect:
noClasses()
  .that().resideInAPackage(INCOMING_ADAPTER_PACKAGE)
  .should().dependOnClassesThat(INFRASTRUCTURE_IMPLEMENTATION)
  .because("Incoming adapters should only use outbound ports from sharedkernel.application.port, not infrastructure implementation details")
  .check(allClasses)
```
