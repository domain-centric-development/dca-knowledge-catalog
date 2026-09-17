---
type: Reference
title: "Anti-Corruption Layer: upstream contract types must stay inside the matching adapter — C# expression"
tags: [reference]
evidence_for: "/rule/contextmap/dca-map-008.md#c-expression"
---

[Full node and context](/rule/contextmap/dca-map-008.md#c-expression). This is an evidence excerpt; retain the parent selection and caveats.

### C# expression

```csharp
DcaRule.Check(
        "DCA-MAP-008",
        "Anti-Corruption Layer: upstream contract types must stay inside the matching adapter",
        "The ACL sits where the dependency crosses the boundary — outgoing adapters for synchronous API calls,"
            + " incoming adapters for consumed events — and translates the upstream contract into the context's"
            + " own model there",
        arch =>
        {
            var violations = new List<string>();
            var namespacesByName = NamespacesByName(arch);
            foreach (var ns in arch.BoundedContextNamespaces)
            {
                var source = ShortName(arch, ns);
                foreach (var u in arch.NamespaceAttributes<UpstreamAttribute>(ns))
                {
                    if (u.Translation != Translation.AntiCorruptionLayer || !namespacesByName.TryGetValue(u.Context, out var targetNs))
                    {
                        continue;
                    }
                    // Two questions: only an Implemented declaration demands that a translation site exists; whatever
                    // code depends on the upstream is placed correctly whatever the status, Planned included.
                    var demandsTranslationSite = u.Status == UpstreamStatus.Implemented;
                    foreach (var channel in u.Via)
                    {
                        var allowedAdapter = channel == Consumes.Api
                            ? OutgoingAdapterNamespace(ns)
                            : IncomingAdapterNamespace(ns);
                        var channelNs = targetNs + "." + ChannelName(arch, channel);
                        var translationSite = TypesBelow(arch, allowedAdapter).Any(t => DependsOnNamespace(t, channelNs)
                            && (DependsOnNamespace(t, ns + "." + Layout.DomainSegment) || DependsOnNamespace(t, ns + "." + Layout.ApplicationSegment)));
                        if (demandsTranslationSite && !translationSite) violations.Add("Context '" + source + "' needs translation evidence towards '" + u.Context + "' (" + ChannelName(arch, channel) + ") in " + allowedAdapter);
                        foreach (var type in TypesBelow(arch, ns).Where(t => !IsBelow(t, allowedAdapter)))
                        {
                            if (DependsOnNamespace(type, channelNs))
                            {
                                violations.Add("Context '" + source + "' declares AntiCorruptionLayer towards '" + u.Context
                                    + "' (" + ChannelName(arch, channel) + ") — " + type.FullName + " uses upstream contract types"
                                    + " outside " + allowedAdapter + "; translate them there into the context's own model");
                            }
                        }
                    }
                }
            }
            DcaRule.Fail("Anti-Corruption Layer: upstream contract types must stay inside the matching adapter", violations);
        })
    .Selecting(
        "Every [Upstream] declaration with Translation AntiCorruptionLayer on the"
            + " marker class of every namespace carrying [BoundedContext] whose Context"
            + " names an existing bounded context, reading Via and Status. Declarations"
            + " towards an unknown context are skipped.")
    .Checking(
        "Placement, whatever the status: no type below the declaring context's namespace"
            + " outside the matching adapter depends on a type in the target context's channel"
            + " namespace or below - the outgoing adapter (<context>.Adapter.Outgoing) for the Api"
            + " channel, the incoming adapter (<context>.Adapter.Incoming) for the Events channel."
            + " Presence, only for Status Implemented (as in DCA-MAP-007): each declared interaction"
            + " needs a type in that adapter depending on both that upstream channel and its own"
            + " Domain/Application; a Planned declaration without any such code passes. Multiple"
            + " upstream translators may share the namespace. Structure establishes a translation"
            + " site, not translation quality.")
```
