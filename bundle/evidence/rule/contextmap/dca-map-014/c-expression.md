---
type: Reference
title: "Every allowed dependency of a module declaration must be backed by an actual code dependency — C# expression"
tags: [reference]
evidence_for: "/rule/contextmap/dca-map-014.md#c-expression"
---

[Full node and context](/rule/contextmap/dca-map-014.md#c-expression). This is an evidence excerpt; retain the parent selection and caveats.

### C# expression

```csharp
DcaRule.Check(
        "DCA-MAP-014",
        "Every allowed dependency of a module declaration must be backed by an actual code dependency",
        "A context declares only the dependencies it uses. An allowed dependency no code uses is a stale"
            + " edge: the module boundary claims a relationship the code does not have, and the next"
            + " dependency on that module passes without anyone deciding it",
        arch =>
        {
            var declarations = ModuleDeclarationTypes(arch);
            if (declarations.Count == 0)
            {
                return;
            }

            var violations = new List<string>();
            var contexts = NamespacesByName(arch);
            foreach (var ns in arch.BoundedContextNamespaces)
            {
                var source = ShortName(arch, ns);
                foreach (var entry in AllowedDependencies(ModuleDeclarationsOn(arch, ns, declarations))
                    .Select(e => Regex.Replace(e, @"\s*::\s*", " :: ").Trim())
                    .Distinct(StringComparer.Ordinal)
                    .OrderBy(e => e, StringComparer.Ordinal))
                {
                    var parts = entry.Split(" :: ");
                    var module = contexts.TryGetValue(parts[0], out var contextNamespace)
                        ? contextNamespace
                        : arch.Layout.RootNamespace + "." + parts[0];
                    var target = parts.Length > 1 ? module + "." + parts[1] : module;
                    var backed = TypesBelow(arch, ns).Any(t => t.Dependencies.Any(d =>
                        d.Target.Namespace is { } targetNamespace
                        && !IsBelow(d.Target, ns)
                        && (string.Equals(targetNamespace.FullName, target, StringComparison.OrdinalIgnoreCase)
                            || targetNamespace.FullName.StartsWith(target + ".", StringComparison.OrdinalIgnoreCase))));
                    if (!backed)
                    {
                        violations.Add("Context '" + source + "': the module declaration allows '" + entry
                            + "' but no type of the context depends on " + target);
                    }
                }
            }

            DcaRule.Fail(
                "Every allowed dependency of a module declaration must be backed by an actual code dependency",
                violations,
                "remove the entry from the module declaration, or add it back when code first needs it");
        })
    .Experimental()
    .Selecting(
        "Every namespace carrying [BoundedContext], provided the layout configures at least one module"
            + " declaration attribute (a module system's per-module declaration) that is in the loaded"
            + " assemblies; reads, reflectively, the AllowedDependencies entries of every configured module"
            + " declaration the marker class carries. Without a configured and loadable module declaration"
            + " the rule selects nothing and passes - the default here, because .NET draws module"
            + " boundaries with projects and no preset names an attribute.")
    .Checking(
        "For every entry - 'module' or 'module :: named-interface', whitespace around '::' normalized -"
            + " at least one type below the context namespace has a direct dependency on a type in the"
            + " named module's namespace (a bounded context by its name, any other module as"
            + " <root>.<module>) or, for a named interface, in that segment below it, compared ignoring"
            + " case. Dependencies within the context itself do not count. Whether an undeclared"
            + " dependency exists is DCA-MAP-006's and the isolation rules' business, not this rule's.")
```
