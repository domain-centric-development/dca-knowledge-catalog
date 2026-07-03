---
type: Rule
title: "Outgoing Adapters must only use outbound ports (not infrastructure implementations)"
rule: "Outgoing adapters should only use outbound ports from sharedkernel.application.port, not infrastructure implementation details."
constraint: "Outgoing Adapters must only use outbound ports (not infrastructure implementations)."
enforced_by: "HexagonalArchitectureArchUnitTest#Outgoing Adapters must only use outbound ports (not infrastructure implementations)"
status: enforced
test_class: HexagonalArchitectureArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/HexagonalArchitectureArchUnitTest.groovy
tags: [hexagonal, archunit]
---

```groovy
expect:
noClasses()
  .that().resideInAPackage(OUTGOING_ADAPTER_PACKAGE)
  .should().dependOnClassesThat(INFRASTRUCTURE_IMPLEMENTATION)
  .because("Outgoing adapters should only use outbound ports from sharedkernel.application.port, not infrastructure implementation details")
  .check(allClasses)
```
