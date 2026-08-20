---
type: Rule
title: Repository methods must not return non-root Entities
rule: Repository methods must not return non-root Entities.
constraint: Repository methods must not return non-root Entities.
enforced_by: "DddTacticalPatternsArchUnitTest#Repository methods must not return non-root Entities"
status: enforced
test_class: DddTacticalPatternsArchUnitTest
resource: dca-ecommerce-sample/src/test-architecture/groovy/de/sample/aiarchitecture/DddTacticalPatternsArchUnitTest.groovy
tags: [tactical, archunit]
---

```groovy
when:
// The prohibition, not a positive requirement. A repository may legitimately return a
// boolean, a count, a page wrapper or a Value Object composed for one use case (Vernon's
// use-case optimal query). What it must never hand out is an Entity that is not an
// Aggregate Root: the caller could then mutate a part of an aggregate without going
// through the root, and the root's invariants would never run.
//
// The type parameter side needs no rule — the compiler pins it via
// Repository<T extends AggregateRoot<T, ID>, ID extends Id>. Only method returns are open.
def repositoryInterfaces = allClasses.stream()
  .filter { it.isAssignableTo(Repository.class) }
  .filter { it.isInterface() }
  .filter { !it.getSimpleName().equals("Repository") }
  .collect()

def violations = []
repositoryInterfaces.each { repoInterface ->
  repoInterface.getMethods().each { method ->
    typesInvolvedIn(method.getReturnType()).each { type ->
      if (type.isAssignableTo(Entity.class) && !type.isAssignableTo(AggregateRoot.class)) {
        violations.add("${repoInterface.getName()}.${method.getName()} exposes ${type.getName()}, an Entity that is not an Aggregate Root")
      }
    }
  }
}

then:
if (!violations.isEmpty()) {
  throw new AssertionError(
  "Repository methods must not expose an Entity that is not an Aggregate Root: a caller " +
  "could mutate part of an aggregate without passing its root (DDD pattern).\n" +
  "Violations found:\n" + violations.join("\n"))
}
true
```

## Applies to markers

- [Repository<T, ID>](/marker/port-out/repository.md)
- [AggregateRoot<T, ID>](/marker/tactical/aggregateroot.md)
- [Entity<T, ID>](/marker/tactical/entity.md)
- [Id](/marker/tactical/id.md)
