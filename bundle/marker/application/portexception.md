---
type: Marker
title: PortException
category: application
kind: class
signature: public abstract class PortException extends RuntimeException
package: dev.domaincentric.dca.buildingblocks.application
modifiers: [public, abstract]
extends: [RuntimeException]
resource: dca-java/dca-building-blocks/src/main/java/dev/domaincentric/dca/buildingblocks/application/PortException.java
tags: [application, marker]
---

Base class of every failure a port's contract declares.

A port is a contract between the application and the outside: an input port between the
application and the adapter that drives it, an output port between the application and the
adapter it drives. A failure that belongs to such a contract is declared by the port, raised on
one side of it and caught on the other. Which side is which depends on the direction, so the two
kinds have their own bases: `InputPortException` - declared by an input port, raised by the
use case, caught by the incoming adapter - and `OutputPortException` - declared by an
output port, raised by the adapter that implements it, caught by the use case.

**Abstract on purpose, and never caught as such.** No code raises a `PortException`
directly, and a caller that catches it, or one of its two direct subclasses, answers every
outcome the same way - the named subtypes exist so that each outcome gets its own answer.

**What is not a port failure.** A broken rule of the model is a `DomainException`; an argument guard stays the
platform's own argument exception; a failure of the infrastructure - a connection lost, a timeout
- is the platform's own exception and travels to the boundary that can answer it.

**Where it lives.** In the application layer, beside the port that declares it. It carries
no metadata for container management or transport and names no transport vocabulary.

## Related mentions in guides (heuristic)

- [Building blocks, as the library defines them](/guide/elements/building-blocks-as-the-library-defines-them.md)
- [ERROR HANDLING RULES](/guide/rules/error-handling-rules.md)
