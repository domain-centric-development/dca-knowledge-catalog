---
type: Rule
title: Aggregate Roots must not hold references to Repositories or other Output Ports
rule: Aggregate Roots must not hold references to Repositories or other Output Ports.
constraint: Aggregate Roots must not hold references to Repositories or other Output Ports.
enforced_by: "DddTacticalPatternsArchUnitTest#Aggregate Roots must not hold references to Repositories or other Output Ports"
status: enforced
test_class: DddTacticalPatternsArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/DddTacticalPatternsArchUnitTest.groovy
tags: [tactical, archunit]
---

```groovy
when:
// Aggregates must be persistence-ignorant: dependencies like repositories or
// domain services are looked up by the use case and passed as method parameters,
// never injected as fields (Vernon, IDDD Ch10; Wrox PPP-DDD).

def aggregateRootClasses = allClasses.stream()
  .filter { it.isAssignableTo(AggregateRoot.class) }
  .filter { !it.isInterface() }
  .collect()

def violations = []
aggregateRootClasses.each { aggregateClass ->
  aggregateClass.getAllFields().each { field ->
    def fieldType = field.getRawType()
    if (fieldType.isAssignableTo(REPOSITORY_MARKER) || fieldType.isAssignableTo(OUTPUT_PORT_MARKER)) {
      violations.add("${aggregateClass.getName()} has field '${field.getName()}' of type ${fieldType.getName()} which is a repository/output port")
    }
  }
}

then:
if (!violations.isEmpty()) {
  throw new AssertionError(
  "Aggregates must not have injected repositories or output ports - pass dependencies as method parameters.\n" +
  "Violations found:\n" + violations.join("\n"))
}
true
```

## Applies to markers

- [OutputPort](/marker/port-out/outputport.md)
- [Repository<T, ID>](/marker/port-out/repository.md)
- [AggregateRoot<T, ID>](/marker/tactical/aggregateroot.md)
