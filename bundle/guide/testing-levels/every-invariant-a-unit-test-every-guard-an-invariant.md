---
type: Section
title: "Every invariant a unit test, every guard an invariant"
chapter: Test Levels in Domain-Centric Architecture
source: guide
resource: dca-guide/topics/testing-levels.md
tags: [guide, section]
---

**Rule: every rule a domain type enforces is an invariant, and every invariant has a unit test. A guard nobody
named as an invariant is not written.**

An invariant is what the domain must never let happen, whatever calls it: a title that is empty or longer than
allowed, a task completed twice, an order line with a negative quantity. It belongs to the aggregate, entity or
value object that holds the data, and it is tested there, without a framework — the part of the suite that
survives a rewrite of every adapter.

The guards a type's constructor carries are invariants too: a value that is required, trimmed, within a range,
unique within its aggregate. A criterion rarely names them, because a user never reaches them through the page —
the page trims, the form requires. That is exactly why they need their own test: the next caller is not the page.
A guard written without a test is code nobody asked for; one that is needed is named as an invariant and tested
first. Planning names the invariants of every domain type a change touches, its guards included, or says why a
type has none.
