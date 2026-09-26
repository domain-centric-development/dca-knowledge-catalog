---
type: Recipe
title: Test a scenario integrated, the external system stubbed at the protocol
tags: [recipe, testing, use-case, adapter]
review: draft
owner: DCA catalog maintainers
evidence: [/guide/testing-levels.md, /guide/factory.md, /marker/port-in/usecase.md, /marker/port-out/outputport.md, /marker/tactical/domaingateway.md]
---

Test one scenario of a story below the page: the use case runs through the wired application — its input port or its HTTP surface, whichever the scenario's `When` names — with real adapters and persistence as the project runs it in tests. An external system the use case calls is a real HTTP server on a free port that answers what the test arranges. The test proves the scenario's `Then` and every adapter the use case passes through, the translation included.

This is not the use-case unit test, which fakes the output ports to test orchestration alone ([Test a use case](/recipe/test-a-use-case.md)). Both have their place; when a change is about an adapter, only this one covers it.

## Steps

1. **Take the scenario's level from the plan.** The story's happy path is tested end to end; every other scenario is tested here, unless its `Then` only a browser can observe ([Which level for a scenario](/decision/test-level-for-a-scenario.md)).
2. **Start the application as the tests run it** — the project's integration source set or test project, with the persistence it uses in tests. No browser.
3. **Point the adapter at a stub.** Start an HTTP stub on a free port and set the adapter's base URL from configuration to the stub's URL. The URL is a property of the application, never a constant in the adapter.
4. **Arrange** — the `Given`: state through the application's own ports, and the external system's answer as the stub's arrangement (a status, a body, a delay for a timeout).
5. **Act once** — the `When`, through the input port or the HTTP surface.
6. **Assert the `Then`** — the result or response, the state the application now shows, and where the scenario names it the request the adapter sent to the stub.
7. **Cover the adapter's cases** — a case the adapter handles that no scenario names (a malformed body, a status the story does not mention) gets an integration test of its own, outside the story's criteria.

## Checklist

- The adapter talks to a real server; its port is not mocked ([pitfall](/pitfall/mocking-the-port-of-the-changed-adapter.md)).
- No shared or real instance of the external system: the test passes or fails on this code alone.
- One scenario per test, the scenario's own values.

## Anchors

- Guide: [Test levels](/guide/testing-levels.md) · [Factory process](/guide/factory.md)
- Markers: [UseCase](/marker/port-in/usecase.md) · [OutputPort](/marker/port-out/outputport.md) · [DomainGateway](/marker/tactical/domaingateway.md)
- Related: [Add an anti-corruption layer](/recipe/add-an-anti-corruption-layer.md) — the adapter this test usually proves
