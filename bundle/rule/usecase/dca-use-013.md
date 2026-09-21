---
type: Rule
id: DCA-USE-013
title: Declaratively transactional use cases must not call remote-capable output ports
rule: "A declaratively transactional use case holds a database connection for its whole run. Calling an output port that may leave the process (another context's API, a payment provider, a mail gateway) inside it blocks that connection for the remote round trip; under load the pool runs dry, and a rollback cannot undo the remote effect. Only transactional resources belong inside the boundary: Repository, Store, DomainEventPublisher, IntegrationEventPublisher. Everything else is called before the transaction - draw the boundary by hand with TransactionBoundary.inTransaction(...) - or after it, as a reaction to an integration event."
constraint: Declaratively transactional use cases must not call remote-capable output ports.
selects: "Non-interface classes in <module>.application.. that implement InputPort or whose simple name ends with the configured use-case suffix."
checks: "Every method that runs under one of the configured transactional annotations - on the class, on itself, or on a method that reaches it within the class - calls no OutputPort other than Repository, Store, DomainEventPublisher or IntegrationEventPublisher. A use case without such an annotation (explicit TransactionBoundary or none) is selected but never reported; with an empty role nothing is ever reported."
enforced_by: "UseCaseRules#DCA-USE-013"
status: enforced
rule_set: usecase
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/UseCaseRules.java
tags: [usecase, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/UseCaseRules.cs
---

# Declaratively transactional use cases must not call remote-capable output ports

## Selection

Non-interface classes in <module>.application.. that implement InputPort or whose simple name ends with the configured use-case suffix.

## Check

Every method that runs under one of the configured transactional annotations - on the class, on itself, or on a method that reaches it within the class - calls no OutputPort other than Repository, Store, DomainEventPublisher or IntegrationEventPublisher. A use case without such an annotation (explicit TransactionBoundary or none) is selected but never reported; with an empty role nothing is ever reported.

## .NET reading

**Selection.** Concrete application operations selected by IInputPort marker or configured use-case suffix, with loadable runtime types. Nothing at all while no transactional attribute is configured, which is the default: neither .NET preset names one, because ASP.NET Core has no ambient transaction attribute.

**Check.** Every code unit that runs under the configured transactional attribute - on the class, on itself, or on an entry point that reaches it within the class - calls no output port other than IRepository, IStore, IDomainEventPublisher or IIntegrationEventPublisher. A use case without such an attribute (an explicit ITransactionBoundary, or none) is selected but never reported, and with no attribute configured nothing is ever reported - the rule then carries the id without checking anything, as the Java twin does where no framework annotation is on the class path. What happens inside an InTransactionAsync block is not inspected; the explicit boundary is the developer's own and its extent is visible at the call site.

## Implementation

```java
DcaRule.of(
        "DCA-USE-013",
        "Declaratively transactional use cases must not call remote-capable output ports",
        "A declaratively transactional use case holds a database connection for its whole run."
            + " Calling an"
            + " output port that may leave the process (another context's API, a payment provider,"
            + " a mail gateway) inside it blocks that connection for the remote round trip; under"
            + " load the pool runs dry, and a rollback cannot undo the remote effect. Only"
            + " transactional resources belong inside the boundary: Repository, Store,"
            + " DomainEventPublisher, IntegrationEventPublisher. Everything else is called before"
            + " the transaction - draw the boundary by hand with TransactionBoundary.inTransaction(...)"
            + " - or after it, as a reaction to an integration event",
        arch ->
            classes()
                .that(useCases(arch, layout))
                .should(
                    notCallRemotePortsWhenTransactional(
                        layout.frameworkAnnotations().transactional(), layout.markers()))
                .allowEmptyShould(true))
    .selecting(
        "Non-interface classes in <module>.application.. that implement InputPort or whose simple name ends with the configured use-case suffix.")
    .checking(
        "Every method that runs under one of the configured transactional annotations - on the"
            + " class, on itself, or on a method that reaches it within the class - calls no"
            + " OutputPort other than Repository, Store, DomainEventPublisher or"
            + " IntegrationEventPublisher. A use case without such an annotation (explicit"
            + " TransactionBoundary or none) is selected but never reported; with an empty role"
            + " nothing is ever reported.")
```

## Helpers

### `useCases`

```java
/**
   * The documented use-case selection: a non-interface class in an application package that either
   * carries the configured use-case suffix or implements the input-port role.
   *
   * <p>Spelled inline, ArchUnit joins {@code and}/{@code or} left to right, so {@code
   * resideInAnyPackage(app).and().haveSimpleNameEndingWith(suffix).or().areAssignableTo(port)
   * .and().areNotInterfaces()} reads {@code ((inApplication ∧ suffix) ∨ isInputPort) ∧ ¬interface}
   * and selects every input-port implementation anywhere, adapters included — which is neither what
   * the rule texts say nor what the .NET twin does.
   */
  private static DescribedPredicate<JavaClass> useCases(DcaArchitecture arch, DcaLayout layout) {
    DescribedPredicate<JavaClass> inApplication =
        JavaClass.Predicates.resideInAnyPackage(arch.allApplicationPatterns());
    DescribedPredicate<JavaClass> named =
        JavaClass.Predicates.simpleNameEndingWith(layout.useCaseSuffix());
    DescribedPredicate<JavaClass> port =
        JavaClass.Predicates.assignableTo(arch.layout().markers().inputPort());
    return inApplication
        .and(named.or(port))
        .and(DescribedPredicate.not(JavaClass.Predicates.INTERFACES))
        .as(
            "non-interface classes in an application package that implement the input port or end"
                + " with \"%s\"",
            layout.useCaseSuffix());
  }
```

### `notCallRemotePortsWhenTransactional`

```java
private static ArchCondition<JavaClass> notCallRemotePortsWhenTransactional(
    List<String> transactional, DcaMarkers markers) {
  return new ArchCondition<>("not call remote-capable output ports while transactional") {
    @Override
    public void check(JavaClass item, ConditionEvents events) {
      IntraClassCalls calls = new IntraClassCalls(item);
      for (JavaCodeUnit unit : item.getCodeUnits()) {
        if (!isTransactional(item, unit, calls, transactional)) {
          continue;
        }
        List<String> remotePorts =
            unit.getMethodCallsFromSelf().stream()
                .map(call -> call.getTargetOwner())
                .filter(owner -> owner.isAssignableTo(markers.outputPort()))
                .filter(owner -> !isTransactionalResource(owner, markers))
                .map(JavaClass::getSimpleName)
                .distinct()
                .sorted()
                .toList();
        if (!remotePorts.isEmpty()) {
          events.add(
              SimpleConditionEvent.violated(
                  item,
                  item.getSimpleName()
                      + "."
                      + unit.getName()
                      + " runs under "
                      + FrameworkAnnotations.describe(transactional, "a transaction annotation")
                      + " and calls "
                      + String.join(", ", remotePorts)
                      + " inside the transaction - call it before, or draw the boundary with"
                      + " TransactionBoundary.inTransaction(...)"));
        }
      }
    }
  };
}
```

### `isTransactional`

```java
/**
   * Whether the unit may run inside declared transaction metadata: the class is annotated, the unit
   * is, or a unit that reaches it through calls within the class is. Used where one covered path is
   * enough to matter (a remote call inside a transaction).
   */
  private static boolean isTransactional(
      JavaClass item, JavaCodeUnit unit, IntraClassCalls calls, List<String> transactional) {
    return AnnotationRoles.isMetaAnnotatedWithAny(item, transactional)
        || calls.callersOf(unit).stream()
            .anyMatch(u -> AnnotationRoles.isMetaAnnotatedWithAny(u, transactional));
  }
```

### `isTransactionalResource`

```java
/**
   * Output ports that live inside the transaction; every other output port may leave the process.
   */
  private static boolean isTransactionalResource(JavaClass owner, DcaMarkers markers) {
    return owner.isAssignableTo(markers.repository())
        || owner.isAssignableTo(markers.store())
        || owner.isAssignableTo(markers.domainEventPublisher())
        || owner.isAssignableTo(markers.integrationEventPublisher());
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

### `IntraClassCalls.callersOf`

```java
/** The unit itself and every unit that reaches it through calls within the class. */
  Set<JavaCodeUnit> callersOf(JavaCodeUnit unit) {
    return closure(unit, callers);
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

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allApplicationPatterns()`, `layout()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Check("DCA-USE-013", "Declaratively transactional use cases must not call remote-capable output ports",
        "A declaratively transactional use case holds a database connection for its whole run. Calling an output port"
        + " that may leave the process (another context's API, a payment provider, a mail gateway) inside it blocks"
        + " that connection for the remote round trip; under load the pool runs dry, and a rollback cannot undo the"
        + " remote effect. Awaiting the call does not help: the thread is released, the transaction and its connection"
        + " are not. Only transactional resources belong inside the boundary: IRepository, IStore,"
        + " IDomainEventPublisher, IIntegrationEventPublisher. Everything else is called before the transaction - draw"
        + " the boundary by hand with ITransactionBoundary.InTransactionAsync(...) - or after it, as a reaction to an"
        + " integration event",
        arch => {
            var attribute = layout.FrameworkTypes.TransactionalAttribute;
            var violations = new List<string>();
            if (FrameworkTypes.IsSet(attribute)) {
                foreach (var type in arch.Types.Where(t => OperationPolicy.Operation(t, arch))) {
                    var runtime = arch.RuntimeType(type)!;
                    var graph = new IntraClassCalls(runtime);
                    foreach (var unit in graph.Units) {
                        if (!Transactional(runtime, attribute)
                            && !graph.EntryPointsOf(unit).Any(entry =>
                                Transactional(entry, attribute)
                                || !graph.ReachableThrough(entry, u => !Transactional(u, attribute)).Contains(unit)))
                            continue;
                        var remotePorts = RemotePortsCalledBy(unit, arch).ToList();
                        if (remotePorts.Count == 0) continue;
                        violations.Add(
                            $"{type.FullName}.{IntraClassCalls.DisplayName(unit)} runs under {attribute} and calls "
                            + string.Join(", ", remotePorts)
                            + " inside the transaction - call it before, or draw the boundary with"
                            + " ITransactionBoundary.InTransactionAsync(...)");
                    }
                }
            }

            DcaRule.Fail(
                "Declaratively transactional use cases must not call remote-capable output ports",
                violations.Distinct().ToList(),
                "call the remote port before the transaction, or draw the boundary explicitly with"
                + " ITransactionBoundary.InTransactionAsync(...) around the transactional part only");
        })
    .Selecting("Concrete application operations selected by IInputPort marker or configured use-case suffix, with loadable runtime types. Nothing at all while no transactional attribute is configured, which is the default: neither .NET preset names one, because ASP.NET Core has no ambient transaction attribute.")
    .Checking("Every code unit that runs under the configured transactional attribute - on the class, on itself, or on an entry point that reaches it within the class - calls no output port other than IRepository, IStore, IDomainEventPublisher or IIntegrationEventPublisher. A use case without such an attribute (an explicit ITransactionBoundary, or none) is selected but never reported, and with no attribute configured nothing is ever reported - the rule then carries the id without checking anything, as the Java twin does where no framework annotation is on the class path. What happens inside an InTransactionAsync block is not inspected; the explicit boundary is the developer's own and its extent is visible at the call site.")
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
        && (type.IsAssignableTo(arch.Layout.Markers.InputPort) || type.Name.EndsWith(arch.Layout.UseCaseSuffix, StringComparison.Ordinal));

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
            if (target.IsAssignableTo(arch.Layout.Markers.InputPort) || Operation(target, arch))
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
            var methods = runtime.GetInterfaces().Where(i => DcaMarkers.IsAssignableToByName(i, arch.Layout.Markers.InputPort))
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
    public static bool Calls(MethodBase unit, string method, string marker) =>
        IlCalls(unit).Any(m => m.Name == method && m.DeclaringType is not null && DcaMarkers.IsAssignableToByName(m.DeclaringType, marker));

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
- [IntegrationEventPublisher](/marker/port-out/integrationeventpublisher.md)
- [OutputPort](/marker/port-out/outputport.md)
- [Repository<T, ID>](/marker/port-out/repository.md)
- [TransactionBoundary](/marker/application/transactionboundary.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)

## Evidence slices

- [Overview](/evidence/rule/usecase/dca-use-013/overview.md)
- [`useCases`](/evidence/rule/usecase/dca-use-013/usecases.md)
- [`notCallRemotePortsWhenTransactional`](/evidence/rule/usecase/dca-use-013/notcallremoteportswhentransactional.md)
- [`isTransactional`](/evidence/rule/usecase/dca-use-013/istransactional.md)
- [`isTransactionalResource`](/evidence/rule/usecase/dca-use-013/istransactionalresource.md)
- [`AnnotationRoles.isMetaAnnotatedWithAny`](/evidence/rule/usecase/dca-use-013/annotationroles-ismetaannotatedwithany.md)
- [`IntraClassCalls.callersOf`](/evidence/rule/usecase/dca-use-013/intraclasscalls-callersof.md)
- [`IntraClassCalls.closure`](/evidence/rule/usecase/dca-use-013/intraclasscalls-closure.md)
- [C# expression](/evidence/rule/usecase/dca-use-013/c-expression.md)
- [C# helper OperationPolicy](/evidence/rule/usecase/dca-use-013/c-helper-operationpolicy.md)
- [C# helper IntraClassCalls](/evidence/rule/usecase/dca-use-013/c-helper-intraclasscalls.md)
