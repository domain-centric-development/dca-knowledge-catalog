---
type: Pitfall
title: A request modelled as an event
tags: [pitfall, domain-event, events, adapter, application]
review: draft
owner: DCA catalog maintainers
evidence: [/guide/rules/domain-layer-rules.md, /guide/rules/application-layer-rules.md, /marker/tactical/domainevent.md, /marker/port-in/usecase.md, /decision/coordinating-a-multi-step-process.md, /decision/reacting-to-an-event.md]
---

Something arrives at the edge and asks for work: a button press, a file dropped into an inbox folder, a message on a queue that says "export this report". The model calls it `ExportRequested`, a domain event, and a listener does the export. There is no object that holds the request: whether it was refused, is still waiting or failed halfway is written nowhere.

## Why it is wrong

- **A request can be refused; a fact cannot.** An event says what happened, and nobody may say no to it. A request may be turned down, may wait for its turn, may fail and be retried. Modelled as an event, each of those outcomes has nowhere to go.
- **Its state is lost.** The caller asks "what happened to my export?" and nothing answers — the event was published, the listener ran or did not.
- **The events that matter are missing.** `ReportExported` and `ExportRefused` are the facts others want to react to. With the request itself as the event, they are never raised.

## How to spot it

- An event named `…Requested`, `…Pressed`, `…Submitted` whose listener decides whether to do it.
- A listener that can refuse, retry or give up on an event.
- A request whose status users ask about, with no aggregate that holds it.

## What catches it

No rule — the name of a type does not say whether it is a fact or a wish. It is a modelling question: can anyone say no to this?

## Do instead

A request is a command. The incoming adapter — a controller, a queue consumer, a reader of the inbox folder — turns it into the command of a use case. Where the request has a life of its own (it waits, it is retried, someone asks about it), it gets a lifecycle: an aggregate that holds it, or a process manager when it spans several steps ([Coordinating a multi-step process](/decision/coordinating-a-multi-step-process.md)). Its outcomes raise the events: `ReportExported`, `ExportRefused`. A file or a queue as an inbox is a legitimate transport for commands — the port stays the same when the transport changes.

## Anchors

- Guide: [Domain layer rules](/guide/rules/domain-layer-rules.md) · [Application layer rules](/guide/rules/application-layer-rules.md)
- Markers: [DomainEvent](/marker/tactical/domainevent.md) · [UseCase](/marker/port-in/usecase.md)
- Decisions: [Coordinating a multi-step process](/decision/coordinating-a-multi-step-process.md) · [Reacting to an event](/decision/reacting-to-an-event.md)
