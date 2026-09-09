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

## `package-info.java` — the declaration

```java
/**
 * {Context} — one sentence on what this context is responsible for, in its own language.
 *
 * <p><b>Subdomain type:</b> core | supporting | generic.
 * <b>Pattern style:</b> full tactical DDD | transaction script | bought/integrated.
 * <b>Rule set:</b> complete | relaxed (which rule sets are enforced follows from the style).
 *
 * <p><b>Layout</b> — a context owns its layers directly below this package:
 * <pre>
 * {context}/
 * ├── domain/            pure model: aggregates, value objects, domain events, domain services
 * ├── application/       use cases (one package each, optionally grouped into features), shared/ ports
 * ├── adapter/
 * │   ├── incoming/      web/, api/, events/, mcp/ — drive the input ports
 * │   └── outgoing/      persistence/, ... — implement the output ports
 * ├── api/               published interface for other contexts (optional, named interface "api")
 * ├── events/            published integration events (optional, named interface "events")
 * └── infrastructure/    context-specific framework configuration (optional)
 * </pre>
 */
@BoundedContext(
        name = "{context}",
        description = "What this context owns and decides, in the ubiquitous language.")
@ApplicationModule(
        allowedDependencies = { "sharedkernel", "{othercontext} :: api", "{othercontext} :: events" })
@Upstream(
        context = "{othercontext}",
        translation = Upstream.Translation.ANTI_CORRUPTION_LAYER,
        via = Upstream.Consumes.API)
@Upstream(
        context = "{othercontext}",
        translation = Upstream.Translation.CONFORMIST,
        via = Upstream.Consumes.EVENTS)
package {basePackage}.{context};

import dev.domaincentric.dca.buildingblocks.ddd.strategic.BoundedContext;
import dev.domaincentric.dca.buildingblocks.ddd.strategic.relationships.Upstream;
import org.springframework.modulith.ApplicationModule;
```

A context without upstreams keeps only `@BoundedContext` (and `@ApplicationModule` if Modulith is in use); delete the `@Upstream` lines rather than declaring a relationship that does not exist — a declaration without a code dependency behind it is only legal as `PLANNED`.

## What goes where

- **`@BoundedContext`** — `name` is the identifier the context map and the rule reports use; keep it lowercase and equal to the package segment where possible. `description` is one sentence in the context's own language. This is the only annotation that *creates* a context: a package that owns `domain`/`application`/`adapter` layers without it is still a structural *module root* and is governed by the layer rules, but it does not appear on the context map and cannot declare relationships.
- **`@Upstream` / `@Partnership`** — declared on the *same* `package-info.java`, and only there: the rules reject relationship annotations on any package that is not a bounded context. `@Upstream` sits on the downstream side, one annotation per `(context, via)` channel, and states how the downstream protects its model (`ANTI_CORRUPTION_LAYER` or `CONFORMIST`); `@Partnership` is declared symmetrically on both sides.
- **`@ApplicationModule`** (Spring Modulith, optional) — makes the same package a module boundary. Its `allowedDependencies` must agree with the `@Upstream` declarations: every `"{othercontext} :: api"` / `"{othercontext} :: events"` entry corresponds to exactly one `@Upstream` channel, and vice versa. The shared kernel is listed by name.
- **Javadoc** — the subdomain type and pattern style are decisions, not code; record them here so the next reader knows why the context looks the way it does and which strictness the architecture tests apply to it. Revisit them when the context's value to the business changes.

## Realizes / governed by

- Markers: [@BoundedContext](/marker/strategic/boundedcontext.md) · [@Upstream](/marker/strategic/upstream.md) · [@Partnership](/marker/strategic/partnership.md)
- Rules: [Diagnostic: Display discovered bounded contexts](/rule/strategic/dca-str-001.md) · [Upstream, ExternalUpstream, and Partnership may only be declared on bounded context packages](/rule/contextmap/dca-map-001.md) · [Upstream declarations and Spring Modulith allowedDependencies must agree](/rule/contextmap/dca-map-006.md)
- Reference: [DcaArchitecture](/reference/architecture.md) (how contexts and module roots are discovered)
- Guide: [Java package structure](/guide/readme/java-package-structure.md) · [Context-specific rule sets](/guide/archunit-governance/context-specific-rule-sets.md) · [Spring Modulith core concepts](/guide/spring-modulith/core-concepts.md)
- Decision: [Pattern style per subdomain](/decision/pattern-style-per-subdomain.md)
- Recipe: [Add a bounded context](/recipe/add-a-bounded-context.md)
