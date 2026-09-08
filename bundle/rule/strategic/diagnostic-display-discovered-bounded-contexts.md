---
type: Rule
id: DCA-STR-001
title: "Diagnostic: Display discovered bounded contexts"
rule: Making the discovered contexts visible shows which packages the strategic rules govern.
constraint: "Diagnostic: Display discovered bounded contexts."
selects: "Every package whose package-info carries @BoundedContext, at any depth below the base package, plus the package annotated with @SharedKernel if there is one. Modules that own layers without declaring @BoundedContext are not listed."
checks: "Diagnostic - prints each discovered context's name, package and description and the shared kernel package to standard output. It asserts nothing and never fails."
enforced_by: "StrategicPatternRules#DCA-STR-001"
status: informational
rule_set: strategic
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/StrategicPatternRules.java
tags: [strategic, archunit]
---

## Selection

Every package whose package-info carries @BoundedContext, at any depth below the base package, plus the package annotated with @SharedKernel if there is one. Modules that own layers without declaring @BoundedContext are not listed.

## Check

Diagnostic - prints each discovered context's name, package and description and the shared kernel package to standard output. It asserts nothing and never fails.

## .NET reading

**Selection.** Every namespace whose marker class carries [BoundedContext], at any depth below the root namespace, plus the namespace whose marker class carries [SharedKernel] if there is one. Modules that own layers without declaring [BoundedContext] are not listed.

**Check.** Diagnostic - prints each discovered context's name, namespace and description and the shared kernel namespace to standard output. It asserts nothing and never fails.

## Implementation

```java
DcaRule.check(
        "DCA-STR-001",
        "Diagnostic: Display discovered bounded contexts",
        "Making the discovered contexts visible shows which packages the strategic rules govern",
        arch -> {
          System.out.println("=== Discovered Bounded Contexts ===");
          for (Map.Entry<String, BoundedContext> e : arch.boundedContexts().entrySet()) {
            System.out.println("  " + e.getValue().name() + ": " + e.getKey());
            if (!e.getValue().description().isEmpty()) {
              System.out.println("    Description: " + e.getValue().description());
            }
          }
          System.out.println("=== Shared Kernel ===");
          System.out.println("  Package: " + arch.sharedKernelPackage().orElse("<none>"));
          System.out.println("==================================");
        })
    .selecting(
        "Every package whose package-info carries @BoundedContext, at any depth below the base"
            + " package, plus the package annotated with @SharedKernel if there is one. Modules"
            + " that own layers without declaring @BoundedContext are not listed.")
    .checking(
        "Diagnostic - prints each discovered context's name, package and description and the"
            + " shared kernel package to standard output. It asserts nothing and never fails.")
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `boundedContexts()`, `sharedKernelPackage()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).

## Applies to markers

- [@BoundedContext](/marker/strategic/boundedcontext.md)
- [@SharedKernel](/marker/strategic/sharedkernel.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
