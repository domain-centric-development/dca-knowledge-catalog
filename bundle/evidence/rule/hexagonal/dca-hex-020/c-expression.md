---
type: Reference
title: "Diagnostic: incoming adapters that read the caller's roles in their own code — C# expression"
tags: [reference]
evidence_for: "/rule/hexagonal/dca-hex-020.md#c-expression"
---

[Full node and context](/rule/hexagonal/dca-hex-020.md#c-expression). This is an evidence excerpt; retain the parent selection and caveats.

### C# expression

```csharp
DcaRule.Informational(
        "DCA-HEX-020",
        "Diagnostic: incoming adapters that read the caller's roles in their own code",
        "A check that reads nothing but the caller's roles or claims - is this caller staff? - is a property of"
            + " the exposure and is declared on the route, with the framework's authorization annotation, where a"
            + " reader of the route sees it and the framework answers an unauthenticated and an unauthorized"
            + " caller apart. A branch on the caller's roles inside the adapter's code hides the gate and renders"
            + " whatever status the branch writes. A check that needs the stored data - is this yours? - is not"
            + " claims-only and belongs to the use case",
        arch =>
        {
            var attributes = Layout.FrameworkTypes.AuthorizationAttributeTypes;
            if (attributes.Count == 0)
            {
                return new List<string>();
            }

            var declare = string.Join(" or ", attributes.Select(a => "[" + a[(a.LastIndexOf('.') + 1)..].Replace("Attribute", "", StringComparison.Ordinal) + "]"));
            var observed = new SortedSet<string>(StringComparer.Ordinal);
            foreach (var adapter in arch.Types.Where(arch.InIncomingAdapter))
            {
                var runtime = arch.RuntimeType(adapter);
                if (runtime is null || runtime.IsNested)
                {
                    continue;
                }

                foreach (var unit in new IntraClassCalls(runtime).Units)
                {
                    foreach (var (_, operand) in IntraClassCalls.IlInstructions(unit))
                    {
                        if (operand is MethodBase call && RoleQuestion.IsMatch(call.Name))
                        {
                            observed.Add(
                                $"{adapter.FullName}.{IntraClassCalls.DisplayName(unit)} reads the caller's roles through"
                                + $" {call.DeclaringType?.Name}.{call.Name}() - declare a claims-only check on the route with"
                                + $" {declare}; a check that needs the stored data belongs to the use case");
                        }
                    }
                }
            }

            return observed.ToList();
        })
    .Experimental()
    .Selecting(
        "Non-nested types in the incoming adapter layer of every module root - by default <Module>.Adapter.Incoming"
            + " - with their runtime type in the loaded assemblies, together with their nested, async state-machine"
            + " and closure types, and the calls their IL makes. Nothing is selected when the configured"
            + " authorization-attribute role is empty: without a declarative form there is nothing to advise.")
    .Checking(
        "Informational diagnostic only: lists every call of a method whose name asks whether the caller holds a"
            + " role or an authority - IsInRole, IsUserInRole, HasRole, HasAnyRole, HasAuthority, HasAnyAuthority,"
            + " compared ignoring case - on any declaring type, and never fails. A policy or role named in the"
            + " authorization attribute is metadata, not a call, and is not listed. A member that only hands the"
            + " roles over is not listed, so an adapter that issues a token or builds the caller's principal"
            + " passes; for the same reason a role compared by the adapter itself - a claim of the role type"
            + " searched with FindAll or HasClaim - is not seen, nor is a helper of the project's own - IsAdmin(),"
            + " IsStaff() - declared outside the incoming adapter.")
```
