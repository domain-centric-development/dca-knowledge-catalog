---
type: Marker
title: InputPortException
category: application
kind: class
signature: public abstract class InputPortException extends PortException
package: dev.domaincentric.dca.buildingblocks.application
modifiers: [public, abstract]
extends: [PortException]
resource: dca-java/dca-building-blocks/src/main/java/dev/domaincentric/dca/buildingblocks/application/InputPortException.java
tags: [application, marker]
---

Base class of every failure an input port's contract declares.

**Who declares, raises and catches it.** The input port declares it as part of what its
operation may answer; the use case behind the port raises it; the incoming adapter that drives
the port catches it and turns it into its protocol's answer. Its one concrete branch is `UseCaseException`: every failure a use case reports extends that, so this type stays the
classification in the hierarchy, not something a project subclasses directly.

**Never caught as such.** An incoming adapter that catches `InputPortException`
answers every outcome the same way; it catches the named subtypes, each with its own answer.

## Extends

- [PortException](/marker/application/portexception.md)

## Related mentions in guides (heuristic)

- [Building blocks, as the library defines them](/guide/elements/building-blocks-as-the-library-defines-them.md)
- [Building Blocks](/guide/language-mappings/building-blocks.md)
- [ERROR HANDLING RULES](/guide/rules/error-handling-rules.md)
