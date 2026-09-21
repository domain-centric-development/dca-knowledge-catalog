---
type: Reference
title: "Use cases that save an aggregate must publish its domain events — C# expression"
tags: [reference]
evidence_for: "/rule/usecase/dca-use-009.md#c-expression"
---

[Full node and context](/rule/usecase/dca-use-009.md#c-expression). This is an evidence excerpt; retain the parent selection and caveats.

### C# expression

```csharp
DcaRule.Check(
        "DCA-USE-009",
        "Use cases that save an aggregate must publish its domain events",
        "A saved aggregate must not keep its events: unpublished, they are lost, and stored on the"
            + " instance they may later be published out of context. Publishing belongs after the"
            + " save, in the use case that owns the unit of work - unless the aggregate is proven never to register an"
            + " event. Checked per entry path, following calls within the use case class: every"
            + " entry point that reaches a save - a method callable from outside the class, or one"
            + " nothing in the class calls - must also reach a publication; a wrapper that publishes"
            + " does not cover a direct call of the public method it wraps, and a helper two methods"
            + " share does not connect them. That the"
            + " publication follows the save and concerns the same aggregate is not established"
            + " statically. Only IDomainEventPublisher.PublishAndClearEventsAsync counts as a"
            + " publication: iterating DomainEvents and calling PublishAsync(event), even followed by"
            + " ClearDomainEvents(), separates dispatch from acknowledgement and is not accepted",
        arch =>
        {
            var violations = new List<string>();
            var useCases = arch.Classes
                .Where(c => c.Namespace is not null
                    && Matches(c.Namespace.FullName, DcaLayout.AnyOf(arch.AllApplicationPatterns()))
                    && (IsAssignableTo(arch, c, arch.Layout.Markers.InputPort) || c.Name.Split('`')[0].EndsWith(arch.Layout.UseCaseSuffix, StringComparison.Ordinal)))
                .OrderBy(c => c.FullName, StringComparer.Ordinal);
            foreach (var useCase in useCases)
            {
                var runtime = arch.RuntimeType(useCase);
                if (runtime is null)
                {
                    continue;
                }

                var calls = new IntraClassCalls(runtime);
                foreach (var unit in calls.Units.Where(u => IntraClassCalls.Calls(u, "SaveAsync", arch.Layout.Markers.Repository)))
                {
                    if (IntraClassCalls.IlCalls(unit).Where(m => m.Name == "SaveAsync" && m.DeclaringType is not null && DcaMarkers.IsAssignableToByName(m.DeclaringType, arch.Layout.Markers.Repository))
                        .All(m => EventFreeAggregate.Repository(m, arch))) continue;
                    foreach (var entry in calls.EntryPointsOf(unit))
                    {
                        var publishes = calls.ReachableFrom(entry)
                            .Any(u => IntraClassCalls.Calls(u, "PublishAndClearEventsAsync", arch.Layout.Markers.DomainEventPublisher));
                        if (!publishes)
                        {
                            violations.Add($"{useCase.FullName}.{IntraClassCalls.PathName(entry, unit)} saves an aggregate without"
                                + " publishing its domain events - no method reached from there calls PublishAndClearEventsAsync");
                        }
                    }
                }
            }

            DcaRule.Fail(
                "Use cases that save an aggregate must publish its domain events",
                violations.Distinct().ToList(),
                "call IDomainEventPublisher.PublishAndClearEventsAsync(aggregate) after IRepository.SaveAsync(aggregate) on every path that saves");
        })
    .Selecting(
        "Classes in <module>.Application of every module root selected by IInputPort assignability or the"
            + " configured use-case suffix, whose runtime type is in the loaded assemblies.")
    .Checking(
        "Only a resolved IRepository<T,ID> aggregate is exempt, and only when its complete hierarchy is under scan and nothing registers an event on it: neither the hierarchy itself nor a type outside it. The walk stops at the platform and at the namespaces the configured marker roles live in, so a project's own vocabulary stops it where the library's does. Unresolved arguments and partial scans are not exempt. For every non-exempt method calling IRepository.SaveAsync, every entry point"
            + " reaching it (a method callable from outside the class, or one nothing in the"
            + " class calls) also reaches, through calls within the class, a call of"
            + " IDomainEventPublisher.PublishAndClearEventsAsync. Calls are read from the IL of"
            + " the class and its nested state-machine and closure types, so async methods and"
            + " lambdas are followed. Only PublishAndClearEventsAsync counts - PublishAsync(event),"
            + " even followed by ClearDomainEvents(), does not. A use case without a save (a query,"
            + " a bulk delete) is selected but has nothing to check and passes. The method names are fixed and are not part of the marker roles: a vocabulary whose repository writes under another name is selected and then found to save nothing, so this rule passes over it.")
```
