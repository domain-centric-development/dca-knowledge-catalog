---
type: Section
title: "Building one: what actually holds"
chapter: "Delivering a story: backlog, stages, gates"
source: guide
resource: dca-guide/process/factory.md
tags: [guide, section]
---

Everything above is the shape. This is why it is that shape — each rule with the failure it
prevents, because a rule without its failure gets dropped the first time it is inconvenient.

### Evidence, never assertion

**An agent's report about its own work is not evidence.** It is the one sentence the whole
construction rests on. Every claim that decides whether a story is done must be checkable by
something that does not want the answer to be yes: a script, a build, a file on disk.

**A stage is finished when its file exists** — not when a delegation reports success. A mechanism
that says "done" and produced nothing has to be indistinguishable from one that stalled, or the
run waits for something that will never arrive. Check for the artefact; where it is missing, do
the stage differently and say that you did.

**A missing test looks exactly like a red test at the runner.** Both come back as failure. So
before "the test is red" means anything, the test has to be *found in the sources*. Without that
step, an empty test table and a correct one produce the same green run.

**A run that matched no test at all is not a verdict.** It exits successfully on some runners and
unsuccessfully on others — so one stack reads it as a passing test and another as a failing one,
and both are wrong. Therefore: pick the command from *where the test actually lives*, declare one
command per test source set, and treat "no declared command covers this test" as a configuration
error rather than a result.

**A test that was never red proves nothing.** Green after the code exists is only evidence if the
same test failed before it. Record which tests were seen failing, and require that record before
accepting green — otherwise a criterion with a mistyped, misplaced or trivially-true test is
certified as met.

**A stub must refuse to answer.** It throws; it never returns a value, not even an empty list. For
a criterion whose expected answer *is* the empty case, a stub returning empty makes the test green
before any code exists — and that test will never fail again.

**A report names what happened, not what the script can do.** A run that lists six stages after
one of them ran is the same self-assessment as an agent grading itself, in a place nobody thinks
to distrust.

### State lives in files

**Anything the run needs to remember is a file.** The round counter, the record of which tests
were red, which stage is next, what the reviewer decided. An orchestrator that remembers cannot be
resumed, cannot be handed to another tool, and cannot be checked afterwards — and its memory is the
one part of the run nobody can audit.

**A repeat round must be able to read why the last one was refused.** Hand the refusal on as a
file the stage is told to read. A stage that repeats blind reproduces exactly what was rejected,
and the loop burns rounds on it.

**A round belongs to the story, not to the machine.** A refusal whose cause no stage can change — a
build tool missing on the gate's path — is named as the environment's and stops the run once,
without counting. Counted as a round, it sends a stage three times against a wall it cannot move,
and the story stops as if it had failed.

**Resume where the files say, and check them before a stage reads them.** A run started on one story
begins at the state its files record, not at the first stage by default: a delivered story runs
nothing, an accepted one only its last gate. Where the file of the stage it resumes at exists, the
gate checks it on today's tree first. A report from a round the machine lost otherwise becomes the
next stage's instruction, and the stage fixes what is no longer wrong.

**An answer that exists only in a reply is lost.** A scoping decision, an assumption the domain
expert settled, a reason for a deviation: if it is not written where the next run will look, the
same question comes back in a month with a different answer.

### One source, or two truths

**Never copy what you can point at.** A copied skill folder, a vendored knowledge catalog, a
duplicated template: each is a second truth that drifts silently, and the drift is invisible
precisely because both copies look right. Point at the source; where a copy is unavoidable, make
its staleness visible and say when it needs renewing.

**A copy that must exist gets a freshness statement, not trust.** Naming a knowledge source means
vouching that it is current — a citation from a stale catalog makes a wrong rule id look verified.
Whoever reads it cannot tell; whoever wrote it must.

**Instructions have a size budget.** Tools stop reading project documents at a limit and truncate
without a word, so an instruction past that point does not exist for them while its author
believes it is in force. Keep the always-loaded file short and put the detail in documents it
points at.

### Where a run must stop

**Three verdicts, not two.** Pass and "fix this" are not enough: the third case is that the *story*
is wrong. That one must never go back to the builder, because a correction that silently changes an
agreed criterion replaces the contract with an opinion.

**A plan may not invent a way in for its actor.** If the criteria can only be observed through a
page, an endpoint or a consumer the system does not have, adding one is a product decision — and
where that surface needs a guard, an authorisation decision too. Both belong to a human. A guard
that arrives as a side effect of a story is a guard nobody reviewed and no test holds.

**A new boundary is not a story.** A new bounded context, or a new relationship between contexts,
is a decision about language and ownership. Recorded, then reflected on the map; never smuggled in
by the first story that needs it.

**The enforcement boundary is the commit.** Tool configurations do not travel between tools, and
whoever changes tools loses them silently. The commit is the one gate everybody passes through, so
the project's own compile, test, architecture and format commands belong there — narrow enough that
nobody has a reason to bypass it, because a bypassed check guards nothing.

### Configuration, not knowledge

**A command the project has not declared is skipped and named, never failed** — unless the project
itself declared it mandatory (`required:`). A gate that fails on something nobody configured gets
switched off within a week, and then there is no governance at all. Skipping loudly keeps the gate
installed and the gap visible.

**The process knows no project.** Build commands, test source sets, runners, formatters, the
reviewer for a perspective: all of it is the project's, in one file the project owns. A stage that
would break in a system without your domain in it is not a stage, it is a local habit.

**Model and effort are the project's choice per tool, never the process's, and a broken default must
not stop the run.** The process names no model; the project may bind one to a tool
(`model.<tool>.<stage>`, above), and without that key the tool's own default applies — otherwise the
pipeline is unusable wherever a default provider happens to be unavailable.

### Doctrine has to decide

**Where guidance can be read two ways, two builders produce two designs.** Two teams given the same
story, the same conventions and the same reference produced a repository finder and a composable
rule object — both defensible, because the decision guide let two of its own criteria fire at once
and never said which wins. The fix is not in either code base: it is in the sentence that failed to
decide.

**Fix a divergence at its source, or it returns.** Reconciling the two code bases leaves the
ambiguity in place for the next pair. Sharpen the rule, the guidance or the checkable constraint —
and record which one you sharpened.

**Reviewing follows use, not stock.** A body of guidance is too large to review as a whole and most
of it is never load-bearing. What a delivery run actually cites is the list worth reading; a
proposal that decided a design question is the finding, and the rest can wait.

### Verifying the machinery itself

**The checker needs a checker.** The gate is the argument for everything else, so it earns tests of
its own: fixtures where every check must refuse what it should refuse. Defects found by running
real stories cost an hour apiece; the same defects fail a fixture in milliseconds.

**A regression test that does not fail on the bug is decoration.** Put the defect back, watch the
test go red, then remove it again. A test written from the fix rather than from the failure usually
asserts the wrong thing.

**Make the orchestration testable without a model.** Give the tool invocation a seam that a test can
replace, or the loop — the part where a skipped stage or a false success hides — can only be
exercised by burning real runs.

**A verification names its own blind spots.** What it could not observe is not what it found to be
fine. A report that hides the difference invites exactly the trust it has not earned.
