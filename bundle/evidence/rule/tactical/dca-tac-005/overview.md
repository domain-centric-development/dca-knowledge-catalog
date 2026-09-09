---
type: Reference
title: Entities must not be instantiated directly from outside the aggregate — Overview
tags: [reference]
evidence_for: /rule/tactical/dca-tac-005.md
---

[Full node and context](/rule/tactical/dca-tac-005.md). This is an evidence excerpt; retain the parent selection and caveats.

# Entities must not be instantiated directly from outside the aggregate

## Selection

Constructor calls to non-root Entity types, records included.

## Check

The caller is the entity itself or an AggregateRoot, Entity or Factory in the same context domain layer. Same aggregate ownership is not decidable: another aggregate in that context passes and needs review. Reconstitution goes through an aggregate or factory; reflection is not inspected.

## .NET reading

**Selection.** Constructor calls to non-root IEntity types, records and structs included.

**Check.** The caller is the entity itself or an IAggregateRoot, IEntity or IFactory in the same context domain layer. Same aggregate ownership is not decidable: another aggregate in that context passes and needs review. Reconstitution goes through an aggregate or factory; reflection is not inspected.

## Implementation

```java
DcaRule.check(
        "DCA-TAC-005",
        "Entities must not be instantiated directly from outside the aggregate",
        "Entities are created through their aggregate root so that the root can enforce its"
            + " invariants",
        arch -> {
          List<String> violations = new ArrayList<>();
          for (JavaClass entity : nonRootEntities(arch)) {
            String root = arch.moduleRootOf(entity.getPackageName());
            for (var constructor : entity.getConstructors()) {
              for (var call : constructor.getCallsOfSelf()) {
                JavaClass caller = call.getOriginOwner();
                String domain =
                    root == null ? "" : root + "." + arch.layout().domainSubpackage();
                boolean sameDomain =
                    root != null
                        && root.equals(arch.moduleRootOf(caller.getPackageName()))
                        && (caller.getPackageName().equals(domain)
                            || caller.getPackageName().startsWith(domain + "."));
                boolean role =
                    caller.isAssignableTo(AggregateRoot.class)
                        || caller.isAssignableTo(Entity.class)
                        || caller.isAssignableTo(
                            dev.domaincentric.dca.buildingblocks.ddd.tactical.Factory.class);
                if (!caller.equals(entity) && !(sameDomain && role)) {
                  violations.add(
                      caller.getName()
                          + " constructs entity "
                          + entity.getName()
                          + " outside its domain construction boundary");
                }
              }
            }
          }
          fail(
              "Entities are constructed by their own domain aggregate, entity or factory.",
              violations);
        })
    .selecting("Constructor calls to non-root Entity types, records included.")
    .checking(
        "The caller is the entity itself or an AggregateRoot, Entity or Factory in the same context domain layer. Same aggregate ownership is not decidable: another aggregate in that context passes and needs review. Reconstitution goes through an aggregate or factory; reflection is not inspected.")
```

## Helpers
