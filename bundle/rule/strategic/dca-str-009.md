---
type: Rule
id: DCA-STR-009
title: Anti-Corruption Layer components must be in acl packages
rule: "Anti-Corruption Layer components must be in 'acl' packages for clear architectural intent (DDD Strategic Pattern)."
constraint: Anti-Corruption Layer components must be in acl packages.
selects: "Classes anywhere on the classpath under scan whose simple name ends with EventTranslator, ACL or AntiCorruptionLayer - selected by name alone, no marker or annotation is read."
checks: "Each resides in a package whose path contains an acl segment (..acl..), at any depth. A translation class named otherwise is neither selected nor checked."
enforced_by: "StrategicPatternRules#DCA-STR-009"
status: enforced
rule_set: strategic
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/StrategicPatternRules.java
tags: [strategic, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/StrategicPatternRules.cs
---

# Anti-Corruption Layer components must be in acl packages

## Selection

Classes anywhere on the classpath under scan whose simple name ends with EventTranslator, ACL or AntiCorruptionLayer - selected by name alone, no marker or annotation is read.

## Check

Each resides in a package whose path contains an acl segment (..acl..), at any depth. A translation class named otherwise is neither selected nor checked.

## .NET reading

**Selection.** Types anywhere below the root namespace whose name ends with EventTranslator, ACL or AntiCorruptionLayer - selected by name alone, no marker or attribute is read.

**Check.** Each resides in a namespace whose path contains an Acl segment, at any depth. A translation class named otherwise is neither selected nor checked.

## Implementation

```java
DcaRule.of(
        "DCA-STR-009",
        "Anti-Corruption Layer components must be in acl packages",
        "Anti-Corruption Layer components must be in 'acl' packages for clear architectural intent"
            + " (DDD Strategic Pattern)",
        arch ->
            classes()
                .that()
                .haveSimpleNameEndingWith("EventTranslator")
                .or()
                .haveSimpleNameEndingWith("ACL")
                .or()
                .haveSimpleNameEndingWith("AntiCorruptionLayer")
                .should()
                .resideInAPackage("..acl..")
                .allowEmptyShould(true))
    .selecting(
        "Classes anywhere on the classpath under scan whose simple name ends with"
            + " EventTranslator, ACL or AntiCorruptionLayer - selected by name alone, no marker"
            + " or annotation is read.")
    .checking(
        "Each resides in a package whose path contains an acl segment (..acl..), at any depth."
            + " A translation class named otherwise is neither selected nor checked.")
```
### C# expression

```csharp
DcaRule.Of(
        "DCA-STR-009",
        "Anti-Corruption Layer components must be in Acl namespaces",
        "Anti-Corruption Layer components must be in 'Acl' namespaces for clear architectural intent (DDD Strategic Pattern)",
        arch =>
            Types().That().HaveNameMatching("(EventTranslator|ACL|AntiCorruptionLayer)$")
                .Should().ResideInNamespaceMatching(AnySegment("Acl")))
    .Selecting(
        "Types anywhere below the root namespace whose name ends with"
            + " EventTranslator, ACL or AntiCorruptionLayer - selected by name alone, no marker"
            + " or attribute is read.")
    .Checking(
        "Each resides in a namespace whose path contains an Acl segment, at any depth."
            + " A translation class named otherwise is neither selected nor checked.")
```

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
