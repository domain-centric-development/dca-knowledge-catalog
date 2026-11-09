---
type: Rule
id: DCA-ADV-021
title: Domain services are used only by the application and by other domain services
rule: "A domain service holds logic that spans aggregates, and the use case decides when it runs and puts its outcome into the result. A model type, a read model, an adapter or the composition root that calls one takes that decision outside the application - the incoming adapter and the model type are each held by a narrower rule too (DCA-HEX-012, DCA-ADV-019)."
constraint: Domain services are used only by the application and by other domain services.
selects: "Every class under scan outside the application layer that does not carry the domain-service role, with the classes nested in it - the domain model, the adapters of both directions, the composition root (the infrastructure layer) and classes outside every layer. A class nested in an application class or in a domain service counts as its outer class and is not selected."
checks: "None of them calls a method of, reads a field of, references a method of or instantiates a type carrying the domain-service role. A class in the infrastructure layer - the composition root - may construct one (a constructor call or a constructor reference) to hand it to a use case; a call there is reported. Naming the type as a parameter, a field or a return type is not an access and is not reported. An empty selection passes."
enforced_by: "AdvancedPatternRules#DCA-ADV-021"
status: enforced
maturity: experimental
rule_set: advanced
implementations: [java, dotnet, rust]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/AdvancedPatternRules.java
tags: [advanced, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/AdvancedPatternRules.cs
---

# Domain services are used only by the application and by other domain services

**Experimental.** This rule is binding only in a project that opted in to experimental rules - the architecture test calls `withExperimental()` (.NET: `WithExperimental()`) on its rule selection, or `dca-archunit.properties` sets `dca.rules.experimental = true`; without that opt-in the rule does not run and is information only, never a finding and never a reason to change code.

## Selection

Every class under scan outside the application layer that does not carry the domain-service role, with the classes nested in it - the domain model, the adapters of both directions, the composition root (the infrastructure layer) and classes outside every layer. A class nested in an application class or in a domain service counts as its outer class and is not selected.

## Check

None of them calls a method of, reads a field of, references a method of or instantiates a type carrying the domain-service role. A class in the infrastructure layer - the composition root - may construct one (a constructor call or a constructor reference) to hand it to a use case; a call there is reported. Naming the type as a parameter, a field or a return type is not an access and is not reported. An empty selection passes.

## .NET reading

**Selection.** Every type under scan, with its runtime type in the loaded assemblies, outside the application layer that does not carry the domain-service role - the domain model, the adapters of both directions, the composition root (the infrastructure layer) and types outside every layer - with the types nested in it, compiler-generated state machines and closures included. A type nested in an application type or in a domain service counts as its outer type and is not selected.

**Check.** No method body calls a method or property of, constructs, or makes a delegate of a method of a type carrying the domain-service role. A type in the infrastructure layer - the composition root - may construct one to hand it to a use case; a call there is reported. Naming the type as a parameter, a field or a return type is not a use and is not reported; a public field of a service read directly is not seen. An empty selection passes.

## Rust reading

Unpublished (dca-rust); the suite implements it. **Held by** a lint or a test (source-test).

**Selection.** Every function body - free functions and the methods of impl blocks - in every crate except the application crates, the impls of a type that implements DomainService excluded. A domain service is a type that implements DomainService, as DCA-ADV-010 selects it: Rust marks no module, so a module of free functions is no domain service by this rule.

**Check.** No body names a type that implements DomainService as an expression (a struct literal, a unit value, an associated function), nor calls a method on a parameter, a local binding or a field of self whose type implements it, nor on one built in place. In an infrastructure or bootstrap crate - the composition root - a construction (a struct literal, a unit value, an associated function without a receiver that returns Self) passes; a call there is reported. A parameter or a field of that type alone is not reported; a call through a generic bound or a trait object is not seen.

## Implementation

The verbatim ArchUnit expression is in the evidence slice [Overview](/evidence/rule/advanced/dca-adv-021/overview.md); every helper it calls has a slice of its own, listed under *Evidence slices* below.

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `classes()`, `inApplication()`, `inInfrastructure()`, `layout()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)

## Evidence slices

- [Overview](/evidence/rule/advanced/dca-adv-021/overview.md)
- [`outermost`](/evidence/rule/advanced/dca-adv-021/outermost.md)
- [`failIfAny`](/evidence/rule/advanced/dca-adv-021/failifany.md)
- [C# expression](/evidence/rule/advanced/dca-adv-021/c-expression.md)
- [C# helper IntraClassCalls](/evidence/rule/advanced/dca-adv-021/c-helper-intraclasscalls.md)
