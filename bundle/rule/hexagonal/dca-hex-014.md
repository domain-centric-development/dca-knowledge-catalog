---
type: Rule
id: DCA-HEX-014
title: GET handlers must not drive an input port that takes a command
rule: "A state-changing use case is reached only by an unsafe HTTP method, never by GET. Links, prefetching, crawlers and cross-site navigation issue GET requests on their own; a GET that runs a command changes state nobody asked to change."
constraint: GET handlers must not drive an input port that takes a command.
selects: "Classes in <module>.adapter.incoming.. of every module root that are directly annotated with one of the configured web-controller stereotypes; within them, the methods carrying, directly or as a meta-annotation, an annotation of the configured GET-mapping role."
checks: "No such method - or a method of the same class it reaches through calls within the class - calls a type assignable to the configured input-port role whose input ends with Command: a parameter of the called method, of a public method of the port, or a type argument of the input port it extends. A mapping that names its HTTP method in an attribute is not read. With an empty web-controller or GET-mapping role nothing is selected and the rule passes."
enforced_by: "HexagonalRules#DCA-HEX-014"
status: enforced
maturity: experimental
rule_set: hexagonal
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/HexagonalRules.java
tags: [hexagonal, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/HexagonalRules.cs
---

# GET handlers must not drive an input port that takes a command

**Experimental.** This rule is binding only in a project that opted in to experimental rules - the architecture test calls `withExperimental()` (.NET: `WithExperimental()`) on its rule selection, or `dca-archunit.properties` sets `dca.rules.experimental = true`; without that opt-in the rule does not run and is information only, never a finding and never a reason to change code.

## Selection

Classes in <module>.adapter.incoming.. of every module root that are directly annotated with one of the configured web-controller stereotypes; within them, the methods carrying, directly or as a meta-annotation, an annotation of the configured GET-mapping role.

## Check

No such method - or a method of the same class it reaches through calls within the class - calls a type assignable to the configured input-port role whose input ends with Command: a parameter of the called method, of a public method of the port, or a type argument of the input port it extends. A mapping that names its HTTP method in an attribute is not read. With an empty web-controller or GET-mapping role nothing is selected and the rule passes.

## .NET reading

**Selection.** Methods declared by classes in <module>.Adapter.Incoming of every module root that carry an attribute of the configured GET-mapping role (derived attributes included), or - on a class recognised as a controller or page model - whose name starts with a configured GET-handler prefix. Both roles are empty in the None() preset, which then selects nothing.

**Check.** No method reached from the handler through calls within the class - async state machines and lambdas included - calls a method of a type assignable to IInputPort that takes a parameter whose type name ends in Command. A handler mapped by a routing call rather than by an attribute or a name is not seen, and a command reached through a second class is not followed. An empty selection passes.

## Implementation

The verbatim ArchUnit expression is in the evidence slice [Overview](/evidence/rule/hexagonal/dca-hex-014/overview.md); every helper it calls has a slice of its own, listed under *Evidence slices* below.

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allIncomingAdapterPatterns()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).

## Related mentions (heuristic)

- [UseCase<INPUT, OUTPUT>](/marker/port-in/usecase.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)

## Evidence slices

- [Overview](/evidence/rule/hexagonal/dca-hex-014/overview.md)
- [`driveNoCommandFromGet`](/evidence/rule/hexagonal/dca-hex-014/drivenocommandfromget.md)
- [`AnnotationRoles.annotatedWithAny`](/evidence/rule/hexagonal/dca-hex-014/annotationroles-annotatedwithany.md)
- [`takesCommand`](/evidence/rule/hexagonal/dca-hex-014/takescommand.md)
- [`AnnotationRoles.isMetaAnnotatedWithAny`](/evidence/rule/hexagonal/dca-hex-014/annotationroles-ismetaannotatedwithany.md)
- [`IntraClassCalls.reachableFrom`](/evidence/rule/hexagonal/dca-hex-014/intraclasscalls-reachablefrom.md)
- [`TypeInspection.takesInputEndingWith`](/evidence/rule/hexagonal/dca-hex-014/typeinspection-takesinputendingwith.md)
- [`IntraClassCalls.closure`](/evidence/rule/hexagonal/dca-hex-014/intraclasscalls-closure.md)
- [`TypeInspection.inputTypes`](/evidence/rule/hexagonal/dca-hex-014/typeinspection-inputtypes.md)
- [`TypeInspection.collectInputs`](/evidence/rule/hexagonal/dca-hex-014/typeinspection-collectinputs.md)
- [`TypeInspection.involvedTypes`](/evidence/rule/hexagonal/dca-hex-014/typeinspection-involvedtypes.md)
- [`TypeInspection.collect`](/evidence/rule/hexagonal/dca-hex-014/typeinspection-collect.md)
- [`TypeInspection.typeArgumentBindings`](/evidence/rule/hexagonal/dca-hex-014/typeinspection-typeargumentbindings.md)
- [`TypeInspection.variableKey`](/evidence/rule/hexagonal/dca-hex-014/typeinspection-variablekey.md)
- [C# expression](/evidence/rule/hexagonal/dca-hex-014/c-expression.md)
- [C# helper IntraClassCalls](/evidence/rule/hexagonal/dca-hex-014/c-helper-intraclasscalls.md)
