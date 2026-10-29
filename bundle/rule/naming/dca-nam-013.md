---
type: Rule
id: DCA-NAM-013
title: "Use cases, input ports and published operations must not be named after a field they write"
rule: "An operation speaks the domain, not data access. A name after the field it writes (setLimit, updateStatus) says how the data changes, not what the change means; the glossary's verb says that (raise a limit, grant an initial limit), and the caller learns which rules run."
constraint: "Use cases, input ports and published operations must not be named after a field they write."
selects: "Non-nested types in <module>.application.. of every module root that are assignable to the configured input-port role - interfaces and classes - and classes whose simple name ends with the configured use-case suffix; and the public methods of every non-nested type in the published api package of every module root (<module>.<api>..)."
checks: "No selected type name - with the use-case suffix or InputPort removed - and no selected method name starts with set or update followed by a capital (SetLimit, updateStatus). settle and updated are not matched. Whether the remaining verb is in the glossary is not checked. The events package is not selected. An empty selection passes."
enforced_by: "NamingRules#DCA-NAM-013"
status: enforced
maturity: experimental
rule_set: naming
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/NamingRules.java
tags: [naming, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/NamingRules.cs
---

# Use cases, input ports and published operations must not be named after a field they write

**Experimental.** This rule is binding only in a project that opted in to experimental rules - the architecture test calls `withExperimental()` (.NET: `WithExperimental()`) on its rule selection, or `dca-archunit.properties` sets `dca.rules.experimental = true`; without that opt-in the rule does not run and is information only, never a finding and never a reason to change code.

## Selection

Non-nested types in <module>.application.. of every module root that are assignable to the configured input-port role - interfaces and classes - and classes whose simple name ends with the configured use-case suffix; and the public methods of every non-nested type in the published api package of every module root (<module>.<api>..).

## Check

No selected type name - with the use-case suffix or InputPort removed - and no selected method name starts with set or update followed by a capital (SetLimit, updateStatus). settle and updated are not matched. Whether the remaining verb is in the glossary is not checked. The events package is not selected. An empty selection passes.

## .NET reading

**Selection.** Interfaces in <module>.Application of every module root assignable to IInputPort, concrete application operations selected by IInputPort assignability or the configured use-case suffix, and the public methods declared by types in <module>.Api and below of every module root. Type names are read without the interface's I prefix and the generic arity.

**Check.** No selected name starts with Set or Update followed by an upper-case letter. Property accessors and other compiler-named methods are not methods in this sense, and a name such as Settle or Updated passes. Whether another verb names a field is not checked. An empty selection passes.

## Implementation

```java
DcaRule.check(
        "DCA-NAM-013",
        "Use cases, input ports and published operations must not be named after a field they"
            + " write",
        "An operation speaks the domain, not data access. A name after the field it writes"
            + " (setLimit, updateStatus) says how the data changes, not what the change means;"
            + " the glossary's verb says that (raise a limit, grant an initial limit), and the"
            + " caller learns which rules run",
        arch -> {
          List<String> violations = new ArrayList<>();
          for (JavaClass type : operations(arch, layout)) {
            if (DATA_WRITE.matcher(operationName(type, layout)).matches()) {
              violations.add(
                  type.getName()
                      + " is named after a data write - name it after what the change means,"
                      + " with the glossary's verb");
            }
          }
          String[] published = publishedApiPatterns(arch);
          for (JavaClass type : arch.classes()) {
            if (type.isNestedClass()
                || !JavaClass.Predicates.resideInAnyPackage(published).test(type)) {
              continue;
            }
            for (JavaMethod method : type.getMethods()) {
              if (method.getModifiers().contains(JavaModifier.PUBLIC)
                  && !method.getModifiers().contains(JavaModifier.SYNTHETIC)
                  && !method.getModifiers().contains(JavaModifier.BRIDGE)
                  && DATA_WRITE.matcher(method.getName()).matches()) {
                violations.add(
                    method.getFullName()
                        + " of a published type is named after a data write - name it after"
                        + " what the change means, with the glossary's verb");
              }
            }
          }
          if (!violations.isEmpty()) {
            throw new dev.domaincentric.dca.archunit.DcaRuleViolation(
                "Use cases, input ports and published operations must not be named after a"
                    + " field they write",
                violations);
          }
        })
    .experimental()
    .selecting(
        "Non-nested types in <module>.application.. of every module root that are assignable"
            + " to the configured input-port role - interfaces and classes - and classes whose"
            + " simple name ends with the configured use-case suffix; and the public methods of"
            + " every non-nested type in the published api package of every module root"
            + " (<module>.<api>..).")
    .checking(
        "No selected type name - with the use-case suffix or InputPort removed - and no"
            + " selected method name starts with set or update followed by a capital"
            + " (SetLimit, updateStatus). settle and updated are not matched. Whether the"
            + " remaining verb is in the glossary is not checked. The events package is not"
            + " selected. An empty selection passes.",
        "name the operation after what the change means, with the glossary's verb")
```

## Helpers

### `operations`

```java
/** The input ports and use cases of every module, nested types left out. */
  private static List<JavaClass> operations(DcaArchitecture arch, DcaLayout layout) {
    List<JavaClass> operations = new ArrayList<>();
    for (JavaClass type : arch.classes()) {
      if (!type.isNestedClass()
          && !type.isAnonymousClass()
          && JavaClass.Predicates.resideInAnyPackage(arch.allApplicationPatterns()).test(type)
          && (type.isAssignableTo(layout.markers().inputPort())
              || (!type.isInterface() && type.getSimpleName().endsWith(layout.useCaseSuffix())))) {
        operations.add(type);
      }
    }
    return operations;
  }
```

### `operationName`

```java
/** The simple name without the use-case suffix, the input-port suffix or {@code InputPort}. */
  private static String operationName(JavaClass type, DcaLayout layout) {
    String name = type.getSimpleName();
    for (String suffix :
        List.of(layout.useCaseSuffix(), layout.inputPortSuffix(), "InputPort").stream()
            .distinct()
            .toList()) {
      if (name.endsWith(suffix) && name.length() > suffix.length()) {
        return name.substring(0, name.length() - suffix.length());
      }
    }
    return name;
  }
```

### `publishedApiPatterns`

```java
private static String[] publishedApiPatterns(DcaArchitecture arch) {
  return arch.moduleRoots().stream()
      .map(root -> root + "." + arch.layout().apiSubpackage() + "..")
      .toArray(String[]::new);
}
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allApplicationPatterns()`, `classes()`, `layout()`, `moduleRoots()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Check(
    "DCA-NAM-013",
    "Use cases, input ports and published operations must not be named after a field they write",
    "An operation speaks the domain, not data access. Neither a use case nor an operation of the"
        + " context's published API is named after a field it writes; it is named after what the"
        + " change means, with the verb from the glossary",
    arch =>
    {
        var violations = OperationNames(arch)
            .Where(o => FieldWriteVerb.IsMatch(o.Name))
            .Select(o => $"{o.Type} is named after a field it writes")
            .Concat(PublishedMethods(arch)
                .Where(m => FieldWriteVerb.IsMatch(m.Name))
                .Select(m => $"{m.DeclaringType!.FullName}.{m.Name} is a published operation named after a field it writes"))
            .Distinct()
            .OrderBy(v => v, StringComparer.Ordinal)
            .ToList();
        DcaRule.Fail(
            "Use cases, input ports and published operations must not be named after a field they write",
            violations,
            "name the operation after what the change means, with the verb from the glossary");
    })
    .Experimental()
    .Selecting(
        "Interfaces in <module>.Application of every module root assignable to IInputPort, concrete"
        + " application operations selected by IInputPort assignability or the configured use-case"
        + " suffix, and the public methods declared by types in <module>.Api and below of every module"
        + " root. Type names are read without the interface's I prefix and the generic arity.")
    .Checking(
        "No selected name starts with Set or Update followed by an upper-case letter. Property"
        + " accessors and other compiler-named methods are not methods in this sense, and a name"
        + " such as Settle or Updated passes. Whether another verb names a field is not checked. An"
        + " empty selection passes.")
```

## Related mentions (heuristic)

- [InputPort](/marker/port-in/inputport.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
