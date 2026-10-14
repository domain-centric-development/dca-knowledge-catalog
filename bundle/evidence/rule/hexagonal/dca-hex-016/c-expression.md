---
type: Reference
title: "Diagnostic: adapters that publish an enum by its member name — C# expression"
tags: [reference]
evidence_for: "/rule/hexagonal/dca-hex-016.md#c-expression"
---

[Full node and context](/rule/hexagonal/dca-hex-016.md#c-expression). This is an evidence excerpt; retain the parent selection and caveats.

### C# expression

```csharp
DcaRule.Informational(
        "DCA-HEX-016",
        "Diagnostic: adapters that publish an enum by its member name",
        "A value an adapter publishes from an enum is spelled explicitly - a code per value on the enum or"
            + " a mapping in the adapter - never derived from the member's name: renaming a member is a"
            + " refactoring inside the code and must not change what a client reads",
        arch =>
        {
            var inner = new Regex(DcaLayout.AnyOf(arch.AllDomainPatterns().Concat(arch.AllApplicationPatterns())));
            bool InnerEnum(Type? type) => type is { IsEnum: true, Namespace: { } ns } && inner.IsMatch(ns);

            var adapters = DcaLayout.AnyOf(arch.AllAdapterPatterns());
            var observed = new List<string>();
            foreach (var adapter in arch.Types.Where(t => InNamespace(t, adapters)).OrderBy(t => t.FullName, StringComparer.Ordinal))
            {
                var runtime = arch.RuntimeType(adapter);
                if (runtime is null || runtime.IsNested)
                {
                    continue;
                }

                // A record's generated PrintMembers/ToString spells every member - not the adapter's choice.
                foreach (var unit in new IntraClassCalls(runtime).Units.Where(u => !u.IsDefined(typeof(System.Runtime.CompilerServices.CompilerGeneratedAttribute), false)))
                {
                    Type? pending = null;
                    foreach (var (code, operand) in IntraClassCalls.IlInstructions(unit))
                    {
                        if ((code == System.Reflection.Emit.OpCodes.Box || code == System.Reflection.Emit.OpCodes.Constrained) && operand is Type boxed)
                        {
                            pending = InnerEnum(boxed) ? boxed : null;
                            continue;
                        }

                        if (operand is not MethodBase call)
                        {
                            continue;
                        }

                        var how = EnumNameUse(call, pending, InnerEnum, out var spelled);
                        pending = null;
                        if (how is not null)
                        {
                            observed.Add($"{adapter.FullName}.{IntraClassCalls.DisplayName(unit)} {how} the enum {spelled!.FullName}");
                        }
                    }
                }
            }

            return observed.Distinct().ToList();
        })
    .Experimental()
    .Selecting(
        "Non-nested types in <module>.Adapter of every module root, incoming and outgoing, with their"
            + " runtime type in the loaded assemblies, together with their nested, async state-machine and"
            + " closure types; enums declared in a domain or application namespace of any module root.")
    .Checking(
        "Informational diagnostic only: lists a method that turns such an enum into its member name as"
            + " the IL shows it - ToString in any overload, called through a constrained call or on the"
            + " boxed value; the boxed value passed straight into a string-building call (concatenation,"
            + " formatting, joining, appending); an interpolation hole of the enum type; Enum.GetName or"
            + " Enum.GetNames over it - and never fails. Compiler-generated methods, such as a record's generated"
            + " PrintMembers and ToString, are not read. A boxed value stored first and formatted later,"
            + " a serializer that writes names, and a name read through a generic helper are not seen;"
            + " whether the text reaches a client stays with review.")
```
