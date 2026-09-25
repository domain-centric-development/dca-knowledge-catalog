---
type: Pitfall
title: Mocking the port whose adapter the change is about
tags: [pitfall, testing, adapter, port]
review: draft
owner: DCA catalog maintainers
evidence: [/guide/testing-levels.md, /marker/port-out/outputport.md, /marker/tactical/domaingateway.md]
---

A story changes an outgoing adapter — a new call to an external system, a different mapping, a new error case — and its tests replace the adapter's port with a mock. The use case is tested; the adapter is not. The request the adapter builds, the status and body it reads, its timeout: none of it runs.

## Why it is wrong

- The test covers everything except the one thing the change is about. It stays green when the adapter sends the wrong path, maps a field wrongly or treats a refusal as success.
- The mock encodes what the test author believes the external system does, twice: once in the adapter, once in the mock. When the belief is wrong, both agree and the suite is green.
- A browser test on top does not repair it: it passes through the adapter only on the happy path, and often against a stand-in that is not the adapter at all.

## Do instead

Test the scenario integrated: the application wired as in production, the adapter pointed at an HTTP stub on a free port that answers what the test arranges ([Recipe](/recipe/test-a-scenario-integrated.md)). A refusal is an arranged status, a timeout an arranged delay. Faked output ports stay right for a use-case unit test that tests orchestration only — where the adapter is not what changed.

## Anchors

- Guide: [Test levels](/guide/testing-levels.md)
- Markers: [OutputPort](/marker/port-out/outputport.md) · [DomainGateway](/marker/tactical/domaingateway.md)
- Related decision: [Which level for a scenario](/decision/test-level-for-a-scenario.md)
