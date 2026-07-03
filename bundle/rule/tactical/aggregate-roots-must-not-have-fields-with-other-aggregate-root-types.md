---
type: Rule
title: Aggregate Roots must not have fields with other Aggregate Root types
rule: Aggregate Roots must not have fields with other Aggregate Root types.
constraint: Aggregate Roots must not have fields with other Aggregate Root types.
enforced_by: "DddTacticalPatternsArchUnitTest#Aggregate Roots must not have fields with other Aggregate Root types"
status: enforced
test_class: DddTacticalPatternsArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/DddTacticalPatternsArchUnitTest.groovy
tags: [tactical, archunit]
---

```groovy
expect:
// This test enforces Vaughn Vernon's Aggregate Design Rule #2:
// "Reference other Aggregates by Identity"
// An aggregate should not hold direct references to other aggregate roots,
// only their IDs. This maintains aggregate boundaries and transaction consistency.

def aggregateRootClasses = allClasses.stream()
  .filter { it.isAssignableTo(AggregateRoot.class) }
  .filter { !it.isInterface() }
  .collect()

def violations = []
aggregateRootClasses.each { aggregateClass ->
  aggregateClass.getAllFields().each { field ->
    def fieldType = field.getRawType()

    // Check if field type implements AggregateRoot
    if (fieldType.isAssignableTo(AggregateRoot.class) &&
      !fieldType.equals(aggregateClass) &&  // Allow self-reference
      !fieldType.isInterface()) {
      violations.add("${aggregateClass.getName()} has field '${field.getName()}' of type ${fieldType.getName()} which is another aggregate root")
    }

    // Check collections/arrays of aggregate roots
    if (field.getRawType().getName().startsWith("java.util.List") ||
      field.getRawType().getName().startsWith("java.util.Set") ||
      field.getRawType().getName().startsWith("java.util.Collection")) {
      // Check generic type parameter
      field.getType().getActualTypeArguments().each { typeArg ->
        if (typeArg.toErasure().isAssignableTo(AggregateRoot.class) &&
          !typeArg.toErasure().isInterface()) {
          violations.add("${aggregateClass.getName()} has field '${field.getName()}' containing ${typeArg.getName()} which is an aggregate root")
        }
      }
    }
  }
}

if (!violations.isEmpty()) {
  throw new AssertionError(
  "Aggregates must reference other aggregates by ID only (Vernon's Rule #2).\n" +
  "Violations found:\n" + violations.join("\n"))
}

true
```

## Applies to markers

- [AggregateRoot<T, ID>](/marker/tactical/aggregateroot.md)
