---
type: Reference
title: ERROR HANDLING RULES — Absence is not always a refusal
tags: [reference]
evidence_for: "/guide/rules/error-handling-rules.md#absence-is-not-always-a-refusal"
---

[Full node and context](/guide/rules/error-handling-rules.md#absence-is-not-always-a-refusal). This is an evidence excerpt; retain the parent selection and caveats.

### Absence is not always a refusal

**"Which one, if any" answers *none* with an empty value.** A query that asks whether there is one — the caller's
active session, an open order, the current draft — has "none" among its normal answers. It returns an empty value
(`Optional.empty()`, `null` in C#, `None` in Rust) inside its plain result, not a refusal case and not an exception.
The caller shows the empty state or goes on without it.

**"Not found" is a refusal only where the caller demands a specific thing.** A query or a command that names one
thing by its id — `GetOrderById`, `CancelOrder` — refuses when that thing does not exist: `OrderNotFound` where the
context returns, `OrderNotFoundException` where it throws. The test is the caller's question: "give me this one" can
fail, "is there one?" cannot.
