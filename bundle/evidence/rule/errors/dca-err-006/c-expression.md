---
type: Reference
title: "Diagnostic: incoming adapter packages that drive a use case without translating its failures — C# expression"
tags: [reference]
evidence_for: "/rule/errors/dca-err-006.md#c-expression"
---

[Full node and context](/rule/errors/dca-err-006.md#c-expression). This is an evidence excerpt; retain the parent selection and caveats.

### C# expression

```csharp
DcaRule.Informational(
    "DCA-ERR-006",
    "Diagnostic: incoming adapter namespaces that drive a use case without translating its failures",
    "A namespace that drives the application and knows neither failure type nor a case of a closed"
        + " result either lets everything escape to a generic handler or catches a generic type and answers"
        + " every outcome the same way; whether it does is not visible in the type model. A use case may"
        + " return its expected refusals as cases of a closed result instead of throwing them; a switch"
        + " over those cases is the translation then. An adapter that catches the abstract base of the"
        + " port failures answers every outcome the same way",
    arch =>
    {
        var domainException = arch.Layout.Markers.DomainException;
        var useCaseException = arch.Layout.Markers.UseCaseException;
        var anyFailureType = arch.Types.Any(t =>
            t.FullName != domainException && t.FullName != useCaseException
            && (arch.Layout.Markers.Is(nameof(DcaMarkers.DomainException), t) || arch.Layout.Markers.Is(nameof(DcaMarkers.UseCaseException), t)));
        if (!anyFailureType)
        {
            return new List<string>
            {
                $"no class of the scan is assignable to {domainException} or {useCaseException}, so no namespace "
                + "can be seen to name a failure - nothing is listed. Where the project has failure types of its "
                + "own, point the DomainException and UseCaseException roles at their base types "
                + "(DcaMarkers with-expression).",
            };
        }

        var observed = GenericPortFailureCatches(arch);
        var resultCases = CasesOfClosedResults(arch);
        var driving = new SortedDictionary<string, List<string>>(StringComparer.Ordinal);
        var namespacesThatName = new HashSet<string>(StringComparer.Ordinal);
        foreach (var type in arch.Types)
        {
            var ns = type.Namespace?.FullName ?? "";
            if (!arch.InIncomingAdapter(type))
            {
                continue;
            }

            var targets = type.Dependencies.Select(d => d.Target).ToList();
            if (targets.Any(t => arch.Layout.Markers.Is(nameof(DcaMarkers.DomainException), t) || arch.Layout.Markers.Is(nameof(DcaMarkers.UseCaseException), t)
                || resultCases.Contains(t.FullName)))
            {
                namespacesThatName.Add(ns);
            }

            if (type is not Interface && targets.Any(t => arch.Layout.Markers.Is(nameof(DcaMarkers.InputPort), t)))
            {
                if (!driving.TryGetValue(ns, out var names))
                {
                    names = new List<string>();
                    driving[ns] = names;
                }

                names.Add(type.Name);
            }
        }

        foreach (var (ns, names) in driving)
        {
            if (namespacesThatName.Contains(ns))
            {
                continue;
            }

            names.Sort(StringComparer.Ordinal);
            observed.Add(
                $"{ns}: drives an input port and names neither a failure type of the inner layers nor a case of a closed result ({string.Join(", ", names)})");
        }

        return observed;
    })
    .Selecting(
        "Incoming adapter namespaces of every module root (<Module>.Adapter.Incoming) that hold at "
        + "least one non-interface type depending on a type assignable to IInputPort - the "
        + "namespaces that drive the application.")
    .Checking(
        "Informational diagnostic only: when no type of the scan is assignable to DomainException or "
        + "UseCaseException, it lists no namespace and says once that it cannot see the failures; otherwise it "
        + "lists a namespace when no type in it - a central exception "
        + "handler beside the adapters included - depends on a type assignable to DomainException or "
        + "UseCaseException, nor on a case of a closed result, and never fails. A closed result is a type "
        + "an input port answers with - a type argument of its use-case interface or the return type of "
        + "one of its methods, a task unwrapped - that derives from one of the configured closed-result "
        + "base types (FrameworkTypes.ClosedResultBaseTypes, matched by name; every preset names the "
        + "generic base of a discriminated-union library, for example OneOf.OneOfBase); its cases are the "
        + "generic arguments of that base. A type test, a cast, a case type in a function's or an action's "
        + "signature (one handler per case) and a member call on the union base that names its cases all "
        + "count, so this approximates an exhaustive switch: one reference to one case counts, and whether "
        + "every case is handled is left to the compiler. A handler in a different namespace of the same "
        + "module is not seen, and a caught type is not visible to the type model, so this does not "
        + "establish that a namespace translates nothing. Beside the namespaces it lists every incoming-"
        + "adapter type that catches - read from the exception-handling clauses of its methods' bodies, "
        + "compiler-generated nested types such as async state machines included - or refers to the "
        + "abstract bases PortException, InputPortException or OutputPortException themselves: it handles "
        + "the port failures generically.")
```
