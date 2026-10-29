---
type: Rule
id: DCA-HEX-018
title: Controllers must reside in an incoming adapter package
rule: "A controller turns a request into a command or a query and is an incoming adapter. Outside the incoming adapter packages it is outside the selection of every rule written for incoming adapters - the GET-handler rule, the controller naming rules, the boundary rules - and passes them all."
constraint: Controllers must reside in an incoming adapter package.
selects: "Non-interface classes anywhere on the classpath under scan that are directly annotated with one of the configured web-controller or REST-controller stereotypes. An interface carrying the same annotation - a declarative REST client in an outgoing adapter - is not selected, and a class is not selected for its name. With empty web-controller and REST-controller roles nothing is selected and the rule passes."
checks: "Each resides in <module>.adapter.incoming.. of some module root. Where in the incoming adapters it sits - which protocol segment - is not checked."
enforced_by: "HexagonalRules#DCA-HEX-018"
status: enforced
maturity: experimental
rule_set: hexagonal
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/HexagonalRules.java
tags: [hexagonal, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/HexagonalRules.cs
---

# Controllers must reside in an incoming adapter package

**Experimental.** This rule is binding only in a project that opted in to experimental rules - the architecture test calls `withExperimental()` (.NET: `WithExperimental()`) on its rule selection, or `dca-archunit.properties` sets `dca.rules.experimental = true`; without that opt-in the rule does not run and is information only, never a finding and never a reason to change code.

## Selection

Non-interface classes anywhere on the classpath under scan that are directly annotated with one of the configured web-controller or REST-controller stereotypes. An interface carrying the same annotation - a declarative REST client in an outgoing adapter - is not selected, and a class is not selected for its name. With empty web-controller and REST-controller roles nothing is selected and the rule passes.

## Check

Each resides in <module>.adapter.incoming.. of some module root. Where in the incoming adapters it sits - which protocol segment - is not checked.

## .NET reading

**Selection.** Non-abstract classes of the scan that derive from the configured controller or page-model base or carry the configured API-controller attribute. A class is not selected for its name. In the None() preset every role is empty and nothing is selected.

**Check.** Each resides in <Module>.Adapter.Incoming of some module root. Where in the incoming adapters it sits - which protocol segment - is not checked.

## Implementation

```java
DcaRule.of(
        "DCA-HEX-018",
        "Controllers must reside in an incoming adapter package",
        "A controller turns a request into a command or a query and is an incoming adapter."
            + " Outside the incoming adapter packages it is outside the selection of every rule"
            + " written for incoming adapters - the GET-handler rule, the controller naming"
            + " rules, the boundary rules - and passes them all",
        arch ->
            classes()
                .that()
                .areNotInterfaces()
                .and(AnnotationRoles.annotatedWithAny(webControllers, restControllers))
                .should()
                .resideInAnyPackage(arch.allIncomingAdapterPatterns())
                .allowEmptyShould(true))
    .experimental()
    .selecting(
        "Non-interface classes anywhere on the classpath under scan that are directly annotated"
            + " with one of the configured web-controller or REST-controller stereotypes. An"
            + " interface carrying the same annotation - a declarative REST client in an outgoing"
            + " adapter - is not selected, and a class is not selected for its name. With empty web-controller and REST-controller roles"
            + " nothing is selected and the rule passes.")
    .checking(
        "Each resides in <module>.adapter.incoming.. of some module root. Where in the incoming"
            + " adapters it sits - which protocol segment - is not checked.",
        "move the controller into the incoming adapter package of its module")
```

## Helpers

### `AnnotationRoles.annotatedWithAny`

```java
/** Directly annotated with any annotation of the role; never true for an empty role. */
  static DescribedPredicate<CanBeAnnotated> annotatedWithAny(List<String> role) {
    if (role.isEmpty()) {
      return DescribedPredicate.<CanBeAnnotated>alwaysFalse()
          .as("annotated with a configured annotation (none configured)");
    }
    DescribedPredicate<CanBeAnnotated> predicate =
        CanBeAnnotated.Predicates.annotatedWith(role.get(0));
    for (String fqn : role.subList(1, role.size())) {
      predicate = predicate.or(CanBeAnnotated.Predicates.annotatedWith(fqn));
    }
    return predicate.as("annotated with any of " + role);
  }

static DescribedPredicate<CanBeAnnotated> annotatedWithAny(List<String>... roles) {
  DescribedPredicate<CanBeAnnotated> predicate = null;
  for (List<String> role : roles) {
    if (role.isEmpty()) {
      continue;
    }
    predicate = predicate == null ? annotatedWithAny(role) : predicate.or(annotatedWithAny(role));
  }
  return predicate == null
      ? DescribedPredicate.<CanBeAnnotated>alwaysFalse()
          .as("annotated with a configured annotation (none configured)")
      : predicate;
}
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allIncomingAdapterPatterns()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Check(
        "DCA-HEX-018",
        "Controllers must reside in an incoming adapter package",
        "A controller turns a request into a command or a query and is an incoming adapter. Outside the incoming"
            + " adapter packages it is outside the selection of every rule written for incoming adapters - the"
            + " GET-handler rule, the controller naming rules, the boundary rules - and passes them all",
        arch =>
        {
            var roles = arch.Layout.FrameworkTypes;
            var incoming = new Regex(DcaLayout.AnyOf(arch.AllIncomingAdapterPatterns()));
            var violations = arch.Classes
                .Where(c => !c.IsCompilerGenerated && c.IsAbstract != true
                    && ((FrameworkTypes.IsSet(roles.ControllerBase) && c.IsAssignableTo(roles.ControllerBase))
                        || (FrameworkTypes.IsSet(roles.PageModelBase) && c.IsAssignableTo(roles.PageModelBase))
                        || (FrameworkTypes.IsSet(roles.ApiControllerAttribute) && c.Attributes.Any(a => a.FullName == roles.ApiControllerAttribute))))
                .Where(c => !incoming.IsMatch(c.Namespace?.FullName ?? ""))
                .Select(c => $"{c.FullName} is a controller outside the incoming adapters")
                .OrderBy(v => v, StringComparer.Ordinal)
                .ToList();
            DcaRule.Fail(
                "Controllers must reside in an incoming adapter package",
                violations,
                "move the controller into the incoming adapter namespace of its module");
        })
    .Experimental()
    .Selecting(
        "Non-abstract classes of the scan that derive from the configured controller or page-model base or carry"
            + " the configured API-controller attribute. A class is not selected for its name. In the None() preset"
            + " every role is empty and nothing is selected.")
    .Checking(
        "Each resides in <Module>.Adapter.Incoming of some module root. Where in the incoming adapters it sits -"
            + " which protocol segment - is not checked.")
```

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
