---
type: Decision
title: "Failure channel: exception or a closed set of result variants"
tags: [decision, error-handling, domain, application, use-case]
review: draft
owner: DCA catalog maintainers
evidence: [/marker/tactical/domainexception.md, /marker/application/usecaseexception.md, /rule/errors/dca-err-001.md, /rule/errors/dca-err-002.md, /rule/errors/dca-err-003.md, /rule/errors/dca-err-006.md, /decision/result-shape-and-assembly.md, /pitfall/business-rule-reported-as-an-argument-error.md]
---

Something did not work out, and the layer that noticed has to tell the layer that asked. Two channels carry that message: an **exception** that travels past every frame until someone catches it, or a **closed set of result variants** the operation returns, one per outcome, which the caller takes apart at the call site. The building blocks name the exception channel, and the error-handling rules govern it; this node says when the other channel is the better answer, and what it costs to use it.

The question is not "which is cleaner". It is **who must be forced to deal with the outcome, and can that layer do anything about it**.

## The discriminator

Ask, in order:

1. **Is the outcome part of what the operation promises?** If the caller was always going to have to render one of several answers — accepted, refused for this reason, refused for that one — the outcome set belongs in the signature, where the compiler can check the caller handled all of it. That is the result-variant channel. If the outcome means the call itself was wrong given the state, it is not a promise, it is a refusal.
2. **Can the caller act on it?** A caller that can retry differently, offer an alternative or show a specific message needs the distinction in its hands. A caller that can only pass the failure upwards gains nothing from being forced to unpack it — and every intermediate frame pays for the unpacking.
3. **Who raises it — the model or the operation?** A behaviour method on an aggregate enforces an invariant while it mutates state. Making it return an outcome instead forces every call site to unpack a variant for a case that a correct call never produces, and turns mutators into functions that must be threaded through. The model is the strongest case for the exception channel. The use case, which already returns something, is the strongest case for variants.
4. **How far does it travel?** An outcome that passes through several layers unchanged is cheaper as an exception: one raise, one catch, nothing in between. An outcome consumed one frame up is cheaper as a variant.
5. **Is it a caller contract rather than a failure at all?** A null check or a range check states what a caller must never pass. That is neither channel — it stays the platform's own argument exception, and no rule of this catalog selects it.

## Options

| | Exception (`DomainException` / `UseCaseException`) | Closed set of result variants |
|---|---|---|
| Use when | an invariant refuses the call; the caller can only pass it on; the outcome crosses several frames | the outcome set is part of the promise; the caller must handle each case; one frame consumes it |
| Visible in the signature | no | yes |
| Caller forced to handle | no — silence compiles | yes, where the language checks the variants are exhausted |
| Cost at the call site | none until something goes wrong | every caller unpacks, including those that only forward |
| Aggregate behaviour methods | natural | awkward: mutators grow return values |
| Governed by rules here | yes — base type, layer, metadata, naming | **no** |

**Default: the model refuses with an exception; the operation answers with whatever its result type is.** A broken invariant inside an aggregate is a `DomainException`. An outcome the use case promises its caller — this identifier is unknown, this request is not permitted for this actor, this precondition elsewhere does not hold — is a legitimate result variant *or* a `UseCaseException`, and that is the real fork. Choose variants when the caller must handle each case and one frame consumes them; choose the exception when the caller can only forward it.

Mixing both in one code base is not a defect as long as the split is by question, not by mood: keep the model's refusals in the exception channel and decide the use-case boundary once, per project, and write the decision down.

## Consequences

- **The two are not symmetric in governance.** The exception channel has base types a rule can select on, so the layer, the metadata and the naming of every failure type are checked. The result-variant channel has none of that: a project that answers all use-case outcomes with variants leaves that area ungoverned — the error-handling rules select nothing there and report success. That is not the rules being satisfied, it is them being silent.
- **An incoming adapter still decides the answer**, in both channels. Whether it unpacks a variant or catches a type, the mapping from outcome to protocol lives there and nowhere further in. A result variant that carries a status code has made the same mistake a domain exception with a status annotation makes.
- **The diagnostic that lists untranslating adapters reads the exception channel only.** In a code base that answers with variants, it lists every incoming adapter, because none of them names a failure type. The listing is noise there, and it never fails a build — but it is worth knowing before reading the output.
- **A variant channel does not remove the exception channel**, it narrows it. Programming errors and infrastructure faults keep travelling as exceptions, so the adapter still needs the last resort that turns anything unrecognised into a server fault with no message.
- **One type per outcome holds in both.** The reason a caller can answer differently is that the outcomes are distinguishable types, not one type carrying a string.

## Anchors

- Markers: [DomainException](/marker/tactical/domainexception.md) · [UseCaseException](/marker/application/usecaseexception.md)
- Rules: [Exceptions declared in the domain layer must extend DomainException](/rule/errors/dca-err-001.md) · [Domain and use-case exceptions reside in the layer whose failure they name](/rule/errors/dca-err-002.md) · [Exceptions declared in the application layer must extend UseCaseException](/rule/errors/dca-err-003.md) · [Diagnostic: incoming adapters that drive a use case without translating its failures](/rule/errors/dca-err-006.md)
- Template: [Domain exception skeleton](/template/domain-exception.md)
- Pitfall: [A business rule reported as an argument error](/pitfall/business-rule-reported-as-an-argument-error.md)
- Related decision: [Result shape and assembly](/decision/result-shape-and-assembly.md) · [Where authorization and validation live](/decision/where-authorization-and-validation-live.md)
