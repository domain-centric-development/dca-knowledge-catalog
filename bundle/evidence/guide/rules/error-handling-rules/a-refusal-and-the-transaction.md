---
type: Reference
title: ERROR HANDLING RULES — A refusal and the transaction
tags: [reference]
evidence_for: "/guide/rules/error-handling-rules.md#a-refusal-and-the-transaction"
---

[Full node and context](/guide/rules/error-handling-rules.md#a-refusal-and-the-transaction). This is an evidence excerpt; retain the parent selection and caveats.

### A refusal and the transaction

**Decide, then write.** A use case writes only once it can no longer refuse: it loads, asks the model, refuses or
goes on, and saves last. A refusal that can only come after a write is a cut that changes two aggregates in one
transaction — the second refuses what the first already did. That is a design question, not a rollback question.

**A returned refusal rolls back like a thrown exception.** A thrown refusal rolls the transaction back because it
leaves the boundary as an exception. A returned one leaves it as a value, and without a net it would commit
whatever the use case wrote before it. So every refusal case of a result implements the marker `Refusal` from the
building blocks, and the transaction boundary rolls back when the work returns one: `TransactionBoundary`
(`ITransactionBoundary` in .NET) does, and so does the interceptor that marks a declarative `@Transactional` use case
rollback-only on a returned `Refusal`. A refusal rolls back wherever in the use case it arises, thrown or returned.
The refusal cases of `CancelOrderResult` above carry the marker for that reason. The net catches a violation of
"decide, then write"; it does not make the violation good code.

**A step after the commit only reads.** What runs once the transaction has committed — a step after
`inTransaction` returns, a listener after the commit — is out of the rollback's reach. It reads and reports; a
change it would refuse is already stored.

**A remote effect keeps its compensation.** A remote effect made before the local write — a payment, a reservation
at another system — was never undone by a thrown exception either; a rollback reaches only the local store. A
refusal after such an effect, thrown or returned, calls the compensation the
[transaction rules](#transaction-boundary-placement) describe.
