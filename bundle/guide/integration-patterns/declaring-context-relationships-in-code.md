---
type: Section
title: Declaring Context Relationships in Code
chapter: Integration Patterns
source: guide
resource: dca-guide/architecture/integration-patterns.md
tags: [guide, section]
---

Context-map relationships are declared on the bounded context's `package-info.java`, next to
`@BoundedContext`. The declaration is the single source of truth: architecture tests verify that the
declared relationships match the actual dependencies, and the human-readable context map (table +
diagram) is rendered from the same annotations — an **executable context map** that cannot drift.

```java
// checkout/package-info.java
@BoundedContext(name = "Checkout", description = "Checkout process, order placement, payment orchestration")
@Upstream(
    context = "product",
    translation = Upstream.Translation.ANTI_CORRUPTION_LAYER,
    via = Upstream.Consumes.API,
    rationale = "Product data is translated into checkout's own article types")
@Upstream(
    context = "cart",
    translation = Upstream.Translation.CONFORMIST,
    via = Upstream.Consumes.EVENTS,
    rationale = "CartCheckedOutEvent is consumed as published, no translation needed")
@ExternalUpstream(
    name = "Payment Provider",
    translation = Upstream.Translation.ANTI_CORRUPTION_LAYER,
    interaction = ExternalUpstream.Interaction.OUTBOUND,
    protocol = "REST",
    contractPackages = "..checkout.adapter.outgoing.payment..")
package com.company.project.checkout;
```

| Annotation | Declares | Key attributes |
|------------|----------|----------------|
| `@Upstream` (repeatable) | this context is **downstream** of `context` | `translation` = `ANTI_CORRUPTION_LAYER` \| `CONFORMIST`; `via` = `API` \| `EVENTS`; `status` = `IMPLEMENTED` \| `PLANNED`; `rationale` |
| `@ExternalUpstream` (repeatable) | an **external system** the context talks to | `interaction` = `OUTBOUND` \| `INBOUND`; `protocol`, `exchanges`, `contractPackages` |
| `@Partnership` (repeatable) | mutual, coordinated evolution with `context` | `rationale` |
| `@OpenHostService` | this adapter is a published API for other contexts | on the adapter class, not the package |
| `@SharedKernel` | the package is the shared kernel | on `package-info.java` |

**What `translation` is, and what it is not.** It states how *this* context protects its own
model — `ANTI_CORRUPTION_LAYER` or `CONFORMIST` — and nothing else. Three questions are
easily collapsed into one and must not be:

| Question | Where it is answered | Values |
|---|---|---|
| How does the downstream protect its model? | `translation` on `@Upstream` | ACL, Conformist |
| How does the upstream publish? | `@OpenHostService` on the published type, and the `api` / `events` packages themselves | Open Host Service, Published Language |
| How do the two teams work together? | nowhere in the code — prose, or `rationale` | Customer/Supplier, Partnership, Separate Ways |

One relationship normally answers all three at once: a context consumes another through
its Open Host Service, translates it with an Anti-Corruption Layer, and the two teams work
as Customer/Supplier. Writing "Customer/Supplier" where the declaration says
`ANTI_CORRUPTION_LAYER` is not a contradiction but a category error, and it costs the
mechanical check: `DCA-MAP-008` demands a translation site for every declared channel, and
an organisational pattern names no site.

Rules the declarations enable (see [ArchUnit Governance](/guide/archunit-governance.md)):

- Every cross-context dependency in code must be covered by an `@Upstream`/`@Partnership` declaration
  (undeclared coupling fails the build).
- Every declared relationship with `status = IMPLEMENTED` must have a matching dependency (dead
  declarations fail the build); `PLANNED` relationships are exempt.
- `ANTI_CORRUPTION_LAYER`: the upstream's contract types must stay inside the matching outgoing
  adapter (or event consumer) — they never leak into application or domain.
- `CONFORMIST`: the upstream's contract types may be used as-is in the application layer, but still
  never reach the domain layer — conformism does not suspend domain purity.
- Declarations must be well-formed: target context exists, never the declaring context itself, unique
  per context and channel, `@Partnership` symmetric on both sides, and consistent with Spring Modulith
  `allowedDependencies` where used.

## Related mentions (heuristic)

- [@BoundedContext](/marker/strategic/boundedcontext.md)
- [@ExternalUpstream](/marker/strategic/externalupstream.md)
- [@OpenHostService](/marker/strategic/openhostservice.md)
- [@Partnership](/marker/strategic/partnership.md)
- [@SharedKernel](/marker/strategic/sharedkernel.md)
- [@Upstream](/marker/strategic/upstream.md)
