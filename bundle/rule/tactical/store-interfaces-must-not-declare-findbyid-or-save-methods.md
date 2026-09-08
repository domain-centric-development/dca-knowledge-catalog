---
type: Rule
id: DCA-TAC-021
title: Store interfaces must not declare findById or save methods
rule: "findById/save are Repository semantics; a Store that has them is a Repository wearing the wrong name, and the stored object should then be an Aggregate Root."
constraint: Store interfaces must not declare findById or save methods.
selects: "Interfaces anywhere under scan assignable to Store, the marker Store itself excluded."
checks: "No method declared on the interface itself is named findById, save, deleteById or delete - matched by name alone, parameters and return type disregarded. Inherited methods are not inspected, and no particular vocabulary (record, count, exists) is required."
enforced_by: "TacticalPatternRules#DCA-TAC-021"
status: enforced
rule_set: tactical
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/TacticalPatternRules.java
tags: [tactical, archunit]
---

## Selection

Interfaces anywhere under scan assignable to Store, the marker Store itself excluded.

## Check

No method declared on the interface itself is named findById, save, deleteById or delete - matched by name alone, parameters and return type disregarded. Inherited methods are not inspected, and no particular vocabulary (record, count, exists) is required.

## .NET reading

**Selection.** Interfaces below the root namespace assignable to IStore; an interface named exactly Store excluded.

**Check.** No method declared on the interface itself is named FindByIdAsync, SaveAsync, DeleteByIdAsync or DeleteAsync, nor their synchronous forms FindById, Save, DeleteById and Delete, nor the camel-cased findById, save, deleteById and delete - matched by name alone, parameters and return type disregarded. Inherited methods are not inspected, and no particular vocabulary (Record, Count, Exists) is required.

## Implementation

```java
DcaRule.check(
        "DCA-TAC-021",
        "Store interfaces must not declare findById or save methods",
        "findById/save are Repository semantics; a Store that has them is a Repository wearing the"
            + " wrong name, and the stored object should then be an Aggregate Root",
        arch -> {
          List<String> violations = new ArrayList<>();
          for (JavaClass store : storeInterfaces(arch)) {
            for (JavaMethod method : store.getMethods()) {
              if (REPOSITORY_METHOD_NAMES.contains(method.getName())) {
                violations.add(
                    store.getFullName()
                        + "."
                        + method.getName()
                        + "() - Repository semantics on a Store");
              }
            }
          }
          fail(
              "Store interfaces use record/count/exists semantics, not findById/save."
                  + " Fix: rename to *Repository if the stored object is an Aggregate Root,"
                  + " otherwise rename the methods to record(...), count(...), exists(...).",
              violations);
        })
    .selecting(
        "Interfaces anywhere under scan assignable to Store, the marker Store itself "
            + "excluded.")
    .checking(
        "No method declared on the interface itself is named findById, save, deleteById "
            + "or delete - matched by name alone, parameters and return type disregarded. "
            + "Inherited methods are not inspected, and no particular vocabulary (record, "
            + "count, exists) is required.")
```

## Helpers

### `storeInterfaces`

```java
private static List<JavaClass> storeInterfaces(DcaArchitecture arch) {
  return classesMatching(
      arch,
      c ->
          c.isAssignableTo(Store.class)
              && c.isInterface()
              && !c.getSimpleName().equals(STORE_SUFFIX));
}
```

### `fail`

```java
private static void fail(String message, List<String> violations) {
  if (!violations.isEmpty()) {
    throw new DcaRuleViolation(message, violations);
  }
}
```

### `classesMatching`

```java
private static List<JavaClass> classesMatching(
    DcaArchitecture arch, Predicate<JavaClass> filter) {
  return arch.classes().stream().filter(filter).collect(Collectors.toList());
}
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `classes()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).

## Applies to markers

- [Repository<T, ID>](/marker/port-out/repository.md)
- [Store](/marker/port-out/store.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
