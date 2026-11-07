---
type: Reference
title: A domain exception is constructed only in the domain layer — Overview
tags: [reference]
evidence_for: /rule/errors/dca-err-009.md
---

[Full node and context](/rule/errors/dca-err-009.md). This is an evidence excerpt; retain the parent selection and caveats.

# A domain exception is constructed only in the domain layer

**Experimental.** This rule is binding only in a project that opted in to experimental rules - the architecture test calls `withExperimental()` (.NET: `WithExperimental()`) on its rule selection, or `dca-archunit.properties` sets `dca.rules.experimental = true`; without that opt-in the rule does not run and is information only, never a finding and never a reason to change code.

## Selection

Every class of the scan outside <module>.domain.. of every module root - the application layer, the adapters, configuration and any unplaced class - with each constructor call and constructor reference it makes, lambdas, anonymous and nested classes included. Classes in the package of the configured domain-exception role are library code and not selected; test code is not imported.

## Check

No such call or reference creates a type assignable to the configured domain-exception role (by default DomainException of the building blocks). A subclass constructor chaining to its parent's constructor is not a construction - where a misplaced exception type lives is DCA-ERR-002's finding. Construction in the domain layer passes, a domain service and a factory included. A domain exception the application catches, wraps or rethrows is not constructed and passes. A construction through reflection or a generic factory method outside the domain is not seen. An empty selection passes.

## .NET reading

**Selection.** Every type of the scan outside <Module>.Domain of every module root - the application layer, the adapters, configuration and any unplaced type - with each object creation its methods and constructors make, the compiler's async state machines, lambda closures and nested types included. Types in the namespace of the configured domain-exception role are library code and not selected; test assemblies are not loaded.

**Check.** No such creation (a newobj instruction) creates a type assignable to the configured domain-exception role (by default DomainException of the building blocks). A constructor chaining to its base constructor is not a creation - where a misplaced exception type lives is DCA-ERR-002's finding. Construction in the domain layer passes, a domain service and a factory included. A domain exception the application catches, wraps or rethrows is not constructed and passes. A construction through reflection or a generic factory method outside the domain is not seen. An empty selection passes.

## Rust reading

Unpublished (dca-rust); the suite implements it. **Held by** a lint or a test (source-test).

**Selection.** Every expression in a function body of a module outside the domain crates - application, adapters, api, infrastructure, bootstrap and unplaced crates; #[cfg(test)] items and test targets are not read: a struct literal, a call of a tuple struct or an enum variant, a unit struct or unit variant used as a value, a variant or tuple struct passed as a function, and a call of an associated function without a receiver that returns Self or the type itself, whose type implements DomainFailure.

**Check.** None of them names a domain failure - only a domain crate constructs one. Self is not followed: a domain failure declared outside the domain is DCA-ERR-002's finding. A failure the application only passes on (a variant wrapping it, ? or map_err with a conversion) is not a construction. Constructions inside macro invocations, through From/Into conversions or a generic constructor are not seen. An empty selection passes.

## Implementation

```java
DcaRule.check(
        "DCA-ERR-009",
        "A domain exception is constructed only in the domain layer",
        "The model refuses: a domain exception names a business rule the model itself broke"
            + " off. A use case never invents one. A failure the use case finds - an output"
            + " port returned nothing, the caller does not own what it names, a precondition"
            + " on a second aggregate - is the application's, a case of its result or a"
            + " use-case exception; dressed as a domain failure it claims a rule the model"
            + " never checked, and the model cannot know what a search found",
        arch -> {
          DcaMarkers markers = arch.layout().markers();
          DescribedPredicate<JavaClass> domainException = markers.is("domainException");
          DescribedPredicate<JavaClass> inDomain = arch.inDomain();
          List<String> vocabulary =
              markers.declaringPackagePatternsOf(List.of("domainException"));
          CollectedViolations collected =
              CollectedViolations.withHeader(
                  "A domain exception is constructed outside the domain layer");
          Set<String> seen = new LinkedHashSet<>();
          for (JavaClass origin : arch.classes()) {
            if (inDomain.test(origin)
                || vocabulary.stream()
                    .anyMatch(
                        pattern ->
                            PackageMatcher.of(pattern).matches(origin.getPackageName()))) {
              continue;
            }
            List<JavaCodeUnitAccess<?>> constructions = new ArrayList<>();
            constructions.addAll(origin.getConstructorCallsFromSelf());
            constructions.addAll(origin.getConstructorReferencesFromSelf());
            for (JavaCodeUnitAccess<?> construction : constructions) {
              JavaClass target = construction.getTargetOwner();
              if (!domainException.test(target) || chainsTo(construction, target)) {
                continue;
              }
              String finding =
                  construction.getOrigin().getFullName()
                      + " constructs "
                      + target.getName()
                      + " "
                      + construction.getSourceCodeLocation()
                      + " - only the domain layer raises a domain failure; a failure the"
                      + " application finds is a case of its result or a use-case exception";
              if (seen.add(finding)) {
                collected.add(finding);
              }
            }
          }
          collected.throwIfAny();
        })
    .experimental()
    .selecting(
        "Every class of the scan outside <module>.domain.. of every module root - the"
            + " application layer, the adapters, configuration and any unplaced class - with"
            + " each constructor call and constructor reference it makes, lambdas, anonymous"
            + " and nested classes included. Classes in the package of the configured"
            + " domain-exception role are library code and not selected; test code is not"
            + " imported.")
    .checking(
        "No such call or reference creates a type assignable to the configured"
            + " domain-exception role (by default DomainException of the building blocks). A"
            + " subclass constructor chaining to its parent's constructor is not a"
            + " construction - where a misplaced exception type lives is DCA-ERR-002's"
            + " finding. Construction in the domain layer passes, a domain service and a"
            + " factory included. A domain exception the application catches, wraps or"
            + " rethrows is not constructed and passes. A construction through reflection or"
            + " a generic factory method outside the domain is not seen. An empty selection"
            + " passes.",
        "let the aggregate, value object or domain service that checks the rule throw it;"
            + " for a failure the use case finds itself - nothing found, not owned - return a"
            + " refusal case of the result or throw a use-case exception declared beside the"
            + " use case")
```

## Helpers
