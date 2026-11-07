---
type: Reference
title: "Diagnostic: closed use-case results without a case marked as a refusal — C# expression"
tags: [reference]
evidence_for: "/rule/errors/dca-err-008.md#c-expression"
---

[Full node and context](/rule/errors/dca-err-008.md#c-expression). This is an evidence excerpt; retain the parent selection and caveats.

### C# expression

```csharp
DcaRule.Informational(
    "DCA-ERR-008",
    "Diagnostic: closed use-case results without a case marked as a refusal",
    "A closed result describes the outcomes a use case can answer with; some of them are refusals, some are"
        + " not. A result may hold several outcomes of which none refuses - found or nothing found, sent or"
        + " already sent - and that alone is reason enough to close it. The refusal marker on a case says the"
        + " request was refused, a meaning the caller answers with or without a transaction, and it is what"
        + " lets the transaction boundary roll a refusal back like a thrown failure. Whether a case refuses is"
        + " domain knowledge the type does not show, so a closed result without any marked case is listed for"
        + " a look, not failed: if one of its outcomes is a refusal and stays unmarked, the transaction"
        + " commits the writes made before it",
    arch =>
    {
        var markers = arch.Layout.Markers;
        var observed = new List<string>();
        foreach (var (result, closed) in ClosedResults(arch))
        {
            if (!arch.InLayer(result, DcaLayout.Layer.Application))
            {
                continue;
            }

            if (closed.Cases.Any(c => markers.Is(nameof(DcaMarkers.Refusal), c)))
            {
                continue;
            }

            observed.Add(
                $"{result.FullName} is answered by [{string.Join(", ", closed.Ports.Select(p => p.Name).OrderBy(n => n, StringComparer.Ordinal))}]"
                + $" and none of its cases [{string.Join(", ", closed.Cases.Select(c => c.Name).OrderBy(n => n, StringComparer.Ordinal))}]"
                + $" is marked as a refusal ({markers.Marker(nameof(DcaMarkers.Refusal))}) - check: is none of these"
                + " outcomes a refusal? If one is, mark it, or the transaction commits when it is returned");
        }

        return observed;
    })
    .Experimental()
    .Selecting(
        "Closed results under <Module>.Application of every module root: a type an input port answers with"
        + " - a type argument of its use-case interface or the return type of one of its methods, a task"
        + " unwrapped - that derives from one of the configured closed-result base types"
        + " (FrameworkTypes.ClosedResultBaseTypes, matched by name). An empty list of base types selects"
        + " nothing.")
    .Checking(
        "Informational diagnostic only: lists every closed result none of whose cases - the generic arguments"
        + " of the closed-result base - is assignable to the configured refusal role (by default the IRefusal"
        + " marker of the building blocks), and never fails. The result type itself carrying the marker does"
        + " not count. A listed result is not a finding by itself: a closed result whose outcomes are all"
        + " successes - found or nothing found - is correct as it is. A context that throws its refusals has"
        + " no closed results and lists nothing.")
```
