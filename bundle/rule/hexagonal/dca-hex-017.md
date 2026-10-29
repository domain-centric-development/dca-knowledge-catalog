---
type: Rule
id: DCA-HEX-017
title: Event listeners that drive an input port must run after the commit in their own transaction
rule: "A reaction to an event changes state or performs an external effect through a use case. Run inside the transaction that raised the event, it changes a second aggregate in the first one's transaction, a failure in the reaction rolls back the fact that caused it, and a retry of the request runs the reaction again. A listener that only translates or measures calls output ports and may run in that transaction."
constraint: Event listeners that drive an input port must run after the commit in their own transaction.
selects: "Classes of every module root; within them, the methods carrying, directly or as a meta-annotation, an annotation of the configured event-listener role - on the method or on one of its parameters, where CDI puts its observer. With an empty event-listener or transactional-event-listener role nothing is selected and the rule passes."
checks: "A selected method that - itself or a method of the same class it reaches through calls within the class - calls a type assignable to the configured input-port role carries, directly or as a meta-annotation, an annotation of the configured transactional-event-listener role - on the method or a parameter; an entry <annotation>#<attribute>=<value> asks for that attribute value, as CDI's observer phase - and an annotation of the configured transactional role on the method or its class. The rule reads the listener's phase and transaction, not whether a durable publication store backs it; an input port reached through a second class is not followed. An empty selection passes."
enforced_by: "HexagonalRules#DCA-HEX-017"
status: enforced
maturity: experimental
rule_set: hexagonal
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/HexagonalRules.java
tags: [hexagonal, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/HexagonalRules.cs
---

# Event listeners that drive an input port must run after the commit in their own transaction

**Experimental.** This rule is binding only in a project that opted in to experimental rules - the architecture test calls `withExperimental()` (.NET: `WithExperimental()`) on its rule selection, or `dca-archunit.properties` sets `dca.rules.experimental = true`; without that opt-in the rule does not run and is information only, never a finding and never a reason to change code.

## Selection

Classes of every module root; within them, the methods carrying, directly or as a meta-annotation, an annotation of the configured event-listener role - on the method or on one of its parameters, where CDI puts its observer. With an empty event-listener or transactional-event-listener role nothing is selected and the rule passes.

## Check

A selected method that - itself or a method of the same class it reaches through calls within the class - calls a type assignable to the configured input-port role carries, directly or as a meta-annotation, an annotation of the configured transactional-event-listener role - on the method or a parameter; an entry <annotation>#<attribute>=<value> asks for that attribute value, as CDI's observer phase - and an annotation of the configured transactional role on the method or its class. The rule reads the listener's phase and transaction, not whether a durable publication store backs it; an input port reached through a second class is not followed. An empty selection passes.

## .NET reading

**Selection.** Classes of every module root assignable to a type of the configured event-listener role and to none of the configured transactional-event-listener role. With either role empty - both are empty in every preset - nothing is selected and the rule passes.

**Check.** No method of such a class - async state machines and lambdas included - calls a method of a type assignable to IInputPort. The rule reads the listener's kind, not whether an outbox backs it; an input port reached through a second class is not followed. An empty selection passes.

## Implementation

The verbatim ArchUnit expression is in the evidence slice [Overview](/evidence/rule/hexagonal/dca-hex-017/overview.md); every helper it calls has a slice of its own, listed under *Evidence slices* below.

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)

## Evidence slices

- [Overview](/evidence/rule/hexagonal/dca-hex-017/overview.md)
- [`driveAnInputPortOnlyAfterTheCommit`](/evidence/rule/hexagonal/dca-hex-017/driveaninputportonlyafterthecommit.md)
- [`AnnotationRoles.listenerEntry`](/evidence/rule/hexagonal/dca-hex-017/annotationroles-listenerentry.md)
- [`IntraClassCalls.reachableFrom`](/evidence/rule/hexagonal/dca-hex-017/intraclasscalls-reachablefrom.md)
- [`AnnotationRoles.isMetaAnnotatedWithAny`](/evidence/rule/hexagonal/dca-hex-017/annotationroles-ismetaannotatedwithany.md)
- [`AnnotationRoles.matchingEntry`](/evidence/rule/hexagonal/dca-hex-017/annotationroles-matchingentry.md)
- [`AnnotationRoles.collect`](/evidence/rule/hexagonal/dca-hex-017/annotationroles-collect.md)
- [`IntraClassCalls.closure`](/evidence/rule/hexagonal/dca-hex-017/intraclasscalls-closure.md)
- [`AnnotationRoles.addValues`](/evidence/rule/hexagonal/dca-hex-017/annotationroles-addvalues.md)
- [C# expression](/evidence/rule/hexagonal/dca-hex-017/c-expression.md)
- [C# helper IntraClassCalls](/evidence/rule/hexagonal/dca-hex-017/c-helper-intraclasscalls.md)
