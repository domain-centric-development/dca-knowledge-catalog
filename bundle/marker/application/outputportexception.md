---
type: Marker
title: OutputPortException
category: application
kind: class
signature: public abstract class OutputPortException extends PortException
package: dev.domaincentric.dca.buildingblocks.application
modifiers: [public, abstract]
extends: [PortException]
resource: dca-java/dca-building-blocks/src/main/java/dev/domaincentric/dca/buildingblocks/application/OutputPortException.java
tags: [application, marker]
---

Base class of every failure an output port's contract declares.

**Who declares, raises and catches it.** The output port declares it in its contract, in
the application layer beside the port; the outgoing adapter that implements the port raises it,
because the contract asks for it; the use case that calls the port catches it and decides the
answer - a case of its result where the caller can answer it, or its own `UseCaseException`. The adapter raises it, but does not own it: an adapter never invents a failure
the application has not declared.

**For an expected failure the port's caller can answer** - a uniqueness only the store can
see, or a foreign system behind the port that refused or did not answer (a payment provider, a
mail provider: an external system on the context map). A failure of the system's own
infrastructure - its database, its broker - is no part of the contract and stays the platform's
own exception.

**Inside the transaction.** The use case may catch it inside its transaction and return a
refusal: a returned `Refusal` rolls the transaction back like the exception would have.

**Never caught as such.** A use case catches the named subtype the port declares, not this
base.

## Extends

- [PortException](/marker/application/portexception.md)

## Related mentions in guides (heuristic)

- [ERROR HANDLING RULES](/guide/rules/error-handling-rules.md)
