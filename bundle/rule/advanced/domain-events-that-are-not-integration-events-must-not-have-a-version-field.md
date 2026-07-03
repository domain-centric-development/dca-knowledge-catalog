---
type: Rule
title: Domain Events that are not Integration Events must not have a version field
rule: Domain Events that are not Integration Events must not have a version field.
constraint: Domain Events that are not Integration Events must not have a version field.
enforced_by: "DddAdvancedPatternsArchUnitTest#Domain Events that are not Integration Events must not have a version field"
status: enforced
test_class: DddAdvancedPatternsArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/DddAdvancedPatternsArchUnitTest.groovy
tags: [advanced, archunit]
---

```groovy
when:
def domainOnlyEventClasses = allClasses.stream()
  .filter { it.isAssignableTo(DomainEvent.class) }
  .filter { !it.isAssignableTo(IntegrationEvent.class) }
  .filter { !it.isInterface() }
  .collect()

def violations = []

domainOnlyEventClasses.each { eventClass ->
  def hasVersionField = eventClass.getAllFields().stream()
    .anyMatch { field ->
      field.getName() == "version"
    }

  if (hasVersionField) {
    violations.add("${eventClass.getName()} has a version field but is not an IntegrationEvent — only IntegrationEvents need versioning")
  }
}

then:
if (!violations.isEmpty()) {
  throw new AssertionError(
  "Domain Events (non-IntegrationEvent) must not have a version field — versioning is only for IntegrationEvents:\n" +
  violations.join("\n")
  )
}
true
```

## Applies to markers

- [DomainEvent](/marker/tactical/domainevent.md)
- [IntegrationEvent](/marker/tactical/integrationevent.md)
