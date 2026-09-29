---
type: Rule
id: DCA-MAP-006
title: Upstream declarations and the module declaration's allowed dependencies must agree
rule: Neither the context map nor the module boundary may know more than the other — an edge that exists only on one side is stale.
constraint: Upstream declarations and the module declaration's allowed dependencies must agree.
selects: "Every package carrying @BoundedContext, provided the layout configures at least one module declaration annotation (a module system's per-package declaration, for example Spring Modulith's) that is on the class path; reads its @Upstream declarations (context(), via(); PLANNED included) and, reflectively, the allowedDependencies attribute of every configured and loadable module declaration the package carries. Without a configured and loadable module declaration the rule selects nothing and passes."
checks: "The set of declared edges 'context :: channel' equals the set of allowedDependencies entries of the form 'module :: named-interface' whose module is a bounded context, whitespace around '::' normalized. Entries without '::' and entries naming a non-context module are ignored. A context that declares @Upstream edges but whose package-info carries none of the configured module declaration annotations is reported once, as a missing module declaration with unknown allowed dependencies - its edges are not compared; a context without @Upstream declarations and without a module declaration has nothing to compare and passes."
enforced_by: "ContextMapRules#DCA-MAP-006"
status: enforced
rule_set: contextmap
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/ContextMapRules.java
tags: [contextmap, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/ContextMapRules.cs
---

# Upstream declarations and the module declaration's allowed dependencies must agree

## Selection

Every package carrying @BoundedContext, provided the layout configures at least one module declaration annotation (a module system's per-package declaration, for example Spring Modulith's) that is on the class path; reads its @Upstream declarations (context(), via(); PLANNED included) and, reflectively, the allowedDependencies attribute of every configured and loadable module declaration the package carries. Without a configured and loadable module declaration the rule selects nothing and passes.

## Check

The set of declared edges 'context :: channel' equals the set of allowedDependencies entries of the form 'module :: named-interface' whose module is a bounded context, whitespace around '::' normalized. Entries without '::' and entries naming a non-context module are ignored. A context that declares @Upstream edges but whose package-info carries none of the configured module declaration annotations is reported once, as a missing module declaration with unknown allowed dependencies - its edges are not compared; a context without @Upstream declarations and without a module declaration has nothing to compare and passes.

## .NET reading

**Selection.** Every namespace carrying [BoundedContext], provided the layout configures at least one module declaration attribute (a module system's per-module declaration) that is in the loaded assemblies; reads its [Upstream] declarations (Context, Via; Planned included) and, reflectively, the AllowedDependencies property of every configured module declaration the marker class carries. Without a configured and loadable module declaration the rule selects nothing and passes - which is the default here, because .NET draws module boundaries with projects and no preset names an attribute.

**Check.** The set of declared edges 'context :: channel' equals the set of AllowedDependencies entries of the form 'module :: named-interface' whose module is a bounded context, whitespace around '::' normalized. Entries without '::' and entries naming a non-context module are ignored. A context that declares [Upstream] edges but whose marker class carries none of the configured module declaration attributes is reported once, as a missing module declaration with unknown allowed dependencies - its edges are not compared; a context without [Upstream] declarations and without a module declaration has nothing to compare and passes.

## Implementation

The verbatim ArchUnit expression is in the evidence slice [Overview](/evidence/rule/contextmap/dca-map-006/overview.md); every helper it calls has a slice of its own, listed under *Evidence slices* below.

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `boundedContextPackages()`, `contextName()`, `layout()`, `packageAnnotation()`, `packageAnnotations()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).

## Related mentions (heuristic)

- [@BoundedContext](/marker/strategic/boundedcontext.md)
- [@Upstream](/marker/strategic/upstream.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)

## Evidence slices

- [Overview](/evidence/rule/contextmap/dca-map-006/overview.md)
- [`moduleAnnotationTypes`](/evidence/rule/contextmap/dca-map-006/moduleannotationtypes.md)
- [`moduleNames`](/evidence/rule/contextmap/dca-map-006/modulenames.md)
- [`declaredEdges`](/evidence/rule/contextmap/dca-map-006/declarededges.md)
- [`carriesModuleDeclaration`](/evidence/rule/contextmap/dca-map-006/carriesmoduledeclaration.md)
- [`allowedDependencies`](/evidence/rule/contextmap/dca-map-006/alloweddependencies.md)
- [`CollectedViolations.check`](/evidence/rule/contextmap/dca-map-006/collectedviolations-check.md)
- [`CollectedViolations.withoutHeader`](/evidence/rule/contextmap/dca-map-006/collectedviolations-withoutheader.md)
- [`CollectedViolations.isEmpty`](/evidence/rule/contextmap/dca-map-006/collectedviolations-isempty.md)
- [`CollectedViolations.add`](/evidence/rule/contextmap/dca-map-006/collectedviolations-add.md)
- [`CollectedViolations.require`](/evidence/rule/contextmap/dca-map-006/collectedviolations-require.md)
- [`CollectedViolations.throwIfAny`](/evidence/rule/contextmap/dca-map-006/collectedviolations-throwifany.md)
- [`channelName`](/evidence/rule/contextmap/dca-map-006/channelname.md)
- [`CollectedViolations.addAll`](/evidence/rule/contextmap/dca-map-006/collectedviolations-addall.md)
- [C# expression](/evidence/rule/contextmap/dca-map-006/c-expression.md)
