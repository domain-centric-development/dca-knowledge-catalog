---
type: Section
title: One test per acceptance criterion
chapter: E2E Testing for Domain-Centric Architecture
source: guide
resource: dca-guide/topics/e2e-testing.md
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
story. That is exactly why a project that shows pages takes it **before its first story**. Otherwise
every story about a page falls back to reading the page's markup or script as text. Such a test proves
the wording, not what the browser does: that a countdown ticks, that a click hides a hint, that a
notification appears. A fallback taken story by story is a decision nobody took, and it grows with
every story. So the project sets up its browser runner once, when it is created, or records that it
deliberately has none.

### Adding a browser runner to an existing project

A project that shows pages and has no browser runner gets one as its own step, before the next story
that needs it — never inside that story:

1. **Pick the runner the stack already speaks.** The one the project's build can run without a second
   toolchain: a library in the test dependencies for a JVM or .NET build, a package in the project's
   own package manager for a JavaScript build. Pin its version, and install the browser builds that
   release expects.
2. **Give the browser tests their own place and command.** A source set or test project of their own,
   and one command that runs them; they are slower than the unit tests and may need the application
   running, so they are not mixed into the fast suite. Decide where the application runs — started by
   the test or beside it (below) — and say which.
3. **Write one smoke test first.** It opens the start page and asserts its title through a stable
   `data-test` selector — nothing about behaviour yet. The Page Object and the base class it needs
   are the ones every later test uses.
4. **Show that it can fail.** Empty the start page's title, run the command, see the smoke test go
   red, put the title back, see it green. A browser test that has never been red may be testing
   nothing — a wrong URL, a page that never loaded, a selector that matches an error page.
5. **Record it where the next change is planned.** The command and the runner's name go where the
   project keeps its build facts, so a plan takes browser tests as the shape for a page instead of
   falling back to reading markup as text.

### Time and permissions belong to the test

A page that counts, polls or expires is tested with a **fake clock** that moves only when the test moves
it, never with a sleep. Install it before the page loads, at a fixed time, and pause it there — installed
alone, the fake clock still runs at real speed, and a countdown test depends on how fast the machine is.
Then move it: five minutes of waiting become one call, and the countdown ticks in the order it would in
real time.

```java
page.clock().install(new Clock.InstallOptions().setTime("2026-01-05T08:00:00Z"));
page.clock().pauseAt("2026-01-05T08:00:00Z");
page.navigate(baseUrl + "/");
page.locator("[data-test='start-button']").click();
page.clock().runFor(3_000);
assertThat(page.locator("[data-test='remaining']")).hasText("04:57");
```

A browser API whose answer belongs to the user — notifications, geolocation, the clipboard — is
replaced before the page loads by a **stand-in** that records what it is asked and answers as the test
decides. "The user allowed it" and "the user refused it" are then two tests, not a manual click, and a
notification a headless browser would never show becomes observable.

### Where the application runs

Two variants, and a project picks one and says which:

- **Started by the test**, on a free port (`@SpringBootTest(webEnvironment = RANDOM_PORT)`, a
  `WebApplicationFactory` hosting Kestrel). The suite needs nothing running first and runs the same on a
  laptop, in CI and in an agent's shell. The default for a project whose pages need only the application.
- **Started beside the test**, its address passed in (`e2e.baseUrl`, `E2E_BASE_URL`), as the base classes
  above and the pipeline below do. For a system that needs a database or other services up first, and for
  running the same suite against a staging environment.

Mixing them by accident — a suite that starts the application and still reads a base URL — tests a
different instance than the one it started.

---
