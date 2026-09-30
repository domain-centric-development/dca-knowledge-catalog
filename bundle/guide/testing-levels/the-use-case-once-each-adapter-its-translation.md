---
type: Section
title: "The use case once, each adapter its translation"
chapter: Test Levels in Domain-Centric Architecture
source: guide
resource: dca-guide/topics/testing-levels.md
tags: [guide, section]
---

**Rule: a use case is tested once, through its input port. An incoming adapter is tested for its translation.**

A use case is often called from more than one place: a page, an API, a message consumer, a tool an agent calls.
A scenario tested through each of them tests the same use case once per adapter — the same outcome, the same
persistence, the same stubs — and every one of those tests breaks when the use case changes. So the level has two
shapes:

- **The port test** runs the use case through its input port in the wired application: real outgoing adapters,
  persistence as the project runs it in tests, an external system stubbed at the protocol. It asserts the
  scenario's business outcome — what is stored, refused, published, returned. It is the test of the use case,
  whichever adapter calls it.
- **The adapter test** runs one incoming adapter against a stubbed input port: the request it turns into a
  command, and the page, status or payload it makes of the result and of each refusal. It asserts what only the
  adapter produces — a text on the page, a status code, a redirect, a message's payload. Where the framework
  offers a slice for the adapter alone (a web slice in Spring, a test host in ASP.NET Core), it runs in that.

A scenario's test is the one whose shape observes its `Then`: a business outcome goes to the port test, a text or
status only the page or the API shows goes to that adapter's test, with the stubbed port answering the outcome.
The happy path's end-to-end test is what proves the two fit together.

Stubbing the input port in an adapter test is not the mistake the next section warns about: there the adapter
under test is replaced by a stub of its own port; here the adapter is the unit under test, and the use case behind
the port has a test of its own.
