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

## Related mentions in guides (heuristic)

- [Core Rule Categories](/guide/archunit-governance/core-rule-categories.md)
- [Declaring Context Relationships in Code](/guide/integration-patterns/declaring-context-relationships-in-code.md)
- [Declaring Contexts and Relationships](/guide/language-mappings/declaring-contexts-and-relationships.md)
