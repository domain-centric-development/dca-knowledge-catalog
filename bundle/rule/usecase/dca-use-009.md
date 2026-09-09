---
type: Rule
id: DCA-USE-009
title: Use cases that save an aggregate must publish its domain events
rule: "A saved aggregate must not keep its events: unpublished, they are lost, and stored on the instance they may later be published out of context. Publishing belongs after the save, in the use case that owns the unit of work - unless the aggregate is proven never to register an event. Checked per entry path, following calls within the use case class: every entry point that reaches a save - a method callable from outside the class, or one nothing in the class calls - must also reach a publication; a wrapper that publishes does not cover a direct call of the public method it wraps, and a helper two methods share does not connect them. That the publication follows the save and concerns the same aggregate is not established statically. Only DomainEventPublisher.publishAndClearEvents counts as a publication: iterating domainEvents() and calling publish(event), even followed by clearDomainEvents(), separates dispatch from acknowledgement and is not accepted."
constraint: Use cases that save an aggregate must publish its domain events.
selects: "Non-interface classes in <module>.application.. that implement InputPort or whose simple name ends with the configured use-case suffix."
checks: "Only a resolved Repository<T,ID> whose aggregate and every non-building-block superclass are scanned and have no registration call (including helpers) is exempt. Unresolved generics, partial scans or undecidable external helpers remain required. For every non-exempt method of the class that calls Repository.save, every entry point reaching it (a method callable from outside the class, or one nothing in the class calls) also reaches, through calls within the class, a call of DomainEventPublisher.publishAndClearEvents. Only publishAndClearEvents counts - publish(event), even followed by clearDomainEvents(), does not. A use case without a save (a query, a bulk delete) is selected but has nothing to check and passes."
enforced_by: "UseCaseRules#DCA-USE-009"
status: enforced
rule_set: usecase
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/UseCaseRules.java
tags: [usecase, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/UseCaseRules.cs
---

# Use cases that save an aggregate must publish its domain events

## Selection

Non-interface classes in <module>.application.. that implement InputPort or whose simple name ends with the configured use-case suffix.

## Check

Only a resolved Repository<T,ID> whose aggregate and every non-building-block superclass are scanned and have no registration call (including helpers) is exempt. Unresolved generics, partial scans or undecidable external helpers remain required. For every non-exempt method of the class that calls Repository.save, every entry point reaching it (a method callable from outside the class, or one nothing in the class calls) also reaches, through calls within the class, a call of DomainEventPublisher.publishAndClearEvents. Only publishAndClearEvents counts - publish(event), even followed by clearDomainEvents(), does not. A use case without a save (a query, a bulk delete) is selected but has nothing to check and passes.

## .NET reading

**Selection.** Classes in <module>.Application of every module root selected by IInputPort assignability or the configured use-case suffix, whose runtime type is in the loaded assemblies.

**Check.** Only a resolved IRepository<T,ID> aggregate with its complete non-building-block hierarchy under scan and no registration call, including helpers, is exempt. Unresolved arguments, partial scans and undecidable external helpers are not exempt. For every non-exempt method calling IRepository.SaveAsync, every entry point reaching it (a method callable from outside the class, or one nothing in the class calls) also reaches, through calls within the class, a call of IDomainEventPublisher.PublishAndClearEventsAsync. Calls are read from the IL of the class and its nested state-machine and closure types, so async methods and lambdas are followed. Only PublishAndClearEventsAsync counts - PublishAsync(event), even followed by ClearDomainEvents(), does not. A use case without a save (a query, a bulk delete) is selected but has nothing to check and passes.

## Implementation

```java
DcaRule.of(
        "DCA-USE-009",
        "Use cases that save an aggregate must publish its domain events",
        "A saved aggregate must not keep its events: unpublished, they are lost, and stored on the"
            + " instance they may later be published out of context. Publishing belongs after the"
            + " save, in the use case that owns the unit of work - unless the aggregate is proven never to register an"
            + " event. Checked per entry path, following calls within the use case class: every"
            + " entry point that reaches a save - a method callable from outside the class, or one"
            + " nothing in the class calls - must also reach a publication; a wrapper that publishes"
            + " does not cover a direct call of the public method it wraps, and a helper two methods"
            + " share does not connect them. That the"
            + " publication follows the save and concerns the same aggregate is not established"
            + " statically. Only DomainEventPublisher.publishAndClearEvents counts as a publication:"
            + " iterating domainEvents() and calling publish(event), even followed by"
            + " clearDomainEvents(), separates dispatch from acknowledgement and is not accepted",
        arch ->
            classes()
                .that()
                .resideInAnyPackage(arch.allApplicationPatterns())
                .and()
                .haveSimpleNameEndingWith(layout.useCaseSuffix())
                .or()
                .areAssignableTo(InputPort.class)
                .and()
                .areNotInterfaces()
                .should(publishAfterSaving(arch))
                .allowEmptyShould(true))
    .selecting(
        "Non-interface classes in <module>.application.. that implement InputPort or whose simple name ends with the configured use-case suffix.")
    .checking(
        "Only a resolved Repository<T,ID> whose aggregate and every non-building-block superclass are scanned and have no registration call (including helpers) is exempt. Unresolved generics, partial scans or undecidable external helpers remain required. For every non-exempt method of the class that calls Repository.save, every entry point reaching it (a method callable from outside the class, or one nothing in the class calls) also reaches, through calls within the class, a call of DomainEventPublisher.publishAndClearEvents. Only publishAndClearEvents counts - publish(event), even followed by clearDomainEvents(), does not. A use case without a save (a query, a bulk delete) is selected but has nothing to check and passes.")
```

## Helpers

### `publishAfterSaving`

```java
private static ArchCondition<JavaClass> publishAfterSaving(DcaArchitecture arch) {
  return new ArchCondition<>("publish the aggregate's domain events after saving it") {
    @Override
    public void check(JavaClass item, ConditionEvents events) {
      IntraClassCalls calls = new IntraClassCalls(item);
      for (JavaCodeUnit unit : item.getCodeUnits()) {
        if (unit.getMethodCallsFromSelf().stream()
            .filter(
                c ->
                    c.getTarget().getName().equals("save")
                        && c.getTargetOwner().isAssignableTo(Repository.class))
            .allMatch(c -> EventFreeAggregate.repository(c.getTargetOwner(), arch))) {
          continue;
        }
        for (JavaCodeUnit entry : calls.entryPointsOf(unit)) {
          boolean publishes =
              calls.reachableFrom(entry).stream()
                  .anyMatch(u -> calls(u, DomainEventPublisher.class, "publishAndClearEvents"));
          if (!publishes) {
            events.add(
                SimpleConditionEvent.violated(
                    item,
                    item.getSimpleName()
                        + "."
                        + pathName(entry, unit)
                        + " saves an aggregate without publishing its domain events - no"
                        + " method reached from there calls publishAndClearEvents"));
          }
        }
      }
    }
  };
}
```

### `calls`

```java
private static boolean calls(JavaCodeUnit unit, Class<?> targetType) {
  return unit.getMethodCallsFromSelf().stream()
      .anyMatch(call -> call.getTargetOwner().isAssignableTo(targetType));
}

private static boolean calls(JavaCodeUnit unit, Class<?> targetType, String methodName) {
  return unit.getMethodCallsFromSelf().stream()
      .anyMatch(
          call ->
              call.getTarget().getName().equals(methodName)
                  && call.getTargetOwner().isAssignableTo(targetType));
}
```

### `pathName`

```java
/** {@code execute} for the unit itself, {@code execute (via persist)} when reached through it. */
  private static String pathName(JavaCodeUnit entry, JavaCodeUnit unit) {
    return entry.equals(unit) ? entry.getName() : entry.getName() + " (via " + unit.getName() + ")";
  }
```

### `EventFreeAggregate.repository`

```java
static boolean repository(JavaClass repository, DcaArchitecture arch) {
  Type aggregate;
  try {
    aggregate = aggregate(repository.reflect(), Map.of());
  } catch (LinkageError | RuntimeException failure) {
    return false;
  }
  if (!(aggregate instanceof Class<?> concrete) || concrete.isInterface()) return false;
  Map<String, JavaClass> scanned = new HashMap<>();
  arch.classes().forEach(c -> scanned.put(c.getName(), c));
  JavaClass current = scanned.get(concrete.getName());
  if (current == null) return false;
  while (current != null && !platform(current.getName())) {
    if (!scanned.containsKey(current.getName())
        || !noRegistration(current, scanned, new HashSet<>())) return false;
    current = current.getRawSuperclass().orElse(null);
  }
  return true;
}
```

### `IntraClassCalls.entryPointsOf`

```java
/**
   * The paths a unit can be entered on: those of its (transitive) callers - the unit itself
   * included - that are entry points. A unit is an entry point when it can be called from outside
   * the class (any code unit that is not private, synthetic or a bridge - a public method stays an
   * entry point even when another method of the class also calls it) or when no unit of the class
   * calls it. When the unit is reached only from within a cycle of private helpers, so that no
   * caller qualifies, the unit itself is taken as the entry point.
   */
  Set<JavaCodeUnit> entryPointsOf(JavaCodeUnit unit) {
    Set<JavaCodeUnit> roots = new LinkedHashSet<>();
    for (JavaCodeUnit caller : callersOf(unit)) {
      if (isEntryPoint(caller)) {
        roots.add(caller);
      }
    }
    if (roots.isEmpty()) {
      roots.add(unit);
    }
    return roots;
  }
```

### `IntraClassCalls.reachableFrom`

```java
/** The unit itself and every unit it reaches through calls within the class. */
  Set<JavaCodeUnit> reachableFrom(JavaCodeUnit unit) {
    return closure(unit, callees);
  }
```

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

### `EventFreeAggregate.platform`

```java
private static boolean platform(String name) {
  return name.startsWith("java.") || name.startsWith("dev.domaincentric.dca.buildingblocks.");
}
```

### `EventFreeAggregate.noRegistration`

```java
private static boolean noRegistration(
    JavaClass type, Map<String, JavaClass> scanned, Set<String> visited) {
  if (!visited.add(type.getName())) return true;
  for (var unit : type.getCodeUnits())
    for (var call : unit.getCallsFromSelf()) {
      var owner = call.getTargetOwner();
      if (call.getTarget().getName().equals("registerEvent")
          && owner.isAssignableTo(AggregateRoot.class)) return false;
      if (platform(owner.getName())) continue;
      var target = scanned.get(owner.getName());
      if (target == null || !noRegistration(target, scanned, visited)) return false;
    }
  return true;
}
```

### `IntraClassCalls.callersOf`

```java
/** The unit itself and every unit that reaches it through calls within the class. */
  Set<JavaCodeUnit> callersOf(JavaCodeUnit unit) {
    return closure(unit, callers);
  }
```

### `IntraClassCalls.isEntryPoint`

```java
private boolean isEntryPoint(JavaCodeUnit unit) {
  Set<JavaModifier> modifiers = unit.getModifiers();
  boolean externallyCallable =
      !modifiers.contains(JavaModifier.PRIVATE)
          && !modifiers.contains(JavaModifier.SYNTHETIC)
          && !modifiers.contains(JavaModifier.BRIDGE);
  return externallyCallable || callers.getOrDefault(unit, Set.of()).isEmpty();
}
```

### `IntraClassCalls.closure`

```java
private static Set<JavaCodeUnit> closure(
    JavaCodeUnit start, Map<JavaCodeUnit, Set<JavaCodeUnit>> edges) {
  Set<JavaCodeUnit> reached = new LinkedHashSet<>();
  Deque<JavaCodeUnit> pending = new ArrayDeque<>();
  pending.add(start);
  while (!pending.isEmpty()) {
    JavaCodeUnit current = pending.remove();
    if (reached.add(current)) {
      pending.addAll(edges.getOrDefault(current, Set.of()));
    }
  }
  return reached;
}
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allApplicationPatterns()`, `classes()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Check(
        "DCA-USE-009",
        "Use cases that save an aggregate must publish its domain events",
        "A saved aggregate must not keep its events: unpublished, they are lost, and stored on the"
            + " instance they may later be published out of context. Publishing belongs after the"
            + " save, in the use case that owns the unit of work - unless the aggregate is proven never to register an"
            + " event. Checked per entry path, following calls within the use case class: every"
            + " entry point that reaches a save - a method callable from outside the class, or one"
            + " nothing in the class calls - must also reach a publication; a wrapper that publishes"
            + " does not cover a direct call of the public method it wraps, and a helper two methods"
            + " share does not connect them. That the"
            + " publication follows the save and concerns the same aggregate is not established"
            + " statically. Only IDomainEventPublisher.PublishAndClearEventsAsync counts as a"
            + " publication: iterating DomainEvents and calling PublishAsync(event), even followed by"
            + " ClearDomainEvents(), separates dispatch from acknowledgement and is not accepted",
        arch =>
        {
            var violations = new List<string>();
            var useCases = arch.Classes
                .Where(c => c.Namespace is not null
                    && Matches(c.Namespace.FullName, DcaLayout.AnyOf(arch.AllApplicationPatterns()))
                    && (IsAssignableTo(arch, c, typeof(IInputPort)) || c.Name.Split('`')[0].EndsWith(arch.Layout.UseCaseSuffix, StringComparison.Ordinal)))
                .OrderBy(c => c.FullName, StringComparer.Ordinal);
            foreach (var useCase in useCases)
            {
                var runtime = arch.RuntimeType(useCase);
                if (runtime is null)
                {
                    continue;
                }

                var calls = new IntraClassCalls(runtime);
                foreach (var unit in calls.Units.Where(u => IntraClassCalls.Calls(u, "SaveAsync", typeof(IRepository))))
                {
                    if (IntraClassCalls.IlCalls(unit).Where(m => m.Name == "SaveAsync" && m.DeclaringType is not null && typeof(IRepository).IsAssignableFrom(m.DeclaringType))
                        .All(m => EventFreeAggregate.Repository(m, arch))) continue;
                    foreach (var entry in calls.EntryPointsOf(unit))
                    {
                        var publishes = calls.ReachableFrom(entry)
                            .Any(u => IntraClassCalls.Calls(u, "PublishAndClearEventsAsync", typeof(IDomainEventPublisher)));
                        if (!publishes)
                        {
                            violations.Add($"{useCase.FullName}.{IntraClassCalls.PathName(entry, unit)} saves an aggregate without"
                                + " publishing its domain events - no method reached from there calls PublishAndClearEventsAsync");
                        }
                    }
                }
            }

            DcaRule.Fail(
                "Use cases that save an aggregate must publish its domain events",
                violations.Distinct().ToList(),
                "call IDomainEventPublisher.PublishAndClearEventsAsync(aggregate) after IRepository.SaveAsync(aggregate) on every path that saves");
        })
    .Selecting(
        "Classes in <module>.Application of every module root selected by IInputPort assignability or the"
            + " configured use-case suffix, whose runtime type is in the loaded assemblies.")
    .Checking(
        "Only a resolved IRepository<T,ID> aggregate with its complete non-building-block hierarchy under scan and no registration call, including helpers, is exempt. Unresolved arguments, partial scans and undecidable external helpers are not exempt. For every non-exempt method calling IRepository.SaveAsync, every entry point"
            + " reaching it (a method callable from outside the class, or one nothing in the"
            + " class calls) also reaches, through calls within the class, a call of"
            + " IDomainEventPublisher.PublishAndClearEventsAsync. Calls are read from the IL of"
            + " the class and its nested state-machine and closure types, so async methods and"
            + " lambdas are followed. Only PublishAndClearEventsAsync counts - PublishAsync(event),"
            + " even followed by ClearDomainEvents(), does not. A use case without a save (a query,"
            + " a bulk delete) is selected but has nothing to check and passes.")
```

### C# helper EventFreeAggregate

```csharp
using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using DomainCentric.BuildingBlocks.Ddd.Tactical;
using DomainCentric.BuildingBlocks.Hexagonal.Ports.Out;

namespace DomainCentric.ArchRules.Rules;

internal static class EventFreeAggregate
{
    internal static bool Repository(MethodBase save, DcaArchitecture arch)
    {
        var owner = save.DeclaringType;
        if (owner is null) return false;
        var repository = owner.GetInterfaces().Append(owner).FirstOrDefault(t => t.IsGenericType && t.GetGenericTypeDefinition() == typeof(IRepository<,>));
        var aggregate = repository?.GetGenericArguments()[0];
        if (aggregate is null || aggregate.IsGenericParameter || aggregate.IsInterface) return false;
        var scanned = arch.Types.Select(arch.RuntimeType).Where(t => t is not null).Cast<Type>().ToHashSet();
        if (!scanned.Contains(aggregate)) return false;
        for (var current = aggregate; current is not null && !Platform(current); current = current.BaseType)
            if (!scanned.Contains(current) || !NoRegistration(current, scanned, new HashSet<Type>())) return false;
        return true;
    }

    private static bool NoRegistration(Type type, HashSet<Type> scanned, HashSet<Type> visited)
    {
        if (!visited.Add(type)) return true;
        foreach (var call in new IntraClassCalls(type).Units.SelectMany(IntraClassCalls.IlCalls))
        {
            var owner = call.DeclaringType;
            if (owner is null) return false;
            if (call.Name == "RegisterEvent" && typeof(IAggregateRoot).IsAssignableFrom(owner)) return false;
            if (Platform(owner)) continue;
            if (!scanned.Contains(owner) || !NoRegistration(owner, scanned, visited)) return false;
        }
        return true;
    }

    private static bool Platform(Type type) => (type.FullName ?? "").StartsWith("System.", StringComparison.Ordinal)
        || (type.FullName ?? "").StartsWith("DomainCentric.BuildingBlocks.", StringComparison.Ordinal);
}
```

### C# helper IntraClassCalls

```csharp
using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using System.Reflection.Emit;
using System.Runtime.CompilerServices;
using System.Text.RegularExpressions;

namespace DomainCentric.ArchRules.Rules;

/// <summary>
/// The calls of one class to its own methods — the directed graph a use case forms when <c>ExecuteAsync</c>
/// delegates to a private helper. Built from the IL of the runtime type: the compiler moves an <c>async</c>
/// method's body into a nested state machine and a lambda's body into a nested closure type, which ArchUnitNET
/// does not load, so those nested methods are units of the graph too, joined to the method that declares them
/// (the state-machine attribute, the <c>ldftn</c>/<c>newobj</c> that creates the delegate).
/// </summary>
/// <remarks>
/// The rules reason along the graph's direction: what a method reaches (its callees, transitively) is what
/// runs when it runs; the units that reach it are the paths it can be entered on. A helper two entry methods
/// both call is reached from both, but connects neither to the other — a shared callee is not an execution
/// path. An entry point is a unit callable from outside the class, or one nothing in the class calls. Order of calls
/// and the identity of the aggregate passed are not modelled.
/// </remarks>
internal sealed class IntraClassCalls
{
    private static readonly Regex CompilerGeneratedFor = new("^<([^>]+)>", RegexOptions.Compiled);

    private readonly Dictionary<MethodBase, HashSet<MethodBase>> _callers = new();
    private readonly Dictionary<MethodBase, HashSet<MethodBase>> _callees = new();

    public IntraClassCalls(Type owner)
    {
        Units = UnitsOf(owner).ToList();
        var byToken = Units.ToDictionary(u => (u.Module, u.MetadataToken));
        foreach (var unit in Units)
        {
            foreach (var target in IlCalls(unit))
            {
                if (byToken.TryGetValue((target.Module, target.MetadataToken), out var callee))
                {
                    AddEdge(unit, callee);
                }
            }

            var stateMachine = unit.GetCustomAttribute<StateMachineAttribute>()?.StateMachineType;
            if (stateMachine is not null)
            {
                foreach (var moved in Units.Where(u => u.DeclaringType == stateMachine))
                {
                    AddEdge(unit, moved);
                }
            }
        }
    }

    /// <summary>Every method and constructor of the type and its nested types (state machines, closures).</summary>
    public IReadOnlyList<MethodBase> Units { get; }

    /// <summary>The unit itself and every unit that reaches it through calls within the class.</summary>
    public ISet<MethodBase> CallersOf(MethodBase unit) => Closure(unit, _callers);

    /// <summary>The unit itself and every unit it reaches through calls within the class.</summary>
    public ISet<MethodBase> ReachableFrom(MethodBase unit) => Closure(unit, _callees);

    /// <summary>Reachability along paths whose units all satisfy the predicate.</summary>
    public ISet<MethodBase> ReachableThrough(MethodBase start, Func<MethodBase, bool> allowed)
    {
        var reached = new HashSet<MethodBase>();
        var pending = new Queue<MethodBase>(); pending.Enqueue(start);
        while (pending.Count > 0)
        {
            var current = pending.Dequeue();
            if (!allowed(current) || !reached.Add(current)) continue;
            if (_callees.TryGetValue(current, out var next)) foreach (var unit in next) pending.Enqueue(unit);
        }
        return reached;
    }

    /// <summary>
    /// The paths a unit can be entered on: those of its (transitive) callers - the unit itself included - that are
    /// entry points. A unit is an entry point when it can be called from outside the class (a non-private method or
    /// constructor written in source - a public method stays an entry point even when another method of the class
    /// also calls it; compiler-generated units such as state machines and closures are not) or when no unit of the
    /// class calls it. When the unit is reached only from within a cycle of private helpers, so that no caller
    /// qualifies, the unit itself is taken as the entry point.
    /// </summary>
    public ISet<MethodBase> EntryPointsOf(MethodBase unit)
    {
        var roots = new HashSet<MethodBase>(CallersOf(unit).Where(IsEntryPoint));
        if (roots.Count == 0)
        {
            roots.Add(unit);
        }

        return roots;
    }

    private bool IsEntryPoint(MethodBase unit) =>
        (!unit.IsPrivate && !IsCompilerGenerated(unit)) || !_callers.ContainsKey(unit);

    private static bool IsCompilerGenerated(MethodBase unit) =>
        unit.Name.StartsWith('<')
        || unit.DeclaringType is { } declaring
            && (declaring.Name.StartsWith('<') || declaring.IsDefined(typeof(CompilerGeneratedAttribute), inherit: false));

    /// <summary>Whether the unit's IL calls a method named <paramref name="method"/> on a type assignable to <paramref name="marker"/>.</summary>
    public static bool Calls(MethodBase unit, string method, Type marker) =>
        IlCalls(unit).Any(m => m.Name == method && m.DeclaringType is not null && marker.IsAssignableFrom(m.DeclaringType));

    /// <summary>
    /// The source-level name of a unit: <c>ExecuteAsync</c> for the method itself, for its state machine's
    /// <c>MoveNext</c> and for a lambda it declares (<c>&lt;ExecuteAsync&gt;b__0</c>).
    /// </summary>
    public static string DisplayName(MethodBase unit)
    {
        var own = CompilerGeneratedFor.Match(unit.Name);
        if (own.Success)
        {
            return own.Groups[1].Value;
        }

        var host = unit.DeclaringType is { IsNested: true } declaring ? CompilerGeneratedFor.Match(declaring.Name) : Match.Empty;
        return host.Success ? host.Groups[1].Value : unit.Name;
    }

    /// <summary><c>Execute</c> for the unit itself, <c>Execute (via Persist)</c> when reached through it.</summary>
    public static string PathName(MethodBase entry, MethodBase unit)
    {
        var entryName = DisplayName(entry);
        var unitName = DisplayName(unit);
        return entryName == unitName ? entryName : $"{entryName} (via {unitName})";
    }

    private void AddEdge(MethodBase caller, MethodBase callee)
    {
        if (!_callers.TryGetValue(callee, out var callers))
        {
            _callers[callee] = callers = new HashSet<MethodBase>();
        }

        callers.Add(caller);
        if (!_callees.TryGetValue(caller, out var callees))
        {
            _callees[caller] = callees = new HashSet<MethodBase>();
        }

        callees.Add(callee);
    }

    private static ISet<MethodBase> Closure(MethodBase start, IReadOnlyDictionary<MethodBase, HashSet<MethodBase>> edges)
    {
        var reached = new HashSet<MethodBase>();
        var pending = new Queue<MethodBase>();
        pending.Enqueue(start);
        while (pending.Count > 0)
        {
            var current = pending.Dequeue();
            if (reached.Add(current) && edges.TryGetValue(current, out var next))
            {
                foreach (var n in next)
                {
                    pending.Enqueue(n);
                }
            }
        }

        return reached;
    }

    private static IEnumerable<MethodBase> UnitsOf(Type type)
    {
        const BindingFlags all = BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance | BindingFlags.Static | BindingFlags.DeclaredOnly;
        foreach (var method in type.GetMethods(all).Cast<MethodBase>().Concat(type.GetConstructors(all)))
        {
            yield return method;
        }

        foreach (var nested in type.GetNestedTypes(all))
        {
            foreach (var unit in UnitsOf(nested))
            {
                yield return unit;
            }
        }
    }

    private static readonly Lazy<IReadOnlyDictionary<short, OpCode>> OpCodeTable = new(() =>
        typeof(OpCodes).GetFields(BindingFlags.Public | BindingFlags.Static)
            .Select(f => (OpCode)f.GetValue(null)!)
            .ToDictionary(o => o.Value, o => o));

    /// <summary>
    /// The methods a unit's IL refers to: the targets of <c>call</c>, <c>callvirt</c> and <c>newobj</c>, and the
    /// method a <c>ldftn</c>/<c>ldvirtftn</c> turns into a delegate — every instruction with a method operand.
    /// </summary>
    public static IEnumerable<MethodBase> IlCalls(MethodBase method)
    {
        byte[]? il;
        try
        {
            il = method.GetMethodBody()?.GetILAsByteArray();
        }
        catch (InvalidOperationException)
        {
            il = null;
        }

        if (il is null)
        {
            yield break;
        }

        var typeArgs = method.DeclaringType is { IsGenericType: true } dt ? dt.GetGenericArguments() : null;
        var methodArgs = method is MethodInfo { IsGenericMethod: true } mi ? mi.GetGenericArguments() : null;
        var position = 0;
        while (position < il.Length)
        {
            short code = il[position++];
            if (code == 0xFE)
            {
                code = (short)(0xFE00 | il[position++]);
            }

            if (!OpCodeTable.Value.TryGetValue(code, out var opCode))
            {
                yield break; // unknown opcode — stop scanning this body rather than misreading operands
            }

            MethodBase? target = null;
            switch (opCode.OperandType)
            {
                case OperandType.InlineMethod:
                    var token = BitConverter.ToInt32(il, position);
                    position += 4;
                    try
                    {
                        target = method.Module.ResolveMethod(token, typeArgs, methodArgs);
                    }
                    catch (ArgumentException)
                    {
                        target = null;
                    }

                    break;
                case OperandType.InlineSwitch:
                    var count = BitConverter.ToInt32(il, position);
                    position += 4 + (4 * count);
                    break;
                case OperandType.InlineNone:
                    break;
                case OperandType.ShortInlineBrTarget:
                case OperandType.ShortInlineI:
                case OperandType.ShortInlineVar:
                    position += 1;
                    break;
                case OperandType.InlineVar:
                    position += 2;
                    break;
                case OperandType.InlineI8:
                case OperandType.InlineR:
                    position += 8;
                    break;
                default:
                    position += 4;
                    break;
            }

            if (target is not null)
            {
                yield return target;
            }
        }
    }
}
```

## Related mentions (heuristic)

- [AggregateRoot<T, ID>](/marker/tactical/aggregateroot.md)
- [DomainEventPublisher](/marker/port-out/domaineventpublisher.md)
- [InputPort](/marker/port-in/inputport.md)
- [Repository<T, ID>](/marker/port-out/repository.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)

## Evidence slices

- [Overview](/evidence/rule/usecase/dca-use-009/overview.md)
- [`publishAfterSaving`](/evidence/rule/usecase/dca-use-009/publishaftersaving.md)
- [`calls`](/evidence/rule/usecase/dca-use-009/calls.md)
- [`pathName`](/evidence/rule/usecase/dca-use-009/pathname.md)
- [`EventFreeAggregate.repository`](/evidence/rule/usecase/dca-use-009/eventfreeaggregate-repository.md)
- [`IntraClassCalls.entryPointsOf`](/evidence/rule/usecase/dca-use-009/intraclasscalls-entrypointsof.md)
- [`IntraClassCalls.reachableFrom`](/evidence/rule/usecase/dca-use-009/intraclasscalls-reachablefrom.md)
- [`EventFreeAggregate.aggregate`](/evidence/rule/usecase/dca-use-009/eventfreeaggregate-aggregate.md)
- [`EventFreeAggregate.platform`](/evidence/rule/usecase/dca-use-009/eventfreeaggregate-platform.md)
- [`EventFreeAggregate.noRegistration`](/evidence/rule/usecase/dca-use-009/eventfreeaggregate-noregistration.md)
- [`IntraClassCalls.callersOf`](/evidence/rule/usecase/dca-use-009/intraclasscalls-callersof.md)
- [`IntraClassCalls.isEntryPoint`](/evidence/rule/usecase/dca-use-009/intraclasscalls-isentrypoint.md)
- [`IntraClassCalls.closure`](/evidence/rule/usecase/dca-use-009/intraclasscalls-closure.md)
- [C# expression](/evidence/rule/usecase/dca-use-009/c-expression.md)
- [C# helper EventFreeAggregate](/evidence/rule/usecase/dca-use-009/c-helper-eventfreeaggregate.md)
- [C# helper IntraClassCalls](/evidence/rule/usecase/dca-use-009/c-helper-intraclasscalls.md)
