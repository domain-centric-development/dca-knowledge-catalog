---
type: Template
title: "Bounded context declaration (package-info.java)"
tags: [template, strategic, bounded-context, context-map, modulith]
review: draft
owner: DCA catalog maintainers
evidence: [/marker/strategic/boundedcontext.md, /marker/strategic/upstream.md, /marker/strategic/partnership.md, /rule/strategic/dca-str-001.md, /rule/contextmap/dca-map-001.md, /rule/contextmap/dca-map-006.md, /reference/architecture.md, /guide/readme/java-package-structure.md]
applies_to: [java]
framework: [framework-neutral]
---

Domain-free skeleton for the one file that turns a package into a **bounded context**: `package-info.java` at the context root, annotated with `@BoundedContext`. The architecture rules discover contexts by this annotation, at any depth below the base package — the annotation is the declaration, the position in the package tree is not. Everything the strategic rules need to know about the context is declared here: its name and purpose, its upstream and partnership relationships and, if Spring Modulith is used, its module boundary. The javadoc records what no annotation carries: the subdomain type, the chosen pattern style and the rule-set strictness that follows from it, and the package layout below. Replace `{context}` / `{Context}` / `{basePackage}`.

## Languages

The code lives in one child node per language, so the prose below is written once and a
further language is one more file rather than a second copy of this node.

- Java — [`bounded-context-package-info/java.md`](/template/bounded-context-package-info/java.md)

## Realizes / governed by

- Markers: [@BoundedContext](/marker/strategic/boundedcontext.md) · [@Upstream](/marker/strategic/upstream.md) · [@Partnership](/marker/strategic/partnership.md)
- Rules: [Diagnostic: Display discovered bounded contexts](/rule/strategic/dca-str-001.md) · [Upstream, ExternalUpstream, and Partnership may only be declared on bounded context packages](/rule/contextmap/dca-map-001.md) · [Upstream declarations and Spring Modulith allowedDependencies must agree](/rule/contextmap/dca-map-006.md)
- Reference: [DcaArchitecture](/reference/architecture.md) (how contexts and module roots are discovered)
- Guide: [Java package structure](/guide/readme/java-package-structure.md) · [Context-specific rule sets](/guide/archunit-governance/context-specific-rule-sets.md) · [Spring Modulith core concepts](/guide/spring-modulith/core-concepts.md)
- Decision: [Pattern style per subdomain](/decision/pattern-style-per-subdomain.md)
- Recipe: [Add a bounded context](/recipe/add-a-bounded-context.md)
