---
type: Section
title: "Smoke test, happy-path test, journey test"
chapter: Test Levels in Domain-Centric Architecture
source: guide
resource: dca-guide/topics/testing-levels.md
tags: [guide, section]
---

All three drive the running application end to end. They answer different questions and belong to different
places.

| | Smoke test | Happy-path e2e test | Journey test |
|---|---|---|---|
| question | does the system run at all? | does this story do what it promises? | does the critical flow still work? |
| scope | broad and shallow: the application starts, a page or endpoint answers | one flow, the story's own surface | one flow across stories and contexts, to the epic's outcome |
| assertions | barely more than "no error, page there" | the scenario's `Then` | the business outcome — the epic's outcome event |
| belongs to | the setup of the project and of each test runner | a story, as a criterion | an epic, as a guard |
| proof that it works | broken once on purpose at setup | red before the build | none — when it can be written, every step exists |
| runs | after the setup, and whenever the runner changes | with the story's tests | in CI |

**A journey is defined by an epic, not by the product description.** An epic states an intent and names its
outcome event — the fact at the end of the flow. Its journey is that flow, walked end to end until the outcome
event is published, and it can only be written once the stories that build its steps are delivered. Before the
first line of code nobody can say which flow that will be; an epic without a journey has decided against one.

A journey test is a regression guard. It is green when it is written, which a criterion may never be, so it is
not a story's criterion but an item of its own that depends on the stories it walks. A journey run against a
deployed environment with synthetic data works as a post-deploy check; that is operations, not development.
