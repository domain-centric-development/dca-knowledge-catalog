---
type: Section
title: The three levels
chapter: Test Levels in Domain-Centric Architecture
source: guide
resource: dca-guide/topics/testing-levels.md
tags: [guide, section]
---

| Level | What it runs | What it proves |
|---|---|---|
| **unit** | one aggregate, value object or domain service, no framework | an invariant the domain must never break |
| **integration** | a use case through the wired application — its input port or its HTTP surface — with real adapters and persistence as the project runs it in tests; an external system stubbed at the protocol | a scenario's `Then` as the user states it, and every adapter the use case passes through |
| **e2e** | the running application through its page, in a browser | that the page is wired to the use case, and what only a browser can observe |

**Rule: a scenario is tested at the lowest level that observes its `Then` from outside.**

The layering makes the integration level strong. The domain is free of framework types, adapters translate at
the edge, a use case sits behind an input port. A scenario whose `Then` is a business outcome or a response is
fully observable below the page, through the same adapters a browser test would pass. What is left to a browser
is what the page does after it has loaded: a countdown, a script's reaction to a click, a notification.

**Rule: the end-to-end suite starts the application itself, on a free port.** A suite that drives an
application someone started beforehand tests whatever happens to answer on that address: another service on
the port turns every test red, a missing one skips them all, and neither says anything about the page. A suite
that starts its own application brings what it needs — an external system as a stub it starts first, the
database the application's tests already use — and runs the same on a laptop, in CI and in a pipeline's gate.
The same tests may still be pointed at a deployment by naming its address; that is a check of the deployment,
not the suite's normal run.
