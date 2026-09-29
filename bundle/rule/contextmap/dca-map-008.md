---
type: Rule
id: DCA-MAP-008
title: "Anti-Corruption Layer: upstream contract types must stay inside the matching adapter"
rule: "The ACL sits where the dependency crosses the boundary — outgoing adapters for synchronous API calls, incoming adapters for consumed events — and translates the upstream contract into the context's own model there."
constraint: "Anti-Corruption Layer: upstream contract types must stay inside the matching adapter."
selects: "Every @Upstream declaration with translation() ANTI_CORRUPTION_LAYER on the package-info of every package carrying @BoundedContext whose context() names an existing bounded context, reading via() and status(). Declarations towards an unknown context are skipped."
checks: "Placement, whatever the status: no class below the declaring context's package outside the matching adapter depends on a class in the target context's channel sub-package or below - the outgoing adapter (<context>.adapter.outgoing..) for the API channel, the incoming adapter (<context>.adapter.incoming..) for the EVENTS channel. Presence, only for status() IMPLEMENTED (as in DCA-MAP-007): each declared interaction needs a class in that adapter depending on both that upstream channel and its own domain/application; a PLANNED declaration without any such code passes. Multiple upstream translators may share the package. Structure establishes a translation site, not translation quality."
enforced_by: "ContextMapRules#DCA-MAP-008"
status: enforced
rule_set: contextmap
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/ContextMapRules.java
tags: [contextmap, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/ContextMapRules.cs
---

# Anti-Corruption Layer: upstream contract types must stay inside the matching adapter

## Selection

Every @Upstream declaration with translation() ANTI_CORRUPTION_LAYER on the package-info of every package carrying @BoundedContext whose context() names an existing bounded context, reading via() and status(). Declarations towards an unknown context are skipped.

## Check

Placement, whatever the status: no class below the declaring context's package outside the matching adapter depends on a class in the target context's channel sub-package or below - the outgoing adapter (<context>.adapter.outgoing..) for the API channel, the incoming adapter (<context>.adapter.incoming..) for the EVENTS channel. Presence, only for status() IMPLEMENTED (as in DCA-MAP-007): each declared interaction needs a class in that adapter depending on both that upstream channel and its own domain/application; a PLANNED declaration without any such code passes. Multiple upstream translators may share the package. Structure establishes a translation site, not translation quality.

## .NET reading

**Selection.** Every [Upstream] declaration with Translation AntiCorruptionLayer on the marker class of every namespace carrying [BoundedContext] whose Context names an existing bounded context, reading Via and Status. Declarations towards an unknown context are skipped.

**Check.** Placement, whatever the status: no type below the declaring context's namespace outside the matching adapter depends on a type in the target context's channel namespace or below - the outgoing adapter (<context>.Adapter.Outgoing) for the Api channel, the incoming adapter (<context>.Adapter.Incoming) for the Events channel. Presence, only for Status Implemented (as in DCA-MAP-007): each declared interaction needs a type in that adapter depending on both that upstream channel and its own Domain/Application; a Planned declaration without any such code passes. Multiple upstream translators may share the namespace. Structure establishes a translation site, not translation quality.

## Implementation

The verbatim ArchUnit expression is in the evidence slice [Overview](/evidence/rule/contextmap/dca-map-008/overview.md); every helper it calls has a slice of its own, listed under *Evidence slices* below.

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `boundedContextPackages()`, `classes()`, `contextName()`, `layout()`, `packageAnnotations()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).

## Related mentions (heuristic)

- [@BoundedContext](/marker/strategic/boundedcontext.md)
- [@Upstream](/marker/strategic/upstream.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)

## Evidence slices

- [Overview](/evidence/rule/contextmap/dca-map-008/overview.md)
- [`packagesByName`](/evidence/rule/contextmap/dca-map-008/packagesbyname.md)
- [`channelName`](/evidence/rule/contextmap/dca-map-008/channelname.md)
- [`CollectedViolations.check`](/evidence/rule/contextmap/dca-map-008/collectedviolations-check.md)
- [`CollectedViolations.withoutHeader`](/evidence/rule/contextmap/dca-map-008/collectedviolations-withoutheader.md)
- [`CollectedViolations.require`](/evidence/rule/contextmap/dca-map-008/collectedviolations-require.md)
- [`CollectedViolations.addAll`](/evidence/rule/contextmap/dca-map-008/collectedviolations-addall.md)
- [`CollectedViolations.throwIfAny`](/evidence/rule/contextmap/dca-map-008/collectedviolations-throwifany.md)
- [`CollectedViolations.add`](/evidence/rule/contextmap/dca-map-008/collectedviolations-add.md)
- [`CollectedViolations.isEmpty`](/evidence/rule/contextmap/dca-map-008/collectedviolations-isempty.md)
- [C# expression](/evidence/rule/contextmap/dca-map-008/c-expression.md)
