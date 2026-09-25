---
type: Section
title: "Integrated, not integrated against another system"
chapter: Test Levels in Domain-Centric Architecture
source: guide
resource: dca-guide/topics/testing-levels.md
tags: [guide, section]
---

**Rule: an external system is stubbed at the protocol, never mocked at the port and never called for real.**

An integration test of an outgoing adapter runs the adapter against a real HTTP server on a free port that
answers what the test arranges (WireMock in Java, WireMock.Net in .NET). The adapter builds its request and
reads the status and body exactly as it does in production, so the test proves the translation.

Two alternatives look similar and prove less:

- **A mock of the port** replaces the adapter itself. The test then covers everything except the one thing the
  change is about — the translation. When a story changes an adapter, mocking its port is a defect in the test.
- **A shared or real instance** of the other system makes the test pass or fail on that system's state and
  availability. Spotify calls this an *integrated test*: "a test that will pass or fail based on the correctness
  of another system". It belongs in a staging check, not in the suite a change must pass.
