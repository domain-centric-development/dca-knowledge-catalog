---
type: Reference
title: GET handlers must not drive an input port that takes a command — Overview
tags: [reference]
evidence_for: /rule/hexagonal/dca-hex-014.md
---

[Full node and context](/rule/hexagonal/dca-hex-014.md). This is an evidence excerpt; retain the parent selection and caveats.

# GET handlers must not drive an input port that takes a command

**Experimental.** This rule is binding only in a project that opted in to experimental rules - the architecture test calls `withExperimental()` (.NET: `WithExperimental()`) on its rule selection, or `dca-archunit.properties` sets `dca.rules.experimental = true`; without that opt-in the rule does not run and is information only, never a finding and never a reason to change code.

## Selection

Classes in <module>.adapter.incoming.. of every module root that are directly annotated with one of the configured web-controller or REST-controller stereotypes; within them, the methods carrying, directly or as a meta-annotation, an annotation of the configured GET-mapping role - or, for an entry that names an attribute value, an annotation of that type whose attribute holds the value (a general mapping annotation restricted to GET), and for an entry that names an attribute without a value, an annotation of that type whose attribute holds none (a general mapping that names no HTTP method). The values of the same annotation on the declaring class count as well; a class-level mapping alone makes no method a handler. A mapping that names no HTTP method answers every method, GET included, and counts as a GET handler.

## Check

No such method - or a method of the same class it reaches through calls within the class - calls a type assignable to the configured input-port role whose input is a command (the configured command role, by default a simple name ending with Command): a parameter of the called method, of a public method of the port, or a type argument of the input port it extends. A mapping that names no HTTP method is checked like a GET handler. With empty web-controller and REST-controller roles, or an empty GET-mapping role, nothing is selected and the rule passes.

## .NET reading

**Selection.** Methods declared by classes in <module>.Adapter.Incoming of every module root that carry an attribute of the configured GET-mapping role (derived attributes included) - for an entry that names a property value, an attribute of that type whose property holds the value (a general verb attribute restricted to GET); for an entry that names a property without a value, a public instance method of a class recognised as a controller, not a page model, that carries no attribute of the configured non-action role and none of whose attributes of that type holds a value (an action that names no HTTP method) - or - on a class recognised as a controller or page model - whose name starts with a configured GET-handler prefix. A mapping that names no HTTP method answers every method, GET included, and counts as a GET handler. Both roles are empty in the None() preset, which then selects nothing.

**Check.** No method reached from the handler through calls within the class - async state machines and lambdas included - calls a method of a type assignable to IInputPort that takes a command (the configured command role, by default a simple name ending with Command) as a parameter. A mapping that names no HTTP method is checked like a GET handler. A handler mapped by a routing call rather than by an attribute or a name is not seen, and a command reached through a second class is not followed. An empty selection passes.

## Implementation

```java
DcaRule.of(
        "DCA-HEX-014",
        "GET handlers must not drive an input port that takes a command",
        "A state-changing use case is reached only by an unsafe HTTP method, never by GET."
            + " Links, prefetching, crawlers and cross-site navigation issue GET requests on"
            + " their own; a GET that runs a command changes state nobody asked to change. A"
            + " handler that names no HTTP method answers GET as well",
        arch ->
            classes()
                .that(arch.inIncomingAdapter())
                .and(AnnotationRoles.annotatedWithAny(webControllers, restControllers))
                .should(driveNoCommandFromGet(getMapping, layout.markers()))
                .allowEmptyShould(true))
    .experimental()
    .selecting(
        "Classes in <module>.adapter.incoming.. of every module root that are directly"
            + " annotated with one of the configured web-controller or REST-controller"
            + " stereotypes; within them,"
            + " the methods carrying, directly or as a meta-annotation, an annotation of the"
            + " configured GET-mapping role - or, for an entry that names an attribute value, an"
            + " annotation of that type whose attribute holds the value (a general mapping"
            + " annotation restricted to GET), and for an entry that names an attribute without a"
            + " value, an annotation of that type whose attribute holds none (a general mapping"
            + " that names no HTTP method). The values of the same annotation on the declaring"
            + " class count as well; a class-level mapping alone makes no method a handler. A"
            + " mapping that names no HTTP method answers every method, GET included, and counts"
            + " as a GET handler.")
    .checking(
        "No such method - or a method of the same class it reaches through calls within the"
            + " class - calls a type assignable to the configured input-port role whose input is"
            + " a command (the configured command role, by default a simple name ending with"
            + " Command): a parameter of the called method, of a public method of the port, or a"
            + " type argument of the input port it extends. A mapping that names no"
            + " HTTP method is checked like a GET handler. With empty web-controller and"
            + " REST-controller roles, or an empty GET-mapping role, nothing is selected and the"
            + " rule passes.",
        "map the handler to POST, PUT or DELETE, or let the GET handler ask a query")
```

## Helpers
