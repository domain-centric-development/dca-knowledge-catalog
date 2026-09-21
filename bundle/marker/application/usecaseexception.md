---
type: Marker
title: UseCaseException
category: application
kind: class
signature: public abstract class UseCaseException extends RuntimeException
package: dev.domaincentric.dca.buildingblocks.application
modifiers: [public, abstract]
extends: [RuntimeException]
resource: dca-java/dca-building-blocks/src/main/java/dev/domaincentric/dca/buildingblocks/application/UseCaseException.java
tags: [application, marker]
---

Base class of every use-case failure the application layer reports to its callers.

A use case fails for reasons the domain model cannot state on its own, because they are about
the request rather than about an invariant: the addressed aggregate does not exist, the caller
may not act on it, or a precondition on a second aggregate does not hold. Those failures belong
to the application layer, which knows the request, and they get a name that says which of them
happened — one type per outcome, so a caller can tell them apart without reading a message.

**What is not a use-case failure.** A broken rule of the model is a `n` and stays in the domain layer;
an argument guard stays the platform's own argument exception. A use-case failure is raised by
the use case, never by the model.

**Where it lives.** In the application layer, beside the use case that raises it. It
carries no metadata for container management or transport and names no transport vocabulary — the
incoming adapter maps each type onto the answer its protocol has for it, and it is the only layer
that decides which answer that is. Keeping the type free of that decision is what lets one use
case serve several protocols at once.

**Unchecked on purpose.** A failure the caller cannot repair by retrying with the same
request is not an alternative return value; it travels to the boundary that can answer it.

## Related mentions in guides (heuristic)

- [Core Rule Categories](/guide/archunit-governance/core-rule-categories.md)
- [ERROR HANDLING RULES](/guide/rules/error-handling-rules.md)
