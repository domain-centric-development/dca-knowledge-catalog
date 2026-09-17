---
type: Reference
title: "Transaction boundaries belong to the application layer — C# expression"
tags: [reference]
evidence_for: "/rule/layered/dca-lay-004.md#c-expression"
---

[Full node and context](/rule/layered/dca-lay-004.md#c-expression). This is an evidence excerpt; retain the parent selection and caveats.

### C# expression

```csharp
DcaRule.Check(
    "DCA-LAY-004",
    "Transaction boundaries belong to the application layer",
    rationale,
    arch =>
    {
        // Structural, over every module root: the application layer and the outgoing adapters
        // (which implement the transaction boundary) of any module, at any depth.
        // The configured transaction APIs (TransactionScope plus TransactionApiTypes) and DCA's own
        // ITransactionBoundary port. The boundary's implementations are the one legitimate site that
        // depends on both, wherever they live; the composition root (the global infrastructure
        // namespace) and the shared kernel's infrastructure wire the transaction handle and its plumbing
        // and draw no boundary.
        var wiringAllowed = new Regex(DcaLayout.AnyOf(
            arch.AllApplicationPatterns().Concat(arch.AllOutgoingAdapterPatterns())
                .Append(Layout.InfrastructurePattern)
                .Append(DcaLayout.Below($"{Layout.SharedKernelNamespace}.{Layout.InfrastructureSegment}"))));
        var types = Layout.FrameworkTypes;
        var transactionApis = new HashSet<string>(types.TransactionApiTypes, StringComparer.Ordinal);
        if (FrameworkTypes.IsSet(types.TransactionScope)) transactionApis.Add(types.TransactionScope);
        bool IsBoundary(IType t) => t.FullName == BoundaryPort || t.ImplementsInterface(BoundaryPort);
        bool Programmatic(IType target) => transactionApis.Contains(target.FullName) || IsBoundary(target);
        var violations = arch.Types
            .Where(t => t.Namespace is null || !wiringAllowed.IsMatch(t.Namespace.FullName))
            .Where(t => !IsBoundary(t))
            .SelectMany(t => t.Dependencies.Select(d => d.Target).Where(Programmatic).Select(target => target.FullName).Distinct()
                .Select(target => $"{t.FullName} uses {target} outside the application layer"))
            .ToList();
        DcaRule.Fail($"Transaction boundaries belong to the application layer\nbecause {rationale}", violations);
    })
    .Selecting(
        "Types under scan that have any dependency on a configured transaction type - TransactionScope "
        + "(by default System.Transactions.TransactionScope) or one of the TransactionApiTypes (by default "
        + "CommittableTransaction, IDbTransaction, DbTransaction and the persistence library's "
        + "IDbContextTransaction) - or on ITransactionBoundary; a field, a local, a method call or a using "
        + "block all count. Implementations of ITransactionBoundary itself and types in the global "
        + "infrastructure namespace (<Root>.Infrastructure, the composition root that wires the "
        + "transaction handle) or in the shared kernel's infrastructure namespace "
        + "(<Root>.SharedKernel.Infrastructure, its plumbing) are not selected. With no transaction "
        + "type configured only ITransactionBoundary dependencies are selected.")
    .Checking(
        "Each resides in an application namespace of some module root (<module>.Application or "
        + "below) or in an outgoing adapter namespace of some module root "
        + "(<module>.Adapter.Outgoing or below). A use in a domain, incoming-adapter or "
        + "module-infrastructure namespace is reported, one finding per type and transaction type; all "
        + "findings are collected into one violation. The check is per type, not per method; which "
        + "transaction a boundary opens is not checked.")
```
