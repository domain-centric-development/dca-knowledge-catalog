---
type: Section
title: Test shapes
chapter: Test Levels in Domain-Centric Architecture
source: guide
resource: dca-guide/topics/testing-levels.md
tags: [guide, section]
---

The pyramid (Cohn, Fowler) asks for many unit tests and few UI tests; the trophy (Kent C. Dodds) for mostly
integration tests; the honeycomb (Spotify) for integration tests at the service boundary and no integrated
tests against other systems. Martin Fowler points out that much of the debate is vocabulary: what one team
calls a sociable unit test, another calls an integration test. The levels above use the words in the sense of
the table at the top.

A recent position starts with end-to-end tests, because agents make them cheap to write. That is an argument
about writing tests. In a pipeline that runs every test several times per story, the cost is in running them,
and the part that carries over is "cover the critical path end to end" — the happy path per story, the journey
per epic.
