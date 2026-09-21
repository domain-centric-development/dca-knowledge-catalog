---
type: Rule
id: DCA-USE-014
title: "Use case packages within a module must use one consistent depth (flat or grouped by feature)"
rule: "A use case package sits either directly below the application package (application.<usecase>) or one level deeper inside a feature (application.<feature>.<usecase>). A feature is an optional, domain-named group of related use cases - a navigation boundary inside one bounded context, not a layer, module or aggregate owner. Mixing both forms in one module makes it unclear whether a package is a feature, a use case or a leftover; nesting deeper than a feature hides the use case. The rule checks legibility only: it does not infer bounded contexts, feature semantics or aggregate ownership. application.shared holds the context-wide output ports and is not a use case package."
constraint: "Use case packages within a module must use one consistent depth (flat or grouped by feature)."
selects: "Per module root: non-interface, non-abstract, non-nested classes below <module>.application that implement InputPort or whose simple name ends with the configured use-case suffix, excluding application.shared and everything below it."
checks: "After removing configured operationContainers segments, all of them sit at one depth: application.<usecase> (flat) or application.<feature>.<usecase> (grouped). Reported are a use case directly in the application package, one nested deeper than a feature, and a module mixing both depths. What a feature means is not checked."
enforced_by: "UseCaseRules#DCA-USE-014"
status: enforced
rule_set: usecase
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/UseCaseRules.java
tags: [usecase, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/UseCaseRules.cs
---

# Use case packages within a module must use one consistent depth (flat or grouped by feature)

## Selection

Per module root: non-interface, non-abstract, non-nested classes below <module>.application that implement InputPort or whose simple name ends with the configured use-case suffix, excluding application.shared and everything below it.

## Check

After removing configured operationContainers segments, all of them sit at one depth: application.<usecase> (flat) or application.<feature>.<usecase> (grouped). Reported are a use case directly in the application package, one nested deeper than a feature, and a module mixing both depths. What a feature means is not checked.

## .NET reading

**Selection.** Per module root: non-abstract, non-nested classes below <module>.Application that implement IInputPort or whose name ends with the configured use-case suffix, excluding Application.Shared and everything below it.

**Check.** After removing configured OperationContainers segments, all of them sit at one depth: Application.<UseCase> (flat) or Application.<Feature>.<UseCase> (grouped). Reported are a use case directly in the application namespace, one nested deeper than a feature, and a module mixing both depths. What a feature means is not checked.

## Implementation

```java
DcaRule.check(
        "DCA-USE-014",
        "Use case packages within a module must use one consistent depth (flat or grouped by"
            + " feature)",
        "A use case package sits either directly below the application package"
            + " (application.<usecase>) or one level deeper inside a feature"
            + " (application.<feature>.<usecase>). A feature is an optional, domain-named group of"
            + " related use cases - a navigation boundary inside one bounded context, not a layer,"
            + " module or aggregate owner. Mixing both forms in one module makes it unclear whether"
            + " a package is a feature, a use case or a leftover; nesting deeper than a feature hides"
            + " the use case. The rule checks legibility only: it does not infer bounded contexts,"
            + " feature semantics or aggregate ownership. application.shared holds the context-wide"
            + " output ports and is not a use case package",
        arch -> checkUseCaseDepth(arch, layout))
    .selecting(
        "Per module root: non-interface, non-abstract, non-nested classes below <module>.application that implement InputPort or whose simple name ends with the configured use-case suffix, excluding application.shared and everything below it.")
    .checking(
        "After removing configured operationContainers segments, all of them sit at one depth: application.<usecase> (flat) or application.<feature>.<usecase> (grouped). Reported are a use case directly in the application package, one nested deeper than a feature, and a module mixing both depths. What a feature means is not checked.",
        "keep every use case of the module at application.<usecase>, one package per use case")
```

## Helpers

### `checkUseCaseDepth`

```java
private static void checkUseCaseDepth(DcaArchitecture arch, DcaLayout layout) {
  List<String> violations = new ArrayList<>();
  for (String root : arch.moduleRoots()) {
    String application = root + "." + layout.applicationSubpackage();
    String shared = application + "." + layout.sharedSubpackage();
    // depth -> use case packages at that depth, both sorted for a stable message
    Map<Integer, TreeSet<String>> byDepth = new TreeMap<>();
    for (JavaClass candidate : arch.classes()) {
      String pkg = candidate.getPackageName();
      if (!(pkg.equals(application) || pkg.startsWith(application + "."))
          || pkg.equals(shared)
          || pkg.startsWith(shared + ".")
          || candidate.isInterface()
          || candidate.getModifiers().contains(JavaModifier.ABSTRACT)
          || candidate.isNestedClass()
          || candidate.isAnonymousClass()
          || !(candidate.isAssignableTo(arch.layout().markers().inputPort())
              || candidate.getSimpleName().endsWith(layout.useCaseSuffix()))) {
        continue;
      }
      int depth =
          pkg.equals(application)
              ? 0
              : (int)
                  java.util.Arrays.stream(pkg.substring(application.length() + 1).split("\\."))
                      .filter(segment -> !layout.operationContainers().contains(segment))
                      .count();
      byDepth.computeIfAbsent(depth, d -> new TreeSet<>()).add(pkg);
    }
    if (byDepth.isEmpty()) {
      continue;
    }
    byDepth
        .getOrDefault(0, new TreeSet<>())
        .forEach(
            pkg ->
                violations.add(
                    "Module "
                        + root
                        + ": use case directly in the application package "
                        + pkg
                        + " - give it a package of its own (application.<usecase>)"));
    byDepth.forEach(
        (depth, pkgs) -> {
          if (depth > 2) {
            pkgs.forEach(
                pkg ->
                    violations.add(
                        "Module "
                            + root
                            + ": use case package "
                            + pkg
                            + " is nested deeper than application.<feature>.<usecase>"));
          }
        });
    if (byDepth.containsKey(1) && byDepth.containsKey(2)) {
      violations.add(
          "Module "
              + root
              + " mixes flat use case packages "
              + byDepth.get(1)
              + " with feature-grouped ones "
              + byDepth.get(2)
              + " - finish the migration in one direction");
    }
  }
  if (!violations.isEmpty()) {
    throw new DcaRuleViolation(
        "Use case packages within a module must use one consistent depth (flat or grouped by"
            + " feature)",
        violations);
  }
}
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `classes()`, `layout()`, `moduleRoots()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Check(
        "DCA-USE-014",
        "Use case namespaces within a module must use one consistent depth (flat or grouped by feature)",
        "A use case namespace sits either directly below the application namespace (Application.<UseCase>) or"
            + " one level deeper inside a feature (Application.<Feature>.<UseCase>). A feature is an optional,"
            + " domain-named group of related use cases - a navigation boundary inside one bounded context, not"
            + " a layer, module or aggregate owner. Mixing both forms in one module makes it unclear whether a"
            + " namespace is a feature, a use case or a leftover; nesting deeper than a feature hides the use"
            + " case. The rule checks legibility only: it does not infer bounded contexts, feature semantics or"
            + " aggregate ownership. Application.Shared holds the context-wide output ports and is not a use"
            + " case namespace",
        arch => CheckUseCaseDepth(arch, layout))
    .Selecting(
        "Per module root: non-abstract, non-nested classes below <module>.Application"
            + " that implement IInputPort or whose name ends with the configured use-case suffix, excluding Application.Shared"
            + " and everything below it.")
    .Checking(
        "After removing configured OperationContainers segments, all of them sit at one depth: Application.<UseCase> (flat) or"
            + " Application.<Feature>.<UseCase> (grouped). Reported are a use case directly in the"
            + " application namespace, one nested deeper than a feature, and a module mixing both"
            + " depths. What a feature means is not checked.")
```

## Related mentions (heuristic)

- [InputPort](/marker/port-in/inputport.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
