---
type: Reference
title: "ERROR HANDLING RULES — An expected refusal, thrown or returned"
tags: [reference]
evidence_for: "/guide/rules/error-handling-rules.md#an-expected-refusal-thrown-or-returned"
---

[Full node and context](/guide/rules/error-handling-rules.md#an-expected-refusal-thrown-or-returned). This is an evidence excerpt; retain the parent selection and caveats.

### An expected refusal, thrown or returned

An expected refusal is one a caller answers: the addressed thing does not exist, it is not the caller's, the use
case refuses the input, a business rule of the model refused the change, a foreign system refused or did not
answer. Everything else — a defect, the system's own database or broker that does not answer, a malformed call, a
stop — nobody can handle where it happens, and it travels as an exception to the place that can.

DCA carries an expected refusal one of two ways. Both are complete, and neither is the default:

- **Thrown.** The refusal is an exception: the model's domain exception, passed through, or a use-case exception
  the use case raises. The input port's signature names the success only. The context's exception handler maps
  each type to its answer. A new refusal compiles at every call site; a test or a review holds that the handler
  answers it.
- **Returned.** The refusal is a case of the use case's sealed result. The signature says how the operation can
  end, a switch over the result names every case, and a new refusal is a compile error at every call site that
  must answer it. Every caller reads the result, also one with nobody to answer, and the use case catches each
  refusal of the model it can raise.

**The choice is made per bounded context, and the project records it.** Every use case of a context carries its
refusals the same way. No context mixes a returned refusal with a thrown one, so its call sites have one style and a
review checks one shape. Two contexts of one project may choose differently.

The record is a line in the project's technical description, where everyone who builds, plans or reviews reads it:
`Refusals: thrown` or `Refusals: returned` for the whole project, and `Refusals (<context>): returned` for a context
that departs from it. A context without its own line follows the project's. Unrecorded, each piece of work picks a
style again, and a context drifts into both.

```
Refusals: thrown
Refusals (ordering): returned
```

**The model throws in both.** An aggregate refuses inside a behaviour method, and a method that returned an outcome
instead would make every caller unpack a case a correct call never produces. A value object's constructor can only
throw. So the model's refusals stay `DomainException`s. A context that throws lets them pass to its handler. A
context that returns catches the concrete ones the use case can raise, once, and returns the case:
`catch (OrderAlreadyShippedException e)`, never a base type that would also catch a defect.

**A use case never constructs a domain exception.** A refusal the use case finds itself — a port returned nothing,
the caller does not own what it names — is the application's, not the model's: a use-case exception where the
context throws, a case of the result where it returns, never a `DomainException` thrown from the application layer.
