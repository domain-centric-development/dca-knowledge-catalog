---
type: Rule
title: Integration Events must be annotated with IntegrationEventType
rule: "@IntegrationEventType(name, version) is the contract identity of every ."
constraint: Integration Events must be annotated with IntegrationEventType.
enforced_by: "DddAdvancedPatternsArchUnitTest#Integration Events must be annotated with IntegrationEventType"
status: enforced
test_class: DddAdvancedPatternsArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/DddAdvancedPatternsArchUnitTest.groovy
tags: [advanced, archunit]
---

```groovy
expect:
// The annotation carries the stable logical name + schema version as a class property —
// the single source of truth for an event's contract identity (see ADR-027).
classes()
  .that().areAssignableTo(IntegrationEvent.class)
  .and().areNotInterfaces()
  .should().beAnnotatedWith(IntegrationEventType.class)
  .because("@IntegrationEventType(name, version) is the contract identity of every " +
           "integration event — the serializer keys (name, version) to the class and stamps " +
           "both onto the wire envelope")
  .allowEmptyShould(true)
  .check(allClasses)
```

## Applies to markers

- [IntegrationEvent](/marker/tactical/integrationevent.md)
- [@IntegrationEventType](/marker/tactical/integrationeventtype.md)
