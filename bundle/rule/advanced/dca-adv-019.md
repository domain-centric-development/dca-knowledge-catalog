---
type: Rule
id: DCA-ADV-019
title: "Aggregates, entities and value objects must not use domain services"
rule: "A domain service exists for logic that spans several aggregates, so the application calls it; a model type that reaches for one would drive another aggregate from inside its own."
constraint: "Aggregates, entities and value objects must not use domain services."
selects: "Classes anywhere on the classpath under scan that carry the aggregate-root, entity or value role."
checks: "None of them calls a method of, reads a field of, or instantiates a type carrying the domain-service role. Holding one as a parameter or a field type is not an access and is not reported. A domain service calling another domain service is outside this selection. An empty selection passes."
enforced_by: "AdvancedPatternRules#DCA-ADV-019"
status: enforced
rule_set: advanced
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/AdvancedPatternRules.java
tags: [advanced, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/AdvancedPatternRules.cs
---

# Aggregates, entities and value objects must not use domain services

## Selection

Classes anywhere on the classpath under scan that carry the aggregate-root, entity or value role.

## Check

None of them calls a method of, reads a field of, or instantiates a type carrying the domain-service role. Holding one as a parameter or a field type is not an access and is not reported. A domain service calling another domain service is outside this selection. An empty selection passes.

## .NET reading

**Selection.** Types anywhere under scan that carry the aggregate-root, entity or value role.

**Check.** None of them calls a method of, or constructs, a type carrying the domain-service role. Holding one as a parameter or a field type is not a call and is not reported. A domain service calling another domain service is outside this selection. An empty selection passes.

## Implementation

```java
DcaRule.of(
        "DCA-ADV-019",
        "Aggregates, entities and value objects must not use domain services",
        "A domain service exists for logic that spans several aggregates, so the application"
            + " calls it; a model type that reaches for one would drive another aggregate from"
            + " inside its own",
        arch ->
            noClasses()
                .that()
                .areAssignableTo(arch.layout().markers().aggregateRoot())
                .or()
                .areAssignableTo(arch.layout().markers().entity())
                .or()
                .areAssignableTo(arch.layout().markers().value())
                .should()
                .accessClassesThat()
                .areAssignableTo(arch.layout().markers().domainService())
                .allowEmptyShould(true))
    .selecting(
        "Classes anywhere on the classpath under scan that carry the aggregate-root, entity or"
            + " value role.")
    .checking(
        "None of them calls a method of, reads a field of, or instantiates a type carrying the"
            + " domain-service role. Holding one as a parameter or a field type is not an"
            + " access and is not reported. A domain service calling another domain service is"
            + " outside this selection. An empty selection passes.",
        "let the use case call the domain service and hand the model the result")
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `layout()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Check(
    "DCA-ADV-019",
    "Aggregates, entities and value objects must not use domain services",
    "A domain service exists for logic that spans several aggregates, so the application calls it; "
        + "a model type that reaches for one would drive another aggregate from inside its own",
    arch =>
    {
        var violations = new List<string>();
        foreach (var type in arch.Types.Where(t => IsModelType(arch, t)))
        {
            foreach (var target in type.Dependencies
                .Where(d => d is MethodCallDependency)
                .Select(d => d.Target)
                .Distinct())
            {
                if (target.IsAssignableTo(arch.Layout.Markers.DomainService))
                {
                    violations.Add($"{type.FullName} uses {target.FullName}");
                }
            }
        }

        DcaRule.Fail("A model type reaches for a domain service", violations.Distinct().ToList(),
            "let the use case call the domain service and hand the model the result");
    })
    .Selecting("Types anywhere under scan that carry the aggregate-root, entity or value role.")
    .Checking(
        "None of them calls a method of, or constructs, a type carrying the domain-service role. "
        + "Holding one as a parameter or a field type is not a call and is not reported. A domain "
        + "service calling another domain service is outside this selection. An empty selection passes.")
```

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
