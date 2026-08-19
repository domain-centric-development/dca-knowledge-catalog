---
type: Rule
title: Value Objects must be records
rule: "A Value Object is defined by its attributes, which a record gives for free: ."
constraint: Value Objects must be records.
enforced_by: "DddTacticalPatternsArchUnitTest#Value Objects must be records"
status: enforced
test_class: DddTacticalPatternsArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/DddTacticalPatternsArchUnitTest.groovy
tags: [tactical, archunit]
---

```groovy
expect:
// Was a tautology: "records in the domain model should reside in the domain model", which
// passes for any codebase. The real rule is ADR-009 — a Value Object is a record, so the
// compiler grants immutability and attribute equality instead of a rule having to check them.
classes()
  .that().areAssignableTo(VALUE_MARKER)
  .and().areNotInterfaces()
  .and().areNotEnums()
  .should().beRecords()
  .because("A Value Object is defined by its attributes, which a record gives for free: "
  + "final components, attribute-based equality and no identity (ADR-009). An enum is "
  + "already a fixed set of immutable values and needs no record.")
  .allowEmptyShould(true)
  .check(allClasses)
```
