---
type: Reference
title: Declaratively transactional use cases must not call remote-capable output ports — Overview
tags: [reference]
evidence_for: /rule/usecase/dca-use-013.md
---

[Full node and context](/rule/usecase/dca-use-013.md). This is an evidence excerpt; retain the parent selection and caveats.

# Declaratively transactional use cases must not call remote-capable output ports

## Selection

Non-interface classes in <module>.application.. that implement InputPort or whose simple name ends with the configured use-case suffix.

## Check

Every method that runs under one of the configured transactional annotations - on the class, on itself, or on a method that reaches it within the class - calls no OutputPort other than Repository, Store, DomainEventPublisher or IntegrationEventPublisher. A use case without such an annotation (explicit TransactionBoundary or none) is selected but never reported; with an empty role nothing is ever reported.

## .NET reading

**Selection.** Concrete application operations selected by IInputPort marker or configured use-case suffix, with loadable runtime types. Nothing at all while no transactional attribute is configured, which is the default: neither .NET preset names one, because ASP.NET Core has no ambient transaction attribute.

**Check.** Every code unit that runs under the configured transactional attribute - on the class, on itself, or on an entry point that reaches it within the class - calls no output port other than IRepository, IStore, IDomainEventPublisher or IIntegrationEventPublisher. A use case without such an attribute (an explicit ITransactionBoundary, or none) is selected but never reported, and with no attribute configured nothing is ever reported - the rule then carries the id without checking anything, as the Java twin does where no framework annotation is on the class path. What happens inside an InTransactionAsync block is not inspected; the explicit boundary is the developer's own and its extent is visible at the call site.

## Implementation

```java
DcaRule.of(
        "DCA-USE-013",
        "Declaratively transactional use cases must not call remote-capable output ports",
        "A declaratively transactional use case holds a database connection for its whole run."
            + " Calling an"
            + " output port that may leave the process (another context's API, a payment provider,"
            + " a mail gateway) inside it blocks that connection for the remote round trip; under"
            + " load the pool runs dry, and a rollback cannot undo the remote effect. Only"
            + " transactional resources belong inside the boundary: Repository, Store,"
            + " DomainEventPublisher, IntegrationEventPublisher. Everything else is called before"
            + " the transaction - draw the boundary by hand with TransactionBoundary.inTransaction(...)"
            + " - or after it, as a reaction to an integration event",
        arch ->
            classes()
                .that(useCases(arch, layout))
                .should(
                    notCallRemotePortsWhenTransactional(
                        layout.frameworkAnnotations().transactional(), layout.markers()))
                .allowEmptyShould(true))
    .selecting(
        "Non-interface classes in <module>.application.. that implement InputPort or whose simple name ends with the configured use-case suffix.")
    .checking(
        "Every method that runs under one of the configured transactional annotations - on the"
            + " class, on itself, or on a method that reaches it within the class - calls no"
            + " OutputPort other than Repository, Store, DomainEventPublisher or"
            + " IntegrationEventPublisher. A use case without such an annotation (explicit"
            + " TransactionBoundary or none) is selected but never reported; with an empty role"
            + " nothing is ever reported.")
```

## Helpers
