---
type: Rule
id: DCA-STR-001
title: "Diagnostic: Display discovered bounded contexts"
rule: Making the discovered contexts visible shows which packages the strategic rules govern.
constraint: "Diagnostic: Display discovered bounded contexts."
selects: "Every package whose package-info carries @BoundedContext, at any depth below the base package, plus the package annotated with @SharedKernel if there is one. Modules that own layers without declaring @BoundedContext are not listed."
checks: "Diagnostic - reports each discovered context's name, package and description and the shared kernel package in the rule's own outcome. It asserts nothing and never fails."
enforced_by: "StrategicPatternRules#DCA-STR-001"
status: informational
rule_set: strategic
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/StrategicPatternRules.java
tags: [strategic, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/StrategicPatternRules.cs
---

# Diagnostic: Display discovered bounded contexts

## Selection

Every package whose package-info carries @BoundedContext, at any depth below the base package, plus the package annotated with @SharedKernel if there is one. Modules that own layers without declaring @BoundedContext are not listed.

## Check

Diagnostic - reports each discovered context's name, package and description and the shared kernel package in the rule's own outcome. It asserts nothing and never fails.

## .NET reading

**Selection.** Every namespace whose marker class carries [BoundedContext], at any depth below the root namespace, plus the namespace whose marker class carries [SharedKernel] if there is one. Modules that own layers without declaring [BoundedContext] are not listed.

**Check.** Diagnostic - reports each discovered context's name, namespace and description and the shared kernel namespace in the rule's own outcome. It asserts nothing and never fails.

## Implementation

```java
DcaRule.informational(
        "DCA-STR-001",
        "Diagnostic: Display discovered bounded contexts",
        "Making the discovered contexts visible shows which packages the strategic rules govern",
        arch -> {
          List<String> observed = new ArrayList<>();
          for (Map.Entry<String, BoundedContext> e : arch.boundedContexts().entrySet()) {
            String description =
                e.getValue().description().isEmpty() ? "" : " - " + e.getValue().description();
            observed.add(e.getValue().name() + ": " + e.getKey() + description);
          }
          observed.add("shared kernel: " + arch.sharedKernelPackage().orElse("<none>"));
          return observed;
        })
    .selecting(
        "Every package whose package-info carries @BoundedContext, at any depth below the base"
            + " package, plus the package annotated with @SharedKernel if there is one. Modules"
            + " that own layers without declaring @BoundedContext are not listed.")
    .checking(
        "Diagnostic - reports each discovered context's name, package and description and the"
            + " shared kernel package in the rule's own outcome. It asserts nothing and never fails.")
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `boundedContexts()`, `sharedKernelPackage()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Informational(
        "DCA-STR-001",
        "Diagnostic: Display discovered bounded contexts",
        "Making the discovered contexts visible shows which namespaces the strategic rules govern",
        arch =>
        {
            var observed = new List<string>();
            foreach (var e in arch.BoundedContexts)
            {
                var description = e.Value.Description.Length > 0 ? " - " + e.Value.Description : "";
                observed.Add(e.Value.Name + ": " + e.Key + description);
            }

            observed.Add("shared kernel: " + (arch.SharedKernelNamespace ?? "<none>"));
            return observed;
        })
    .Selecting(
        "Every namespace whose marker class carries [BoundedContext], at any depth below the root"
            + " namespace, plus the namespace whose marker class carries [SharedKernel] if there is one."
            + " Modules that own layers without declaring [BoundedContext] are not listed.")
    .Checking(
        "Diagnostic - reports each discovered context's name, namespace and description and the"
            + " shared kernel namespace in the rule's own outcome. It asserts nothing and never fails.")
```

## Related mentions (heuristic)

- [@BoundedContext](/marker/strategic/boundedcontext.md)
- [@SharedKernel](/marker/strategic/sharedkernel.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
