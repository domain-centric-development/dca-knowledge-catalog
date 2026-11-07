---
type: Reference
title: "The repository of an owned aggregate declares a lookup by the aggregate's id and the owner's id — `repositoriesOf`"
tags: [reference]
evidence_for: "/rule/tactical/dca-tac-026.md#repositoriesof"
---

[Full node and context](/rule/tactical/dca-tac-026.md#repositoriesof). This is an evidence excerpt; retain the parent selection and caveats.

### `repositoriesOf`

```java
/** The repository interfaces that bind the aggregate, by type argument or, raw, by name. */
  private static List<JavaClass> repositoriesOf(
      JavaClass aggregate, List<JavaClass> repositories, DcaArchitecture arch) {
    String markerName = arch.layout().markers().repository();
    List<JavaClass> bound = new ArrayList<>();
    for (JavaClass repository : repositories) {
      Optional<JavaType> argument = boundAggregateArgument(repository, markerName);
      if (argument.isPresent()) {
        if (!(argument.get() instanceof JavaTypeVariable)
            && argument.get().toErasure().equals(aggregate)) {
          bound.add(repository);
        }
      } else if (repository
              .getSimpleName()
              .equals(aggregate.getSimpleName() + arch.layout().repositorySuffix())
          && Objects.equals(
              arch.rootContextPackage(repository.getPackageName()),
              arch.rootContextPackage(aggregate.getPackageName()))) {
        bound.add(repository);
      }
    }
    return bound;
  }
```
