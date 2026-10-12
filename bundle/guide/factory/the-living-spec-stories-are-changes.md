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
own: `product/spec/<context>/scenarios.md`, one file per bounded context, carrying every criterion that
holds today — in the story's own shape, a scenario under its rule or a line — and under each the one test
that proves it. No status, no ticks, no story id: what stands there holds. A criterion without a test
line, or with a red test, is visibly unproven, readable without any tool. Flows across contexts stand in
`product/spec/journeys.md`.

A criterion's key is unique within its context and names one behaviour for good. That makes the change
a story carries computable. The person writes the wish in their own words — new criteria, and where
behaviour the system has changes, a sentence under `## Changed expectations`. The plan reads the spec
and derives the delta by key: what the story adds, what it changes, what it takes away, which rule it
rewords. A check holds the delta to the story and the spec, and to one rule above all: nothing that
holds changes without a person's sentence behind it — the story's changed expectations, or an answered
question. Where neither says it, the plan asks.

The gate that delivers merges the delta — after the human's acceptance, where there is one — and writes
each criterion's test line. Nothing else writes the scenarios. Stories delivered side by side meet at
the merge: the gate checks the delta again against the spec as it stands then, and a criterion another
story changed meanwhile is a question, not a silent overwrite. From then on the story is history; editing
it changes nothing that holds, and a change of delivered behaviour is a new story. The context's
glossary stands beside its scenarios: the language of what holds, kept by the glossary work as before.

Two questions, two places: *which stories are done, by whom?* — the stories' front matter; *what holds
today?* — the spec. Two implementations of the same backlog end in the same spec, criterion by criterion.
