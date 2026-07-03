---
type: Rule
title: Domain Packages must not have cyclic dependencies
rule: "Domain model packages should have clear boundaries and no cycles (Acyclic Dependencies Principle)."
constraint: Domain Packages must not have cyclic dependencies.
enforced_by: "PackageCyclesArchUnitTest#Domain Packages must not have cyclic dependencies"
status: enforced
test_class: PackageCyclesArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/PackageCyclesArchUnitTest.groovy
tags: [cycles, archunit]
---

```groovy
expect:
slices()
  .matching("${BASE_PACKAGE}.(*).domain.model..")
  .should().beFreeOfCycles()
  .because("Domain model packages should have clear boundaries and no cycles (Acyclic Dependencies Principle)")
  .check(allClasses)
```
