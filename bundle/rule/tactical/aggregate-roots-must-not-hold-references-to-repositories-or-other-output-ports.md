---
type: Rule
id: DCA-TAC-002
title: Aggregate Roots must not hold references to Repositories or other Output Ports
rule: "Aggregates are persistence-ignorant: repositories and services are passed as method parameters by the use case, never injected as fields."
constraint: Aggregate Roots must not hold references to Repositories or other Output Ports.
enforced_by: "TacticalPatternRules#DCA-TAC-002"
status: enforced
rule_set: tactical
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/TacticalPatternRules.java
tags: [tactical, archunit]
---

```java
DcaRule.check(
    "DCA-TAC-002",
    "Aggregate Roots must not hold references to Repositories or other Output Ports",
    "Aggregates are persistence-ignorant: repositories and services are passed as method"
        + " parameters by the use case, never injected as fields",
    arch -> {
      List<String> violations = new ArrayList<>();
      for (JavaClass aggregate : concreteClassesAssignableTo(arch, AggregateRoot.class)) {
        for (JavaField field : aggregate.getAllFields()) {
          JavaClass fieldType = field.getRawType();
          if (fieldType.isAssignableTo(Repository.class)
              || fieldType.isAssignableTo(OutputPort.class)) {
            violations.add(
                aggregate.getName()
                    + " has field '"
                    + field.getName()
                    + "' of type "
                    + fieldType.getName()
                    + " which is a repository/output port");
          }
        }
      }
      fail(
          "Aggregates must not have injected repositories or output ports - pass dependencies"
              + " as method parameters.",
          violations);
    })
```

## Applies to markers

- [OutputPort](/marker/port-out/outputport.md)
- [Repository<T, ID>](/marker/port-out/repository.md)
- [AggregateRoot<T, ID>](/marker/tactical/aggregateroot.md)
