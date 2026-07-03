---
type: Rule
title: Repository methods must return Aggregate Roots
rule: Repository methods must return Aggregate Roots.
constraint: Repository methods must return Aggregate Roots.
enforced_by: "DddTacticalPatternsArchUnitTest#Repository methods must return Aggregate Roots"
status: enforced
test_class: DddTacticalPatternsArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/DddTacticalPatternsArchUnitTest.groovy
tags: [tactical, archunit]
---

```groovy
when:
// Repository methods should return Aggregate Roots or collections of Aggregate Roots
// Not entities or value objects

def repositoryInterfaces = allClasses.stream()
  .filter { it.isAssignableTo(Repository.class) }
  .filter { it.isInterface() }
  .filter { !it.getSimpleName().equals("Repository") }
  .collect()

def violations = []
repositoryInterfaces.each { repoInterface ->
  repoInterface.getMethods().each { method ->
    def returnType = method.getRawReturnType()

    // Skip void methods (like save, delete operations)
    if (returnType.getName() == "void") {
      return
    }

    // Skip methods that return primitives, Optional, or common Java types
    if (returnType.isPrimitive() ||
      returnType.getName().startsWith("java.lang") ||
      returnType.getName().startsWith("java.util.Optional")) {
      return
    }

    // Check if return type is a collection
    if (returnType.getName().startsWith("java.util.List") ||
      returnType.getName().startsWith("java.util.Set") ||
      returnType.getName().startsWith("java.util.Collection")) {
      // Check generic type parameter
      method.getRawReturnType().tryGetComponentType().ifPresent { componentType ->
        if (componentType.isAssignableTo(Entity.class) &&
          !componentType.isAssignableTo(AggregateRoot.class)) {
          violations.add("${repoInterface.getName()}.${method.getName()} returns collection of ${componentType.getName()} which is an Entity but not an Aggregate Root")
        }
      }
    } else {
      // Check if direct return type is an Entity but not Aggregate Root
      if (returnType.isAssignableTo(Entity.class) &&
        !returnType.isAssignableTo(AggregateRoot.class) &&
        !returnType.isInterface()) {
        violations.add("${repoInterface.getName()}.${method.getName()} returns ${returnType.getName()} which is an Entity but not an Aggregate Root")
      }
    }
  }
}

then:
if (!violations.isEmpty()) {
  throw new AssertionError(
  "Repository methods should return Aggregate Roots, not Entities (DDD pattern).\n" +
  "Violations found:\n" + violations.join("\n"))
}
true
```

## Applies to markers

- [Repository<T, ID>](/marker/port-out/repository.md)
- [AggregateRoot<T, ID>](/marker/tactical/aggregateroot.md)
- [Entity<T, ID>](/marker/tactical/entity.md)
