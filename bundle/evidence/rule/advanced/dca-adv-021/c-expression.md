---
type: Reference
title: "Domain services are used only by the application and by other domain services — C# expression"
tags: [reference]
evidence_for: "/rule/advanced/dca-adv-021.md#c-expression"
---

[Full node and context](/rule/advanced/dca-adv-021.md#c-expression). This is an evidence excerpt; retain the parent selection and caveats.

### C# expression

```csharp
DcaRule.Check(
    "DCA-ADV-021",
    "Domain services are used only by the application and by other domain services",
    "A domain service holds logic that spans aggregates, and the use case decides when it runs and puts its "
        + "outcome into the result. A model type, a read model, an adapter or the composition root that calls "
        + "one takes that decision outside the application - the incoming adapter and the model type are each "
        + "held by a narrower rule too (DCA-HEX-012, DCA-ADV-019)",
    arch =>
    {
        var markers = arch.Layout.Markers;
        var violations = new SortedSet<string>(StringComparer.Ordinal);
        foreach (var origin in arch.RuntimeTypes().Where(t => !t.IsNested))
        {
            if (arch.InLayer(origin, DcaLayout.Layer.Application)
                || markers.Is(nameof(DcaMarkers.DomainService), origin))
            {
                continue;
            }

            var compositionRoot = arch.InLayer(origin, DcaLayout.Layer.Infrastructure);
            foreach (var unit in new IntraClassCalls(origin).Units)
            {
                foreach (var (code, operand) in IntraClassCalls.IlInstructions(unit))
                {
                    if (operand is not MethodBase target || target.DeclaringType is not { } owner
                        || !markers.Is(nameof(DcaMarkers.DomainService), owner))
                    {
                        continue;
                    }

                    var construction = code == System.Reflection.Emit.OpCodes.Newobj && target is ConstructorInfo;
                    if (compositionRoot && construction)
                    {
                        continue;
                    }

                    violations.Add(
                        $"{origin.FullName}.{IntraClassCalls.DisplayName(unit)} "
                        + (construction ? "constructs " : "calls ")
                        + $"{owner.FullName}{(construction ? "" : "." + target.Name)}");
                }
            }
        }

        DcaRule.Fail(
            "Domain services are used only by the application and by other domain services",
            violations.ToList(),
            "let the use case call the domain service and carry its outcome in the result; the composition root"
            + " only constructs it");
    })
    .Experimental()
    .Selecting(
        "Every type under scan, with its runtime type in the loaded assemblies, outside the application layer "
        + "that does not carry the domain-service role - the domain model, the adapters of both directions, the "
        + "composition root (the infrastructure layer) and types outside every layer - with the types nested in "
        + "it, compiler-generated state machines and closures included. A type nested in an application type or "
        + "in a domain service counts as its outer type and is not selected.")
    .Checking(
        "No method body calls a method or property of, constructs, or makes a delegate of a method of a type "
        + "carrying the domain-service role. A type in the infrastructure layer - the composition root - may "
        + "construct one to hand it to a use case; a call there is reported. Naming the type as a parameter, a "
        + "field or a return type is not a use and is not reported; a public field of a service read directly is "
        + "not seen. An empty selection passes.")
```
