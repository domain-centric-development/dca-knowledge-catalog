---
type: Template
title: "Bounded context declaration (package-info.java) — Java"
parent: /template/bounded-context-package-info.md
tags: [template, strategic, bounded-context, context-map, modulith]
review: draft
owner: DCA catalog maintainers
evidence: [/marker/strategic/boundedcontext.md, /marker/strategic/upstream.md, /marker/strategic/partnership.md, /rule/strategic/dca-str-001.md, /rule/contextmap/dca-map-001.md, /rule/contextmap/dca-map-006.md, /reference/architecture.md, /guide/package-structure.md]
applies_to: [java]
framework: [framework-neutral]
---

The Java code of [Bounded context declaration (package-info.java)](/template/bounded-context-package-info.md). The prose, the evidence and what
governs it stay in that node; this file carries the skeleton only.

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
