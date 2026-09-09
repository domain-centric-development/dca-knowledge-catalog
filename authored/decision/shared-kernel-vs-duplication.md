---
type: Decision
title: "Shared kernel or duplication: where a value object lives"
tags: [decision, strategic, shared-kernel, value-object]
review: draft
owner: DCA catalog maintainers
evidence: [/marker/strategic/sharedkernel.md, /rule/strategic/dca-str-002.md, /guide/spring-modulith/shared-kernel-in-spring-modulith.md]
---

When two contexts both need a concept — a `Money`, a `UserId`, an `Address` — you can promote it into the `sharedkernel` or let each context own its own copy. The shared kernel removes duplication but creates a coupling that every sharing context must agree to maintain. Choose deliberately; the default leans toward duplication.

## The discriminator

1. **Is the concept genuinely universal and stable?** A truly context-free value with a meaning that does not drift (a currency amount, a technical identifier) is a shared-kernel candidate. A concept that *sounds* the same but means different things per context (a "Customer" in Sales vs. Billing) is **not** — duplicate it.
2. **Would divergence be a bug or a feature?** If the two contexts must evolve the concept in lockstep, share it. If either context might legitimately need its own variation later, duplicating now keeps them free.
3. **Are the sharing teams willing to co-own it?** The shared kernel is a *partnership contract*: no single team may change it unilaterally. Without that agreement, duplicate.

## Options

| | Shared kernel | Duplication |
|---|---|---|
| Lives in | `sharedkernel/domain/model` | each context's own domain |
| Coupling | shared type, coordinated change | zero — contexts evolve independently |
| Best for | universal, stable, co-owned values & markers | same-name-different-meaning, or likely-to-diverge concepts |
| Cost | change coordination across teams | drift risk, mapping at boundaries |

**Default:** duplicate. Only promote to the shared kernel when the concept is provably universal, stable, and jointly owned. Keep the shared kernel **minimal** — architectural markers and a small set of universal value objects, never entities or aggregate roots, never domain logic that belongs to one context.

## Consequences

- The shared kernel may depend on **nothing** — it must not reference any bounded context (enforced, see anchors). If your "shared" value needs a context's type, it does not belong there.
- What you put in the shared kernel is Value Objects and markers, built the same way as any value object: [Recipe: add a value object](/recipe/add-a-value-object.md) · [Template: value object](/template/value-object.md).
- Promoting a duplicated concept into the shared kernel later is a coordinated refactor; starting shared and splitting later is harder. When in doubt, stay duplicated.

## Anchors

- Markers: [@SharedKernel](/marker/strategic/sharedkernel.md)
- Rules: [Shared Kernel must not have dependencies on any bounded context](/rule/strategic/dca-str-002.md)
- Guide: [Shared kernel](/guide/spring-modulith/shared-kernel-in-spring-modulith.md)
- Related pitfall: [Raw cross-context import](/pitfall/raw-cross-context-import.md)
