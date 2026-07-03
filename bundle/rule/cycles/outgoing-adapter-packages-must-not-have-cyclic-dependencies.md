---
type: Rule
title: Outgoing Adapter Packages must not have cyclic dependencies
rule: Outgoing adapters should have clear boundaries and no cycles.
constraint: Outgoing Adapter Packages must not have cyclic dependencies.
enforced_by: "PackageCyclesArchUnitTest#Outgoing Adapter Packages must not have cyclic dependencies"
status: enforced
test_class: PackageCyclesArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/PackageCyclesArchUnitTest.groovy
tags: [cycles, archunit]
---

```groovy
expect:
slices()
  .matching("${BASE_PACKAGE}.(*).adapter.outgoing..")
  .should().beFreeOfCycles()
  .because("Outgoing adapters should have clear boundaries and no cycles")
  .check(allClasses)
```
