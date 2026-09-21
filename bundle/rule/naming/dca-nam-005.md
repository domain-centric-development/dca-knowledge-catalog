---
type: Rule
id: DCA-NAM-005
title: Controller classes must end with 'Controller'
rule: Classes carrying the web-controller stereotype should follow naming conventions.
constraint: Controller classes must end with 'Controller'.
selects: "Classes in <module>.adapter.incoming.. of every module root that are directly annotated with one of the configured web-controller stereotypes."
checks: "The simple name ends with the configured controller suffix (default Controller). A class carrying only a REST-controller stereotype is not selected here, and a controller outside an incoming-adapter package is not checked. An empty selection passes - which is always the case when the role is empty."
enforced_by: "NamingRules#DCA-NAM-005"
status: enforced
rule_set: naming
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/NamingRules.java
tags: [naming, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/NamingRules.cs
---

# Controller classes must end with 'Controller'

## Selection

Classes in <module>.adapter.incoming.. of every module root that are directly annotated with one of the configured web-controller stereotypes.

## Check

The simple name ends with the configured controller suffix (default Controller). A class carrying only a REST-controller stereotype is not selected here, and a controller outside an incoming-adapter package is not checked. An empty selection passes - which is always the case when the role is empty.

## .NET reading

**Selection.** Classes in <module>.Adapter.Incoming of every module root that derive from the configured controller base class without carrying the configured API-controller attribute, or that derive from the configured page-model base class.

**Check.** The name ends with the configured controller suffix (default Controller). A class carrying the API-controller attribute is not selected here, and a controller outside an incoming-adapter namespace is not checked. An empty selection passes.

## Implementation

```java
DcaRule.of(
        "DCA-NAM-005",
        "Controller classes must end with '" + layout.controllerSuffix() + "'",
        "Classes carrying the web-controller stereotype should follow naming conventions",
        arch ->
            classes()
                .that()
                .resideInAnyPackage(arch.allIncomingAdapterPatterns())
                .and(
                    AnnotationRoles.annotatedWithAny(
                        layout.frameworkAnnotations().webController()))
                .should()
                .haveSimpleNameEndingWith(layout.controllerSuffix())
                .allowEmptyShould(true))
    .selecting(
        "Classes in <module>.adapter.incoming.. of every module root that are directly"
            + " annotated with one of the configured web-controller stereotypes.")
    .checking(
        "The simple name ends with the configured controller suffix (default Controller). A"
            + " class carrying only a REST-controller stereotype is not selected here, and a"
            + " controller outside an incoming-adapter package is not checked. An empty"
            + " selection passes - which is always the case when the role is empty.",
        "rename the class to *" + layout.controllerSuffix())
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

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allIncomingAdapterPatterns()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Check(
        "DCA-NAM-005",
        $"Controller classes must end with '{layout.ControllerSuffix}'",
        "MVC controller and page model classes should follow naming conventions",
        arch =>
        {
            var violations = arch.Classes
                .Where(c => InNamespace(c, DcaLayout.AnyOf(arch.AllIncomingAdapterPatterns()))
                    && IsMvcController(arch, c)
                    && !c.Name.EndsWith(arch.Layout.ControllerSuffix, StringComparison.Ordinal))
                .Select(c => $"{c.FullName} is a controller but does not end with '{arch.Layout.ControllerSuffix}'")
                .ToList();
            DcaRule.Fail($"Controller classes must end with '{arch.Layout.ControllerSuffix}'", violations, $"rename the class to *{arch.Layout.ControllerSuffix}");
        })
    .Selecting(
        "Classes in <module>.Adapter.Incoming of every module root that derive from the"
            + " configured controller base class without carrying the configured API-controller"
            + " attribute, or that derive from the configured page-model base class.")
    .Checking(
        "The name ends with the configured controller suffix (default Controller). A"
            + " class carrying the API-controller attribute is not selected here, and a"
            + " controller outside an incoming-adapter namespace is not checked. An empty"
            + " selection passes.")
```

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
