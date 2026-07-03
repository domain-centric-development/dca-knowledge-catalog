---
type: Section
title: Best Practices
chapter: ArchUnit Governance for Domain-Centric Architecture
source: guide
resource: implementing-domain-centric-architecture/archunit-governance.md
tags: [guide, section]
---

### 1. Organize Tests by Category

Create separate test classes for different rule categories:
- `LayerDependencyTest` - Layer dependency rules
- `FrameworkIndependenceTest` - Framework usage rules
- `DddPatternTest` - DDD pattern implementation
- `NamingConventionTest` - Naming standards
- `PortAdapterTest` - Hexagonal architecture rules

### 2. Use Descriptive Test Names and Messages

```java
// ❌ Bad - Vague
@ArchTest
static final ArchRule rule1 =
    noClasses().that().resideInAPackage("..domain..").should().dependOnClassesThat()...;

// ✅ Good - Descriptive
@ArchTest
static final ArchRule domain_should_not_depend_on_infrastructure =
    noClasses()
        .that().resideInAPackage("..domain..")
        .should().dependOnClassesThat().resideInPackage("..infrastructure..")
        .because("Domain must remain independent of infrastructure concerns");
```

### 3. Start Simple, Add Rules Incrementally

Don't try to add all rules at once:
1. Start with basic layer dependency rules
2. Add framework independence rules
3. Add DDD pattern rules
4. Add naming convention rules
5. Add custom business-specific rules

### 4. Freeze Violations for Legacy Code

If adding ArchUnit to an existing codebase with violations:

```java
@ArchTest
static final ArchRule domain_is_framework_independent =
    FreezingArchRule.freeze(
        noClasses()
            .that().resideInAPackage("..domain..")
            .should().dependOnClassesThat().resideInAnyPackage("org.springframework..")
    );
```

This allows you to:
- Prevent new violations
- Fix existing violations incrementally
- Track progress over time

### 5. Exclude Generated Code

```java
@AnalyzeClasses(
    packages = "com.company.project",
    importOptions = {
        ImportOption.DoNotIncludeTests.class,
        ImportOption.DoNotIncludeJars.class
    }
)
```

Or create custom import options:

```java
public class DoNotIncludeGenerated implements ImportOption {
    @Override
    public boolean includes(Location location) {
        return !location.contains("/generated/");
    }
}
```

---
