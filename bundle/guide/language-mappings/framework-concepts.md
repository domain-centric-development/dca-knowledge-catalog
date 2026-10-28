---
type: Section
title: Framework Concepts
chapter: "Language Mappings: Java/Spring ↔ C#/.NET"
source: guide
resource: dca-guide/topics/language-mappings.md
tags: [guide, section]
---

| Concern | Java / Spring | .NET / ASP.NET Core |
|---|---|---|
| Component registration | `@Service`, `@Component`, component scan | explicit `services.AddScoped<IPlaceOrderInputPort, PlaceOrderUseCase>()` in the context's `Infrastructure/` |
| Configuration per context | `@Configuration` class in `{context}/infrastructure/` | extension method `Add{Context}Context()` called by the composition root |
| Module verification | Spring Modulith `ApplicationModules.verify()` | project references (a context cannot reference another's internals) + the `DCA-STR` / `DCA-CYC` rules |
| Transaction boundary | `@Transactional` on the use case, or `TransactionBoundary.inTransaction(...)` (`DCA-USE-012`) | `ITransactionBoundary.InTransactionAsync(...)` or a decorator around `IUseCase` — no attribute; `DCA-USE-012` checks that every entry path to a saving, deleting or publishing method passes through the boundary call (`DCA-USE-013` is not applicable) |
| Composition root | the container: `@SpringBootApplication`, the component scan, `@Configuration` classes in `{context}/infrastructure/`; a port implemented by another use case is a `@Bean` there | `Program.cs` and each context's `Add{Context}Context()`; a port implemented by another use case is a registration there (`services.AddScoped<IPriceSetter>(sp => …)`) |
| Cancellation | interruption: `InterruptedException`, rethrown or the flag restored, never swallowed | `CancellationToken` through every port call; `OperationCanceledException`, never caught by a use case |
| Domain event dispatch | `ApplicationEventPublisher` behind `DomainEventPublisher`; synchronous listener `@EventListener`, transactional listener `@ApplicationModuleListener` (registry) | dispatcher behind `IDomainEventPublisher`; synchronous listeners run in the transaction, transactional listeners are delivered from an outbox after the commit; consumers subscribe explicitly |
| Integration events | Modulith event publication registry, or outbox | outbox table / `Channel<T>` queue drained after commit, with retry |
| Event consumer | `@ApplicationModuleListener void on(OrderCompletedEvent e)` | `*EventConsumer` class registered as a transactional listener; delivered after the commit from the outbox |
| Web adapter | `@Controller` `*PageController`, `@RestController` `*Resource` | MVC `*PageController : Controller`, `[ApiController]` `*Resource` / `*Controller` |
| Security context | `SecurityContextHolder` behind an `IdentityProvider` port | `HttpContext.User` behind an `IIdentityProvider` port; own `AuthenticationHandler` |
| Validation | Bean Validation on commands at the adapter edge | DataAnnotations / FluentValidation at the adapter edge |
| Persistence (in-memory phase) | `ConcurrentHashMap` repository | `ConcurrentDictionary` repository |
| Persistence (SQL) | JPA/JDBC in `adapter/outgoing/persistence/` | EF Core / Dapper in `Adapter/Outgoing/Persistence/` |
| Build / test | Gradle, JUnit 5 | `dotnet build` / `dotnet test`, xUnit |

The rules do not care which framework you register with — they check that framework types stay out of
`domain` and `application`, resolved by *role* through `DcaLayout.withFrameworkAnnotations(...)` /
`WithFrameworkTypes(...)`. Java ships presets for Spring (default), Jakarta EE, Quarkus, Micronaut and none; .NET
ships ASP.NET Core (default) and none. A Jakarta or Quarkus project therefore reads the Java column with CDI's
`@ApplicationScoped` for `@Service`, `jakarta.transaction.Transactional` for `@Transactional`, `@Path` for
`@RestController` and `@Observes` for `@EventListener` — the rule ids and texts are the same.

## Related mentions (heuristic)

- [TransactionBoundary](/marker/application/transactionboundary.md)
- [DomainEventPublisher](/marker/port-out/domaineventpublisher.md)
