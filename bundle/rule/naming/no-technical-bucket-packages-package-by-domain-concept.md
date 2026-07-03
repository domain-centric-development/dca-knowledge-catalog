---
type: Rule
title: No technical bucket packages - package by domain concept
rule: "Packages are named after domain concepts from the ubiquitous language, not technical patterns."
constraint: No technical bucket packages - package by domain concept.
enforced_by: "NamingConventionsArchUnitTest#No technical bucket packages - package by domain concept"
status: enforced
test_class: NamingConventionsArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/NamingConventionsArchUnitTest.groovy
tags: [naming, archunit]
---

```groovy
expect:
// Top-level structure must scream business capabilities (screaming architecture).
// Technical buckets like 'entities' or 'util' hide the domain and attract
// unrelated code. DTOs/Converters/ViewModels have their own placement rules above.
noClasses()
  .should().resideInAnyPackage("..entities..", "..valueobjects..", "..helpers..", "..util..", "..utils..")
  .because("Packages are named after domain concepts from the ubiquitous language, not technical patterns")
  .allowEmptyShould(true)
  .check(allClasses)
```
