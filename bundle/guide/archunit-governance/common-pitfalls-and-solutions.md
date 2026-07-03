---
type: Section
title: Common Pitfalls and Solutions
chapter: ArchUnit Governance for Domain-Centric Architecture
source: guide
resource: implementing-domain-centric-architecture/archunit-governance.md
tags: [guide, section]
---

### Pitfall 1: Tests Failing for Test Code

**Problem:** ArchUnit analyzes test code and finds violations

**Solution:** Exclude tests from analysis
```java
@AnalyzeClasses(
    packages = "com.company.project",
    importOptions = ImportOption.DoNotIncludeTests.class
)
```

### Pitfall 2: Too Many Rules at Once

**Problem:** Adding all rules to legacy codebase causes hundreds of failures

**Solution:** Use `FreezingArchRule` or add rules incrementally
```java
@ArchTest
static final ArchRule frozen_rule =
    FreezingArchRule.freeze(your_rule_here);
```

### Pitfall 3: False Positives from Generated Code

**Problem:** Generated classes (e.g., from Lombok, MapStruct) violate rules

**Solution:** Create custom import option to exclude generated code
```java
public class ExcludeGenerated implements ImportOption {
    @Override
    public boolean includes(Location location) {
        return !location.contains("/generated/") &&
               !location.contains("/lombok/");
    }
}
```

### Pitfall 4: Package Patterns Not Matching

**Problem:** Rule doesn't catch violations due to incorrect package pattern

**Solution:** Use `..` for any number of subpackages
```java
// ❌ Wrong - matches only direct children
"com.company.project.domain"

// ✅ Right - matches any depth
"..domain.."
```

### Pitfall 5: Slow Test Execution

**Problem:** ArchUnit tests take too long to run

**Solution:**
- Cache imported classes
- Split into multiple test classes
- Run architecture tests separately in CI pipeline

---
