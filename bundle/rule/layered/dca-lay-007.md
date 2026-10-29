---
type: Rule
id: DCA-LAY-007
title: "Diagnostic: classes of a module that sit in no layer"
rule: "Every rule written for a layer selects by the layer a class is placed in. A class of a module that sits in none - a mapper or a persistence entity beside the adapter packages, a class whose layer is declared only on its neighbour - is seen by none of them."
constraint: "Diagnostic: classes of a module that sit in no layer."
selects: "Classes under a module root, below its own package, that the layout places in no layer - neither by a layer annotation on the class or a package above it nor by the package path. Not selected: classes directly in the module root's package, the published packages (api, events) of a module and its own infrastructure package - the shared kernel's included, which is shared support rather than a layer."
checks: "Informational - lists every selected class and never fails. Place each in a layer: move it into the layer package it belongs to, or declare its package's layer."
enforced_by: "LayeredRules#DCA-LAY-007"
status: informational
maturity: experimental
rule_set: layered
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/LayeredRules.java
tags: [layered, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/LayeredRules.cs
---

# Diagnostic: classes of a module that sit in no layer

**Experimental.** This rule is binding only in a project that opted in to experimental rules - the architecture test calls `withExperimental()` (.NET: `WithExperimental()`) on its rule selection, or `dca-archunit.properties` sets `dca.rules.experimental = true`; without that opt-in the rule does not run and is information only, never a finding and never a reason to change code.

## Selection

Classes under a module root, below its own package, that the layout places in no layer - neither by a layer annotation on the class or a package above it nor by the package path. Not selected: classes directly in the module root's package, the published packages (api, events) of a module and its own infrastructure package - the shared kernel's included, which is shared support rather than a layer.

## Check

Informational - lists every selected class and never fails. Place each in a layer: move it into the layer package it belongs to, or declare its package's layer.

## .NET reading

**Selection.** Types under a module root, below its own namespace, that the layout places in no layer - neither by a layer attribute on the type, its namespace or its assembly nor by the namespace path; compiler-generated types are not selected. Not selected: types directly in the module root's namespace, the published namespaces (Api, Events) of a module and its own Infrastructure namespace - the shared kernel's included, which is shared support rather than a layer.

**Check.** Informational - lists every selected type and never fails. Place each in a layer: move it into the layer namespace it belongs to, or declare its namespace's layer.

## Implementation

```java
DcaRule.informational(
        "DCA-LAY-007",
        "Diagnostic: classes of a module that sit in no layer",
        "Every rule written for a layer selects by the layer a class is placed in. A class of a"
            + " module that sits in none - a mapper or a persistence entity beside the adapter"
            + " packages, a class whose layer is declared only on its neighbour - is seen by"
            + " none of them",
        arch -> {
          java.util.Set<String> published =
              new java.util.HashSet<>(arch.layout().publishedSubpackages());
          List<String> observed = new java.util.ArrayList<>();
          for (JavaClass type : arch.classes()) {
            String pkg = type.getPackageName();
            String root =
                arch.moduleRoots().stream()
                    .filter(r -> DcaArchitecture.inPackageTree(pkg, r))
                    .max(java.util.Comparator.comparingInt(String::length))
                    .orElse(null);
            if (root == null
                || pkg.equals(root)
                || type.getSimpleName().equals("package-info")
                || type.getModifiers()
                    .contains(com.tngtech.archunit.core.domain.JavaModifier.SYNTHETIC)
                || arch.placement(type).isPresent()) {
              continue;
            }
            String below = pkg.substring(root.length() + 1).split("\\.")[0];
            if (published.contains(below)
                || below.equals(arch.layout().infrastructureSubpackage())) {
              continue;
            }
            observed.add(type.getName() + " (module " + root + ")");
          }
          return observed.stream().sorted().toList();
        })
    .experimental()
    .selecting(
        "Classes under a module root, below its own package, that the layout places in no layer"
            + " - neither by a layer annotation on the class or a package above it nor by the"
            + " package path. Not selected: classes directly in the module root's package, the"
            + " published packages (api, events) of a module and its own infrastructure package"
            + " - the shared kernel's included, which is shared support rather than a layer.")
    .checking(
        "Informational - lists every selected class and never fails. Place each in a layer:"
            + " move it into the layer package it belongs to, or declare its package's layer.")
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `classes()`, `layout()`, `moduleRoots()`, `placement()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Informational(
    "DCA-LAY-007",
    "Diagnostic: types of a module that sit in no layer",
    "Every rule written for a layer selects by the layer a type is placed in. A type of a module that sits"
        + " in none - a mapper or a persistence entity beside the adapter namespaces, a type whose layer is"
        + " declared only on its neighbour - is seen by none of them",
    arch =>
    {
        var published = new HashSet<string>(arch.Layout.PublishedSegments, StringComparer.Ordinal);
        var roots = arch.ModuleRoots();
        var observed = new List<string>();
        foreach (var type in arch.Types.Where(t => !t.IsCompilerGenerated))
        {
            var ns = type.Namespace?.FullName ?? "";
            var root = roots.Where(r => DcaLayout.IsBelow(ns, r)).OrderByDescending(r => r.Length).FirstOrDefault();
            if (root is null || ns == root || arch.PlacementOf(type) is not null)
            {
                continue;
            }

            var below = ns.Substring(root.Length + 1).Split('.')[0];
            if (published.Contains(below) || below == arch.Layout.InfrastructureSegment)
            {
                continue;
            }

            observed.Add($"{type.FullName} (module {root})");
        }

        return observed.OrderBy(o => o, StringComparer.Ordinal).ToList();
    })
    .Experimental()
    .Selecting(
        "Types under a module root, below its own namespace, that the layout places in no layer - neither by a"
        + " layer attribute on the type, its namespace or its assembly nor by the namespace path; compiler-"
        + "generated types are not selected. Not selected: types directly in the module root's namespace,"
        + " the published namespaces (Api, Events) of a module and its own Infrastructure namespace - the"
        + " shared kernel's included, which is shared support rather than a layer.")
    .Checking(
        "Informational - lists every selected type and never fails. Place each in a layer: move it into the"
        + " layer namespace it belongs to, or declare its namespace's layer.")
```

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
