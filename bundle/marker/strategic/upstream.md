---
type: Marker
title: "@Upstream"
category: strategic
kind: annotation
signature: "public @interface Upstream"
package: dev.domaincentric.dca.buildingblocks.ddd.strategic.relationships
methods: ["String context()", "Translation translation()", "Consumes[] via()", "String rationale() default \"\"", "Status status() default Status.IMPLEMENTED"]
resource: dca-java/dca-building-blocks/src/main/java/dev/domaincentric/dca/buildingblocks/ddd/strategic/relationships/Upstream.java
tags: [strategic, marker]
---

Declares that this bounded context consumes another bounded context as its upstream.

Placed on the *downstream* side because that is where the dependency originates and
where the translation decision is made. The upstream's publication style is not declared here —
it is expressed by the upstream itself through its `api`/`events` named interfaces
and `e`.

`@Upstream` declares only the directed dependency and how the downstream protects its
model. Organizational patterns such as Customer–Supplier are not machine-classified; document
them in `rationale()` if relevant.

**Usage:** Place on the bounded context's `package-info.java`, one annotation per
`(context, translation)` pair. Different translation strategies per channel require
separate annotations:

```java
@Upstream(
    context = "product",
    translation = Upstream.Translation.ANTI_CORRUPTION_LAYER,
    via = Upstream.Consumes.API)
@Upstream(
    context = "product",
    translation = Upstream.Translation.CONFORMIST,
    via = Upstream.Consumes.EVENTS)
package com.acme.shop.cart;
```

**Architectural rules** (enforced by `ContextMapArchUnitTest`):

- Only packages annotated with `t` may
declare `@Upstream`
- The target context must exist and must not be the declaring context itself
- `(context, via)` must be unique across all declarations of one context
- Every declaration must match a `"{context` :: api"} or `"{context` :: events"}
entry in `@ApplicationModule.allowedDependencies` — and vice versa
- Every `IMPLEMENTED` declaration must be backed by at least one actual code dependency
on the declared channel package — a declaration without code is only legal as `PLANNED`
- `ANTI_CORRUPTION_LAYER` + `API`: upstream contract types appear only in the
downstream's outgoing adapters
- `ANTI_CORRUPTION_LAYER` + `EVENTS`: upstream contract types appear only in the
downstream's incoming adapters
- `CONFORMIST`: upstream contract types may appear outside adapters but never in the
downstream's domain layer

## Governed by

- [Anti-Corruption Layer: upstream contract types must stay inside the matching adapter](/rule/contextmap/anti-corruption-layer-upstream-contract-types-must-stay-inside-the-matching-adapter.md)
- [Conformist: upstream contract types must never reach the domain layer](/rule/contextmap/conformist-upstream-contract-types-must-never-reach-the-domain-layer.md)
- [Cross-context dependencies on published interfaces require an Upstream declaration](/rule/contextmap/cross-context-dependencies-on-published-interfaces-require-an-upstream-declaration.md)
- [Diagnostic: Display declared context map](/rule/contextmap/diagnostic-display-declared-context-map.md)
- [External system contract types must respect the declared translation and interaction](/rule/contextmap/external-system-contract-types-must-respect-the-declared-translation-and-interaction.md)
- [ExternalUpstream declarations must be well-formed and unique per name and interaction](/rule/contextmap/externalupstream-declarations-must-be-well-formed-and-unique-per-name-and-interaction.md)
- [Implemented Upstream declarations must be backed by an actual code dependency](/rule/contextmap/implemented-upstream-declarations-must-be-backed-by-an-actual-code-dependency.md)
- [Upstream declarations and Spring Modulith allowedDependencies must agree](/rule/contextmap/upstream-declarations-and-spring-modulith-alloweddependencies-must-agree.md)
- [Upstream declarations must be unique per context and channel, and via must not be empty](/rule/contextmap/upstream-declarations-must-be-unique-per-context-and-channel-and-via-must-not-be-empty.md)
- [Upstream declarations must reference an existing bounded context and never the declaring context itself](/rule/contextmap/upstream-declarations-must-reference-an-existing-bounded-context-and-never-the-declaring-context-itself.md)
- [Upstream, ExternalUpstream, and Partnership may only be declared on bounded context packages](/rule/contextmap/upstream-externalupstream-and-partnership-may-only-be-declared-on-bounded-context-packages.md)

## Discussed in

- [Core Rule Categories](/guide/archunit-governance/core-rule-categories.md)
- [INTEGRATION PATTERNS](/guide/readme/integration-patterns.md)
