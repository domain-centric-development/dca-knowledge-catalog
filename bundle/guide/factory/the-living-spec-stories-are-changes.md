---
type: Section
title: "The living spec: stories are changes"
chapter: "Delivering a story: backlog, stages, gates"
source: guide
resource: dca-guide/process/factory.md
tags: [guide, section]
---

A story says what is to change; it does not stay true. A later story changes the same behaviour, and
the first one, still in its folder, says what no longer holds. So what holds lives in one place of its
own: `product/spec/<context>/`, per bounded context, carrying every criterion that holds today — in the story's
own shape, a scenario under its rule or a line — and under each the one test that proves it. No status, no ticks,
no story id: what stands there holds. A criterion without a test line, or with a red test, is visibly unproven,
readable without any tool. Flows across contexts stand in `product/spec/journeys.md`.

Within a context, what holds is grouped by **feature**: `product/spec/<context>/<feature>/scenarios.md`, and the
context's own `scenarios.md` for what belongs to no feature. Not by epic: an epic is a change like a story and is
over once delivered, while a feature lasts — a later epic extends it or rebuilds it. A feature is a word of the
context's language, with its glossary entry; it is born in the plan of the story that first needs it, and a person
accepting that story sees it come. A story names one feature; criteria of two are two stories.

A criterion's key is unique within its context and names one behaviour for good. That makes the change
a story carries computable. The person writes the wish in their own words — new criteria, and where
behaviour the system has changes, a sentence under `## Changed expectations`. The plan reads the spec
and derives the delta by key: what the story adds, what it changes, what it takes away, which rule it
rewords, and where a criterion moves from one feature to another — the key stays, it is unique across the
context. A check holds the delta to the story and the spec, and to one rule above all: nothing that
holds changes without a person's sentence behind it — the story's changed expectations, or an answered
question. Where neither says it, the plan asks.

The person who accepts a story sees what the spec will say: per criterion what is added, changed, taken away —
with the reason — or moved, and a new feature named. They accept what will hold, not only the story. The gate that
delivers merges the delta — after that acceptance, where there is one — writes each criterion's test line, and
checks the spec's shape before it writes: a key twice, a scenario without its trigger or its outcome, a feature
without its glossary entry stop it. Nothing else writes the scenarios. Stories delivered side by side meet at
the merge: the gate checks the delta again against the spec as it stands then, and a criterion another
story changed meanwhile is a question, not a silent overwrite. From then on the story is history; editing
it changes nothing that holds, and a change of delivered behaviour is a new story. The context's
glossary stands beside its scenarios: the language of what holds, kept by the glossary work as before.

Two questions, two places: *which stories are done, by whom?* — the stories' front matter; *what holds
today?* — the spec. Two implementations of the same backlog end in the same spec, criterion by criterion, and in
the same order: a rule's criteria stand as the story that delivered them last lists them, whichever of them arrived
first.
