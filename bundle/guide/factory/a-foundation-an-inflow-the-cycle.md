---
type: Section
title: "A foundation, an inflow, the cycle"
chapter: "Delivering a story: backlog, stages, gates"
source: guide
resource: dca-guide/process/factory.md
tags: [guide, section]
---

A person meets the factory in three parts. The **foundation** is written once and changed when the product or
the stack moves: setting the factory up, and describing the project. The **inflow** fills the backlog when there
is new work to find. The **cycle** is what every story turns through, one turn per story:

```text
foundation   set up · describe                              once, and when something moves
inflow       discover — beside it a wish, a judge's finding, an epic's journey     when there is new work
cycle        backlog → run → decide → delivered             with every story
                      └ plan → test → build → tidy → judge → document
```

- **Discover** finds the problem worth solving and proposes epics, each with its outcome event. It is one way
  into the backlog, not a step every story passes: a person who knows the epic writes it straight away, a wish
  becomes a story in a person's words, a judge's finding taken to the backlog becomes one, and a delivered epic
  without a journey test proposes its journey. A discovery's own questions are answered where it is read.
- **Backlog** turns a released proposal, or a person's words, into an epic and its stories, and releases them.
- **Run** takes a released story through the six stages. The stages are the inside of this one step, and only
  of this one.
- **Decide** answers what a stage of a story may not decide alone, and accepts what a person looked at.
- **Delivered** shows what is done: stories, epics and their outcome events. Delivered is not shipped — the
  factory delivers stories into the repository, a release is the project's own step.

Above the cycle runs a slower loop that is no step of its own. An epic names its outcome event; a discovery
proposes the epic with it. Delivered shows whether the event happens — the epic's journey ends in it —, and an
event that does not happen can start the next discovery.

Beside the three parts stands the **rulebook**: what the gate checks, what the runner decides, what each stage is
told. A person looks it up; no story passes through it.

Describe stays out of the cycle because the description is not rewritten per story. It is amended in parts,
each by the step that found the reason: a structural answer brings the designed map and the product's
surfaces in line, the document stage the glossary and the map, a discovery may propose a description change
that a person releases, and a new technical capability adds its line to the stack. Each of these goes
through the description skill or the step that owns the part, never through a build stage.

Every step of the inflow and the cycle leaves its state in files and answers a command — `status`, `decisions`, `discover
--list`, also as JSON. So any tool may draw them; none has to. Every order a view shows is the factory's
too — what comes next in the schedule's order, the backlog newest first by the `created:` each epic and story
carries, the newest delivery first — so two views never sort the same backlog differently. The status a person
asks for is short: what runs, what waits for them, what comes next and the totals; every story, one story or one
epic only on request.
