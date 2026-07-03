---
type: Rule
title: Classes from the domain should not access port adapters
rule: "Domain should not depend on adapters (ports and adapters pattern)."
constraint: Classes from the domain should not access port adapters.
enforced_by: "HexagonalArchitectureArchUnitTest#Classes from the domain should not access port adapters"
status: enforced
test_class: HexagonalArchitectureArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/HexagonalArchitectureArchUnitTest.groovy
tags: [hexagonal, archunit]
---

```groovy
expect:
noClasses()
  .that().resideInAPackage(DOMAIN_MODEL_PACKAGE)
  .should().accessClassesThat().resideInAPackage(ADAPTER_PACKAGE)
  .because("Domain should not depend on adapters (ports and adapters pattern)")
  .check(allClasses)
```
