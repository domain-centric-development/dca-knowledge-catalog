---
type: Rule
title: Value Objects must not contain Aggregate Roots or Entities
rule: Value Objects must not contain Aggregate Roots or Entities.
constraint: Value Objects must not contain Aggregate Roots or Entities.
enforced_by: "DddTacticalPatternsArchUnitTest#Value Objects must not contain Aggregate Roots or Entities"
status: enforced
test_class: DddTacticalPatternsArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/DddTacticalPatternsArchUnitTest.groovy
tags: [tactical, archunit]
---

```groovy
when:
def valueObjectClasses = allClasses.stream()
  .filter { it.isAssignableTo(Value.class) }
  .filter { !it.isInterface() }
  .collect()

def violations = []
valueObjectClasses.each { voClass ->
  voClass.getAllFields().each { field ->
    def fieldType = field.getRawType()

    if (fieldType.isAssignableTo(AggregateRoot.class) &&
      !fieldType.isInterface()) {
      violations.add("${voClass.getName()} has field '${field.getName()}' of type ${fieldType.getName()} which is an aggregate root")
    }

    if (fieldType.isAssignableTo(Entity.class) &&
      !fieldType.isAssignableTo(AggregateRoot.class) &&
      !fieldType.isInterface()) {
      violations.add("${voClass.getName()} has field '${field.getName()}' of type ${fieldType.getName()} which is an entity")
    }

    if (field.getRawType().getName().startsWith("java.util.List") ||
      field.getRawType().getName().startsWith("java.util.Set") ||
      field.getRawType().getName().startsWith("java.util.Collection")) {
      field.getType().getActualTypeArguments().each { typeArg ->
        def erasure = typeArg.toErasure()

        if (erasure.isAssignableTo(AggregateRoot.class) &&
          !erasure.isInterface()) {
          violations.add("${voClass.getName()} has field '${field.getName()}' containing ${typeArg.getName()} which is an aggregate root")
        }

        if (erasure.isAssignableTo(Entity.class) &&
          !erasure.isAssignableTo(AggregateRoot.class) &&
          !erasure.isInterface()) {
          violations.add("${voClass.getName()} has field '${field.getName()}' containing ${typeArg.getName()} which is an entity")
        }
      }
    }
  }
}

then:
if (!violations.isEmpty()) {
  throw new AssertionError(
  "Value Objects must only contain other Value Objects or primitives (Vernon's DDD).\n" +
  "Violations found:\n" + violations.join("\n"))
}
true
```

## Applies to markers

- [AggregateRoot<T, ID>](/marker/tactical/aggregateroot.md)
- [Entity<T, ID>](/marker/tactical/entity.md)
- [Value](/marker/tactical/value.md)
