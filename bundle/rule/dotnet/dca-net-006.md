---
type: Rule
id: DCA-NET-006
title: Application layer must not use persistence or transaction frameworks
rule: "The transaction boundary of a use case is drawn by a decorator around IUseCase or by ITransactionBoundary (an application-layer execution abstraction implemented in infrastructure), never by DbContext, SaveChanges, TransactionScope or IDbTransaction in the use case itself. Framework types in the application layer bind use cases to one persistence technology and hide where the boundary is; the ITransactionBoundary implementation is the single place that knows how to open and commit a transaction."
constraint: Application layer must not use persistence or transaction frameworks.
selects: "Types in <module>.Application of every module root."
checks: "No dependency on a type whose full name starts with Microsoft.EntityFrameworkCore, System.Transactions, System.Data, Dapper, NHibernate or MongoDB.Driver. Only these six namespace prefixes are checked - another persistence library is not reported, and the domain and adapter layers are not selected. An empty selection passes. The statement is language-neutral, but it is carried under a dotnet id: Java has no twin, where DCA-LAY-003 forbids the infrastructure packages and not the persistence API itself."
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

No dependency on a type whose full name starts with Microsoft.EntityFrameworkCore, System.Transactions, System.Data, Dapper, NHibernate or MongoDB.Driver. Only these six namespace prefixes are checked - another persistence library is not reported, and the domain and adapter layers are not selected. An empty selection passes. The statement is language-neutral, but it is carried under a dotnet id: Java has no twin, where DCA-LAY-003 forbids the infrastructure packages and not the persistence API itself.

### C# expression

```csharp
DcaRule.Check(
        "DCA-NET-006",
        "Application layer must not use persistence or transaction frameworks",
        "The transaction boundary of a use case is drawn by a decorator around IUseCase or by ITransactionBoundary (an application-layer execution abstraction implemented in infrastructure), never by DbContext, SaveChanges, TransactionScope or IDbTransaction in the use case itself. Framework types in the application layer bind use cases to one persistence technology and hide where the boundary is; the ITransactionBoundary implementation is the single place that knows how to open and commit a transaction",
        arch =>
        {
            var application = arch.AllApplicationPatterns().Select(p => new Regex(p)).ToList();
            var violations = new List<string>();
            foreach (var type in arch.Types.Where(t => application.Any(r => r.IsMatch(t.Namespace.FullName))))
            {
                var frameworks = type.Dependencies
                    .Select(d => d.Target.FullName)
                    .Where(IsPersistenceFrameworkType)
                    .Distinct()
                    .OrderBy(n => n, StringComparer.Ordinal)
                    .ToList();
                if (frameworks.Count > 0)
                {
                    violations.Add($"{type.FullName} depends on {string.Join(", ", frameworks)}");
                }
            }

            DcaRule.Fail(
                "Application layer must not use persistence or transaction frameworks\nbecause the transaction boundary belongs to a decorator or ITransactionBoundary",
                violations,
                "Inject ITransactionBoundary (or let the composition root decorate the use case) and move the framework call into infrastructure.");
        })
    .Selecting(
        "Types in <module>.Application of every module root.")
    .Checking(
        "No dependency on a type whose full name starts with Microsoft.EntityFrameworkCore,"
            + " System.Transactions, System.Data, Dapper, NHibernate or MongoDB.Driver. Only"
            + " these six namespace prefixes are checked - another persistence library is not"
            + " reported, and the domain and adapter layers are not selected. An empty selection"
            + " passes. The statement is language-neutral, but it is carried under a dotnet id:"
            + " Java has no twin, where DCA-LAY-003 forbids the infrastructure packages and not"
            + " the persistence API itself.")
```

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
