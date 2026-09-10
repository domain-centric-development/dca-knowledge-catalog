---
type: Section
title: One test per acceptance criterion
chapter: E2E Testing for Domain-Centric Architecture
source: guide
resource: dca-guide/e2e-testing.md
tags: [guide, section]
---

An end-user test earns its cost when it is the evidence for a stated criterion, and it is easiest to
keep honest when the mapping is explicit: **one end-user test per acceptance criterion of a story**,
recorded next to the criterion's key rather than guessed from test names.

```markdown
| criterion | test |
| --- | --- |
| shows-empty-state | com.example.reporting.MonthlyReportPageTest#showsEmptyState |
| lists-newest-first | com.example.reporting.MonthlyReportPageTest#listsNewestFirst |
```

Three rules keep that mapping meaningful.

**The criterion's key never appears in the test.** Not in its name, not in a display name, not in a
comment. A test says what the user can observe (`showsEmptyState`), and the link between criterion
and test lives in the table alone. A key written into a test name pins the test to a story that will
be closed long before the test is deleted.

**Red for the right reason, before the code exists.** A new end-user test must fail on its
*assertion*, not on a missing class or a wiring error, and it must not be green before the behaviour
is built. A test that is green too early proves nothing about the criterion — and the most common
cause is a stub that returns the very answer the criterion expects, so a stub should throw instead of
answering.

**No later step edits it.** The code changes until the test passes; the test does not change until
the criterion does. A test rewritten to match the implementation has stopped being evidence.

### When there is no browser to drive

A criterion still needs an end-user test when the story has no user interface — and the right shape
is then the highest level the project can actually run today, not a browser runner installed for the
occasion:

| The story delivers | The end-user test drives |
|---|---|
| a server-rendered page or a client app | the browser, through Page Objects (the rest of this document) |
| an HTTP API | the running application over HTTP, asserting status and payload |
| a message consumer | the message, published as a producer would, asserting the effect |
| a scheduled job | the job's entry point, with the clock or trigger the project uses |
| a use case with no surface yet | the input port in the wired application, with the note that no surface exists |

The last row is a real answer, not a fallback to be embarrassed about: a criterion whose actor has
no way in yet is a scoping question, and inventing a page or an endpoint to make a test possible
delivers a surface nobody specified — including, where it needs a guard, an authorisation decision
nobody reviewed. Test at the highest level that exists, say so, and let the missing surface be
decided as its own piece of work.

Adding a test framework the project does not have is a stack decision, never part of delivering a
story.

---
