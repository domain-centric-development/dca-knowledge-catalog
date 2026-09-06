---
type: Rule
id: DCA-USE-014
title: "Use case packages within a module must use one consistent depth (flat or grouped by feature)"
rule: "A use case package sits either directly below the application package (application.<usecase>) or one level deeper inside a feature (application.<feature>.<usecase>). A feature is an optional, domain-named group of related use cases - a navigation boundary inside one bounded context, not a layer, module or aggregate owner. Mixing both forms in one module makes it unclear whether a package is a feature, a use case or a leftover; nesting deeper than a feature hides the use case. The rule checks legibility only: it does not infer bounded contexts, feature semantics or aggregate ownership. application.shared holds the context-wide output ports and is not a use case package."
constraint: "Use case packages within a module must use one consistent depth (flat or grouped by feature)."
enforced_by: "UseCaseRules#DCA-USE-014"
status: enforced
rule_set: usecase
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/UseCaseRules.java
tags: [usecase, archunit]
---

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
```
