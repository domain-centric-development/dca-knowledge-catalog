---
type: Marker
title: DomainException
category: tactical
kind: class
signature: public abstract class DomainException extends RuntimeException
package: dev.domaincentric.dca.buildingblocks.ddd.tactical
modifiers: [public, abstract]
extends: [RuntimeException]
resource: dca-java/dca-building-blocks/src/main/java/dev/domaincentric/dca/buildingblocks/ddd/tactical/DomainException.java
tags: [tactical, marker]
---

Base class of every business-rule violation the domain model raises.

A domain exception has a name a domain expert would recognise: it says which rule of the model
was broken, not which technical operation failed. The test is the name — if the failure has a
word in the Ubiquitous Language, it is a domain exception with that word in its name; if it has
none, it is not one.

**What is not a domain exception.** An argument guard is a programming-error contract, not
a business rule: a null check, a range check or a "must not be blank" check in a constructor
states what a caller must never pass, and the platform's own argument exception remains the
correct answer there. Subclass this type only for a rule the model itself owns — a forbidden
state transition, an invariant across several attributes, a quantity the aggregate refuses.

**Where it lives.** In the domain layer, beside the model that raises it. It carries no
metadata for container management, persistence or transport, and it names no transport vocabulary
— no status code, no response shape. Translating a domain exception into a protocol answer is the
incoming adapter's work, and the adapter is the only layer that knows the protocol.

**Unchecked on purpose.** A broken invariant is not an alternative flow a caller declares
in its signature; it travels to the boundary that can answer it.

## Related mentions in guides (heuristic)

- [Core Rule Categories](/guide/archunit-governance/core-rule-categories.md)
- [ERROR HANDLING RULES](/guide/rules/error-handling-rules.md)
