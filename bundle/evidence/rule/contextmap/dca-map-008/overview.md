---
type: Reference
title: "Anti-Corruption Layer: upstream contract types must stay inside the matching adapter — Overview"
tags: [reference]
evidence_for: /rule/contextmap/dca-map-008.md
---

[Full node and context](/rule/contextmap/dca-map-008.md). This is an evidence excerpt; retain the parent selection and caveats.

# Anti-Corruption Layer: upstream contract types must stay inside the matching adapter

## Selection

Every @Upstream declaration with translation() ANTI_CORRUPTION_LAYER on the package-info of every package carrying @BoundedContext whose context() names an existing bounded context, reading via() and status(). Declarations towards an unknown context are skipped.

## Check

Placement, whatever the status: no class below the declaring context's package outside the matching adapter depends on a class in the target context's channel sub-package or below - the outgoing adapter (<context>.adapter.outgoing..) for the API channel, the incoming adapter (<context>.adapter.incoming..) for the EVENTS channel. Presence, only for status() IMPLEMENTED (as in DCA-MAP-007): each declared interaction needs a class in that adapter depending on both that upstream channel and its own domain/application; a PLANNED declaration without any such code passes. Multiple upstream translators may share the package. Structure establishes a translation site, not translation quality.

## .NET reading

**Selection.** Every [Upstream] declaration with Translation AntiCorruptionLayer on the marker class of every namespace carrying [BoundedContext] whose Context names an existing bounded context, reading Via and Status. Declarations towards an unknown context are skipped.

**Check.** Placement, whatever the status: no type below the declaring context's namespace outside the matching adapter depends on a type in the target context's channel namespace or below - the outgoing adapter (<context>.Adapter.Outgoing) for the Api channel, the incoming adapter (<context>.Adapter.Incoming) for the Events channel. Presence, only for Status Implemented (as in DCA-MAP-007): each declared interaction needs a type in that adapter depending on both that upstream channel and its own Domain/Application; a Planned declaration without any such code passes. Multiple upstream translators may share the namespace. Structure establishes a translation site, not translation quality.

## Implementation

```java
DcaRule.check(
        "DCA-MAP-008",
        "Anti-Corruption Layer: upstream contract types must stay inside the matching adapter",
        "The ACL sits where the dependency crosses the boundary — outgoing adapters for synchronous"
            + " API calls, incoming adapters for consumed events — and translates the upstream"
            + " contract into the context's own model there",
        arch -> {
          CollectedViolations violations = CollectedViolations.withoutHeader();
          Map<String, String> packagesByName = packagesByName(arch);
          for (String pkg : arch.boundedContextPackages()) {
            String source = arch.contextName(pkg);
            for (Upstream u : arch.packageAnnotations(pkg, Upstream.class)) {
              String targetPkg = packagesByName.get(u.context());
              if (u.translation() != Upstream.Translation.ANTI_CORRUPTION_LAYER
                  || targetPkg == null) {
                continue;
              }
              // Two questions: only an IMPLEMENTED declaration demands that a translation site
              // exists; whatever code depends on the upstream is placed correctly whatever the
              // status, PLANNED included.
              boolean demandsTranslationSite = u.status() == Upstream.Status.IMPLEMENTED;
              for (Upstream.Consumes channel : u.via()) {
                String allowedAdapter =
                    channel == Upstream.Consumes.API
                        ? layout.outgoingAdapterPattern(pkg)
                        : layout.incomingAdapterPattern(pkg);
                String contractPattern = targetPkg + "." + channelName(arch, channel) + "..";
                boolean translationSite =
                    arch.classes().stream()
                        .filter(
                            c ->
                                com.tngtech.archunit.core.domain.JavaClass.Predicates
                                    .resideInAPackage(allowedAdapter)
                                    .test(c))
                        .anyMatch(
                            c ->
                                c.getDirectDependenciesFromSelf().stream()
                                        .anyMatch(
                                            d ->
                                                com.tngtech.archunit.core.domain.JavaClass
                                                    .Predicates.resideInAPackage(
                                                        contractPattern)
                                                    .test(d.getTargetClass()))
                                    && c.getDirectDependenciesFromSelf().stream()
                                        .anyMatch(
                                            d ->
                                                com.tngtech.archunit.core.domain.JavaClass
                                                    .Predicates.resideInAnyPackage(
                                                        layout.domainPattern(pkg),
                                                        layout.applicationPattern(pkg))
                                                    .test(d.getTargetClass())));
                violations.require(
                    translationSite || !demandsTranslationSite,
                    "Context '"
                        + source
                        + "' needs translation evidence towards '"
                        + u.context()
                        + "' ("
                        + channelName(arch, channel)
                        + ") in "
                        + allowedAdapter);
                violations.addAll(
                    noClasses()
                        .that()
                        .resideInAPackage(pkg + "..")
                        .and()
                        .resideOutsideOfPackage(allowedAdapter)
                        .should()
                        .dependOnClassesThat()
                        .resideInAPackage(targetPkg + "." + channelName(arch, channel) + "..")
                        .allowEmptyShould(true),
                    arch.classes(),
                    "Context '"
                        + source
                        + "' declares ANTI_CORRUPTION_LAYER towards '"
                        + u.context()
                        + "' ("
                        + channelName(arch, channel)
                        + ") — upstream contract types must not leave "
                        + allowedAdapter
                        + "; translate them there into the context's own model");
              }
            }
          }
          violations.throwIfAny();
        })
    .selecting(
        "Every @Upstream declaration with translation() ANTI_CORRUPTION_LAYER on the"
            + " package-info of every package carrying @BoundedContext whose context()"
            + " names an existing bounded context, reading via() and status(). Declarations"
            + " towards an unknown context are skipped.")
    .checking(
        "Placement, whatever the status: no class below the declaring context's package"
            + " outside the matching adapter depends on a class in the target context's"
            + " channel sub-package or below - the outgoing adapter"
            + " (<context>.adapter.outgoing..) for the API channel, the incoming adapter"
            + " (<context>.adapter.incoming..) for the EVENTS channel. Presence, only for"
            + " status() IMPLEMENTED (as in DCA-MAP-007): each declared interaction needs a"
            + " class in that adapter depending on both that upstream channel and its own"
            + " domain/application; a PLANNED declaration without any such code passes."
            + " Multiple upstream translators may share the package. Structure establishes a"
            + " translation site, not translation quality.")
```

## Helpers
