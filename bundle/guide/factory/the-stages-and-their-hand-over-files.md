---
type: Section
title: The stages and their hand-over files
chapter: "Delivering a story: backlog, stages, gates"
source: guide
resource: dca-guide/process/factory.md
tags: [guide, section]
---

One story runs through six stages. Every stage is a **closed assignment**: it reads the story and
its predecessor's file, and it writes exactly one file of its own. No stage relies on a
conversation, so a stage can run in a fresh context, in a separate process, or on another day
without changing the result.

| Stage | Reads | Writes |
|---|---|---|
| plan | the story, the project description, the glossary and the generated context map if present | `tasks/<story>/plan.md` |
| test | the story, `plan.md` and the files it names | `tasks/<story>/tests.md` — with the criterion-to-test table |
| build | the story, `plan.md`, `tests.md` and the files they name | `tasks/<story>/build.md` |
| tidy | the story, `plan.md`, `build.md`, the files the story changed | `tasks/<story>/tidy.md` |
| judge | the story, all predecessors, the story's diff, the product and the technical description | `tasks/<story>/judge.md` — with a verdict |
| document | the story, all predecessors, the story's diff, the project's documents | `tasks/<story>/document.md` |

**The builder stages may share one context, the judge never.** Plan, test, build and tidy can run one
after another in a single context, each still writing its own file and each still gated. That costs
less, because each stage builds on what the one before read instead of reading it again. What it gives
up is that the build stage knows how the tests were written. The gate compensates for that: it binds
the red proof to the tests as they were seen failing. The judge always starts fresh, because a review
by the context that wrote the code is the self-assessment the gates exist to replace. Sharing is a
choice per run, not the default; a check outside the shared context confirms that the red proof exists
and runs the build and tidy gates again.

**What a story changed is recorded, not reconstructed.** Around every stage the pipeline records
which files changed, and after it the whole story's diff. The diff is taken against a snapshot of the
working tree at the story's first stage, so a repository without a single commit gets one too.
Every hand-over names its files: what the plan expects to change and what a later stage should read,
the tests written, and the files build and tidy touched, which a gate checks against what actually
changed. The next stage opens those files first. A stage that has to rebuild the diff itself
explores the repository, and that exploration is paid again on every turn of the stage.

The **plan** names the elements that change — aggregates, value objects, use cases with their ports,
adapters — in the project's own vocabulary, and picks the shape of the end-user test per criterion
from what the project can run *today*. It backs every statement about the code with a file and a
line. It writes no code.

The **test** stage writes one end-user test per acceptance criterion, plus unit tests for the
invariants the story introduces, and records the mapping:

```markdown
| criterion | test |
| --- | --- |
| shows-empty-state | com.example.reporting.MonthlyReportPageTest#showsEmptyState |
```

It adds only the stubs the test sources need to compile, and a stub **refuses to answer** — it
throws rather than returning a value, even an empty one. A stub that returns the answer a criterion
expects makes the test green before any code exists, and a green test at this point proves nothing.

The **build** stage makes those tests pass with the smallest change that works, following the plan's
change list. An element the plan did not name is a sign the plan was wrong: it is noted, not quietly
added. It never changes a test to make it pass.

The **tidy** stage is the refactor half of red–green–refactor, which the build stage deliberately
leaves undone. It works only inside the story's footprint, changes no test and changes no behaviour.
A tidy stage that changes nothing and says why is finished, not skipped.

The **judge** stage reviews the change from three perspectives that always run — the model, the
boundaries, the craft — with a file and a line behind every finding, and returns one of three
verdicts (below). A project may add further perspectives; it cannot switch the three off, because a
review without the boundaries is not a review of a domain-centric architecture.

The **document** stage brings the glossary, the context map and the project's reader documentation
in line with what the story changed, and it carries the same duty of proof as the code: every path,
file, class and command it names must exist, checked rather than remembered, and written as it
resolves from the project root.
