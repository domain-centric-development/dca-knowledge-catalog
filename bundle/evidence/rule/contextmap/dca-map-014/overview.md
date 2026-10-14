---
type: Reference
title: Every allowed dependency of a module declaration must be backed by an actual code dependency — Overview
tags: [reference]
evidence_for: /rule/contextmap/dca-map-014.md
---

[Full node and context](/rule/contextmap/dca-map-014.md). This is an evidence excerpt; retain the parent selection and caveats.

# Every allowed dependency of a module declaration must be backed by an actual code dependency

**Experimental.** This rule is binding only in a project that opted in to experimental rules - the architecture test calls `withExperimental()` (.NET: `WithExperimental()`) on its rule selection, or `dca-archunit.properties` sets `dca.rules.experimental = true`; without that opt-in the rule does not run and is information only, never a finding and never a reason to change code.

## Selection

Every package carrying @BoundedContext whose package-info carries a configured and loadable module declaration (a module system's per-package declaration, for example Spring Modulith's), and each entry of its allowedDependencies attribute, read as DCA-MAP-006 reads it. Entries that name an edge of a PLANNED @Upstream declaration, and entries whose module is neither a bounded context nor a module root of the scan, are skipped. Without a configured and loadable module declaration the rule selects nothing and passes.

## Check

For every entry, at least one class anywhere below the declaring context's package has a direct dependency on a class in the named module's package - for 'module :: interface' in its sub-package of that name, for 'module' or 'module :: *' anywhere in the module. A named interface declared on a package of another name is not resolved and is reported as unused. Which layer holds the dependency is not checked here.

## .NET reading

**Selection.** Every namespace carrying [BoundedContext], provided the layout configures at least one module declaration attribute (a module system's per-module declaration) that is in the loaded assemblies; reads, reflectively, the AllowedDependencies entries of every configured module declaration the marker class carries. Entries that name an edge of a Planned [Upstream] declaration, and entries whose module is neither a bounded context nor a module root of the scan, are skipped. Without a configured and loadable module declaration the rule selects nothing and passes - the default here, because .NET draws module boundaries with projects, no preset names an attribute, and the compiler drops a project reference no code uses, so the compiled assemblies carry no stale edge to compare.

**Check.** For every entry - 'module', 'module :: *' or 'module :: named-interface', whitespace around '::' normalized - at least one type below the context namespace has a direct dependency on a type in the named module's namespace (a bounded context by its name, any other module root by its last segment) or, for a named interface, in that segment below it, compared ignoring case. Dependencies within the context itself do not count. Whether an undeclared dependency exists is DCA-MAP-006's and the isolation rules' business, not this rule's.

## Implementation

```java
DcaRule.check(
        "DCA-MAP-014",
        "Every allowed dependency of a module declaration must be backed by an actual code"
            + " dependency",
        "A context declares only the dependencies it uses. An allowed dependency no class"
            + " uses is a door left open: the next dependency through it passes the module"
            + " boundary without anyone deciding it",
        arch -> {
          CollectedViolations violations = CollectedViolations.withoutHeader();
          List<Class<? extends Annotation>> moduleAnnotations = moduleAnnotationTypes();
          if (moduleAnnotations.isEmpty()) {
            return;
          }
          Map<String, String> modules = modulePackagesByName(arch);
          for (String pkg : arch.boundedContextPackages()) {
            String source = arch.contextName(pkg);
            Set<String> planned = plannedEdges(arch, pkg);
            for (String entry : allowedDependencies(arch, pkg, moduleAnnotations)) {
              String normalized = entry.replaceAll("\\s*::\\s*", " :: ").trim();
              if (planned.contains(normalized)) {
                continue;
              }
              String[] parts = normalized.split(" :: ", 2);
              String modulePkg = modules.get(parts[0]);
              if (modulePkg == null || modulePkg.equals(pkg)) {
                continue;
              }
              String target =
                  parts.length == 1 || parts[1].equals("*")
                      ? modulePkg
                      : modulePkg + "." + parts[1];
              violations.require(
                  dependsOnTree(arch, pkg, target),
                  "Context '"
                      + source
                      + "' allows the dependency '"
                      + entry
                      + "' in its module declaration, but no class in '"
                      + pkg
                      + "' depends on '"
                      + target
                      + "..' - remove the entry, or declare the upstream PLANNED if the"
                      + " dependency is coming");
            }
          }
          violations.throwIfAny();
        })
    .experimental()
    .selecting(
        "Every package carrying @BoundedContext whose package-info carries a configured and"
            + " loadable module declaration (a module system's per-package declaration, for"
            + " example Spring Modulith's), and each entry of its allowedDependencies attribute,"
            + " read as DCA-MAP-006 reads it. Entries that name an edge of a PLANNED @Upstream"
            + " declaration, and entries whose module is neither a bounded context nor a module"
            + " root of the scan, are skipped. Without a configured and loadable module"
            + " declaration the rule selects nothing and passes.")
    .checking(
        "For every entry, at least one class anywhere below the declaring context's package"
            + " has a direct dependency on a class in the named module's package - for"
            + " 'module :: interface' in its sub-package of that name, for 'module' or"
            + " 'module :: *' anywhere in the module. A named interface declared on a package"
            + " of another name is not resolved and is reported as unused. Which layer holds"
            + " the dependency is not checked here.",
        "remove the unused entry from allowedDependencies, or declare the upstream PLANNED")
```

## Helpers
