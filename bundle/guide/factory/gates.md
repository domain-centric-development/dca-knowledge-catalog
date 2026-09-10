---
type: Section
title: Gates
chapter: "Delivering a story: backlog, stages, gates"
source: guide
resource: dca-guide/factory.md
tags: [guide, section]
---

Between the stages runs a **gate**: a deterministic check, callable from the command line and from
CI, that verifies what a stage may not decide for itself. It is not a review and it has no opinion;
it either finds the evidence or it does not.

| Before | The gate checks |
|---|---|
| plan | the epic is complete; the story is well-formed, released, and its context is on the map |
| after test | every criterion is mapped to a test; the test exists in the sources; the test sources compile; **every mapped test is red** |
| after build | every mapped test is green **and was recorded red by the test stage**; the architecture suite passes; the formatter passes |
| after tidy | the same checks again — the stage's whole claim is that nothing changed |
| after document | every path and identifier the stage claims exists; every glossary row says how it was checked |

Three details in there are worth more than they look.

**A missing test looks exactly like a red one at the runner.** So the gate first finds the test in
the sources; without that, "red before the build" certifies nothing.

**A run that matched no test at all exits successfully on some runners and unsuccessfully on
others.** Neither outcome is evidence. So a mapped test is run with the command that covers the
source set the test actually lives in, and a test in a source set no command covers is a
configuration error rather than a verdict.

**A test that was never red proves nothing.** The test stage records which selectors it saw fail;
the build gate accepts a green test only if it is in that record. This is what closes the gap
between "the criterion is met" and "something green exists".

A command the project has not declared is **skipped and named**, never failed. A gate that fails on
something nobody configured gets switched off, and then there is no governance at all.

The same commands belong on the **commit** as well. Tool configurations do not travel between
editors, but every tool commits through version control, so a pre-commit check that runs the
project's own compile, test, architecture and format commands is the boundary that holds for
everyone. Keep it to what a developer will wait for; a check that takes minutes gets bypassed, and
then it guards nothing.
