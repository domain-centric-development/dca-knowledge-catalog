---
type: Reference
title: Setup and Configuration — Gradle Dependency
tags: [reference]
evidence_for: "/guide/archunit-governance/setup-and-configuration.md#gradle-dependency"
---

[Full node and context](/guide/archunit-governance/setup-and-configuration.md#gradle-dependency). This is an evidence excerpt; retain the parent selection and caveats.

### Gradle Dependency

```kotlin
dependencies {
    implementation("dev.domaincentric:dca-building-blocks:0.1.2")
    testImplementation("dev.domaincentric:dca-archunit:0.3.0")     // brings ArchUnit
    testImplementation("org.junit.jupiter:junit-jupiter")
}
```
