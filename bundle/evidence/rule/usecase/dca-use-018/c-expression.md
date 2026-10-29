---
type: Reference
title: "In a module grouped by feature, incoming adapters must drive the commands of one feature only — C# expression"
tags: [reference]
evidence_for: "/rule/usecase/dca-use-018.md#c-expression"
---

[Full node and context](/rule/usecase/dca-use-018.md#c-expression). This is an evidence excerpt; retain the parent selection and caveats.

### C# expression

```csharp
DcaRule.Check(
        "DCA-USE-018",
        "In a module grouped by feature, incoming adapters must drive the commands of one feature only",
        "Once the application is grouped into features, the incoming adapter is cut the same way: one"
            + " adapter changes through the use cases of one feature. An adapter that drives the commands of"
            + " two features grows with every use case of both and is cut along them. Reading a neighbouring"
            + " feature's query is no reason to cut",
        arch =>
        {
            var violations = new List<string>();
            foreach (var adapter in arch.Classes
                .Where(c => !c.IsCompilerGenerated && c.Namespace is not null && arch.InIncomingAdapter(c))
                .OrderBy(c => c.FullName, StringComparer.Ordinal))
            {
                var root = arch.ModuleRootOf(adapter.Namespace!.FullName);
                if (root is null)
                {
                    continue;
                }

                var features = new SortedDictionary<string, SortedSet<string>>(StringComparer.Ordinal);
                foreach (var port in InputPortsOf(arch, adapter).Where(p => PortInputs(p, arch.Layout.Markers).Any(t => arch.Layout.Markers.Is("Command", t))))
                {
                    var feature = FeatureOf(port.Namespace ?? "", root, layout);
                    if (feature is null)
                    {
                        continue;
                    }

                    if (!features.TryGetValue(feature, out var ports))
                    {
                        features[feature] = ports = new SortedSet<string>(StringComparer.Ordinal);
                    }

                    ports.Add(port.Name.Split('`')[0]);
                }

                if (features.Count > 1)
                {
                    violations.Add($"{adapter.FullName} drives the commands of {features.Count} features: "
                        + string.Join("; ", features.Select(f => $"{f.Key} ({string.Join(", ", f.Value)})")));
                }
            }

            DcaRule.Fail(
                "In a module grouped by feature, incoming adapters must drive the commands of one feature only",
                violations,
                "cut the adapter along the features - one adapter class per feature, below the same protocol segment");
        })
    .Experimental()
    .Selecting(
        "Classes in <module>.Adapter.Incoming of every module root, compiler-generated classes excluded,"
            + " with the command ports they depend on: types assignable to IInputPort in the same module's"
            + " application namespace whose input is a command (the configured command role, by default a simple"
            + " name ending with Command) - the input type argument of IUseCase<TInput, TOutput> or a parameter of"
            + " an input-port method. A port counts toward a feature when it sits at"
            + " Application.<Feature>.<UseCase> after removing configured OperationContainers segments, the"
            + " grouped depth of DCA-USE-014.")
    .Checking(
        "The command ports an adapter depends on belong to one feature. A port whose input is a query, or"
            + " neither, is not counted - reading a neighbouring feature's query is allowed. A port in a"
            + " flat use-case namespace"
            + " (Application.<UseCase>), in Application.Shared or in another module counts toward no"
            + " feature, so a module that is not grouped into features is never reported. Fields,"
            + " constructor parameters and calls all count as a dependency; constructor parameters are read"
            + " from the runtime type as well. An empty selection passes.")
```
