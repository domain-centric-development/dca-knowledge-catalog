---
type: Rule
id: DCA-USE-022
title: Use case results must not be bare primitives or strings
rule: "A use case answers in the application's language: a result type of its own, a value, or a case of a closed result. A bare number, text or flag carries no meaning of its own - an exit code, a status word or a count whose meaning lives in the caller - and it cannot gain a case without changing every caller."
constraint: Use case results must not be bare primitives or strings.
selects: "Interfaces and classes under scan that implement or extend the input-port role's generic contract UseCase<INPUT, OUTPUT> - the type the useCase role names - with its output type argument resolved through the interfaces and superclasses in between. A type that only inherits a binding made by one of its supertypes is reported at that supertype, not again."
checks: "The output type argument is none of String, Boolean, Byte, Short, Integer, Long, Float, Double or Character. Void passes - a command with nothing to answer; an unresolved type argument passes; a container such as List<String> is no bare primitive and passes. An empty selection passes."
enforced_by: "UseCaseRules#DCA-USE-022"
status: enforced
maturity: experimental
rule_set: usecase
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/UseCaseRules.java
tags: [usecase, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/UseCaseRules.cs
---

# Use case results must not be bare primitives or strings

**Experimental.** This rule is binding only in a project that opted in to experimental rules - the architecture test calls `withExperimental()` (.NET: `WithExperimental()`) on its rule selection, or `dca-archunit.properties` sets `dca.rules.experimental = true`; without that opt-in the rule does not run and is information only, never a finding and never a reason to change code.

## Selection

Interfaces and classes under scan that implement or extend the input-port role's generic contract UseCase<INPUT, OUTPUT> - the type the useCase role names - with its output type argument resolved through the interfaces and superclasses in between. A type that only inherits a binding made by one of its supertypes is reported at that supertype, not again.

## Check

The output type argument is none of String, Boolean, Byte, Short, Integer, Long, Float, Double or Character. Void passes - a command with nothing to answer; an unresolved type argument passes; a container such as List<String> is no bare primitive and passes. An empty selection passes.

## .NET reading

**Selection.** Types under scan, interfaces included, with their runtime type in the loaded assemblies that declare the generic use-case contract - the configured UseCase role, by default IUseCase<TInput, TOutput> - closed over its output argument: the input port that names the contract, or the class that implements it directly. A class that receives the contract through its input-port interface counts as that interface, so one contract is reported once; an open generic argument is not selected.

**Check.** The output type argument is none of string, bool, byte, sbyte, short, ushort, int, uint, long, ulong, float, double, decimal or char, nor a Nullable of one. A container of them, such as IReadOnlyList<string>, and the project's own types pass. An empty selection passes.

## Rust reading

Unpublished (dca-rust); planned, not yet implemented. **Held by** a lint or a test (source-test).

**Selection.** impl UseCase<I, O> blocks and the traits that extend UseCase<I, O>.

**Check.** O, or the success type of a Result it names, is none of String, &str, bool, char or a numeric primitive. () passes - a command with nothing to answer -, and so does a container such as Vec<String>. Planned: the suite does not implement it yet.

## Implementation

```java
DcaRule.check(
        "DCA-USE-022",
        "Use case results must not be bare primitives or strings",
        "A use case answers in the application's language: a result type of its own, a"
            + " value, or a case of a closed result. A bare number, text or flag carries no"
            + " meaning of its own - an exit code, a status word or a count whose meaning lives"
            + " in the caller - and it cannot gain a case without changing every caller",
        arch -> {
          String contract = arch.layout().markers().useCase();
          List<String> violations = new ArrayList<>();
          for (JavaClass type : arch.classes()) {
            if (type.getName().equals(contract) || !type.isAssignableTo(contract)) {
              continue;
            }
            String bare = bareOutput(type, contract);
            if (bare == null || inheritsBareOutput(type, contract)) {
              continue;
            }
            violations.add(
                type.getName()
                    + " answers with a bare "
                    + bare.substring(bare.lastIndexOf('.') + 1)
                    + " as the output of "
                    + contract.substring(contract.lastIndexOf('.') + 1));
          }
          if (!violations.isEmpty()) {
            throw new DcaRuleViolation(
                "Use case results must not be bare primitives or strings. Fix: answer with a"
                    + " result type of its own, a value object, or a closed result whose cases"
                    + " name the outcomes.",
                violations.stream().sorted().toList());
          }
        })
    .experimental()
    .selecting(
        "Interfaces and classes under scan that implement or extend the input-port role's"
            + " generic contract UseCase<INPUT, OUTPUT> - the type the useCase role names -"
            + " with its output type argument resolved through the interfaces and superclasses"
            + " in between. A type that only inherits a binding made by one of its supertypes is"
            + " reported at that supertype, not again.")
    .checking(
        "The output type argument is none of String, Boolean, Byte, Short, Integer, Long,"
            + " Float, Double or Character. Void passes - a command with nothing to answer; an"
            + " unresolved type argument passes; a container such as List<String> is no bare"
            + " primitive and passes. An empty selection passes.",
        "answer with a result type of its own, a value object, or a closed result whose cases"
            + " name the outcomes")
```

## Helpers

### `bareOutput`

```java
/** The bare output a type binds on the contract, by class name, or {@code null}. */
  private static String bareOutput(JavaClass type, String contract) {
    java.util.Optional<com.tngtech.archunit.core.domain.JavaType> output =
        TypeInspection.typeArgument(type, contract, 1);
    if (output.isEmpty()
        || !(output.get() instanceof JavaClass resolved)
        || !BARE_RESULTS.contains(resolved.getName())) {
      return null;
    }
    return resolved.getName();
  }
```

### `inheritsBareOutput`

```java
/** Whether a direct supertype already binds the bare output this type inherits. */
  private static boolean inheritsBareOutput(JavaClass type, String contract) {
    List<JavaClass> supertypes = new ArrayList<>(type.getRawInterfaces());
    type.getRawSuperclass().ifPresent(supertypes::add);
    return supertypes.stream()
        .filter(supertype -> !supertype.getName().equals(contract))
        .filter(supertype -> supertype.isAssignableTo(contract))
        .anyMatch(supertype -> bareOutput(supertype, contract) != null);
  }
```

### `TypeInspection.typeArgument`

```java
/**
   * The type argument at {@code index} that a type binds on the given marker, through its
   * interfaces, the interfaces they extend and its superclasses; a type variable of an intermediate
   * type is substituted by the argument the type binds for it. Empty where the marker is used raw
   * or not at all.
   */
  static Optional<JavaType> typeArgument(JavaClass type, String markerName, int index) {
    List<JavaType> candidates = new ArrayList<>(type.getInterfaces());
    type.getSuperclass().ifPresent(candidates::add);
    for (JavaType candidate : candidates) {
      JavaClass erasure = candidate.toErasure();
      if (erasure.getName().equals(markerName)) {
        if (candidate instanceof JavaParameterizedType parameterized
            && parameterized.getActualTypeArguments().size() > index) {
          return Optional.of(parameterized.getActualTypeArguments().get(index));
        }
        return Optional.empty();
      }
      if (!erasure.isAssignableTo(markerName)) {
        continue;
      }
      Optional<JavaType> inherited = typeArgument(erasure, markerName, index);
      if (inherited.isPresent()
          && inherited.get() instanceof JavaTypeVariable<?> variable
          && candidate instanceof JavaParameterizedType parameterized) {
        List<? extends JavaTypeVariable<?>> parameters = erasure.getTypeParameters();
        for (int i = 0; i < parameters.size(); i++) {
          if (parameters.get(i).getName().equals(variable.getName())
              && parameterized.getActualTypeArguments().size() > i) {
            return Optional.of(parameterized.getActualTypeArguments().get(i));
          }
        }
      }
      if (inherited.isPresent()) {
        return inherited;
      }
    }
    return Optional.empty();
  }
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `classes()`, `layout()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Check(
        "DCA-USE-022",
        "Use case results must not be bare primitives or strings",
        "A use case answers in the application's language: a result type of its own, a value, or a case of a"
            + " closed result. A bare number, text or flag carries no meaning of its own - an exit code, a status"
            + " word or a count whose meaning lives in the caller - and it cannot gain a case without changing every"
            + " caller",
        arch =>
        {
            var markers = arch.Layout.Markers;
            var violations = new List<string>();
            foreach (var type in arch.Types.Where(t => !t.IsCompilerGenerated).OrderBy(t => t.FullName, StringComparer.Ordinal))
            {
                var runtime = arch.RuntimeType(type);
                if (runtime is null)
                {
                    continue;
                }

                foreach (var contract in DeclaredUseCaseContracts(runtime, markers))
                {
                    var output = contract.GetGenericArguments()[^1];
                    var bare = Nullable.GetUnderlyingType(output) ?? output;
                    if (BareResultTypes.Contains(bare))
                    {
                        violations.Add($"{type.FullName} answers {contract.Name.Split('`')[0]}<..., {Display(output)}> - a bare {Display(output)}");
                    }
                }
            }

            DcaRule.Fail(
                "Use case results must not be bare primitives or strings",
                violations.Distinct().ToList(),
                "answer with a result type of its own, a value object, or a closed result whose cases name the outcomes");
        })
    .Experimental()
    .Selecting(
        "Types under scan, interfaces included, with their runtime type in the loaded assemblies that declare the"
            + " generic use-case contract - the configured UseCase role, by default IUseCase<TInput, TOutput> -"
            + " closed over its output argument: the input port that names the contract, or the class that"
            + " implements it directly. A class that receives the contract through its input-port interface counts"
            + " as that interface, so one contract is reported once; an open generic argument is not selected.")
    .Checking(
        "The output type argument is none of string, bool, byte, sbyte, short, ushort, int, uint, long, ulong,"
            + " float, double, decimal or char, nor a Nullable of one. A container of them, such as"
            + " IReadOnlyList<string>, and the project's own types pass. An empty selection passes.")
```

## Related mentions (heuristic)

- [UseCase<INPUT, OUTPUT>](/marker/port-in/usecase.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
