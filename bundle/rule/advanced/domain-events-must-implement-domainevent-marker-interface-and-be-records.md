---
type: Rule
title: Domain Events must implement DomainEvent Marker Interface and be records
rule: "Domain events should be immutable records implementing DomainEvent (named in past tense, e.g., ProductCreated, CartCleared)."
constraint: Domain Events must implement DomainEvent Marker Interface and be records.
enforced_by: "DddAdvancedPatternsArchUnitTest#Domain Events must implement DomainEvent Marker Interface and be records"
status: enforced
test_class: DddAdvancedPatternsArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/DddAdvancedPatternsArchUnitTest.groovy
tags: [advanced, archunit]
---

```groovy
expect:
classes()
  .that().implement(DomainEvent.class)
  .and().areNotInterfaces()
  .should().beRecords()
  .because("Domain events should be immutable records implementing DomainEvent (named in past tense, e.g., ProductCreated, CartCleared)")
  .check(allClasses)
```

## Applies to markers

- [DomainEvent](/marker/tactical/domainevent.md)
