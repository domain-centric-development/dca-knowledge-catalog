---
type: Rule
id: DCA-USE-013
title: Declaratively transactional use cases must not call remote-capable output ports
rule: "A @Transactional use case holds a database connection for its whole run. Calling an output port that may leave the process (another context's API, a payment provider, a mail gateway) inside it blocks that connection for the remote round trip; under load the pool runs dry, and a rollback cannot undo the remote effect. Only transactional resources belong inside the boundary: Repository, Store, DomainEventPublisher, IntegrationEventPublisher. Everything else is called before the transaction - draw the boundary by hand with TransactionBoundary.inTransaction(...) - or after it, as a reaction to an integration event."
constraint: Declaratively transactional use cases must not call remote-capable output ports.
enforced_by: "UseCaseRules#DCA-USE-013"
status: enforced
rule_set: usecase
implementations: [java]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/UseCaseRules.java
tags: [usecase, archunit]
not_applicable_dotnet: "Guards against remote-capable output ports called inside a @Transactional use case. .NET has no declarative transaction metadata on use cases — the boundary is a decorator or an explicit ITransactionBoundary.InTransactionAsync — so the rule has nothing to anchor on; DCA-NET-006 keeps transaction and persistence frameworks out of the application layer instead"
---

```java
DcaRule.of(
    "DCA-USE-013",
    "Declaratively transactional use cases must not call remote-capable output ports",
    "A @Transactional use case holds a database connection for its whole run. Calling an"
        + " output port that may leave the process (another context's API, a payment provider,"
        + " a mail gateway) inside it blocks that connection for the remote round trip; under"
        + " load the pool runs dry, and a rollback cannot undo the remote effect. Only"
        + " transactional resources belong inside the boundary: Repository, Store,"
        + " DomainEventPublisher, IntegrationEventPublisher. Everything else is called before"
        + " the transaction - draw the boundary by hand with TransactionBoundary.inTransaction(...)"
        + " - or after it, as a reaction to an integration event",
    arch ->
        classes()
            .that()
            .resideInAPackage(layout.applicationPattern())
            .and()
            .haveSimpleNameEndingWith(layout.useCaseSuffix())
            .and()
            .areNotInterfaces()
            .should(
                notCallRemotePortsWhenTransactional(
                    layout.frameworkAnnotations().transactional()))
            .allowEmptyShould(true))
```

## Applies to markers

- [TransactionBoundary](/marker/application/transactionboundary.md)
- [DomainEventPublisher](/marker/port-out/domaineventpublisher.md)
- [IntegrationEventPublisher](/marker/port-out/integrationeventpublisher.md)
- [Repository<T, ID>](/marker/port-out/repository.md)
