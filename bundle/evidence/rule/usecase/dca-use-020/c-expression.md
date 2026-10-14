---
type: Reference
title: "Use cases must not parse raw input into an id — C# expression"
tags: [reference]
evidence_for: "/rule/usecase/dca-use-020.md#c-expression"
---

[Full node and context](/rule/usecase/dca-use-020.md#c-expression). This is an evidence excerpt; retain the parent selection and caveats.

### C# expression

```csharp
DcaRule.Check(
        "DCA-USE-020",
        "Use cases must not parse raw input into an id",
        "The adapter turns raw input into the types the input port takes: an id arrives in the command as"
            + " the id's value type, parsed at the edge or by the value type's own factory, never as text the"
            + " use case parses. Text that does not parse is a malformed call the adapter answers itself;"
            + " the use case never sees it",
        arch =>
        {
            var application = DcaLayout.AnyOf(arch.AllApplicationPatterns());
            var violations = new List<string>();
            foreach (var type in arch.Types
                .Where(t => t.Namespace is not null && Matches(t.Namespace.FullName, application))
                .OrderBy(t => t.FullName, StringComparer.Ordinal))
            {
                var runtime = arch.RuntimeType(type);
                if (runtime is null || runtime.IsNested)
                {
                    continue;
                }

                foreach (var unit in new IntraClassCalls(runtime).Units)
                {
                    foreach (var call in IntraClassCalls.IlCalls(unit).Where(c => c.DeclaringType == typeof(Guid) && IdParseMethods.Contains(c.Name)))
                    {
                        violations.Add($"{type.FullName}.{IntraClassCalls.DisplayName(unit)} parses an id with Guid.{call.Name}");
                    }
                }
            }

            DcaRule.Fail(
                "Use cases must not parse raw input into an id",
                violations.Distinct().ToList(),
                "let the input port take the id's value type and parse the text in the adapter, or in the value type's own factory");
        })
    .Experimental()
    .Selecting(
        "Non-nested types in <module>.Application of every module root with their runtime type in the"
            + " loaded assemblies - use cases, helpers and application services alike - together with"
            + " their nested, async state-machine and closure types.")
    .Checking(
        "No method calls the platform's parse API for a unique identifier: System.Guid.Parse, TryParse,"
            + " ParseExact or TryParseExact, in any overload. Parsing a project's own id type, or an id"
            + " held as a number or another text format, is not seen; the value type's own factory in the"
            + " domain is outside the selection and may parse. An empty selection passes.")
```
