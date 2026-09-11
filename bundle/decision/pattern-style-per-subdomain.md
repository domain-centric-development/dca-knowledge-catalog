---
type: Decision
title: "Pattern style per subdomain: full tactical DDD, transaction script, or buy"
tags: [decision, strategic, subdomain]
review: draft
owner: DCA catalog maintainers
evidence: [/guide/archunit-governance/context-specific-rule-sets.md, /guide/package-structure.md]
---

Not every bounded context deserves the full tactical DDD toolkit. The effort you invest should track the **subdomain type** — how much competitive value the context carries. Applying rich aggregates everywhere wastes effort on commodity logic; applying transaction scripts to the core erodes the model that justifies building in-house at all.

## The discriminator

Classify the subdomain first, then the pattern style follows:

1. **Is this where the business differentiates?** Complex, changing rules that are your reason to build rather than buy → **Core**.
2. **Is it necessary but undifferentiated?** Supports the core, simpler rules, no competitive edge → **Supporting**.
3. **Is it a solved commodity?** Auth, notifications, payments plumbing → **Generic**.

## Options

| Subdomain type | Pattern style | What that means |
|---|---|---|
| **Core** | Full tactical DDD | rich aggregates, value objects, domain events, ports & adapters, the complete rule set |
| **Supporting** | Transaction script / active record | simple layering is legitimate; a rich domain model is optional, not required |
| **Generic** | Buy / adopt | don't build a bespoke model — integrate an off-the-shelf solution behind an ACL |

**Default:** start a context as **Supporting** with the lightest structure that works, and promote to full tactical DDD only when the domain proves it is core. It is cheaper to add structure than to carry unnecessary structure. Each context **declares its chosen style in an ADR**, and the ArchUnit suite then activates the matching rule subset per context — so a supporting context is not held to core-only aggregate rules.

## Consequences

- The strictness of enforced rules is **per context**, driven by the declared style — there is no single global bar.
- Reclassifying a subdomain (supporting → core) is a real architectural decision: it changes which rules apply and typically triggers a refactor toward a rich model.
- Generic subdomains still get a boundary: wrap the bought solution so its model never leaks inward.

## Anchors

- Guide: [Context-specific rule sets](/guide/archunit-governance/context-specific-rule-sets.md) · [Java package structure](/guide/package-structure.md)
- Related recipe: [Add a bounded context](/recipe/add-a-bounded-context.md)
- Related decision: [Shared kernel vs duplication](/decision/shared-kernel-vs-duplication.md)
