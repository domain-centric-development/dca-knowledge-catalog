---
type: Reference
title: Use cases that save an aggregate must publish its domain events — Overview
tags: [reference]
evidence_for: /rule/usecase/dca-use-009.md
---

[Full node and context](/rule/usecase/dca-use-009.md). This is an evidence excerpt; retain the parent selection and caveats.

# Use cases that save an aggregate must publish its domain events

## Selection

Non-interface classes in <module>.application.. that implement InputPort or whose simple name ends with the configured use-case suffix.

## Check

Only a resolved Repository<T,ID> whose aggregate and every non-building-block superclass are scanned and have no registration call (including helpers) is exempt. Unresolved generics, partial scans or undecidable external helpers remain required. For every non-exempt method of the class that calls Repository.save, every entry point reaching it (a method callable from outside the class, or one nothing in the class calls) also reaches, through calls within the class, a call of DomainEventPublisher.publishAndClearEvents. Only publishAndClearEvents counts - publish(event), even followed by clearDomainEvents(), does not. A use case without a save (a query, a bulk delete) is selected but has nothing to check and passes.

## .NET reading

**Selection.** Classes in <module>.Application of every module root selected by IInputPort assignability or the configured use-case suffix, whose runtime type is in the loaded assemblies.

**Check.** Only a resolved IRepository<T,ID> aggregate with its complete non-building-block hierarchy under scan and no registration call, including helpers, is exempt. Unresolved arguments, partial scans and undecidable external helpers are not exempt. For every non-exempt method calling IRepository.SaveAsync, every entry point reaching it (a method callable from outside the class, or one nothing in the class calls) also reaches, through calls within the class, a call of IDomainEventPublisher.PublishAndClearEventsAsync. Calls are read from the IL of the class and its nested state-machine and closure types, so async methods and lambdas are followed. Only PublishAndClearEventsAsync counts - PublishAsync(event), even followed by ClearDomainEvents(), does not. A use case without a save (a query, a bulk delete) is selected but has nothing to check and passes.

## Implementation

```java
DcaRule.of(
        "DCA-USE-009",
        "Use cases that save an aggregate must publish its domain events",
        "A saved aggregate must not keep its events: unpublished, they are lost, and stored on the"
            + " instance they may later be published out of context. Publishing belongs after the"
            + " save, in the use case that owns the unit of work - unless the aggregate is proven never to register an"
            + " event. Checked per entry path, following calls within the use case class: every"
            + " entry point that reaches a save - a method callable from outside the class, or one"
            + " nothing in the class calls - must also reach a publication; a wrapper that publishes"
            + " does not cover a direct call of the public method it wraps, and a helper two methods"
            + " share does not connect them. That the"
            + " publication follows the save and concerns the same aggregate is not established"
            + " statically. Only DomainEventPublisher.publishAndClearEvents counts as a publication:"
            + " iterating domainEvents() and calling publish(event), even followed by"
            + " clearDomainEvents(), separates dispatch from acknowledgement and is not accepted",
        arch ->
            classes()
                .that()
                .resideInAnyPackage(arch.allApplicationPatterns())
                .and()
                .haveSimpleNameEndingWith(layout.useCaseSuffix())
                .or()
                .areAssignableTo(InputPort.class)
                .and()
                .areNotInterfaces()
                .should(publishAfterSaving(arch))
                .allowEmptyShould(true))
    .selecting(
        "Non-interface classes in <module>.application.. that implement InputPort or whose simple name ends with the configured use-case suffix.")
    .checking(
        "Only a resolved Repository<T,ID> whose aggregate and every non-building-block superclass are scanned and have no registration call (including helpers) is exempt. Unresolved generics, partial scans or undecidable external helpers remain required. For every non-exempt method of the class that calls Repository.save, every entry point reaching it (a method callable from outside the class, or one nothing in the class calls) also reaches, through calls within the class, a call of DomainEventPublisher.publishAndClearEvents. Only publishAndClearEvents counts - publish(event), even followed by clearDomainEvents(), does not. A use case without a save (a query, a bulk delete) is selected but has nothing to check and passes.")
```

## Helpers
