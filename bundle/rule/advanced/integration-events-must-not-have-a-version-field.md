---
type: Rule
title: Integration Events must not have a version field
rule: Integration Events must not have a version field.
constraint: Integration Events must not have a version field.
enforced_by: "DddAdvancedPatternsArchUnitTest#Integration Events must not have a version field"
status: enforced
test_class: DddAdvancedPatternsArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/DddAdvancedPatternsArchUnitTest.groovy
tags: [advanced, archunit]
---

```groovy
when:
// The schema version is a class property (@IntegrationEventType), never per-instance
// payload data — a version data field duplicates the annotation and can drift from it.
def violations = allClasses
  .findAll { it.isAssignableTo(IntegrationEvent.class) && !it.isInterface() }
  .findAll { eventClass ->
    eventClass.getAllFields().stream().anyMatch { it.getName() == "version" }
  }
  .collect { "${it.getName()} carries a version data field — declare the version in @IntegrationEventType instead" }

then:
if (!violations.isEmpty()) {
  throw new AssertionError(
  "Integration Events must not have a version field — @IntegrationEventType is the single source of truth:\n" +
  violations.join("\n")
  )
}
true
```

## Applies to markers

- [IntegrationEvent](/marker/tactical/integrationevent.md)
- [@IntegrationEventType](/marker/tactical/integrationeventtype.md)
