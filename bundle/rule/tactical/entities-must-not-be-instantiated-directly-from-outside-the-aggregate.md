---
type: Rule
title: Entities must not be instantiated directly from outside the aggregate
rule: Entities must not be instantiated directly from outside the aggregate.
constraint: Entities must not be instantiated directly from outside the aggregate.
enforced_by: "DddTacticalPatternsArchUnitTest#Entities must not be instantiated directly from outside the aggregate"
status: enforced
test_class: DddTacticalPatternsArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/DddTacticalPatternsArchUnitTest.groovy
tags: [tactical, archunit]
---

```groovy
when:
// Entities (except Aggregate Roots) should not have public constructors
// They should only be created through their aggregate root
// This enforces aggregate boundaries and ensures invariants

def entityClasses = allClasses.stream()
  .filter { it.isAssignableTo(Entity.class) }
  .filter { !it.isAssignableTo(AggregateRoot.class) }  // Exclude aggregate roots
  .filter { !it.isInterface() }
  .filter { !it.isRecord() }  // Records always have public constructors
  .collect()

def violations = []
entityClasses.each { entityClass ->
  entityClass.getConstructors().each { constructor ->
    if (constructor.getModifiers().contains(JavaModifier.PUBLIC)) {
      violations.add("${entityClass.getName()} has public constructor - should be package-private or protected")
    }
  }
}

then:
if (!violations.isEmpty()) {
  throw new AssertionError(
  "Entities should not have public constructors (access only through aggregate root).\n" +
  "Note: Records are excluded from this rule.\n" +
  "Violations found:\n" + violations.join("\n"))
}
true
```

## Applies to markers

- [AggregateRoot<T, ID>](/marker/tactical/aggregateroot.md)
- [Entity<T, ID>](/marker/tactical/entity.md)
