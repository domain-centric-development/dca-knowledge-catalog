---
type: Decision
title: State machine, coordinator or a workflow of its own
tags: [decision, use-case, application, events]
review: draft
owner: DCA catalog maintainers
evidence: [/rule/usecase/dca-use-016.md, /marker/tactical/aggregateroot.md, /decision/domain-event-vs-integration-event.md]
---

A process with several steps needs a place to live, and the tempting answer — a `Workflow` type beside the
use cases — is the one to avoid. There are two cases, they are different, and each already has a home.

**The steps belong to one aggregate: the aggregate is the state machine.** Which step a thing is in, and
whether it may move to the next, is part of its own state and its own invariants. It is business logic, not
presentation: whether a user interface shows one page or five changes nothing about whether the next step is
allowed. Model the step as a value in the aggregate and the transition as a method that refuses an illegal
move. A separate workflow object placed beside such an aggregate describes the same state a second time, and
the two descriptions drift — the workflow permits what the aggregate refuses, and which one is the truth is
then a matter of who is asked.

**The steps span several aggregates or contexts: that is a coordinator, and it lives in the application.**
A process that must advance three aggregates, or wait for another context to answer, is a Process Manager —
the Saga of the integration literature. It keeps its own state, it reacts to events, and it compensates when
a later step fails, because it cannot hold a transaction across the participants. It is application code: it
orchestrates, it decides nothing about a single aggregate's invariants.

**Why not a third concept.** "Workflow" sits between the two and attracts both, so the state machine that
belonged in the aggregate ends up outside it, and the coordinator loses the vocabulary — compensation,
timeout, correlation — that the process-manager literature already gives it. A style that adds a building
block for every recurring shape stops being learnable. Add the concept only when a case appears that neither
the aggregate nor a coordinating operation can hold.

**Where the decision shows up in the rules.** Operation chaining is forbidden, so one use case does not
drive another to build a process out of them; a coordinating operation is the named exception, declared as
such rather than emerging by accident.

- [Use cases must not invoke other use cases](/rule/usecase/dca-use-016.md)
- [Aggregate root](/marker/tactical/aggregateroot.md)
- [Domain event vs integration event](/decision/domain-event-vs-integration-event.md)
- [Event delivery: sync, async, and when you need an outbox](/decision/event-delivery-sync-async-and-outbox.md)
