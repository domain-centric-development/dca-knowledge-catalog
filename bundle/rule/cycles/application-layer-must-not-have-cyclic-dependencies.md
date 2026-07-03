---
type: Rule
title: Application Layer must not have cyclic dependencies
rule: Application services should have clear boundaries and no cycles.
constraint: Application Layer must not have cyclic dependencies.
enforced_by: "PackageCyclesArchUnitTest#Application Layer must not have cyclic dependencies"
status: enforced
test_class: PackageCyclesArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/PackageCyclesArchUnitTest.groovy
tags: [cycles, archunit]
---

```groovy
expect:
slices()
  .matching("${BASE_PACKAGE}.(*).application..")
  .should().beFreeOfCycles()
  .because("Application services should have clear boundaries and no cycles")
  .check(allClasses)
```
