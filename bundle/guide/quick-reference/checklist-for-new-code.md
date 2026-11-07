---
type: Section
title: Checklist for new code
chapter: Quick Reference
source: guide
resource: dca-guide/architecture/quick-reference.md
tags: [guide, section]
---

- [ ] Does this carry business logic (domain) or technical concern (everything else)?
- [ ] Is this interface an input port (an actor calls it) or an output port (the application calls it)?
- [ ] Does the application need this capability without owning it, and does the adapter depend on the port? Cookies, tokens and a question into the own context are not ports
- [ ] Do all dependencies point inward?
- [ ] Is the domain free of framework annotations?
- [ ] Are the domain model and the persistence model separate types?
- [ ] Does the incoming adapter *use* the input port, and the outgoing adapter *implement* the output port?
- [ ] Does infrastructure do nothing but wiring and configuration?
- [ ] Can the domain and the application layer be tested without a framework?
- [ ] Does each business rule refuse with its own named failure, and each argument guard with the platform's argument exception?
- [ ] Does every use case of the context carry its expected refusals the same way — all thrown, or all returned as cases — and is the choice recorded in the project's technical description (`Refusals: thrown | returned`, or `Refusals (<context>): …` for a context that departs)?
- [ ] Where the context returns: does every switch over a result name each case, without a `default`, and does each refusal case carry `Refusal`?
- [ ] Is each refusal's answer written once per context — in the class the switches call, or in the context's one exception handler?
- [ ] Does every refusal come before the first write?
- [ ] Does a failure an output port declares extend `OutputPortException`, thrown by its adapter and caught by the use case — and does a concrete use-case failure extend `UseCaseException`, never `InputPortException`?
- [ ] Does a failure of the system's own infrastructure — its database, its broker — stay the platform's exception, and is the expected failure of a foreign system (an external system on the context map) declared by its port as an `OutputPortException` and answered by the use case as a refusal?
- [ ] Does a "which one, if any" query answer *none* with an empty value, and is "not found" a refusal only where the caller names a specific thing?
- [ ] Does no incoming adapter catch `PortException` or `InputPortException` generically?
- [ ] Is each rule on input checked once, in its value object — a missing value refused there too, no annotation or default repeating it at the adapter?
- [ ] Are the words a person reads the adapter's, made from the failure's values — never the exception's message?

## Related mentions (heuristic)

- [InputPortException](/marker/application/inputportexception.md)
- [OutputPortException](/marker/application/outputportexception.md)
- [PortException](/marker/application/portexception.md)
- [UseCaseException](/marker/application/usecaseexception.md)
