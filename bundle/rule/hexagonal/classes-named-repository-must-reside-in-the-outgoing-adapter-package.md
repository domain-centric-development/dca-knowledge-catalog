---
type: Rule
title: "Classes named *Repository must reside in the outgoing adapter package"
rule: "Repository implementations are secondary adapters (outgoing ports)."
constraint: "Classes named *Repository must reside in the outgoing adapter package."
enforced_by: "HexagonalArchitectureArchUnitTest#Classes named *Repository must reside in the outgoing adapter package"
status: enforced
test_class: HexagonalArchitectureArchUnitTest
resource: dca-ecommerce-sample/src/test-architecture/groovy/de/sample/aiarchitecture/HexagonalArchitectureArchUnitTest.groovy
tags: [hexagonal, archunit]
---

```groovy
expect:
ArchRuleDefinition.classes()
  .that().haveSimpleNameEndingWith("Repository")
  .and().areNotInterfaces()
  .should().resideInAPackage(OUTGOING_ADAPTER_PACKAGE)
  .because("Repository implementations are secondary adapters (outgoing ports)")
  .check(allClasses)
```

## Applies to markers

- [Repository<T, ID>](/marker/port-out/repository.md)
