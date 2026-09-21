---
type: Reference
title: "Upstream declarations and the module declaration's allowed dependencies must agree — C# expression"
tags: [reference]
evidence_for: "/rule/contextmap/dca-map-006.md#c-expression"
---

[Full node and context](/rule/contextmap/dca-map-006.md#c-expression). This is an evidence excerpt; retain the parent selection and caveats.

### C# expression

```csharp
DcaRule.Check(
        "DCA-MAP-006",
        "Upstream declarations and the module declaration's allowed dependencies must agree",
        "Neither the context map nor the module boundary may know more than the other — an edge"
            + " that exists only on one side is stale",
        arch =>
        {
            var declarations = ModuleDeclarationTypes(arch);
            if (declarations.Count == 0)
            {
                return;
            }

            var violations = new List<string>();
            var moduleNames = ModuleNames(arch);
            foreach (var ns in arch.BoundedContextNamespaces)
            {
                var source = ShortName(arch, ns);
                var declared = DeclaredEdges(arch, ns);
                var carried = ModuleDeclarationsOn(arch, ns, declarations);
                if (declared.Count > 0 && carried.Count == 0)
                {
                    violations.Add("Context '" + source + "': module declaration missing on '" + source
                        + "', allowed dependencies unknown - it declares [Upstream] edges "
                        + Listed(declared)
                        + " but its marker class carries none of the configured module declaration"
                        + " attributes; declare the module there so both sides can be compared");
                    continue;
                }

                var allowed = new HashSet<string>(StringComparer.Ordinal);
                foreach (var entry in AllowedDependencies(carried))
                {
                    var normalized = Regex.Replace(entry, @"\s*::\s*", " :: ").Trim();
                    if (normalized.Contains(" :: ", StringComparison.Ordinal)
                        && moduleNames.Contains(normalized.Split(" :: ")[0]))
                    {
                        allowed.Add(normalized);
                    }
                }

                if (!declared.SetEquals(allowed))
                {
                    violations.Add("Context '" + source + "': [Upstream] declarations " + Listed(declared)
                        + " and the module declaration's allowedDependencies named-interface entries "
                        + Listed(allowed)
                        + " must describe the same edges — neither side may know more than the other");
                }
            }

            DcaRule.Fail("Upstream declarations and the module declaration must agree", violations);
        })
    .Selecting(
        "Every namespace carrying [BoundedContext], provided the layout configures at least one"
            + " module declaration attribute (a module system's per-module declaration) that is in"
            + " the loaded assemblies; reads its [Upstream] declarations (Context, Via; Planned"
            + " included) and, reflectively, the AllowedDependencies property of every configured"
            + " module declaration the marker class carries. Without a configured and loadable"
            + " module declaration the rule selects nothing and passes - which is the default here,"
            + " because .NET draws module boundaries with projects and no preset names an attribute.")
    .Checking(
        "The set of declared edges 'context :: channel' equals the set of AllowedDependencies"
            + " entries of the form 'module :: named-interface' whose module is a bounded context,"
            + " whitespace around '::' normalized. Entries without '::' and entries naming a"
            + " non-context module are ignored. A context that declares [Upstream] edges but whose"
            + " marker class carries none of the configured module declaration attributes is"
            + " reported once, as a missing module declaration with unknown allowed dependencies -"
            + " its edges are not compared; a context without [Upstream] declarations and without a"
            + " module declaration has nothing to compare and passes.")
```
