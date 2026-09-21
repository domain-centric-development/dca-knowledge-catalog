---
type: Reference
title: Upstream declarations and the module declaration's allowed dependencies must agree — Overview
tags: [reference]
evidence_for: /rule/contextmap/dca-map-006.md
---

[Full node and context](/rule/contextmap/dca-map-006.md). This is an evidence excerpt; retain the parent selection and caveats.

# Upstream declarations and the module declaration's allowed dependencies must agree

## Selection

Every package carrying @BoundedContext, provided the layout configures at least one module declaration annotation (a module system's per-package declaration, for example Spring Modulith's) that is on the class path; reads its @Upstream declarations (context(), via(); PLANNED included) and, reflectively, the allowedDependencies attribute of every configured and loadable module declaration the package carries. Without a configured and loadable module declaration the rule selects nothing and passes.

## Check

The set of declared edges 'context :: channel' equals the set of allowedDependencies entries of the form 'module :: named-interface' whose module is a bounded context, whitespace around '::' normalized. Entries without '::' and entries naming a non-context module are ignored. A context that declares @Upstream edges but whose package-info carries none of the configured module declaration annotations is reported once, as a missing module declaration with unknown allowed dependencies - its edges are not compared; a context without @Upstream declarations and without a module declaration has nothing to compare and passes.

## .NET reading

**Selection.** Every namespace carrying [BoundedContext], provided the layout configures at least one module declaration attribute (a module system's per-module declaration) that is in the loaded assemblies; reads its [Upstream] declarations (Context, Via; Planned included) and, reflectively, the AllowedDependencies property of every configured module declaration the marker class carries. Without a configured and loadable module declaration the rule selects nothing and passes - which is the default here, because .NET draws module boundaries with projects and no preset names an attribute.

**Check.** The set of declared edges 'context :: channel' equals the set of AllowedDependencies entries of the form 'module :: named-interface' whose module is a bounded context, whitespace around '::' normalized. Entries without '::' and entries naming a non-context module are ignored. A context that declares [Upstream] edges but whose marker class carries none of the configured module declaration attributes is reported once, as a missing module declaration with unknown allowed dependencies - its edges are not compared; a context without [Upstream] declarations and without a module declaration has nothing to compare and passes.

## Implementation

```java
DcaRule.check(
        "DCA-MAP-006",
        "Upstream declarations and the module declaration's allowed dependencies must agree",
        "Neither the context map nor the module boundary may know more than the other — an edge"
            + " that exists only on one side is stale",
        arch -> {
          CollectedViolations violations = CollectedViolations.withoutHeader();
          List<Class<? extends Annotation>> moduleAnnotations = moduleAnnotationTypes();
          if (moduleAnnotations.isEmpty()) {
            return;
          }
          Set<String> moduleNames = moduleNames(arch);
          for (String pkg : arch.boundedContextPackages()) {
            String source = arch.contextName(pkg);
            Set<String> declared = declaredEdges(arch, pkg);
            if (!declared.isEmpty()
                && !carriesModuleDeclaration(arch, pkg, moduleAnnotations)) {
              violations.add(
                  "Context '"
                      + source
                      + "': module declaration missing on '"
                      + source
                      + "', allowed dependencies unknown - it declares @Upstream edges "
                      + new TreeSet<>(declared)
                      + " but its package-info carries none of the configured module"
                      + " declaration annotations; declare the module there so both sides can"
                      + " be compared");
              continue;
            }
            Set<String> allowed = new LinkedHashSet<>();
            for (String entry : allowedDependencies(arch, pkg, moduleAnnotations)) {
              String normalized = entry.replaceAll("\\s*::\\s*", " :: ").trim();
              if (normalized.contains(" :: ")
                  && moduleNames.contains(normalized.split(" :: ")[0])) {
                allowed.add(normalized);
              }
            }
            violations.require(
                declared.equals(allowed),
                "Context '"
                    + source
                    + "': @Upstream declarations "
                    + new TreeSet<>(declared)
                    + " and the module declaration's allowedDependencies named-interface entries "
                    + new TreeSet<>(allowed)
                    + " must describe the same edges — neither side may know more than the other");
          }
          violations.throwIfAny();
        })
    .selecting(
        "Every package carrying @BoundedContext, provided the layout configures at least one"
            + " module declaration annotation (a module system's per-package declaration, for"
            + " example Spring Modulith's) that is on the class path; reads its @Upstream"
            + " declarations (context(), via(); PLANNED included) and, reflectively, the"
            + " allowedDependencies attribute of every configured and loadable module"
            + " declaration the package carries. Without a configured and loadable module"
            + " declaration the rule selects nothing and passes.")
    .checking(
        "The set of declared edges 'context :: channel' equals the set of"
            + " allowedDependencies entries of the form 'module :: named-interface' whose"
            + " module is a bounded context, whitespace around '::' normalized. Entries"
            + " without '::' and entries naming a non-context module are ignored. A context"
            + " that declares @Upstream edges but whose package-info carries none of the"
            + " configured module declaration annotations is reported once, as a missing"
            + " module declaration with unknown allowed dependencies - its edges are not"
            + " compared; a context without @Upstream declarations and without a module"
            + " declaration has nothing to compare and passes.")
```

## Helpers
