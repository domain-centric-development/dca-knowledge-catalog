---
type: Rule
title: Application Services should not access port adapters
rule: "Application services should only depend on domain and outbound ports, not adapters."
constraint: Application Services should not access port adapters.
enforced_by: "HexagonalArchitectureArchUnitTest#Application Services should not access port adapters"
status: enforced
test_class: HexagonalArchitectureArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/HexagonalArchitectureArchUnitTest.groovy
tags: [hexagonal, archunit]
---

```groovy
expect:
noClasses()
  .that().resideInAPackage(APPLICATION_PACKAGE)
  .should().accessClassesThat().resideInAPackage(ADAPTER_PACKAGE)
  .because("Application services should only depend on domain and outbound ports, not adapters")
  .check(allClasses)
```
