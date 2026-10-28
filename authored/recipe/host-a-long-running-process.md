---
type: Recipe
title: Host a long-running process
tags: [recipe, infrastructure, application, port-out, error-handling]
review: draft
owner: DCA catalog maintainers
evidence: [/rule/hexagonal/dca-hex-004.md, /rule/hexagonal/dca-hex-005.md, /marker/port-out/outputport.md, /guide/dependency-structure/the-composition-root.md, /guide/rules/error-handling-rules.md]
---

A process that runs for minutes or hours — a worker, a command-line run over many steps, a job — has state that
belongs to the process, not to the domain: the claim on a resource, a lock, the working directory, the child
processes it started, the signal that it should stop. In Spring or ASP.NET the host carries it (the application
context, the Generic Host with `IHostedService` and `IHostApplicationLifetime`). Without a framework, or beside it,
it is an object of its own. It is **infrastructure, next to the composition root** — not an adapter's state and not
part of a use case.

## Steps

1. **Separate process state from domain state.** Progress a person or the business cares about — which step a run
   is in, what it decided — is the domain's: an aggregate or a store, behind a port. What exists only while the
   process runs — the lock, the pid, the open handles, the stop signal — is the host's.
2. **Put the host in `infrastructure/`.** One object, created by the composition root before anything else: it
   acquires what the process needs (the claim, the lock), installs the signal handlers, and releases everything on
   the way out, in reverse order. The entry point is `host → composition root → incoming adapter → use case`.
3. **Give the use case a port for what it needs from the host.** A use case that must hold a claim, ask whether it
   should continue, or start a child process declares an output port in its own words (`CheckoutClaim`,
   `StepRunner`); the composition root implements it with the host. The use case never sees the host type.
4. **Let a stop pass through.** The host turns a signal into a stop: a cancelled token (.NET), an interrupt (Java),
   an exception of the application's own stop type (no platform model). Ports raise it while they wait, nothing
   translates it, no use case catches it, and the entry point — the owner of the process — turns it into the exit
   code and releases what the host holds.
5. **Keep incoming adapters off the host.** A command-line handler or a worker loop reaches the host only through
   the composition root's wiring, never by import: an incoming adapter uses no infrastructure (`DCA-HEX-004`), and
   another context's infrastructure is private (`DCA-HEX-005`).
6. **Test the use case without the host.** Fake ports for the claim and the steps; one integration test starts the
   real host, sends the stop signal mid-run and asserts the exit code and that the claim is released.

## Rules to satisfy (build-time checklist)

- [Incoming Adapters must only use outbound ports (not infrastructure implementations)](/rule/hexagonal/dca-hex-004.md)
- [Outgoing adapters must not use another module's infrastructure](/rule/hexagonal/dca-hex-005.md)

## Anchors

- Guide: [The composition root](/guide/dependency-structure/the-composition-root.md) · [Error handling — a stop is not a failure](/guide/rules/error-handling-rules.md) · [A process that spans several transactions](/guide/integration-patterns/a-process-that-spans-several-transactions.md)
- Marker: [OutputPort](/marker/port-out/outputport.md)
- Sibling recipes: [Hand a use case a second operation](/recipe/hand-a-use-case-a-second-operation.md) · [Build DCA without a framework](/recipe/build-dca-without-a-framework.md)
