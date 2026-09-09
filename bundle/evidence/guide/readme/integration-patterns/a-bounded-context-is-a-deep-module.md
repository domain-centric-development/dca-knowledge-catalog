---
type: Reference
title: INTEGRATION PATTERNS — A Bounded Context Is a Deep Module
tags: [reference]
evidence_for: "/guide/readme/integration-patterns.md#a-bounded-context-is-a-deep-module"
---

[Full node and context](/guide/readme/integration-patterns.md#a-bounded-context-is-a-deep-module). This is an evidence excerpt; retain the parent selection and caveats.

### A Bounded Context Is a Deep Module

A bounded context is a *deep module* in the sense of Ousterhout (*A Philosophy of Software
Design*): a lot of implementation behind a deliberately small interface. Its public surface is
the set of input ports, the integration events it publishes and the trigger interfaces it
defines for its suppliers — nothing else. Aggregates, use cases, adapters and read models
stay inside. The architecture rules make this depth enforceable rather than a convention:
no raw import crosses a context boundary, and every published relationship is declared on
`package-info.java` and verified.

Depth is measured at the context, not at the package. The many small use-case packages
inside a context are its interior, not shallow modules of their own. The payoff is the same
for every reader of the code: a person — or a coding agent without memory of previous
sessions — understands a context from its ports and records alone and touches the interior
only when working there.
