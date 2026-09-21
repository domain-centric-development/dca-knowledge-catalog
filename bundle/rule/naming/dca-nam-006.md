---
type: Rule
id: DCA-NAM-006
title: "REST Controllers must end with 'Resource' (REST best practice)"
rule: Classes carrying the REST-controller stereotype should end with 'Resource' following RESTful naming conventions.
constraint: "REST Controllers must end with 'Resource' (REST best practice)."
selects: "Classes in <module>.adapter.incoming.. of every module root that are directly annotated with one of the configured REST-controller stereotypes."
checks: "The simple name ends with the configured REST-controller suffix. Classes annotated only with a web-controller stereotype are not selected, and a REST controller outside an incoming-adapter package is not checked. An empty selection passes - which is always the case when the role is empty."
enforced_by: "NamingRules#DCA-NAM-006"
status: enforced
rule_set: naming
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/NamingRules.java
tags: [naming, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/NamingRules.cs
---

# REST Controllers must end with 'Resource' (REST best practice)

## Selection

Classes in <module>.adapter.incoming.. of every module root that are directly annotated with one of the configured REST-controller stereotypes.

## Check

The simple name ends with the configured REST-controller suffix. Classes annotated only with a web-controller stereotype are not selected, and a REST controller outside an incoming-adapter package is not checked. An empty selection passes - which is always the case when the role is empty.

## .NET reading

**Selection.** Classes in <module>.Adapter.Incoming of every module root that carry the configured API-controller attribute ([ApiController] by default).

**Check.** The name ends with the configured REST-controller suffix. Controllers without the attribute are not selected, and an API controller outside an incoming-adapter namespace is not checked. An empty selection passes.

## Implementation

```java
DcaRule.of(
        "DCA-NAM-006",
        "REST Controllers must end with '"
            + layout.restControllerSuffix()
            + "' (REST best practice)",
        "Classes carrying the REST-controller stereotype should end with '"
            + layout.restControllerSuffix()
            + "' following RESTful naming conventions",
        arch ->
            classes()
                .that()
                .resideInAnyPackage(arch.allIncomingAdapterPatterns())
                .and(
                    AnnotationRoles.annotatedWithAny(
                        layout.frameworkAnnotations().restController()))
                .should()
                .haveSimpleNameEndingWith(layout.restControllerSuffix())
                .allowEmptyShould(true))
    .selecting(
        "Classes in <module>.adapter.incoming.. of every module root that are directly"
            + " annotated with one of the configured REST-controller stereotypes.")
    .checking(
        "The simple name ends with the configured REST-controller suffix. Classes annotated"
            + " only with a web-controller stereotype are not selected, and a REST controller"
            + " outside an incoming-adapter package is not checked. An empty selection"
            + " passes - which is always the case when the role is empty.",
        "rename the class to *" + layout.restControllerSuffix())
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
        "DCA-NAM-006",
        $"REST Controllers must end with '{layout.RestControllerSuffix}' (REST best practice)",
        $"[ApiController] classes should end with '{layout.RestControllerSuffix}' following RESTful naming conventions",
        arch =>
        {
            var violations = arch.Classes
                .Where(c => InNamespace(c, DcaLayout.AnyOf(arch.AllIncomingAdapterPatterns()))
                    && IsApiController(arch, c)
                    && !c.Name.EndsWith(arch.Layout.RestControllerSuffix, StringComparison.Ordinal))
                .Select(c => $"{c.FullName} is an API controller but does not end with '{arch.Layout.RestControllerSuffix}'")
                .ToList();
            DcaRule.Fail(
                $"REST Controllers must end with '{arch.Layout.RestControllerSuffix}'",
                violations,
                $"rename the class to *{arch.Layout.RestControllerSuffix}");
        })
    .Selecting(
        "Classes in <module>.Adapter.Incoming of every module root that carry the"
            + " configured API-controller attribute ([ApiController] by default).")
    .Checking(
        "The name ends with the configured REST-controller suffix. Controllers without the"
            + " attribute are not selected, and an API controller outside an incoming-adapter"
            + " namespace is not checked. An empty selection passes.")
```

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
