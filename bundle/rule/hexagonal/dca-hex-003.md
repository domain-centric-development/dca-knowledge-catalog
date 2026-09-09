---
type: Rule
id: DCA-HEX-003
title: Controllers and Resources must never access repositories directly
rule: "Controllers must go through use cases (input ports), never directly to repositories."
constraint: Controllers and Resources must never access repositories directly.
selects: Classes anywhere on the classpath under scan whose simple name ends with the configured controller suffix or with the configured REST-controller suffix. Also selected by configured web-controller or REST-controller role annotation; not restricted to adapter packages.
checks: "No dependency on a class assignable to Repository - the port interface or an implementation. Other output ports (Store, event publishers) are not checked; a controller that reaches a repository through another class is not reported. An empty selection passes."
enforced_by: "HexagonalRules#DCA-HEX-003"
status: enforced
rule_set: hexagonal
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/HexagonalRules.java
tags: [hexagonal, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/HexagonalRules.cs
---

# Controllers and Resources must never access repositories directly

## Selection

Classes anywhere on the classpath under scan whose simple name ends with the configured controller suffix or with the configured REST-controller suffix. Also selected by configured web-controller or REST-controller role annotation; not restricted to adapter packages.

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
                .or(
                    AnnotationRoles.annotatedWithAny(
                        layout.frameworkAnnotations().webController(),
                        layout.frameworkAnnotations().restController()))
                .should()
                .dependOnClassesThat()
                .areAssignableTo(Repository.class)
                .allowEmptyShould(true))
    .selecting(
        "Classes anywhere on the classpath under scan whose simple name ends with the"
            + " configured controller suffix or with the configured REST-controller suffix."
            + " Also selected by configured web-controller or REST-controller role annotation; not restricted to adapter packages.")
    .checking(
        "No dependency on a class assignable to Repository - the port interface or an"
            + " implementation. Other output ports (Store, event publishers) are not checked; a"
            + " controller that reaches a repository through another class is not reported. An"
            + " empty selection passes.")
```

## Helpers

### `AnnotationRoles.annotatedWithAny`

```java
/** Directly annotated with any annotation of the role; never true for an empty role. */
  static DescribedPredicate<CanBeAnnotated> annotatedWithAny(List<String> role) {
    if (role.isEmpty()) {
      return DescribedPredicate.<CanBeAnnotated>alwaysFalse()
          .as("annotated with a configured annotation (none configured)");
    }
    DescribedPredicate<CanBeAnnotated> predicate =
        CanBeAnnotated.Predicates.annotatedWith(role.get(0));
    for (String fqn : role.subList(1, role.size())) {
      predicate = predicate.or(CanBeAnnotated.Predicates.annotatedWith(fqn));
    }
    return predicate.as("annotated with any of " + role);
  }

static DescribedPredicate<CanBeAnnotated> annotatedWithAny(List<String>... roles) {
  DescribedPredicate<CanBeAnnotated> predicate = null;
  for (List<String> role : roles) {
    if (role.isEmpty()) {
      continue;
    }
    predicate = predicate == null ? annotatedWithAny(role) : predicate.or(annotatedWithAny(role));
  }
  return predicate == null
      ? DescribedPredicate.<CanBeAnnotated>alwaysFalse()
          .as("annotated with a configured annotation (none configured)")
      : predicate;
}
```
### C# expression

```csharp
DcaRule.Of(
        "DCA-HEX-003",
        "Controllers and Resources must never access repositories directly",
        "Controllers must go through use cases (input ports), never directly to repositories",
        arch => Classes().That().FollowCustomPredicate(c => IsController(c, Layout), "are controllers")
            .Should().NotDependOnAnyTypesThat()
            .FollowCustomPredicate(t => t.IsAssignableTo(typeof(IRepository).FullName!), "are repositories"))
    .Selecting(
        "Controller classes anywhere in the loaded assemblies: a class whose name ends with"
            + " the configured controller suffix or the configured REST-controller suffix, one deriving"
            + " from the configured controller or page-model base class, or one carrying the"
            + " configured API-controller attribute. Not restricted to adapter namespaces.")
    .Checking(
        "No dependency on a type assignable to IRepository - the port interface or an"
            + " implementation. Other output ports (IStore, event publishers) are not checked; a"
            + " controller that reaches a repository through another class is not reported. An"
            + " empty selection passes.")
```

## Related mentions (heuristic)

- [Repository<T, ID>](/marker/port-out/repository.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
