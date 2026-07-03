---
type: Rule
title: Integration Events should be immutable records
rule: "Integration Events must be immutable to ensure event integrity across contexts (Event Sourcing best practice)."
constraint: Integration Events should be immutable records.
enforced_by: "DddStrategicPatternsArchUnitTest#Integration Events should be immutable records"
status: enforced
test_class: DddStrategicPatternsArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/DddStrategicPatternsArchUnitTest.groovy
tags: [strategic, archunit]
---

```groovy
expect:
// Integration Events must be immutable to prevent corruption after publishing
// Java records provide immutability by default
classes()
  .that().implement(IntegrationEvent)
  .should().beRecords()
  .allowEmptyShould(true)
  .because("Integration Events must be immutable to ensure event integrity across contexts (Event Sourcing best practice)")
  .check(allClasses)
```

## Applies to markers

- [IntegrationEvent](/marker/tactical/integrationevent.md)
