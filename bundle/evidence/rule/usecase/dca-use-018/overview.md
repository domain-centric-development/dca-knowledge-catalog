---
type: Reference
title: "In a module grouped by feature, incoming adapters must drive the commands of one feature only — Overview"
tags: [reference]
evidence_for: /rule/usecase/dca-use-018.md
---

[Full node and context](/rule/usecase/dca-use-018.md). This is an evidence excerpt; retain the parent selection and caveats.

# In a module grouped by feature, incoming adapters must drive the commands of one feature only

**Experimental.** This rule is binding only in a project that opted in to experimental rules - the architecture test calls `withExperimental()` (.NET: `WithExperimental()`) on its rule selection, or `dca-archunit.properties` sets `dca.rules.experimental = true`; without that opt-in the rule does not run and is information only, never a finding and never a reason to change code.

## Selection

Per module root whose input ports or use cases sit at the feature depth application.<feature>.<usecase> (configured operationContainers segments removed, application.shared excluded): every non-interface class in <module>.adapter.incoming.. of that module. Modules with flat use case packages are not selected.

## Check

The types assignable to the configured input-port role whose input ends with Command - a parameter of a public method, or a type argument of the input port they extend - that the class depends on directly, inside the same module, belong to at most one feature, the feature being the first segment below the application package. Input ports whose input ends with Query, or with neither suffix, are not counted, and neither is an input port of another module. Nested classes are counted on their own. An empty selection passes.

## .NET reading

**Selection.** Classes in <module>.Adapter.Incoming of every module root, compiler-generated classes excluded, with the command ports they depend on: types assignable to IInputPort in the same module's application namespace whose input ends in Command - the input type argument of IUseCase<TInput, TOutput> or a parameter of an input-port method. A port counts toward a feature when it sits at Application.<Feature>.<UseCase> after removing configured OperationContainers segments, the grouped depth of DCA-USE-014.

**Check.** The command ports an adapter depends on belong to one feature. A port whose input ends in Query, or ends in neither, is not counted - reading a neighbouring feature's query is allowed. A port in a flat use-case namespace (Application.<UseCase>), in Application.Shared or in another module counts toward no feature, so a module that is not grouped into features is never reported. Fields, constructor parameters and calls all count as a dependency; constructor parameters are read from the runtime type as well. An empty selection passes.

## Implementation

```java
DcaRule.check(
        "DCA-USE-018",
        "In a module grouped by feature, incoming adapters must drive the commands of one"
            + " feature only",
        "Once the application is grouped, the incoming adapter is cut the same way: one"
            + " controller changes state through the use cases of one feature. A class that"
            + " drives the commands of two features grows with every use case of both and hides"
            + " the cut the application already made. Reading a neighbouring feature's query is"
            + " no reason to cut",
        arch -> checkOneFeaturePerAdapter(arch, layout))
    .experimental()
    .selecting(
        "Per module root whose input ports or use cases sit at the feature depth"
            + " application.<feature>.<usecase> (configured operationContainers segments"
            + " removed, application.shared excluded): every non-interface class in"
            + " <module>.adapter.incoming.. of that module. Modules with flat use case packages"
            + " are not selected.")
    .checking(
        "The types assignable to the configured input-port role whose input ends with"
            + " Command - a parameter of a public method, or a type argument of the input port"
            + " they extend - that the class depends on directly, inside the same module, belong"
            + " to at most one feature, the feature being the first segment below the"
            + " application package. Input ports whose input ends with Query, or with neither"
            + " suffix, are not counted, and neither is an input port of another module. Nested classes are counted on their"
            + " own. An empty selection passes.",
        "cut the class along the features, one incoming adapter per feature, mirroring"
            + " application.<feature> below the protocol segment")
```

## Helpers
