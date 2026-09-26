---
type: Section
title: Starting where you are
chapter: "Delivering a story: backlog, stages, gates"
source: guide
resource: dca-guide/process/factory.md
tags: [guide, section]
---

**From zero, in a fixed order.** A project that starts empty gets its description first — what is to
be built, the technical decisions, the designed cut — and its skeleton second, from the stack's own
generator, so the versions are the generator's and not anyone's memory. Then the repository, the
architecture's building blocks and rule suite, a formatter run once over everything, and a browser
runner wherever the product has pages — each before the first story, because a story that has to set
one of them up in passing takes a stack decision nobody asked for. The decisions those steps need and
the description does not carry — the formatter's style, the browser runner and its selector convention —
are asked together with the description, in one pass, so the setup never stops halfway with a skeleton
on disk. The proof is that the application starts, every suite is green, and the browser smoke test
goes red when the start page's title is emptied.

**Empty means green.** In a project with no backlog, no glossary and no context map, nothing above
fails on absence: each stage says which file to create, and the gate reports what it skipped and
why. The first story is written, and the process works from there.

**Brownfield stays brownfield.** The contract applies to *new* items. An existing backlog is not
migrated wholesale and existing tests are not renamed: rewriting finished work would invent intents,
goals and outcome events nobody ever stated, and every one of those epics would then fail the gate
for good reason. The gate only ever looks at the story it is called with.

**Adopt, do not migrate.** Migrating old tickets invents intent nobody stated, and stays forbidden.
Adopting describes what the system does today, with evidence, and is how a brownfield project enters the
backlog. A story with `status: adopted` is never built: its scenarios are mapped to tests that exist and
are green, a test the adoption has to write itself is shown to work by a break — a minimal change to the
production code, applied to a scratch copy, that turns exactly this test red — and a fresh judge confirms
that each test asserts its scenario. Then the story counts as delivered, and a new story can depend on it.
Two limits hold: green is weaker than red-then-green, which is why the judge reads every mapped test and a
written test needs its break; and adoption is incremental — a project adopts the part the next new story
touches, not the whole system in one run.
