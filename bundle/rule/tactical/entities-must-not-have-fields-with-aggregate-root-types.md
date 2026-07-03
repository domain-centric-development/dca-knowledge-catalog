---
type: Rule
title: Entities must not have fields with Aggregate Root types
rule: Entities must not have fields with Aggregate Root types.
constraint: Entities must not have fields with Aggregate Root types.
enforced_by: "DddTacticalPatternsArchUnitTest#Entities must not have fields with Aggregate Root types"
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
  .filter { !it.isAssignableTo(AggregateRoot.class) }
  .collect()

def violations = []
entityClasses.each { entityClass ->
  entityClass.getAllFields().each { field ->
    def fieldType = field.getRawType()

    if (fieldType.isAssignableTo(AggregateRoot.class) &&
      !fieldType.isInterface()) {
      violations.add("${entityClass.getName()} has field '${field.getName()}' of type ${fieldType.getName()} which is an aggregate root")
    }

    if (field.getRawType().getName().startsWith("java.util.List") ||
      field.getRawType().getName().startsWith("java.util.Set") ||
      field.getRawType().getName().startsWith("java.util.Collection")) {
      field.getType().getActualTypeArguments().each { typeArg ->
        if (typeArg.toErasure().isAssignableTo(AggregateRoot.class) &&
          !typeArg.toErasure().isInterface()) {
          violations.add("${entityClass.getName()} has field '${field.getName()}' containing ${typeArg.getName()} which is an aggregate root")
        }
      }
    }
  }
}

then:
if (!violations.isEmpty()) {
  throw new AssertionError(
  "Entities must not contain references to aggregate roots (reference by ID only).\n" +
  "Violations found:\n" + violations.join("\n"))
}
true
```

## Applies to markers

- [AggregateRoot<T, ID>](/marker/tactical/aggregateroot.md)
- [Entity<T, ID>](/marker/tactical/entity.md)
