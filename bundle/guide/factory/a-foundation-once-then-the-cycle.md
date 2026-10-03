---
type: Section
title: "A foundation once, then the cycle"
chapter: "Delivering a story: backlog, stages, gates"
source: guide
resource: dca-guide/process/factory.md
tags: [guide, section]
---

A person meets the factory in two parts. The **foundation** is written once and changed when the product or
the stack moves: setting the factory up, and describing the project. The **cycle** recurs with every body of
work:

```text
foundation   set up · describe                         once, and when something moves
cycle        discover → backlog → run → decide → delivered      with every body of work
                         └ plan → test → build → tidy → judge → document
```

- **Discover** finds the problem worth solving and proposes epics. It is optional: a person who knows the
  epic writes it straight away.
- **Backlog** turns a released proposal, or a person's words, into an epic and its stories, and releases them.
- **Run** takes a released story through the six stages. The stages are the inside of this one step, and only
  of this one.
- **Decide** answers what a stage may not decide alone, and accepts what a person looked at.
- **Delivered** shows what is done: stories, epics and their outcome events. Delivered is not shipped — the
  factory delivers stories into the repository, a release is the project's own step.

Describe stays out of the cycle because the description is not rewritten per story. It is amended in parts,
each by the step that found the reason: a structural answer brings the designed map and the product's
surfaces in line, the document stage the glossary and the map, a discovery may propose a description change
that a person releases, and a new technical capability adds its line to the stack. Each of these goes
through the description skill or the step that owns the part, never through a build stage.

Every step of the cycle leaves its state in files and answers a command — `status`, `decisions`, `discover
--list`, also as JSON. So any tool may draw the cycle; none has to.
