---
type: Section
title: The composition root
chapter: Dependency Structure
source: guide
resource: dca-guide/architecture/dependency-structure.md
tags: [guide, section]
---

**The composition root is the one place where the application's objects are put together.** It creates the
adapters, hands each use case its output ports, and then hands control to the entry point. Mark Seemann named it:
"a (preferably) unique location in an application where modules are composed together", as close to the entry point
as possible. Robert C. Martin calls the same thing *Main*, "the dirtiest of all the dirty components", a plugin to the
application that nothing depends on. Alistair Cockburn calls it the *configurator*.

The composition root sits in the infrastructure layer, and its form follows the platform:

| Platform | The composition root is |
|---|---|
| Spring Boot | the container: `@SpringBootApplication`, the component scan, and the `@Configuration` classes in `{context}/infrastructure/` |
| ASP.NET Core | `Program.cs` and the `Add{Context}Context()` extension method each context's `Infrastructure/` project provides |
| No container | a module in `infrastructure/` that constructs every object by hand and calls the entry point — Seemann's *Pure DI* |

Most wiring needs no code in a container: the scan finds a use case by its stereotype and injects its ports by type.
Code goes into the composition root where the container cannot decide alone — a factory, a configuration value, a
port whose implementation is chosen per environment, and a port implemented by another use case (see
[A flow that needs a second operation](/guide/rules/operation-boundaries-and-declared-contracts.md)).

**The composition root wires; it never decides.** It holds no `if` over a business value, no loop over a command's
content, no rule. A lambda that turns one port's call into another use case's command is wiring. Once that lambda
needs a condition, the condition is a decision, and a decision belongs to a use case. A composition root that
decides hides behaviour where no use-case test looks for it.

**The composition root implements no port.** Every implementation of an output port is an outgoing adapter and lives
in `adapter/outgoing/`; the root refers to it and wires it (`DCA-HEX-019`). The one exception is the bridge to a
second use case — a lambda in Java, a small forwarding class in C# — because it connects two ports of the application
and belongs to neither adapter side.

Only an application has a composition root. A library ships ports and building blocks and leaves the wiring to the
application that uses it.
