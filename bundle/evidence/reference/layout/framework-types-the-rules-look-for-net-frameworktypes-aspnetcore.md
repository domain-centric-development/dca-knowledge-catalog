---
type: Reference
title: "DcaLayout — Framework types the rules look for (.NET, `FrameworkTypes.AspNetCore()`)"
tags: [reference]
evidence_for: "/reference/layout.md#framework-types-the-rules-look-for-net-frameworktypesaspnetcore"
---

[Full node and context](/reference/layout.md#framework-types-the-rules-look-for-net-frameworktypesaspnetcore). This is an evidence excerpt; retain the parent selection and caveats.

### Framework types the rules look for (.NET, `FrameworkTypes.AspNetCore()`)

Types are matched by full name and grouped by role; `DcaLayout` defaults to the `AspNetCore()` preset, `None()` leaves every role empty (controllers are then recognised by suffix only), and a `with` expression adjusts single roles. The preset in use is part of the layout's `ToString()`.

| Role | `AspNetCore()` | Used for |
|---|---|---|
| `ControllerBase` | `Microsoft.AspNetCore.Mvc.ControllerBase` | Base class of server-rendering and API controllers. |
| `ApiControllerAttribute` | `Microsoft.AspNetCore.Mvc.ApiControllerAttribute` | Attribute marking API controllers. |
| `PageModelBase` | `Microsoft.AspNetCore.Mvc.RazorPages.PageModel` | Base class of page models (server-rendered pages without a controller). |
| `TransactionScope` | `System.Transactions.TransactionScope` | Type used for explicit transaction demarcation. |
| `TransactionalAttribute` | `(empty)` | Optional declarative transaction attribute used to cover publication entry paths. |
| `PersistenceAttributeNamespaces` | `System.ComponentModel.DataAnnotations.Schema, Microsoft.EntityFrameworkCore` | Attribute namespaces classified as persistence metadata, including derived attributes. |
| `InjectionAttributeNamespaces` | `Microsoft.Extensions.DependencyInjection` | Attribute namespaces classified as injection-site metadata. |
| `TransactionAttributeNamespaces` | `(empty)` | Attribute namespaces classified as transaction metadata. |
| `ContainerAttributeNamespaces` | `(empty)` | Attribute namespaces classified as container stereotypes. |
| `role` | `(empty)` | Whether a role is configured (non-blank). |
| `ToString` | `(empty)` |  |

.NET has no injectable stereotype attribute; the Java rules that depend on one have no .NET reading and are listed as not applicable in the rule catalog.
