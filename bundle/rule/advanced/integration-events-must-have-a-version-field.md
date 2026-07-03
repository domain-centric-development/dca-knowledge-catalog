---
type: Rule
title: Integration Events must have a version field
rule: Integration Events must have a version field.
constraint: Integration Events must have a version field.
enforced_by: "DddAdvancedPatternsArchUnitTest#Integration Events must have a version field"
status: enforced
test_class: DddAdvancedPatternsArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/DddAdvancedPatternsArchUnitTest.groovy
tags: [advanced, archunit]
---

```groovy
when:
def integrationEventClasses = allClasses.stream()
  .filter { it.isAssignableTo(IntegrationEvent.class) }
  .filter { !it.isInterface() }
  .collect()

def violations = []

integrationEventClasses.each { eventClass ->
  def hasVersionField = eventClass.getAllFields().stream()
    .anyMatch { field ->
      field.getName() == "version" && field.getRawType().isEquivalentTo(int.class)
    }

  if (!hasVersionField) {
    violations.add("${eventClass.getName()} does not have an int version field")
  }
}

then:
if (!violations.isEmpty()) {
  throw new AssertionError(
  "Integration Events must have an int version field for backward-compatible schema evolution:\n" +
  violations.join("\n")
  )
}
true
```

## Applies to markers

- [IntegrationEvent](/marker/tactical/integrationevent.md)
