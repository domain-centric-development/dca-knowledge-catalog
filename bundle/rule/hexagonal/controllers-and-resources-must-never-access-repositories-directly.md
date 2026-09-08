---
type: Rule
id: DCA-HEX-003
title: Controllers and Resources must never access repositories directly
rule: "Controllers must go through use cases (input ports), never directly to repositories."
constraint: Controllers and Resources must never access repositories directly.
selects: "Classes anywhere on the classpath under scan whose simple name ends with the configured controller suffix or with the configured REST-controller suffix. Selected by name, not by annotation, and not restricted to adapter packages."
checks: "No dependency on a class assignable to Repository - the port interface or an implementation. Other output ports (Store, event publishers) are not checked; a controller that reaches a repository through another class is not reported. An empty selection passes."
enforced_by: "HexagonalRules#DCA-HEX-003"
status: enforced
rule_set: hexagonal
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/HexagonalRules.java
tags: [hexagonal, archunit]
---

## Selection

Classes anywhere on the classpath under scan whose simple name ends with the configured controller suffix or with the configured REST-controller suffix. Selected by name, not by annotation, and not restricted to adapter packages.

## Check

No dependency on a class assignable to Repository - the port interface or an implementation. Other output ports (Store, event publishers) are not checked; a controller that reaches a repository through another class is not reported. An empty selection passes.

## .NET reading

**Selection.** Controller classes anywhere in the loaded assemblies: a class whose name ends with the configured controller suffix or the configured REST-controller suffix, one deriving from the configured controller or page-model base class, or one carrying the configured API-controller attribute. Not restricted to adapter namespaces.

**Check.** No dependency on a type assignable to IRepository - the port interface or an implementation. Other output ports (IStore, event publishers) are not checked; a controller that reaches a repository through another class is not reported. An empty selection passes.

## Implementation

```java
DcaRule.of(
        "DCA-HEX-003",
        "Controllers and Resources must never access repositories directly",
        "Controllers must go through use cases (input ports), never directly to repositories",
        arch ->
            noClasses()
                .that()
                .haveSimpleNameEndingWith(layout.controllerSuffix())
                .or()
                .haveSimpleNameEndingWith(layout.restControllerSuffix())
                .should()
                .dependOnClassesThat()
                .areAssignableTo(Repository.class)
                .allowEmptyShould(true))
    .selecting(
        "Classes anywhere on the classpath under scan whose simple name ends with the"
            + " configured controller suffix or with the configured REST-controller suffix."
            + " Selected by name, not by annotation, and not restricted to adapter packages.")
    .checking(
        "No dependency on a class assignable to Repository - the port interface or an"
            + " implementation. Other output ports (Store, event publishers) are not checked; a"
            + " controller that reaches a repository through another class is not reported. An"
            + " empty selection passes.")
```

## Applies to markers

- [Repository<T, ID>](/marker/port-out/repository.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
