---
type: Pitfall
title: A reference in the request body answered as not found
tags: [pitfall, error-handling, adapter, rest]
review: draft
owner: DCA catalog maintainers
evidence: [/guide/rules/error-handling-rules.md, /guide/rules/adapter-layer-rules.md, /template/rest-resource.md]
---

A request addresses a resource that exists, and its body carries an id that parses but names nothing — an item posted to an existing collection that refers to a record no one ever created. The use case fails with its not-found failure, and the incoming adapter answers that failure with `404`, the same as when the path itself names nothing. One failure type, one status: it reads as consistent.

## Why it is wrong

- `404` is a statement about the addressed resource: the path names nothing. Here the path names something that exists, so the answer claims something false about it.
- The caller looks for the error in the wrong place. A client that receives `404` checks its URL, retries a lookup of the resource it posted to, or drops a cached link to it — none of which helps, because the body was wrong.
- The two cases need different reactions. A missing resource means "ask for something else"; an unknown reference in a well-formed request means "this request cannot be served as sent", which is what `422 Unprocessable Content` says.

## What forbids it

No rule. The status is chosen in the incoming adapter's handler, and whether a not-found failure came from the path or from the body is a fact of the call, not of the import graph. It stays with review: for each not-found failure a handler maps, ask where the id it carries came from.

## Do instead

Decide the status by where the reference sits:

- the path names nothing → `404`;
- the path names an existing resource and a reference in the body parses but names nothing → `422`;
- a reference in the path or the body does not parse at all → `400`, answered by the adapter before any use case runs.

When the same failure type can arise from either place, the adapter that knows which id it took from the path answers it; where one handler serves several endpoints, give the body's case its own failure type, or let the endpoint translate it.

## Anchors

- Guide: [Error handling rules](/guide/rules/error-handling-rules.md) · [Adapter layer rules](/guide/rules/adapter-layer-rules.md)
- Template: [REST resource skeleton](/template/rest-resource.md)
- Related pitfall: [A business rule reported as an argument error](/pitfall/business-rule-reported-as-an-argument-error.md)
