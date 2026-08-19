---
type: Rule
title: Store interfaces must not declare findById or save methods
rule: Store interfaces must not declare findById or save methods.
constraint: Store interfaces must not declare findById or save methods.
enforced_by: "DddTacticalPatternsArchUnitTest#Store interfaces must not declare findById or save methods"
status: enforced
test_class: DddTacticalPatternsArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/DddTacticalPatternsArchUnitTest.groovy
tags: [tactical, archunit]
---

```groovy
when:
// findById/save are Repository semantics. A Store that has them is a Repository wearing the
// wrong name, and the stored object should then be an Aggregate Root.
def violations = allClasses
  .findAll { it.isAssignableTo(Store.class) && it.isInterface() && it.simpleName != "Store" }
  .collectMany { storeInterface ->
    storeInterface.methods
      .findAll { it.name in ["findById", "save", "deleteById", "delete"] }
      .collect { "${storeInterface.fullName}.${it.name}() - Repository semantics on a Store" }
  }

then:
assert violations.isEmpty(),
  "Store interfaces use record/count/exists semantics, not findById/save.\n" +
  "Violations:\n" + violations.join("\n") +
  "\n\nFix: rename to *Repository if the stored object is an Aggregate Root, " +
  "otherwise rename the methods to record(...), count(...), exists(...)."
```

## Applies to markers

- [Repository<T, ID>](/marker/port-out/repository.md)
- [Store](/marker/port-out/store.md)
