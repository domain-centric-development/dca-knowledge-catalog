---
type: Section
title: Language Idioms
chapter: "Language Mappings: Java/Spring ↔ C#/.NET"
source: guide
resource: dca-guide/language-mappings.md
tags: [guide, section]
---

| Java | C# |
|---|---|
| `record` for values, commands, results, events | `record` (reference) for values and events, `readonly record struct` for ids, `sealed record` for commands/results |
| `sealed interface` + `permits` | `abstract record` hierarchy or discriminated pattern matching; no `permits` |
| Checked/unchecked exceptions | exceptions only; domain exceptions are unchecked either way |
| `Optional<T>` return | `T?` with nullable reference types enabled |
| `final` class | `sealed` class |
| `static` factory `Order.create(...)` | same, or `Order.Create(...)` |
| Package-private | `internal` (project scope — coarser than a package) |
| `var` | `var` |
| Text blocks `"""` | raw string literals `"""` |
| `List.of(...)` immutability | `IReadOnlyList<T>`, `ImmutableArray<T>` |
