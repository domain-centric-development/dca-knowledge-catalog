---
type: Reference
title: "Use cases that save an aggregate must publish its domain events — C# helper IntraClassCalls"
tags: [reference]
evidence_for: "/rule/usecase/dca-use-009.md#c-helper-intraclasscalls"
---

[Full node and context](/rule/usecase/dca-use-009.md#c-helper-intraclasscalls). This is an evidence excerpt; retain the parent selection and caveats.

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
