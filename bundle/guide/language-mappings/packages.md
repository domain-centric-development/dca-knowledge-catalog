---
type: Section
title: Packages
chapter: "Language Mappings: Java/Spring ↔ C#/.NET"
source: guide
resource: dca-guide/language-mappings.md
tags: [guide, section]
---

| | Java | .NET |
|---|---|---|
| Building blocks | `dev.domaincentric:dca-building-blocks` (Maven Central) | `DomainCentric.BuildingBlocks` (NuGet) |
| Architecture rules | `dev.domaincentric:dca-archunit` (ArchUnit, JUnit 5 base class) | `DomainCentric.ArchRules` (ArchUnitNET) + `DomainCentric.ArchRules.Xunit` |
| Root package / namespace | `dev.domaincentric.dca.buildingblocks` | `DomainCentric.BuildingBlocks` |
| Dependencies of the building blocks | none | none (`netstandard2.1`, `net8.0`, `net10.0`) |

```kotlin
// Gradle
implementation("dev.domaincentric:dca-building-blocks:0.1.2")
testImplementation("dev.domaincentric:dca-archunit:0.3.0")
```

```
# .NET
dotnet add package DomainCentric.BuildingBlocks
dotnet add package DomainCentric.ArchRules.Xunit      # in the architecture test project
```
