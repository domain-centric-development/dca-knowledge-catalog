---
type: Reference
title: "Diagnostic: failures that carry display data or objects instead of ids and figures — C# expression"
tags: [reference]
evidence_for: "/rule/errors/dca-err-007.md#c-expression"
---

[Full node and context](/rule/errors/dca-err-007.md#c-expression). This is an evidence excerpt; retain the parent selection and caveats.

### C# expression

```csharp
DcaRule.Informational(
    "DCA-ERR-007",
    "Diagnostic: failures that carry display data or objects instead of ids and figures",
    "A failure carries ids and figures, never what a page shows: its fields are the typed identities"
        + " and the values the rule compared. A name or a description of the thing the id refers to is"
        + " resolved by the translation site, through the queries it already has; a failure that"
        + " carries it decides for every surface what it shows, and one that carries the aggregate"
        + " hands its state to every caller",
    arch =>
    {
        var markers = arch.Layout.Markers;
        var observed = new List<string>();
        foreach (var exception in ExceptionsOfEitherLayer(arch).OrderBy(t => t.FullName, StringComparer.Ordinal))
        {
            var runtime = arch.RuntimeType(exception);
            for (var type = runtime; type is not null && !DcaMarkers.IsRole(type, markers.DomainException)
                && !DcaMarkers.IsRole(type, markers.UseCaseException) && !DcaMarkers.IsRole(type, markers.OutputPortException)
                && !DcaMarkers.IsRole(type, markers.PortException) && type != typeof(Exception); type = type.BaseType)
            {
                foreach (var field in type.GetFields(BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance | BindingFlags.DeclaredOnly))
                {
                    var finding = FieldFinding(field.FieldType, markers);
                    if (finding is not null)
                    {
                        observed.Add($"{exception.FullName} holds {FieldName(field)} as {finding} - carry the id or the value the rule compared");
                    }
                }
            }
        }

        return observed.Distinct().ToList();
    })
    .Experimental()
    .Selecting(
        "The project's own types below DomainException or PortException, with their runtime type in"
        + " the loaded assemblies, and the instance fields they and their project base types declare -"
        + " the backing fields of auto-properties included.")
    .Checking(
        "Informational diagnostic only: lists a field whose type is a plain string, or is assignable to"
        + " IAggregateRoot or IEntity - directly, as an array element or as a generic type argument -"
        + " and never fails. Ids, values, numbers and every other type pass. A string that holds a code"
        + " rather than display text is listed as well: the type does not tell the two apart, and the"
        + " remedy is a typed value for the code.")
```
