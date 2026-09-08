---
type: Rule
id: DCA-NET-006
title: Application layer must not use persistence or transaction frameworks
rule: "The transaction boundary of a use case is drawn by a decorator around IUseCase or by ITransactionBoundary (an application-layer execution abstraction implemented in infrastructure), never by DbContext, SaveChanges, TransactionScope or IDbTransaction in the use case itself. Framework types in the application layer bind use cases to one persistence technology and hide where the boundary is; the ITransactionBoundary implementation is the single place that knows how to open and commit a transaction."
constraint: Application layer must not use persistence or transaction frameworks.
selects: "Types in <module>.Application of every module root."
checks: "No dependency on a type whose full name starts with Microsoft.EntityFrameworkCore, System.Transactions, System.Data, Dapper, NHibernate or MongoDB.Driver. Only these six namespace prefixes are checked - another persistence library is not reported, and the domain and adapter layers are not selected. An empty selection passes."
enforced_by: "DotnetRules#DCA-NET-006"
status: enforced
rule_set: dotnet
implementations: [dotnet]
resource: dca-dotnet/src/DomainCentric.ArchRules/Rules/DotnetRules.cs
tags: [dotnet, archunitnet]
---

## Selection

Types in <module>.Application of every module root.

## Check

No dependency on a type whose full name starts with Microsoft.EntityFrameworkCore, System.Transactions, System.Data, Dapper, NHibernate or MongoDB.Driver. Only these six namespace prefixes are checked - another persistence library is not reported, and the domain and adapter layers are not selected. An empty selection passes.

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
