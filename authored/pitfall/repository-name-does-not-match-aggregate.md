---
type: Pitfall
title: Repository name does not match the aggregate
tags: [pitfall, tactical, repository, aggregate, naming, port-out]
review: draft
owner: DCA catalog maintainers
evidence: [/rule/tactical/dca-tac-016.md, /rule/naming/dca-nam-004.md, /marker/port-out/repository.md, /marker/tactical/aggregateroot.md, /guide/rules.md, /guide/package-structure.md]
---

The aggregate is called `Task`; the repository is called `TodoRepository`. Both words are fine ubiquitous language — the team says "todo" in conversation and "task" in the model — and the interface extends `Repository<Task, TaskId>` correctly. The architecture test fails anyway: `TodoRepository refers to 'Todo' which cannot be resolved in its bounded context`.

## Why it is wrong

- A repository is the collection of exactly one aggregate type, and its name is how the codebase says which one. `TodoRepository` claims a `Todo` aggregate that does not exist; a reader who searches for the collection of tasks finds nothing.
- Two names for one concept is the naming drift that the ubiquitous language exists to prevent. The mismatch usually means the glossary has not decided — and the code is where that decision becomes visible.
- The rule derives the aggregate name from the interface's simple name minus `Repository` and looks for a class with exactly that name in the same context implementing `AggregateRoot`. The generic parameter `Repository<Task, TaskId>` plays no role; the interface's methods play no role. Only the name is checked, because the name is the contract with the reader.

## What forbids it

- [Repositories must only exist for Aggregate Roots](/rule/tactical/dca-tac-016.md) — no class `Todo` in the context, so the repository is reported; the same rule fires when a `Todo` exists but is not an aggregate root.
- [Repository Interfaces must end with 'Repository'](/rule/naming/dca-nam-004.md) — the suffix the derivation strips.

## Do instead

Pick one name per concept and use it for the aggregate, its id, its repository and its use cases: `Task`, `TaskId`, `TaskRepository`, `CompleteTaskUseCase` — or `Todo`, `TodoId`, `TodoRepository`, `CompleteTodoUseCase`. Record the choice in the context's glossary so the next repository does not reopen it. Renaming the repository is the cheap fix; renaming the aggregate is the right one when the experts actually say "todo".

- Related pitfall: [A Repository for something that is not an aggregate root](/pitfall/repository-for-non-aggregate.md) — the same rule seen from the other side: the name resolves, but to an entity.

## Anchors

- Markers: [Repository<T, ID>](/marker/port-out/repository.md) · [AggregateRoot<T, ID>](/marker/tactical/aggregateroot.md)
- Rules: [Repositories must only exist for Aggregate Roots](/rule/tactical/dca-tac-016.md) · [Repository Interfaces must end with 'Repository'](/rule/naming/dca-nam-004.md)
- Guide: [Layer rules](/guide/rules.md) · [Java package structure](/guide/package-structure.md)
- Recipe: [Add a repository with adapter](/recipe/add-a-repository-with-adapter.md)
