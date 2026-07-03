---
type: Rule
title: Entities must have an ID field
rule: Entities must have an ID field.
constraint: Entities must have an ID field.
enforced_by: "DddTacticalPatternsArchUnitTest#Entities must have an ID field"
status: enforced
test_class: DddTacticalPatternsArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/DddTacticalPatternsArchUnitTest.groovy
tags: [tactical, archunit]
---

```groovy
when:
def entityClasses = allClasses.stream()
  .filter { it.isAssignableTo(Entity.class) }
  .filter { !it.isInterface() }
  .filter { !it.getModifiers().contains(JavaModifier.ABSTRACT) }
  .collect()

def violations = []
entityClasses.each { entityClass ->
  def hasIdField = entityClass.getAllFields().any { field ->
    def fieldName = field.getName().toLowerCase()
    fieldName == "id" || fieldName.endsWith("id")
  }

  if (!hasIdField) {
    violations.add("${entityClass.getName()} appears to have no ID field")
  }
}

then:
if (!violations.isEmpty()) {
  throw new AssertionError(
  "Entities must have an identity field (DDD pattern).\n" +
  "Violations found:\n" + violations.join("\n"))
}
true
```

## Applies to markers

- [Entity<T, ID>](/marker/tactical/entity.md)
