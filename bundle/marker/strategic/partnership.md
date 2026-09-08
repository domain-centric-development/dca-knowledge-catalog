---
type: Marker
title: "@Partnership"
category: strategic
kind: annotation
signature: "public @interface Partnership"
package: dev.domaincentric.dca.buildingblocks.ddd.strategic.relationships
methods: ["String context()", "String rationale() default \"\""]
resource: dca-java/dca-building-blocks/src/main/java/dev/domaincentric/dca/buildingblocks/ddd/strategic/relationships/Partnership.java
tags: [strategic, marker]
---

Declares a Partnership between two bounded contexts: both teams coordinate the evolution of a
shared contract and succeed or fail together on it.

A partnership is a *governance* relationship, not a technical one. It grants no
dependency permission — every actual directed dependency still requires its own `m`
declaration on the downstream side. A typical example is a consumer-defined trigger interface:
the consumer owns the contract, the producer implements it, and both must evolve it together.

**Usage:** Place on the bounded context's `package-info.java`. Partnerships are
symmetric — the declaration must exist on *both* contexts:

```java
@Partnership(context = "checkout", rationale = "CartCompletionTrigger contract evolves jointly")
package com.acme.shop.cart;
```

**Architectural rules** (enforced by `ContextMapArchUnitTest`):

- Only packages annotated with `t` may
declare `@Partnership`
- The target context must exist and must not be the declaring context itself
- The declaration must be mirrored by the target context (symmetry)

## Governed by

- [Diagnostic: Display declared context map](/rule/contextmap/diagnostic-display-declared-context-map.md)
- [Partnership declarations must reference an existing bounded context, never themselves, and must be symmetric](/rule/contextmap/partnership-declarations-must-reference-an-existing-bounded-context-never-themselves-and-must-be-symmetric.md)
- [Upstream, ExternalUpstream, and Partnership may only be declared on bounded context packages](/rule/contextmap/upstream-externalupstream-and-partnership-may-only-be-declared-on-bounded-context-packages.md)
