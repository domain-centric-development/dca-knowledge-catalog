---
type: Rule
id: DCA-CYC-005
title: Feature and use case packages within a module's application layer must not have cyclic dependencies
rule: "The packages directly below a module's application package are its features (application.<feature>.<usecase>) or, in a flat layout, its use cases (application.<usecase>). A feature is an optional, domain-named group of related use cases; it may depend on another feature in one direction, but a cycle between two of them means the grouping does not carry its weight - the shared concept belongs in application.shared, in the domain, or in one of the two. application.shared is the context-wide port package and is not a slice. The rule does not infer bounded contexts or aggregate ownership from the packages it slices."
constraint: Feature and use case packages within a module's application layer must not have cyclic dependencies.
selects: "One slice per operation-root package (marker or suffix), with configured containers stripped; supporting subfolders join the nearest operation root. Classes directly in an enclosing feature package form its feature slice. Shared and direct application classes are ignored."
checks: "The slices form no dependency cycle: two features or two use cases that depend on each other, directly or through further slices, are reported. Dependencies on application.shared, the domain or an adapter do not count. Slices of all modules are checked together, so a cycle through another module's use case package is reported here as well."
enforced_by: "CycleRules#DCA-CYC-005"
status: enforced
rule_set: cycles
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/CycleRules.java
tags: [cycles, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/CycleRules.cs
---

# Feature and use case packages within a module's application layer must not have cyclic dependencies

## Selection

One slice per operation-root package (marker or suffix), with configured containers stripped; supporting subfolders join the nearest operation root. Classes directly in an enclosing feature package form its feature slice. Shared and direct application classes are ignored.

## Check

The slices form no dependency cycle: two features or two use cases that depend on each other, directly or through further slices, are reported. Dependencies on application.shared, the domain or an adapter do not count. Slices of all modules are checked together, so a cycle through another module's use case package is reported here as well.

## .NET reading

**Selection.** One slice per operation-root namespace selected by marker or suffix, configured containers stripped; supporting sub-namespaces join their nearest operation root. Classes directly in a feature namespace form its feature slice. Shared and direct application types are ignored.

**Check.** The slices form no dependency cycle: two features or two use cases that depend on each other, directly or through further slices, are reported. Dependencies on Application.Shared, the domain or an adapter do not count. Slices of all modules are checked together, so a cycle through another module's use-case namespace is reported here as well.

## Implementation

```java
DcaRule.of(
        "DCA-CYC-005",
        "Feature and use case packages within a module's application layer must not have cyclic"
            + " dependencies",
        "The packages directly below a module's application package are its features"
            + " (application.<feature>.<usecase>) or, in a flat layout, its use cases"
            + " (application.<usecase>). A feature is an optional, domain-named group of related"
            + " use cases; it may depend on another feature in one direction, but a cycle between"
            + " two of them means the grouping does not carry its weight - the shared concept"
            + " belongs in application.shared, in the domain, or in one of the two. application.shared"
            + " is the context-wide port package and is not a slice. The rule does not infer bounded"
            + " contexts or aggregate ownership from the packages it slices",
        arch ->
            slices()
                .assignedFrom(applicationChildSlices(arch, layout))
                .should()
                .beFreeOfCycles()
                .allowEmptyShould(true))
    .selecting(
        "One slice per operation-root package (marker or suffix), with configured containers stripped; supporting subfolders join the nearest operation root. Classes directly in an enclosing feature package form its feature slice. Shared and direct application classes are ignored.")
    .checking(
        "The slices form no dependency cycle: two features or two use cases that depend on"
            + " each other, directly or through further slices, are reported. Dependencies on"
            + " application.shared, the domain or an adapter do not count. Slices of all"
            + " modules are checked together, so a cycle through another module's use case"
            + " package is"
            + " reported here as well.")
```

## Helpers

### `applicationChildSlices`

```java
/**
   * One slice per immediate child package of a module's application package — the module root comes
   * from {@link DcaArchitecture#moduleRootOf(String)}, so the slicing holds at any depth and never
   * assumes a module is a direct child of the base package. Classes directly in the application
   * package and everything below {@code application.shared} are ignored.
   */
  private static SliceAssignment applicationChildSlices(DcaArchitecture arch, DcaLayout layout) {
    return new SliceAssignment() {

      @Override
      public SliceIdentifier getIdentifierOf(JavaClass javaClass) {
        String root = arch.moduleRootOf(javaClass.getPackageName());
        if (root == null) {
          return SliceIdentifier.ignore();
        }
        String application = root + "." + layout.applicationSubpackage();
        String pkg = javaClass.getPackageName();
        if (!pkg.startsWith(application + ".")) {
          return SliceIdentifier.ignore();
        }
        String relative = pkg.substring(application.length() + 1);
        String[] segments = relative.split("\\.");
        int index = 0;
        while (index < segments.length && layout.operationContainers().contains(segments[index]))
          index++;
        if (index == segments.length || segments[index].equals("shared"))
          return SliceIdentifier.ignore();
        String operationRoot =
            arch.classes().stream()
                .filter(c -> OperationPolicy.operation(c, arch))
                .map(JavaClass::getPackageName)
                .filter(
                    p ->
                        p.startsWith(application + ".")
                            && (pkg.equals(p) || pkg.startsWith(p + ".")))
                .max(java.util.Comparator.comparingInt(String::length))
                .orElse(null);
        String physicalFeature =
            application
                + "."
                + String.join(".", java.util.Arrays.copyOfRange(segments, 0, index + 1));
        if (operationRoot == null) {
          boolean feature =
              arch.classes().stream()
                  .anyMatch(
                      c ->
                          OperationPolicy.operation(c, arch)
                              && c.getPackageName().startsWith(physicalFeature + "."));
          if (!feature) return SliceIdentifier.ignore();
          operationRoot = physicalFeature;
        }
        String logical =
            java.util.Arrays.stream(operationRoot.substring(application.length() + 1).split("\\."))
                .filter(segment -> !layout.operationContainers().contains(segment))
                .collect(java.util.stream.Collectors.joining("."));
        return SliceIdentifier.of(application + "." + logical);
      }

      @Override
      public String getDescription() {
        return "feature or use case packages";
      }
    };
  }
```

### `OperationPolicy.operation`

```java
static boolean operation(JavaClass type, DcaArchitecture arch) {
  return !type.isInterface()
      && !type.isNestedClass()
      && !type.getModifiers().contains(JavaModifier.ABSTRACT)
      && JavaClass.Predicates.resideInAnyPackage(arch.allApplicationPatterns()).test(type)
      && (type.isAssignableTo(InputPort.class)
          || type.getSimpleName().endsWith(arch.layout().useCaseSuffix()));
}
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allApplicationPatterns()`, `classes()`, `layout()`, `moduleRootOf()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Check(
    "DCA-CYC-005",
    "Feature and use case namespaces within a module's application layer must not have cyclic dependencies",
    "The namespaces directly below a module's application namespace are its features"
        + " (Application.<Feature>.<UseCase>) or, in a flat layout, its use cases (Application.<UseCase>). A"
        + " feature is an optional, domain-named group of related use cases; it may depend on another feature"
        + " in one direction, but a cycle between two of them means the grouping does not carry its weight -"
        + " the shared concept belongs in Application.Shared, in the domain, or in one of the two."
        + " Application.Shared is the context-wide port namespace and is not a slice. The rule does not infer"
        + " bounded contexts or aggregate ownership from the namespaces it slices",
    arch => CheckSlices(
        arch,
        ns => ApplicationChildSlice(arch, layout, ns),
        "Feature and use case namespaces within a module's application layer must not have cyclic dependencies"))
    .Selecting(
        "One slice per operation-root namespace selected by marker or suffix, configured containers stripped; supporting sub-namespaces join their nearest operation root. Classes directly in a feature namespace form its feature slice. Shared and direct application types are ignored.")
    .Checking(
        "The slices form no dependency cycle: two features or two use cases that depend on each "
        + "other, directly or through further slices, are reported. Dependencies on "
        + "Application.Shared, the domain or an adapter do not count. Slices of all modules are "
        + "checked together, so a cycle through another module's use-case namespace is reported "
        + "here as well.")
```

## Related mentions (heuristic)

- [InputPort](/marker/port-in/inputport.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
