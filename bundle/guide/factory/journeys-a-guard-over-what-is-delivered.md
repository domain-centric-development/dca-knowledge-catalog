---
type: Section
title: "Journeys: a guard over what is delivered"
chapter: "Delivering a story: backlog, stages, gates"
source: guide
resource: dca-guide/process/factory.md
tags: [guide, section]
---

An epic may name its **journey** — the flow through its stories that must never break, walked to its
outcome event. Written as an event timeline, each step is a command and the event it causes, ending in
the outcome event; a step whose command or event the glossary does not name is a question first. The journey test is a backlog item of its own (`kind: journey`) that depends on the stories
building its steps. It becomes ready when they are delivered and runs plan, test, judge and document —
there is nothing to build. Its gate expects the test **green**, the inverse of a story: every step exists
when it is written, so it is a regression guard, not a criterion.

An epic whose stories are all delivered and that has no journey is shown as **delivered, unguarded**: the way
to its outcome event has no test. That is a hint, not a stop. An epic that decides against a journey says so —
`- none: <why>` under `## Journey` — and is no longer named; silence decides nothing.
