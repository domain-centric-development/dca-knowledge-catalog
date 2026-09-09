---
type: Reference
title: "Use cases that save an aggregate must publish its domain events — `EventFreeAggregate.aggregate`"
tags: [reference]
evidence_for: "/rule/usecase/dca-use-009.md#eventfreeaggregateaggregate"
---

[Full node and context](/rule/usecase/dca-use-009.md#eventfreeaggregateaggregate). This is an evidence excerpt; retain the parent selection and caveats.

### `EventFreeAggregate.aggregate`

```java
private static Type aggregate(Type type, Map<TypeVariable<?>, Type> inherited) {
  Class<?> raw;
  Map<TypeVariable<?>, Type> bindings = new HashMap<>(inherited);
  if (type instanceof ParameterizedType p) {
    raw = (Class<?>) p.getRawType();
    for (int i = 0; i < p.getActualTypeArguments().length; i++) {
      Type arg = p.getActualTypeArguments()[i];
      while (arg instanceof TypeVariable<?> v
          && bindings.containsKey(v)
          && bindings.get(v) != arg) arg = bindings.get(v);
      bindings.put(raw.getTypeParameters()[i], arg);
    }
  } else if (type instanceof Class<?> c) raw = c;
  else return null;
  if (raw == Repository.class) return bindings.get(raw.getTypeParameters()[0]);
  for (Type parent : raw.getGenericInterfaces()) {
    Type found = aggregate(parent, bindings);
    if (found != null) return found;
  }
  return raw.getGenericSuperclass() == null
      ? null
      : aggregate(raw.getGenericSuperclass(), bindings);
}
```
