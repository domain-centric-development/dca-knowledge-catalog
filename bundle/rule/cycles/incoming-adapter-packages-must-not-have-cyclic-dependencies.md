---
type: Rule
title: Incoming Adapter Packages must not have cyclic dependencies
rule: Incoming adapters should have clear boundaries and no cycles.
constraint: Incoming Adapter Packages must not have cyclic dependencies.
enforced_by: "PackageCyclesArchUnitTest#Incoming Adapter Packages must not have cyclic dependencies"
status: enforced
test_class: PackageCyclesArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/PackageCyclesArchUnitTest.groovy
tags: [cycles, archunit]
---

```groovy
expect:
slices()
  .matching("${BASE_PACKAGE}.(*).adapter.incoming..")
  .should().beFreeOfCycles()
  .because("Incoming adapters should have clear boundaries and no cycles")
  .check(allClasses)
```
