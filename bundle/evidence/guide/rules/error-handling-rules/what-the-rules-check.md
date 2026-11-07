---
type: Reference
title: ERROR HANDLING RULES — What the rules check
tags: [reference]
evidence_for: "/guide/rules/error-handling-rules.md#what-the-rules-check"
---

[Full node and context](/guide/rules/error-handling-rules.md#what-the-rules-check). This is an evidence excerpt; retain the parent selection and caveats.

### What the rules check

| Id | Rule |
|---|---|
| `DCA-ERR-001` | Exceptions declared in the domain layer must extend `DomainException` |
| `DCA-ERR-002` | Domain and port exceptions reside in the layer whose failure they name |
| `DCA-ERR-003` | Exceptions declared in the application layer must extend `UseCaseException` or `OutputPortException` |
| `DCA-ERR-004` | Domain and port exceptions must not carry prohibited framework metadata |
| `DCA-ERR-005` | Domain and port exception names must stay in the language of their layer |
| `DCA-ERR-006` | Diagnostic: incoming adapter packages that drive a use case without translating its failures |
| `DCA-ERR-007` | Diagnostic: failures that carry display data or objects instead of ids and figures |
| `DCA-ERR-008` | Diagnostic: closed use-case results without a case marked as a refusal (experimental) |

`DCA-ERR-004` is why the handler above carries the status and the exception does not: `@ResponseStatus` on a
domain exception is the adapter's decision taken in the domain layer. `DCA-ERR-005` forbids the simple-name
suffixes `Error`, `Fault`, `Failure` and the words `Http`, `Status`, `Response` in the name.

What no rule can decide: a `throw` and a `catch` are not part of the import model. Whether a specific refusal
should have been a domain exception, and whether an adapter catches too widely, stays with review.
`DCA-ERR-006` therefore only lists incoming adapter packages that name neither base type, and never fails.
A package on that list is not a finding by itself — an event consumer whose failed reaction belongs to the
delivery machinery's retry is a good answer — but each entry should have one.

In a context that returns results, the compiler holds what `DCA-ERR-006` can only list: a switch that misses a
case does not compile. The diagnostic reads the exception channel only, so an adapter that answers every refusal
by a switch and names neither base type appears on its list. The entry's answer is then the switch.

A closed result describes the outcomes of an operation; some are refusals, some are not. `Sent | AlreadySent` holds
no refusal and needs none: marking `AlreadySent` would roll back a success. Whether a case refuses is domain
knowledge the type does not show, so `DCA-ERR-008` lists every closed result without a case marked `Refusal` and
never fails. Each entry asks one question: is none of these outcomes a refusal? If one is, it carries the marker,
or the transaction commits where a thrown refusal rolled back. The marker says "refused" with or without a
transaction — a read-only use case refuses too; the rollback acts only where something was written.
