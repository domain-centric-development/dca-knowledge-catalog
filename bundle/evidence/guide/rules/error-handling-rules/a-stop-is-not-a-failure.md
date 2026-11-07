---
type: Reference
title: ERROR HANDLING RULES — A stop is not a failure
tags: [reference]
evidence_for: "/guide/rules/error-handling-rules.md#a-stop-is-not-a-failure"
---

[Full node and context](/guide/rules/error-handling-rules.md#a-stop-is-not-a-failure). This is an evidence excerpt; retain the parent selection and caveats.

### A stop is not a failure

A run cancelled from outside — a shutdown signal, an interrupt, a deadline — is neither a broken rule, nor a
refusal, nor a request the application cannot serve. It is a case of its own: **a stop passes through untranslated.**

- Any port may raise it, when the work it waits for is cancelled.
- No adapter translates it into a domain or use-case exception, no use case catches it, and no use case returns it
  as a case of its result.
- The entry point that owns the process or the request turns it into the end: an exit code, an aborted response,
  a message left for redelivery.

Both platforms model it so, and cooperatively — the work is asked to stop, never killed:

- **.NET** hands a `CancellationToken` through every port call; a cancelled operation raises
  `OperationCanceledException`.
- **Java** signals a stop by interruption; a blocking call raises `InterruptedException`. Code that is not the
  thread's owner never swallows it: it rethrows, or restores the flag with `Thread.currentThread().interrupt()`.

A `catch` that turns a stop into a failure is the defect to look for in review: the request then answers with an
error for something nobody did wrong, and a retry repeats work the owner wanted to end. A use case that must leave
its state clean on a stop keeps its steps inside one transaction, which the stop rolls back.
