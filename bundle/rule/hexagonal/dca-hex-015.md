---
type: Rule
id: DCA-HEX-015
title: Incoming adapters must not keep state for a later request in one instance
rule: "State a later request needs travels with that request or lives in a store every instance reads. A server session or a message held for the next request is kept by one instance, and behind a load balancer without sticky sessions the next request reaches another one. A message for the page after a redirect is a fixed code in the redirect address, which the page maps to its text."
constraint: Incoming adapters must not keep state for a later request in one instance.
selects: "Classes in <module>.adapter.incoming.. of every module root."
checks: "No code unit calls an entry of the configured instance-local-state role: an entry naming a type matches a call of any method on a type assignable to it, an entry whose last segment starts in lower case (Type.method) a call of that method only. Holding such a type as a parameter or field without calling it is not reported, nor is state kept through an annotation. With an empty role nothing is reported."
enforced_by: "HexagonalRules#DCA-HEX-015"
status: enforced
maturity: experimental
rule_set: hexagonal
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/HexagonalRules.java
tags: [hexagonal, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/HexagonalRules.cs
---

# Incoming adapters must not keep state for a later request in one instance

**Experimental.** This rule is binding only in a project that opted in to experimental rules - the architecture test calls `withExperimental()` (.NET: `WithExperimental()`) on its rule selection, or `dca-archunit.properties` sets `dca.rules.experimental = true`; without that opt-in the rule does not run and is information only, never a finding and never a reason to change code.

## Selection

Classes in <module>.adapter.incoming.. of every module root.

## Check

No code unit calls an entry of the configured instance-local-state role: an entry naming a type matches a call of any method on a type assignable to it, an entry whose last segment starts in lower case (Type.method) a call of that method only. Holding such a type as a parameter or field without calling it is not reported, nor is state kept through an annotation. With an empty role nothing is reported.

## .NET reading

**Selection.** Classes in <module>.Adapter.Incoming of every module root, compiler-generated classes excluded, with their runtime type in the loaded assemblies.

**Check.** No type of the configured instance-local-state role appears as the declaring, parameter or return type of a method the class calls - async state machines and lambdas included - as the type of a field, property or method parameter or return it declares, or as an attribute on the class or its members. The role is empty in the None() preset, which then reports nothing; a project whose instances share that state empties it. Whether the state is read by a later request is not checked. An empty selection passes.

## Implementation

```java
DcaRule.of(
        "DCA-HEX-015",
        "Incoming adapters must not keep state for a later request in one instance",
        "State a later request needs travels with that request or lives in a store every"
            + " instance reads. A server session or a message held for the next request is kept"
            + " by one instance, and behind a load balancer without sticky sessions the next"
            + " request reaches another one. A message for the page after a redirect is a fixed"
            + " code in the redirect address, which the page maps to its text",
        arch ->
            classes()
                .that()
                .resideInAnyPackage(arch.allIncomingAdapterPatterns())
                .should(callNoInstanceLocalState(api))
                .allowEmptyShould(true))
    .experimental()
    .selecting("Classes in <module>.adapter.incoming.. of every module root.")
    .checking(
        "No code unit calls an entry of the configured instance-local-state role: an entry"
            + " naming a type matches a call of any method on a type assignable to it, an entry"
            + " whose last segment starts in lower case (Type.method) a call of that method"
            + " only. Holding such a type as a parameter or field without calling it is not"
            + " reported, nor is state kept through an annotation. With an empty role nothing is"
            + " reported.",
        "carry the state in the request - a fixed code in the redirect address - or keep it"
            + " in a store every instance reads")
```

## Helpers

### `callNoInstanceLocalState`

```java
private static ArchCondition<JavaClass> callNoInstanceLocalState(List<String> api) {
  return new ArchCondition<>("call no instance-local state API") {
    @Override
    public void check(JavaClass item, ConditionEvents events) {
      for (JavaCodeUnit unit : item.getCodeUnits()) {
        java.util.Set<String> used = new java.util.TreeSet<>();
        for (JavaMethodCall call : unit.getMethodCallsFromSelf()) {
          for (String entry : api) {
            if (matchesInstanceLocalState(call, entry)) {
              used.add(call.getTargetOwner().getSimpleName() + "." + call.getName());
            }
          }
        }
        if (!used.isEmpty()) {
          events.add(
              SimpleConditionEvent.violated(
                  item,
                  item.getName()
                      + "."
                      + unit.getName()
                      + " keeps request state in this instance through "
                      + String.join(", ", used)));
        }
      }
    }
  };
}
```

### `matchesInstanceLocalState`

```java
/**
   * {@code com.acme.Session} matches every call on a type assignable to it; {@code
   * com.acme.Redirect.keep} - the last segment in lower case - only calls of {@code keep}.
   */
  private static boolean matchesInstanceLocalState(JavaMethodCall call, String entry) {
    int dot = entry.lastIndexOf('.');
    String last = entry.substring(dot + 1);
    if (dot > 0 && !last.isEmpty() && Character.isLowerCase(last.charAt(0))) {
      return call.getName().equals(last)
          && call.getTargetOwner().isAssignableTo(entry.substring(0, dot));
    }
    return call.getTargetOwner().isAssignableTo(entry);
  }
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allIncomingAdapterPatterns()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Check(
        "DCA-HEX-015",
        "Incoming adapters must not keep state for a later request in one instance",
        "State a later request needs travels with that request or lives in a store every instance"
            + " reads. A server session or a message held for the page after a redirect is kept by one"
            + " instance, and behind a load balancer without sticky sessions the next request reaches"
            + " another one",
        arch =>
        {
            var roles = arch.Layout.FrameworkTypes.InstanceLocalStateTypes;
            var violations = new List<string>();
            if (roles.Count > 0)
            {
                var incoming = DcaLayout.AnyOf(arch.AllIncomingAdapterPatterns());
                foreach (var adapter in arch.Classes.Where(c => !c.IsCompilerGenerated && InNamespace(c, incoming)).OrderBy(c => c.FullName, StringComparer.Ordinal))
                {
                    var runtime = arch.RuntimeType(adapter);
                    if (runtime is null)
                    {
                        continue;
                    }

                    foreach (var used in InstanceLocalStateUsedBy(runtime, roles))
                    {
                        violations.Add($"{adapter.FullName} uses the instance-local state API {used}");
                    }
                }
            }

            DcaRule.Fail(
                "Incoming adapters must not keep state for a later request in one instance",
                violations.Distinct().ToList(),
                "carry the state in the request - a fixed code in the redirect URL for a message - or keep it in a store every instance reads");
        })
    .Experimental()
    .Selecting(
        "Classes in <module>.Adapter.Incoming of every module root, compiler-generated classes"
            + " excluded, with their runtime type in the loaded assemblies.")
    .Checking(
        "No type of the configured instance-local-state role appears as the declaring, parameter or"
            + " return type of a method the class calls - async state machines and lambdas included - as"
            + " the type of a field, property or method parameter or return it declares, or as an"
            + " attribute on the class or its members. The role is empty in the None() preset, which then reports nothing; a project"
            + " whose instances share that state empties it. Whether the state is read by a later"
            + " request is not checked. An empty selection passes.")
```

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
