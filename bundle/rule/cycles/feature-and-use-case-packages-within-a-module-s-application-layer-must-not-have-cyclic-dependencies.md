---
type: Rule
id: DCA-CYC-005
title: Feature and use case packages within a module's application layer must not have cyclic dependencies
rule: "The packages directly below a module's application package are its features (application.<feature>.<usecase>) or, in a flat layout, its use cases (application.<usecase>). A feature is an optional, domain-named group of related use cases; it may depend on another feature in one direction, but a cycle between two of them means the grouping does not carry its weight - the shared concept belongs in application.shared, in the domain, or in one of the two. application.shared is the context-wide port package and is not a slice. The rule does not infer bounded contexts or aggregate ownership from the packages it slices."
constraint: Feature and use case packages within a module's application layer must not have cyclic dependencies.
selects: "One slice per immediate child package of <module>.application, for every module root: a feature in a grouped layout, a use case in a flat one, each with everything below it. Classes directly in the application package and everything below application.shared are ignored."
checks: "The slices form no dependency cycle: two features or two use cases that depend on each other, directly or through further slices, are reported. Dependencies on application.shared, the domain or an adapter do not count. Slices of all modules are checked together, so a cycle through another module's use case package is reported here as well."
enforced_by: "CycleRules#DCA-CYC-005"
status: enforced
rule_set: cycles
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/CycleRules.java
tags: [cycles, archunit]
---

## Selection

One slice per immediate child package of <module>.application, for every module root: a feature in a grouped layout, a use case in a flat one, each with everything below it. Classes directly in the application package and everything below application.shared are ignored.

## Check

The slices form no dependency cycle: two features or two use cases that depend on each other, directly or through further slices, are reported. Dependencies on application.shared, the domain or an adapter do not count. Slices of all modules are checked together, so a cycle through another module's use case package is reported here as well.

## .NET reading

**Selection.** One slice per immediate child namespace of <module>.Application, for every module root: a feature in a grouped layout, a use case in a flat one, each with everything below it. Types directly in the application namespace and everything below Application.Shared are ignored.

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
        "One slice per immediate child package of <module>.application, for every module root:"
            + " a feature in a grouped layout, a use case in a flat one, each with everything"
            + " below it. Classes directly in the application package and everything below"
            + " application.shared are ignored.")
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
        String child = pkg.substring(application.length() + 1).split("\\.")[0];
        return child.equals("shared")
            ? SliceIdentifier.ignore()
            : SliceIdentifier.of(application + "." + child);
      }

      @Override
      public String getDescription() {
        return "feature or use case packages";
      }
    };
  }
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `moduleRootOf()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
