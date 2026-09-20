---
type: Rule
id: DCA-STR-011
title: At least one bounded context is declared
rule: Without a declared context the context-map and isolation rules select nothing and report success over an empty model.
constraint: At least one bounded context is declared.
selects: "The declared bounded contexts of the imported classes — every package whose package-info carries @BoundedContext, at any depth below the base package. No individual class is reported."
checks: "At least one such package exists. The rule says nothing about how many contexts there should be, about their boundaries, or about modules that own a layer without declaring a context — those are governed structurally and are not a substitute for the declaration."
enforced_by: "StrategicPatternRules#DCA-STR-011"
status: enforced
rule_set: strategic
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/StrategicPatternRules.java
tags: [strategic, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/StrategicPatternRules.cs
---

# At least one bounded context is declared

## Selection

The declared bounded contexts of the imported classes — every package whose package-info carries @BoundedContext, at any depth below the base package. No individual class is reported.

## Check

At least one such package exists. The rule says nothing about how many contexts there should be, about their boundaries, or about modules that own a layer without declaring a context — those are governed structurally and are not a substitute for the declaration.

## .NET reading

**Selection.** The declared bounded contexts of the imported types — every namespace carrying a [BoundedContext] marker class, at any depth below the root namespace. No individual type is reported.

**Check.** At least one such namespace exists. The rule says nothing about how many contexts there should be, about their boundaries, or about modules that own a layer without declaring a context — those are governed structurally and are not a substitute for the declaration.

## Implementation

```java
DcaRule.check(
        "DCA-STR-011",
        "At least one bounded context is declared",
        "Without a declared context the context-map and isolation rules select nothing and"
            + " report success over an empty model",
        arch -> {
          if (arch.boundedContexts().isEmpty()) {
            throw new DcaRuleViolation(
                "No package below the base package '"
                    + arch.layout().basePackage()
                    + "' declares @BoundedContext, so every rule that selects over the"
                    + " discovered contexts passes without having looked at anything.",
                List.of(
                    "Declare the context: a package-info.java carrying @BoundedContext in the"
                        + " root package of each context — a single-context application"
                        + " annotates its base package.",
                    "In a multi-module build, check that the module running the architecture"
                        + " test depends on every module that holds a context.",
                    "A code base that deliberately declares no context switches this rule off"
                        + " with a recorded reason; the structural isolation rules keep"
                        + " governing the modules."));
          }
        })
    .selecting(
        "The declared bounded contexts of the imported classes — every package whose"
            + " package-info carries @BoundedContext, at any depth below the base package. No"
            + " individual class is reported.")
    .checking(
        "At least one such package exists. The rule says nothing about how many contexts there"
            + " should be, about their boundaries, or about modules that own a layer without"
            + " declaring a context — those are governed structurally and are not a substitute"
            + " for the declaration.")
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `boundedContexts()`, `layout()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Check(
        "DCA-STR-011",
        "At least one bounded context is declared",
        "Without a declared context the context-map and isolation rules select nothing and report success"
            + " over an empty model",
        arch =>
        {
            if (arch.BoundedContexts.Count > 0)
            {
                return;
            }

            throw DcaRuleViolationException.Of(
                $"No namespace below the root namespace '{arch.Layout.RootNamespace}' declares "
                    + "[BoundedContext], so every rule that selects over the discovered contexts passes "
                    + "without having looked at anything.",
                new[]
                {
                    "Declare the context: a marker class carrying [BoundedContext] directly in the root "
                        + "namespace of each context — a single-context application annotates its root namespace.",
                    "In a multi-project build, check that the test project references every project that holds "
                        + "a context and passes its assembly to Load.",
                    "A code base that deliberately declares no context switches this rule off with a recorded "
                        + "reason; the structural isolation rules keep governing the modules.",
                });
        })
    .Selecting(
        "The declared bounded contexts of the imported types — every namespace carrying a [BoundedContext]"
            + " marker class, at any depth below the root namespace. No individual type is reported.")
    .Checking(
        "At least one such namespace exists. The rule says nothing about how many contexts there should be,"
            + " about their boundaries, or about modules that own a layer without declaring a context — those"
            + " are governed structurally and are not a substitute for the declaration.")
```

## Related mentions (heuristic)

- [@BoundedContext](/marker/strategic/boundedcontext.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
