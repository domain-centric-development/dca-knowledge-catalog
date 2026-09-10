---
type: Rule
id: DCA-USE-012
title: Use cases that save an aggregate or publish domain events must have a transaction boundary
rule: "The use case owns the unit of work. Saving an aggregate is one business fact, yet the repository may write it as several statements - an aggregate of entities and value objects often spans several tables - and a repository adapter draws no boundary of its own; without one, a failure between the statements leaves half an aggregate behind. Publishing adds a second effect that must fall with the save: integration events are relayed after commit by the framework's after-commit listeners, and their publication is registered in the publishing transaction. Without an active transaction the after-commit listeners are skipped silently and nothing is registered: the use case succeeds, the other contexts never hear of it. The boundary is either declarative transaction metadata (the configured transactional annotation on the class or the executing method) or an explicit TransactionBoundary.inTransaction(...) around load, mutate, save and publish. Checked per entry path, following calls within the class: from every entry point - a method callable from outside the class, or one nothing in the class calls - no route down to the saving, deleting or publishing method may be free of an annotation or a boundary; a covered caller does not cover another route to the same helper, and a boundary on one route does not cover a second route. Whether the save or the publication sits inside the block handed to inTransaction(...) is not visible in ArchUnit's call model, which folds a lambda's body into the enclosing method; that placement stays a review check."
constraint: Use cases that save an aggregate or publish domain events must have a transaction boundary.
selects: "Non-interface classes in <module>.application.. that implement InputPort or whose simple name ends with the configured use-case suffix."
checks: "For every method that calls Repository.save, Repository.deleteById or a DomainEventPublisher, every route from each entry point down to it is covered: the class carries one of the configured transactional annotations, or every uncovered unit on the route is either annotated or calls TransactionBoundary.inTransaction. A covered caller does not cover a second route to the same helper. With an empty transactional role only the explicit boundary counts. A use case that neither saves, deletes nor publishes (a query, a Store write) is selected but has nothing to check and passes. Whether the save or publish call sits inside the inTransaction block is not checked - ArchUnit folds a lambda into its enclosing method."
enforced_by: "UseCaseRules#DCA-USE-012"
status: enforced
rule_set: usecase
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/UseCaseRules.java
tags: [usecase, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/UseCaseRules.cs
---

# Use cases that save an aggregate or publish domain events must have a transaction boundary

## Selection

Non-interface classes in <module>.application.. that implement InputPort or whose simple name ends with the configured use-case suffix.

## Check

For every method that calls Repository.save, Repository.deleteById or a DomainEventPublisher, every route from each entry point down to it is covered: the class carries one of the configured transactional annotations, or every uncovered unit on the route is either annotated or calls TransactionBoundary.inTransaction. A covered caller does not cover a second route to the same helper. With an empty transactional role only the explicit boundary counts. A use case that neither saves, deletes nor publishes (a query, a Store write) is selected but has nothing to check and passes. Whether the save or publish call sits inside the inTransaction block is not checked - ArchUnit folds a lambda into its enclosing method.

## .NET reading

**Selection.** Concrete application operations selected by IInputPort marker or suffix with loadable runtime types, including closure and async units.

**Check.** Every entry path to a unit calling IRepository.SaveAsync, IRepository.DeleteByIdAsync or an IDomainEventPublisher crosses a unit calling ITransactionBoundary.InTransactionAsync (including its extension overloads) or carrying the configured TransactionalAttribute; a type-level attribute covers all paths. A use case that neither saves, deletes nor publishes (a query, a Store write) is selected but has nothing to check and passes. Static limit: a boundary call in the same unit passes even when the save or publication follows an empty boundary block. Runtime rollback containment must be tested separately.

## Implementation

```java
DcaRule.of(
        "DCA-USE-012",
        "Use cases that save an aggregate or publish domain events must have a transaction boundary",
        "The use case owns the unit of work. Saving an aggregate is one business fact, yet the"
            + " repository may write it as several statements - an aggregate of entities and value"
            + " objects often spans several tables - and a repository adapter draws no boundary of"
            + " its own; without one, a failure between the statements leaves half an aggregate"
            + " behind. Publishing adds a second effect that must fall with the save: integration"
            + " events are relayed after commit by the framework's after-commit listeners, and their"
            + " publication is registered in the publishing transaction. Without an active"
            + " transaction the after-commit listeners are skipped silently and nothing is"
            + " registered: the use case succeeds, the other contexts never hear of it. The boundary"
            + " is either declarative transaction metadata (the configured transactional annotation"
            + " on the class or the executing method) or an explicit"
            + " TransactionBoundary.inTransaction(...) around load, mutate, save and publish. Checked"
            + " per entry path, following calls within the class: from every entry point - a"
            + " method callable from outside the class, or one nothing in the class calls - no route"
            + " down to the saving, deleting or publishing method may be free of an annotation or a"
            + " boundary; a covered caller does not cover another route to the same helper, and a"
            + " boundary on one route does not cover a second route. Whether the save or the"
            + " publication sits inside the block handed to inTransaction(...) is not visible in"
            + " ArchUnit's call model, which folds a lambda's body into the enclosing method; that"
            + " placement stays a review check",
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
                .should(
                    beTransactionalWhenMutating(layout.frameworkAnnotations().transactional()))
                .allowEmptyShould(true))
    .selecting(
        "Non-interface classes in <module>.application.. that implement InputPort or whose simple name ends with the configured use-case suffix.")
    .checking(
        "For every method that calls Repository.save, Repository.deleteById or a"
            + " DomainEventPublisher, every route from each entry point down to it is covered: the"
            + " class carries one of the configured transactional annotations, or every uncovered"
            + " unit on the route is either annotated or calls TransactionBoundary.inTransaction."
            + " A covered caller does not cover a second route to the same helper. With an empty"
            + " transactional role only the explicit boundary counts. A use case that neither"
            + " saves, deletes nor publishes (a query, a Store write) is selected but has nothing"
            + " to check and passes. Whether the save or publish call sits inside the"
            + " inTransaction block is not checked - ArchUnit folds a lambda into its enclosing"
            + " method.")
```

## Helpers

### `beTransactionalWhenMutating`

```java
private static ArchCondition<JavaClass> beTransactionalWhenMutating(List<String> transactional) {
  return new ArchCondition<>(
      "be transactional when saving an aggregate or publishing domain events") {
    @Override
    public void check(JavaClass item, ConditionEvents events) {
      IntraClassCalls calls = new IntraClassCalls(item);
      for (JavaCodeUnit unit : item.getCodeUnits()) {
        String effect = transactionalEffectOf(unit);
        if (effect == null) {
          continue;
        }
        for (JavaCodeUnit entry : calls.entryPointsOf(unit)) {
          if (pathIsTransactional(item, entry, unit, calls, transactional)) {
            continue;
          }
          events.add(
              SimpleConditionEvent.violated(
                  item,
                  item.getSimpleName()
                      + "."
                      + pathName(entry, unit)
                      + " "
                      + effect
                      + " without "
                      + FrameworkAnnotations.describe(
                          transactional, "declarative transaction metadata (none configured)")
                      + " on the class or on a method of that path, and without"
                      + " TransactionBoundary.inTransaction(...) on it"));
        }
      }
    }
  };
}
```

### `transactionalEffectOf`

```java
/**
   * The effect of a code unit that needs a transaction, worded for the violation, or {@code null}
   * when the unit neither writes through a Repository nor publishes domain events.
   */
  private static String transactionalEffectOf(JavaCodeUnit unit) {
    boolean saves = calls(unit, Repository.class, "save");
    boolean deletes = calls(unit, Repository.class, "deleteById");
    boolean publishes = calls(unit, DomainEventPublisher.class);
    if (!saves && !deletes && !publishes) {
      return null;
    }
    List<String> effects = new ArrayList<>();
    if (saves) {
      effects.add("saves an aggregate");
    }
    if (deletes) {
      effects.add("deletes an aggregate");
    }
    if (publishes) {
      effects.add("publishes domain events");
    }
    return String.join(" and ", effects);
  }
```

### `pathIsTransactional`

```java
/**
   * Whether every route from {@code entry} down to {@code publisher} is covered: the class is
   * annotated, or no route reaches the publisher through units none of which carries the annotation
   * or draws an explicit boundary. A boundary on one route does not cover another route to the same
   * publisher.
   */
  private static boolean pathIsTransactional(
      JavaClass item,
      JavaCodeUnit entry,
      JavaCodeUnit publisher,
      IntraClassCalls calls,
      List<String> transactional) {
    if (AnnotationRoles.isMetaAnnotatedWithAny(item, transactional)) {
      return true;
    }
    Predicate<JavaCodeUnit> uncovered =
        unit ->
            !AnnotationRoles.isMetaAnnotatedWithAny(unit, transactional) && !callsBoundary(unit);
    return !calls.reachableThrough(entry, uncovered).contains(publisher);
  }
```

### `pathName`

```java
/** {@code execute} for the unit itself, {@code execute (via persist)} when reached through it. */
  private static String pathName(JavaCodeUnit entry, JavaCodeUnit unit) {
    return entry.equals(unit) ? entry.getName() : entry.getName() + " (via " + unit.getName() + ")";
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

### `callsBoundary`

```java
private static boolean callsBoundary(JavaCodeUnit unit) {
  return unit.getMethodCallsFromSelf().stream()
      .anyMatch(call -> call.getTargetOwner().isAssignableTo(TransactionBoundary.class));
}
```

### `AnnotationRoles.isMetaAnnotatedWithAny`

```java
/** Meta-annotated with any annotation of the role; false for an empty role. */
  static boolean isMetaAnnotatedWithAny(CanBeAnnotated item, List<String> role) {
    for (String fqn : role) {
      if (item.isMetaAnnotatedWith(fqn)) {
        return true;
      }
    }
    return false;
  }
```

### `IntraClassCalls.reachableThrough`

```java
/**
   * The units reachable from {@code start} on routes that pass only through units satisfying {@code
   * through} - {@code start} included, and only if it satisfies it too. A unit that fails the
   * predicate is not entered, so nothing behind it is reached on that route (it may still be
   * reached on another). Cycle-safe.
   */
  Set<JavaCodeUnit> reachableThrough(JavaCodeUnit start, Predicate<JavaCodeUnit> through) {
    Set<JavaCodeUnit> reached = new LinkedHashSet<>();
    Deque<JavaCodeUnit> pending = new ArrayDeque<>();
    pending.add(start);
    while (!pending.isEmpty()) {
      JavaCodeUnit current = pending.remove();
      if (through.test(current) && reached.add(current)) {
        pending.addAll(callees.getOrDefault(current, Set.of()));
      }
    }
    return reached;
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

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allApplicationPatterns()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Check("DCA-USE-012", "Use cases that save an aggregate or publish domain events must have a transaction boundary",
        "The use case owns the unit of work. Saving an aggregate is one business fact, yet the repository may write it as"
        + " several statements - an aggregate of entities and value objects often spans several tables - and a repository"
        + " adapter draws no boundary of its own; without one, a failure between the statements leaves half an aggregate"
        + " behind. Publishing adds a second effect that must fall with the save: integration-event capture joins the"
        + " modeled transaction, and publication outside a transaction cannot rely on commit semantics. The boundary is"
        + " either the configured transactional attribute (on the class or the executing method) or an explicit"
        + " ITransactionBoundary.InTransactionAsync(...) around load, mutate, save and publish. Checked per entry path,"
        + " following calls within the class: from every entry point - a method callable from outside the class, or one"
        + " nothing in the class calls - no route down to the saving, deleting or publishing method may be free of an"
        + " attribute or a boundary; a covered caller does not cover another route to the same helper, and a boundary on"
        + " one route does not cover a second route",
        arch => {
            var violations = new List<string>();
            foreach (var type in arch.Types.Where(t => OperationPolicy.Operation(t, arch))) {
                var runtime = arch.RuntimeType(type)!;
                var graph = new IntraClassCalls(runtime);
                foreach (var unit in graph.Units) {
                    var effect = TransactionalEffectOf(unit);
                    if (effect is null) continue;
                    foreach (var entry in graph.EntryPointsOf(unit)) {
                        if (!Transactional(runtime, layout.FrameworkTypes.TransactionalAttribute)
                            && graph.ReachableThrough(entry, u => !Transactional(u, layout.FrameworkTypes.TransactionalAttribute) && !CallsBoundary(u)).Contains(unit))
                            violations.Add($"{type.FullName}.{IntraClassCalls.PathName(entry, unit)} {effect} without transaction coverage on every entry path");
                    }
                }
            }
            DcaRule.Fail("Use cases that save, delete or publish require transaction coverage", violations.Distinct().ToList());
        })
    .Selecting("Concrete application operations selected by IInputPort marker or suffix with loadable runtime types, including closure and async units.")
    .Checking("Every entry path to a unit calling IRepository.SaveAsync, IRepository.DeleteByIdAsync or an IDomainEventPublisher crosses a unit calling ITransactionBoundary.InTransactionAsync (including its extension overloads) or carrying the configured TransactionalAttribute; a type-level attribute covers all paths. A use case that neither saves, deletes nor publishes (a query, a Store write) is selected but has nothing to check and passes. Static limit: a boundary call in the same unit passes even when the save or publication follows an empty boundary block. Runtime rollback containment must be tested separately.")
```

### C# helper OperationPolicy

```csharp
using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using System.Runtime.CompilerServices;
using System.Text.RegularExpressions;
using ArchUnitNET.Domain;
using ArchUnitNET.Domain.Extensions;
using DomainCentric.BuildingBlocks.Hexagonal.Ports.In;

namespace DomainCentric.ArchRules.Rules;

internal static class OperationPolicy
{
    internal static bool Operation(IType type, DcaArchitecture arch) => type is Class { IsAbstract: false }
        && arch.RuntimeType(type) is { IsNested: false }
        && Regex.IsMatch(type.Namespace?.FullName ?? "", DcaLayout.AnyOf(arch.AllApplicationPatterns()))
        && (type.IsAssignableTo(typeof(IInputPort).FullName!) || type.Name.EndsWith(arch.Layout.UseCaseSuffix, StringComparison.Ordinal));

    internal static void Invocation(DcaArchitecture arch)
    {
        var violations = new List<string>();
        foreach (var caller in arch.Types.Where(t => Operation(t, arch)))
        {
            var runtime = arch.RuntimeType(caller)!;
            var own = runtime.GetInterfaces().SelectMany(t => new[] {t.FullName, t.IsGenericType ? t.GetGenericTypeDefinition().FullName : t.FullName}).ToHashSet();
            for (var parent = runtime; parent is not null; parent = parent.BaseType) own.Add(parent.FullName);
            Walk(caller, caller, arch, own, new HashSet<IType>(), new List<string>(), violations);
        }
        DcaRule.Fail("Use cases must not invoke other use cases", violations.Distinct().ToList());
    }

    private static void Walk(IType caller, IType current, DcaArchitecture arch, HashSet<string?> own,
        HashSet<IType> seen, List<string> via, List<string> violations)
    {
        if (!seen.Add(current)) return;
        foreach (var target in current.Dependencies.Select(d => d.Target).Distinct())
        {
            if (own.Contains(target.FullName)) continue;
            if (target.IsAssignableTo(typeof(IInputPort).FullName!) || Operation(target, arch))
                violations.Add($"{caller.FullName} -> {target.FullName}" + (via.Count == 0 ? "" : $" [via {string.Join(" -> ", via)}]"));
            else if (target is not Interface && Regex.IsMatch(target.Namespace?.FullName ?? "", DcaLayout.AnyOf(arch.AllApplicationPatterns()))
                && arch.ModuleRootOf(caller.Namespace.FullName) == arch.ModuleRootOf(target.Namespace?.FullName ?? ""))
                Walk(caller, target, arch, own, seen, via.Concat(new[] { target.FullName }).ToList(), violations);
        }
    }

    internal static void Surface(DcaArchitecture arch)
    {
        var violations = new List<string>();
        foreach (var type in arch.Types.Where(t => Operation(t, arch)))
        {
            var runtime = arch.RuntimeType(type)!;
            var methods = runtime.GetInterfaces().Where(i => typeof(IInputPort).IsAssignableFrom(i))
                .SelectMany(i => runtime.GetInterfaceMap(i).TargetMethods).ToHashSet();
            foreach (var method in runtime.GetMethods(BindingFlags.Public | BindingFlags.Instance))
            {
                if (method.DeclaringType == typeof(object) || method.DeclaringType == typeof(ValueType)
                    || method.GetBaseDefinition().DeclaringType == typeof(object)
                    || method.IsDefined(typeof(CompilerGeneratedAttribute), false) || methods.Contains(method)) continue;
                // Property accessors (auto or computed) are reported once, as their property, below.
                if (method.IsSpecialName && (method.Name.StartsWith("get_", StringComparison.Ordinal) || method.Name.StartsWith("set_", StringComparison.Ordinal))) continue;
                violations.Add($"{type.FullName} exposes {method} outside its input port");
            }
            foreach (var property in runtime.GetProperties(BindingFlags.Public | BindingFlags.Instance))
                foreach (var accessor in property.GetAccessors().Where(a => !methods.Contains(a)))
                    violations.Add($"{type.FullName} exposes property {property.Name} ({accessor.Name}) outside its input port");
        }
        DcaRule.Fail("Use cases expose no public operation outside their input port", violations.Distinct().ToList());
    }
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

- [DomainEventPublisher](/marker/port-out/domaineventpublisher.md)
- [InputPort](/marker/port-in/inputport.md)
- [Repository<T, ID>](/marker/port-out/repository.md)
- [TransactionBoundary](/marker/application/transactionboundary.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)

## Evidence slices

- [Overview](/evidence/rule/usecase/dca-use-012/overview.md)
- [`beTransactionalWhenMutating`](/evidence/rule/usecase/dca-use-012/betransactionalwhenmutating.md)
- [`transactionalEffectOf`](/evidence/rule/usecase/dca-use-012/transactionaleffectof.md)
- [`pathIsTransactional`](/evidence/rule/usecase/dca-use-012/pathistransactional.md)
- [`pathName`](/evidence/rule/usecase/dca-use-012/pathname.md)
- [`IntraClassCalls.entryPointsOf`](/evidence/rule/usecase/dca-use-012/intraclasscalls-entrypointsof.md)
- [`calls`](/evidence/rule/usecase/dca-use-012/calls.md)
- [`callsBoundary`](/evidence/rule/usecase/dca-use-012/callsboundary.md)
- [`AnnotationRoles.isMetaAnnotatedWithAny`](/evidence/rule/usecase/dca-use-012/annotationroles-ismetaannotatedwithany.md)
- [`IntraClassCalls.reachableThrough`](/evidence/rule/usecase/dca-use-012/intraclasscalls-reachablethrough.md)
- [`IntraClassCalls.callersOf`](/evidence/rule/usecase/dca-use-012/intraclasscalls-callersof.md)
- [`IntraClassCalls.isEntryPoint`](/evidence/rule/usecase/dca-use-012/intraclasscalls-isentrypoint.md)
- [`IntraClassCalls.closure`](/evidence/rule/usecase/dca-use-012/intraclasscalls-closure.md)
- [C# expression](/evidence/rule/usecase/dca-use-012/c-expression.md)
- [C# helper OperationPolicy](/evidence/rule/usecase/dca-use-012/c-helper-operationpolicy.md)
- [C# helper IntraClassCalls](/evidence/rule/usecase/dca-use-012/c-helper-intraclasscalls.md)
