---
type: Reference
title: "DcaLayout — Derived namespaces and patterns (.NET)"
tags: [reference]
evidence_for: "/reference/layout.md#derived-namespaces-and-patterns-net"
---

[Full node and context](/reference/layout.md#derived-namespaces-and-patterns-net). This is an evidence excerpt; retain the parent selection and caveats.

### Derived namespaces and patterns (.NET)

Patterns are .NET regular expressions over full namespace names for ArchUnitNET's `ResideInNamespaceMatching`.

| Member | Yields |
|---|---|
| `string SharedKernelPattern` | Pattern for `Root.SharedKernel` and everything below. |
| `string SharedKernelDomainPattern` | Pattern for `Root.SharedKernel.Domain` and below. |
| `string SharedKernelDomainModelPattern` | Pattern for `Root.SharedKernel.Domain.Model` and below. |
| `string InfrastructurePattern` | Pattern for `Root.Infrastructure` and below. |
| `string DomainPattern` | Pattern for `Root.*.Domain` and below — the domain layer of every direct child namespace (context). |
| `string DomainModelPattern` | Pattern for `Root.*.Domain.Model` and below. |
| `string ApplicationPattern` | Pattern for `Root.*.Application` and below. |
| `string SharedOutputPortPattern` | Pattern for `Root.*.Application.Shared` and below — output ports shared by the use cases of one context. |
| `string AdapterPattern` | Pattern for `Root.*.Adapter` and below. |
| `string IncomingAdapterPattern` | Pattern for `Root.*.Adapter.Incoming` and below. |
| `string OutgoingAdapterPattern` | Pattern for `Root.*.Adapter.Outgoing` and below. |
| `string DomainPatternOf(string contextNamespace)` |  |
| `string DomainModelPatternOf(string contextNamespace)` |  |
| `string ApplicationPatternOf(string contextNamespace)` |  |
| `string SharedOutputPortPatternOf(string contextNamespace)` |  |
| `string AdapterPatternOf(string contextNamespace)` |  |
| `string IncomingAdapterPatternOf(string contextNamespace)` |  |
| `string OutgoingAdapterPatternOf(string contextNamespace)` |  |
| `static string Below(string ns)` | Regex matching `ns` itself and every namespace below it (ArchUnit's `ns..`). Literal parts are escaped; `Segment` wildcards are kept. |
| `static string AnyOf(IEnumerable<string> patterns)` | Alternation of complete namespace patterns (each already anchored). An empty list yields a pattern that matches nothing — never an empty string, which would match everything. |
| `static string AnySegmentPath(string dottedPath)` | ArchUnit's `..A.B..`: the dotted path appears anywhere on segment boundaries. |
| `static string Exactly(string ns)` | Regex matching exactly `ns` (no sub-namespaces). |
