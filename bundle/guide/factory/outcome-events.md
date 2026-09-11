---
type: Section
title: Outcome events
chapter: "Delivering a story: backlog, stages, gates"
source: guide
resource: dca-guide/process/factory.md
tags: [guide, section]
---

An epic's `metric` is a **domain or integration event whose publication in production is the
evidence that the epic delivered**. Not a story count, not a burndown, not "feature shipped".

The reason is that a story can be complete and an epic still worthless. Every criterion may be met,
every test green, the documentation current — and nobody uses the thing, so the problem in the
epic's `intent` is untouched. A story count measures the team's motion; an outcome event measures
the change in the system's behaviour that the epic existed for.

Because DCA applications already publish domain events for the facts that matter, the metric is
usually a name that exists:

```
metric: OrderPlaced          # the epic's point was that orders can be placed at all
metric: CartRecovered        # the epic's point was that abandoned carts come back
metric: StockChanged         # the epic's point was that an operator reacts before stock runs out
```

Where the event does not exist yet, that is a finding rather than a problem: the event is part of
the work, and naming it in the epic is what makes the epic measurable. Where an application keeps an
event publication log — a record of the events it published, which the event-driven patterns in this
guide produce anyway — that log is the measuring point, and no separate analytics apparatus is
needed to answer whether an epic delivered.

Two failure modes to avoid. An event named after the *implementation* ("row inserted", "endpoint
called") measures that code ran, not that anything happened for anyone. And an event that fires on
the way in ("checkout started") measures intent, not outcome; the outcome is the fact at the end of
the flow.
