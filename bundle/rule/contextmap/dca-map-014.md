---
type: Rule
id: DCA-MAP-014
title: Every allowed dependency of a module declaration must be backed by an actual code dependency
rule: "A context declares only the dependencies it uses. An allowed dependency no class uses is a door left open: the next dependency through it passes the module boundary without anyone deciding it."
constraint: Every allowed dependency of a module declaration must be backed by an actual code dependency.
selects: "Every package carrying @BoundedContext whose package-info carries a configured and loadable module declaration (a module system's per-package declaration, for example Spring Modulith's), and each entry of its allowedDependencies attribute, read as DCA-MAP-006 reads it. Entries that name an edge of a PLANNED @Upstream declaration, and entries whose module is neither a bounded context nor a module root of the scan, are skipped. Without a configured and loadable module declaration the rule selects nothing and passes."
checks: "For every entry, at least one class anywhere below the declaring context's package has a direct dependency on a class in the named module's package - for 'module :: interface' in its sub-package of that name, for 'module' or 'module :: *' anywhere in the module. A named interface declared on a package of another name is not resolved and is reported as unused. Which layer holds the dependency is not checked here."
enforced_by: "ContextMapRules#DCA-MAP-014"
status: enforced
maturity: experimental
rule_set: contextmap
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/ContextMapRules.java
tags: [contextmap, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/ContextMapRules.cs
---

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

The verbatim ArchUnit expression is in the evidence slice [Overview](/evidence/rule/contextmap/dca-map-014/overview.md); every helper it calls has a slice of its own, listed under *Evidence slices* below.

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `boundedContextPackages()`, `classes()`, `contextName()`, `layout()`, `moduleRoots()`, `packageAnnotation()`, `packageAnnotations()`, `sharedKernelPackage()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).

## Related mentions (heuristic)

- [@BoundedContext](/marker/strategic/boundedcontext.md)
- [@Upstream](/marker/strategic/upstream.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)

## Evidence slices

- [Overview](/evidence/rule/contextmap/dca-map-014/overview.md)
- [`moduleAnnotationTypes`](/evidence/rule/contextmap/dca-map-014/moduleannotationtypes.md)
- [`modulePackagesByName`](/evidence/rule/contextmap/dca-map-014/modulepackagesbyname.md)
- [`plannedEdges`](/evidence/rule/contextmap/dca-map-014/plannededges.md)
- [`allowedDependencies`](/evidence/rule/contextmap/dca-map-014/alloweddependencies.md)
- [`dependsOnTree`](/evidence/rule/contextmap/dca-map-014/dependsontree.md)
- [`CollectedViolations.check`](/evidence/rule/contextmap/dca-map-014/collectedviolations-check.md)
- [`CollectedViolations.withoutHeader`](/evidence/rule/contextmap/dca-map-014/collectedviolations-withoutheader.md)
- [`CollectedViolations.isEmpty`](/evidence/rule/contextmap/dca-map-014/collectedviolations-isempty.md)
- [`CollectedViolations.require`](/evidence/rule/contextmap/dca-map-014/collectedviolations-require.md)
- [`CollectedViolations.throwIfAny`](/evidence/rule/contextmap/dca-map-014/collectedviolations-throwifany.md)
- [`lastSegment`](/evidence/rule/contextmap/dca-map-014/lastsegment.md)
- [`channelName`](/evidence/rule/contextmap/dca-map-014/channelname.md)
- [`inPackageTree`](/evidence/rule/contextmap/dca-map-014/inpackagetree.md)
- [`CollectedViolations.addAll`](/evidence/rule/contextmap/dca-map-014/collectedviolations-addall.md)
- [`CollectedViolations.add`](/evidence/rule/contextmap/dca-map-014/collectedviolations-add.md)
- [C# expression](/evidence/rule/contextmap/dca-map-014/c-expression.md)
