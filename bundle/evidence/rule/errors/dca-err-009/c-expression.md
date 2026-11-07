---
type: Reference
title: "A domain exception is constructed only in the domain layer — C# expression"
tags: [reference]
evidence_for: "/rule/errors/dca-err-009.md#c-expression"
---

[Full node and context](/rule/errors/dca-err-009.md#c-expression). This is an evidence excerpt; retain the parent selection and caveats.

### C# expression

```csharp
DcaRule.Check(
    "DCA-ERR-009",
    "A domain exception is constructed only in the domain layer",
    "The model refuses: a domain exception names a business rule the model itself broke off. A use case never"
        + " invents one. A failure the use case finds - an output port returned nothing, the caller does not own"
        + " what it names, a precondition on a second aggregate - is the application's, a case of its result or a"
        + " use-case exception; dressed as a domain failure it claims a rule the model never checked, and the"
        + " model cannot know what a search found",
    arch =>
    {
        var markers = arch.Layout.Markers;
        var vocabulary = markers.DeclaringNamespacesOf(new[] { nameof(DcaMarkers.DomainException) });
        var violations = new SortedSet<string>(StringComparer.Ordinal);
        foreach (var origin in arch.RuntimeTypes().Where(t => !t.IsNested))
        {
            var ns = origin.Namespace ?? "";
            if (arch.InLayer(origin, DcaLayout.Layer.Domain) || vocabulary.Any(v => DcaLayout.IsBelow(ns, v)))
            {
                continue;
            }

            foreach (var unit in new IntraClassCalls(origin).Units)
            {
                foreach (var (code, operand) in IntraClassCalls.IlInstructions(unit))
                {
                    if (code != System.Reflection.Emit.OpCodes.Newobj || operand is not ConstructorInfo constructor
                        || !markers.Is(nameof(DcaMarkers.DomainException), constructor.DeclaringType))
                    {
                        continue;
                    }

                    violations.Add(
                        $"{origin.FullName}.{IntraClassCalls.DisplayName(unit)} constructs {constructor.DeclaringType!.FullName}"
                        + " - only the domain layer raises a domain failure; a failure the application finds is a case of"
                        + " its result or a use-case exception");
                }
            }
        }

        DcaRule.Fail(
            "A domain exception is constructed outside the domain layer",
            violations,
            "let the aggregate, value object or domain service that checks the rule throw it; for a failure the use"
            + " case finds itself - nothing found, not owned - return a refusal case of the result or throw a"
            + " use-case exception declared beside the use case");
    })
    .Experimental()
    .Selecting(
        "Every type of the scan outside <Module>.Domain of every module root - the application layer, the adapters,"
        + " configuration and any unplaced type - with each object creation its methods and constructors make,"
        + " the compiler's async state machines, lambda closures and nested types included. Types in the"
        + " namespace of the configured domain-exception role are library code and not selected; test"
        + " assemblies are not loaded.")
    .Checking(
        "No such creation (a newobj instruction) creates a type assignable to the configured domain-exception role"
        + " (by default DomainException of the building blocks). A constructor chaining to its base constructor"
        + " is not a creation - where a misplaced exception type lives is DCA-ERR-002's finding. Construction in"
        + " the domain layer passes, a domain service and a factory included. A domain exception the application"
        + " catches, wraps or rethrows is not constructed and passes. A construction through reflection or a"
        + " generic factory method outside the domain is not seen. An empty selection passes.")
```
