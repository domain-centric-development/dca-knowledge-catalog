---
type: Rule
id: DCA-ADV-017
title: Specifications reside in the domain layer
rule: "A specification is a rule of the model expressed as a predicate; it belongs where the model is, not in the layer that happens to ask the question."
constraint: Specifications reside in the domain layer.
selects: "Non-interface classes anywhere on the classpath under scan that are assignable to the configured specification role or whose simple name ends with Specification, the role's own type and a class named exactly Specification excluded. The marker and the name both select, so a specification named after the predicate it expresses is governed too."
checks: "Each resides in a domain package of some module root (<module>.domain..). An empty selection passes."
enforced_by: "AdvancedPatternRules#DCA-ADV-017"
status: enforced
rule_set: advanced
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/AdvancedPatternRules.java
tags: [advanced, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/AdvancedPatternRules.cs
---

# Specifications reside in the domain layer

## Selection

Non-interface classes anywhere on the classpath under scan that are assignable to the configured specification role or whose simple name ends with Specification, the role's own type and a class named exactly Specification excluded. The marker and the name both select, so a specification named after the predicate it expresses is governed too.

## Check

Each resides in a domain package of some module root (<module>.domain..). An empty selection passes.

## .NET reading

**Selection.** Non-interface types anywhere under scan that are assignable to the configured specification role or whose simple name ends with Specification, the role's own type and a type named exactly Specification excluded. The marker and the name both select, so a specification named after the predicate it expresses is governed too.

**Check.** Each resides in a domain namespace of some module root (<module>.Domain or below). An empty selection passes.

## Implementation

```java
DcaRule.of(
        "DCA-ADV-017",
        "Specifications reside in the domain layer",
        "A specification is a rule of the model expressed as a predicate; it belongs where the"
            + " model is, not in the layer that happens to ask the question",
        arch ->
            classes()
                .that(
                    specifications(
                        arch.layout().markers(), arch.layout().specificationSuffix()))
                .should()
                .resideInAnyPackage(arch.allDomainPatterns())
                .allowEmptyShould(true))
    .selecting(
        "Non-interface classes anywhere on the classpath under scan that are assignable to the"
            + " configured specification role or whose simple name ends with Specification, the"
            + " role's own type and a class named exactly Specification excluded. The marker"
            + " and the name both select, so a specification named after the predicate it"
            + " expresses is governed too.")
    .checking(
        "Each resides in a domain package of some module root (<module>.domain..). An empty selection"
            + " passes.",
        "move the specification into the module's domain package")
```

## Helpers

### `specifications`

```java
/**
   * A specification: assignable to the configured role, or named after the pattern. Both select,
   * because a project may carry the marker without the suffix — as both reference samples do — or
   * the suffix without the marker.
   */
  private static DescribedPredicate<JavaClass> specifications(DcaMarkers markers, String suffix) {
    DescribedPredicate<JavaClass> byRole =
        JavaClass.Predicates.assignableTo(markers.specification());
    DescribedPredicate<JavaClass> byName = JavaClass.Predicates.simpleNameEndingWith(suffix);
    return byRole
        .or(byName)
        .and(DescribedPredicate.not(JavaClass.Predicates.INTERFACES))
        .and(DescribedPredicate.not(JavaClass.Predicates.simpleName(suffix)))
        .and(
            DescribedPredicate.not(
                DescribedPredicate.describe(
                    "the role's own type", c -> c.getName().equals(markers.specification()))))
        .as("specifications");
  }
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allDomainPatterns()`, `layout()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Of(
    "DCA-ADV-017",
    "Specifications reside in the domain layer",
    "A specification is a rule of the model expressed as a predicate; it belongs where the model"
        + " is, not in the layer that happens to ask the question",
    arch => Types()
        .That()
        .FollowCustomPredicate(
            t => t is not Interface
                && t.Name != arch.Layout.SpecificationSuffix
                && t.FullName != arch.Layout.Markers.Specification
                && (IsSpecificationRole(arch, t)
                    || t.Name.EndsWith(arch.Layout.SpecificationSuffix, StringComparison.Ordinal)),
            "are specifications")
        .Should()
        .ResideInNamespaceMatching(DcaLayout.AnyOf(arch.AllDomainPatterns())))
    .Selecting(
        "Non-interface types anywhere under scan that are assignable to the configured "
        + "specification role or whose simple name ends with Specification, the role's own type "
        + "and a type named exactly Specification excluded. The marker and the name both select, "
        + "so a specification named after the predicate it expresses is governed too.")
    .Checking(
        "Each resides in a domain namespace of some module root (<module>.Domain or below). An "
        + "empty selection passes.")
```

## Related mentions (heuristic)

- [Specification<T>](/marker/tactical/specification.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
