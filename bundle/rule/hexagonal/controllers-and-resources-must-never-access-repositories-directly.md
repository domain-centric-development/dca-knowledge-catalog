---
type: Rule
id: DCA-HEX-003
title: Controllers and Resources must never access repositories directly
rule: "Controllers must go through use cases (input ports), never directly to repositories."
constraint: Controllers and Resources must never access repositories directly.
enforced_by: "HexagonalRules#DCA-HEX-003"
status: enforced
rule_set: hexagonal
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/HexagonalRules.java
tags: [hexagonal, archunit]
---

```java
DcaRule.of(
    "DCA-HEX-003",
    "Controllers and Resources must never access repositories directly",
    "Controllers must go through use cases (input ports), never directly to repositories",
    arch ->
        noClasses()
            .that()
            .haveSimpleNameEndingWith("Controller")
            .or()
            .haveSimpleNameEndingWith(layout.restControllerSuffix())
            .should()
            .dependOnClassesThat()
            .areAssignableTo(Repository.class)
            .allowEmptyShould(true))
```

## Applies to markers

- [Repository<T, ID>](/marker/port-out/repository.md)
