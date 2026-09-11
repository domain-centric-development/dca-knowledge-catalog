---
type: Section
title: Governance
chapter: "Language Mappings: Java/Spring ↔ C#/.NET"
source: guide
resource: dca-guide/topics/language-mappings.md
tags: [guide, section]
---

| | Java | .NET |
|---|---|---|
| Base class | `DcaArchitectureTest` (JUnit 5, dynamic tests) | `DcaArchitectureTest` (xUnit, one theory case per rule) |
| Layout | `DcaLayout.forBasePackage("com.company.project")` | `DcaLayout.ForRootNamespace("Company.Project")` |
| Layout options | `withIncomingSubpackage`, `withUseCaseSuffix`, `withControllerSuffix`, `allowingInDomain`, `withFrameworkAnnotations` (presets `spring`, `jakarta`, `quarkus`, `micronaut`, `none`) | `WithIncomingSegment`, `WithUseCaseSuffix`, `WithRestControllerSuffix`, `AllowingInDomain`, `WithFrameworkTypes` (presets `AspNetCore`, `None`) |
| Selection | `additionalSelection()` → `DcaRuleSelection` | `AdditionalSelection` → `DcaRuleSelection` |
| Properties file | `dca-archunit.properties` on the test class path | `dca-archunit.properties` next to the test assembly (copy to output) |
| Dials | scope, severity, exceptions, **baseline** (`frozen`) | scope, severity, exceptions — no baseline (ArchUnitNET has no `FreezingArchRule`) |
| Build flavour | any | **Debug** — optimized builds hide async dependencies and are refused |
| Without the base class | `DcaRules.checkAll(DcaArchitecture.load(layout))` | `DcaRules.CheckAll(DcaArchitecture.Load(layout, assemblies))` |
| Rule ids | `DCA-<SET>-<NNN>` | identical; plus `DCA-NET-001..006`; four Java rules that check only a container stereotype are *not applicable* |

See [ArchUnit Governance](/guide/archunit-governance.md) for the rule categories and the tuning dials.
