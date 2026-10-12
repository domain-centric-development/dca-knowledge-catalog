---
type: Section
title: Three parts
chapter: "Delivering a story: backlog, stages, gates"
source: guide
resource: dca-guide/process/factory.md
tags: [guide, section]
---

A factory that delivers stories has three parts, and each lives in its own place:

- a **project description** — what is to be built, written by people before the code;
- a **backlog** of epics and stories, written by people, each story small enough for one run;
- a **runner** that works the backlog off, stage by stage, with a check between the stages.

```text
dca-factory.profile.yaml   the stack profile — the person's, committed
dca.profile.yaml           the method's configuration: where things are, the resolved conventions — optional
product/                   what is to be built and what holds (people write it; the spec is kept by delivery)
  overview.md              what, for whom, surfaces, qualities, what it is not
  tech.md                  stack, frontend approach, persistence, runtime, integrations, version policy
  domain.md                the designed cut: contexts, subdomain types, relationships and why
  spec/                    what holds: per context its scenarios and its glossary, and the journeys
  epics/<epic>/            the changes: the epic, its stories, and beside each story its decisions
  discovery/<topic>/       research and proposed epics
.agents/factory/           the installed pipeline (checks, runner) — replaced whole by an update
.dca-factory/runs/<story>/ the run's protocol: hand-overs, marks, journal — disposable
docs/                      what exists and why — written after the code, some of it generated
```

One owner per place. `product/` is the people's — the description, the epics with their stories and,
beside each story, the questions a stage asked and the answers a person gave. `.agents/factory/` is
installed code, `dca-factory.profile.yaml` the person's configuration, `.dca-factory/` the run's
protocol. A story carries its own state: `status: draft | approved | adopted | superseded` is the
person's line; `status: delivered`, `delivered:` and `delivered_by:` say that it is delivered, when, and
who claims it — `gate` where the last gate wrote them, `hand:<who>` where a person built the story and
delivered it by hand. Built or adopted makes no difference once delivered: one end state. A hand's claim
is a claim until the factory checks it the way it checks adopted behaviour; then the gate's line replaces
it. So the run folder can be deleted at any time and the factory still knows what is delivered and what
was decided; what is lost is history — hand-overs, the journal, what a story cost. Which stories are
delivered, and by whom, needs no tool: the front matter says it, and a `grep` lists it.

`product/` holds **intent** and **what holds**: written before the code, and read by every stage as input. `docs/` holds
**what exists and why** — architecture documentation, decision records, maps generated from the
code, user and operations guides — written after the code, by people and by the stage that documents
a story, which writes only what the code confirms. The rule of thumb: an intention that need not be
built yet goes to `product/`; a statement the code could show goes to `docs/`. A context's glossary
belongs to its spec — the language of what holds — not to the code's folders. Where the two places meet — the designed map against a map generated from
the code — a difference is a finding, not a duplicate: a context planned and not built yet, or built
without having been designed.

Setting the factory up is one step that does only what is missing, in any order relative to the
code: the description before the code, the code before the description, or an existing project that
has both and gets the factory added. A second run finds everything in place and writes nothing.
