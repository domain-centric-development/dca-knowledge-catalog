---
type: Rule
title: Entities must have an ID field
rule: Entities must have an ID field.
constraint: Entities must have an ID field.
enforced_by: "DddTacticalPatternsArchUnitTest#Entities must have an ID field"
status: enforced
test_class: DddTacticalPatternsArchUnitTest
resource: dca-ecommerce-sample/src/test-architecture/groovy/de/sample/aiarchitecture/DddTacticalPatternsArchUnitTest.groovy
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
  // Matched by type, not by name: the old check accepted any field whose lowercased name
  // ended in "id", so valid, paid and uuid satisfied it while no identity existed. An
  // identity is a value object implementing the Id marker.
  def hasIdField = entityClass.getAllFields().any { field ->
    field.getRawType().isAssignableTo(ID_MARKER)
  }

  if (!hasIdField) {
    violations.add("${entityClass.getName()} has no field whose type implements ${ID_MARKER.simpleName}")
  }
}

then:
if (!violations.isEmpty()) {
  throw new AssertionError(
  "Entities must have an identity field typed as an Id value object (DDD pattern).\n" +
  "Violations found:\n" + violations.join("\n"))
}
true
```

## Applies to markers

- [Entity<T, ID>](/marker/tactical/entity.md)
