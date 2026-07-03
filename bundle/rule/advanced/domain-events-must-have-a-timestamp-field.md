---
type: Rule
title: Domain Events must have a timestamp field
rule: Domain Events must have a timestamp field.
constraint: Domain Events must have a timestamp field.
enforced_by: "DddAdvancedPatternsArchUnitTest#Domain Events must have a timestamp field"
status: enforced
test_class: DddAdvancedPatternsArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/DddAdvancedPatternsArchUnitTest.groovy
tags: [advanced, archunit]
---

```groovy
when:
def domainEventClasses = allClasses.stream()
  .filter { it.isAssignableTo(DomainEvent.class) }
  .filter { !it.isInterface() }
  .collect()

def violations = []

domainEventClasses.each { eventClass ->
  def hasTimestampField = eventClass.getAllFields().stream()
    .anyMatch { field ->
      field.getRawType().isEquivalentTo(Instant.class) ||
        field.getRawType().isEquivalentTo(LocalDateTime.class) ||
        field.getRawType().isEquivalentTo(ZonedDateTime.class)
    }

  if (!hasTimestampField) {
    violations.add("${eventClass.getName()} does not have a timestamp field")
  }
}

then:
if (!violations.isEmpty()) {
  throw new AssertionError(
  "Domain Events must have a timestamp field (when did the event occur?):\n" +
  violations.join("\n")
  )
}
true
```

## Applies to markers

- [DomainEvent](/marker/tactical/domainevent.md)
