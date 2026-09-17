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
        // Programmatic boundaries, two kinds. Using a transaction API (TransactionScope plus
        // TransactionApiTypes) draws a boundary and is allowed exactly in the application layer and the
        // outgoing adapters. Depending on a transaction manager (TransactionManagerTypes) or on DCA's
        // ITransactionBoundary port is wiring and plumbing as well: the composition root (the global
        // infrastructure namespace) and the shared kernel's infrastructure may do that too. The boundary's
        // implementations are exempt wherever they live.
        var allowed = new Regex(DcaLayout.AnyOf(arch.AllApplicationPatterns().Concat(arch.AllOutgoingAdapterPatterns())));
        var wiringAllowed = new Regex(DcaLayout.AnyOf(
            arch.AllApplicationPatterns().Concat(arch.AllOutgoingAdapterPatterns())
                .Append(Layout.InfrastructurePattern)
                .Append(DcaLayout.Below($"{Layout.SharedKernelNamespace}.{Layout.InfrastructureSegment}"))));
        var types = Layout.FrameworkTypes;
        var transactionApis = new HashSet<string>(types.TransactionApiTypes, StringComparer.Ordinal);
        if (FrameworkTypes.IsSet(types.TransactionScope)) transactionApis.Add(types.TransactionScope);
        var transactionManagers = new HashSet<string>(types.TransactionManagerTypes, StringComparer.Ordinal);
        bool IsBoundary(IType t) => t.FullName == BoundaryPort || t.ImplementsInterface(BoundaryPort);
        bool UsesApi(IType target) => transactionApis.Contains(target.FullName);
        bool ManagerOrBoundary(IType target) => transactionManagers.Contains(target.FullName) || IsBoundary(target);
        IEnumerable<string> Findings(Regex allowedHere, Func<IType, bool> programmatic) => arch.Types
            .Where(t => t.Namespace is null || !allowedHere.IsMatch(t.Namespace.FullName))
            .Where(t => !IsBoundary(t))
            .SelectMany(t => t.Dependencies.Select(d => d.Target).Where(programmatic).Select(target => target.FullName).Distinct()
                .Select(target => $"{t.FullName} uses {target} outside the application layer"));
        var violations = Findings(allowed, UsesApi).Concat(Findings(wiringAllowed, ManagerOrBoundary)).ToList();
        DcaRule.Fail($"Transaction boundaries belong to the application layer\nbecause {rationale}", violations);
    })
    .Selecting(
        "Two selections. Transaction use: types under scan that depend on a configured transaction-API "
        + "type - TransactionScope (by default System.Transactions.TransactionScope) or one of the "
        + "TransactionApiTypes (by default CommittableTransaction, IDbTransaction, DbTransaction and the "
        + "persistence library's IDbContextTransaction), the types code runs a transaction with. Wiring: "
        + "types under scan that depend on one of the TransactionManagerTypes (empty by default) or on "
        + "ITransactionBoundary. A field, a local, a method call or a using block all count; "
        + "implementations of ITransactionBoundary itself are never selected. With no transaction type "
        + "configured only ITransactionBoundary dependencies are selected.")
    .Checking(
        "Transaction use: the type resides in an application namespace of some module root "
        + "(<module>.Application or below) or in an outgoing adapter namespace of some module root "
        + "(<module>.Adapter.Outgoing or below) - a domain, incoming-adapter or infrastructure namespace "
        + "is reported, the global one included. Wiring: additionally allowed in the global "
        + "infrastructure namespace (<Root>.Infrastructure, the composition root that declares the "
        + "manager) and in the shared kernel's infrastructure namespace (<Root>.SharedKernel.Infrastructure, "
        + "plumbing that hooks into the boundary); a domain, incoming-adapter or module-infrastructure "
        + "namespace is reported. One finding per type and transaction type, all collected into one "
        + "violation. The check is per type, not per method. Where manager and boundary dependencies "
        + "are allowed the rule cannot tell wiring from a call: a type in the global or shared-kernel "
        + "infrastructure namespace that obtains the manager and begins a transaction itself passes. "
        + "Which transaction a boundary opens is not checked.")
```
