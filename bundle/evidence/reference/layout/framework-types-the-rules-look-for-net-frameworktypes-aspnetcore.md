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
| `TransactionApiTypes` | `System.Transactions.CommittableTransaction, System.Data.IDbTransaction, System.Data.Common.DbTransaction, Microsoft.EntityFrameworkCore.Storage.IDbContextTransaction` | Full type names of the APIs code *uses* to run a transaction beside `TransactionScope` — committable transactions, connection transactions, a persistence library's transaction handle. Like the scope they belong to the application layer and the outgoing adapters; any other type that depends on one is reported. |
| `TransactionManagerTypes` | `(empty)` | Full type names a composition root *declares or wires* (a transaction manager). The global and the shared kernel's infrastructure may depend on them; the domain, incoming adapters and a module's own infrastructure may not. Empty by default — the platform has no such type; a project's own manager abstraction is added via a with-expression. |
| `PersistenceAttributeNamespaces` | `System.ComponentModel.DataAnnotations.Schema, Microsoft.EntityFrameworkCore` | Attribute namespaces classified as persistence metadata, including derived attributes. |
| `PersistenceAttributeTypes` | `System.ComponentModel.DataAnnotations.KeyAttribute, System.ComponentModel.DataAnnotations.TimestampAttribute, System.ComponentModel.DataAnnotations.ConcurrencyCheckAttribute` | Full attribute type names classified as persistence metadata (base types included) — for mapping attributes that live in a namespace whose other attributes are harmless, such as the key/concurrency attributes beside the validation attributes of System.ComponentModel.DataAnnotations. Mappings of other persistence libraries are added per project via a with-expression. |
| `InjectionAttributeNamespaces` | `Microsoft.Extensions.DependencyInjection` | Attribute namespaces classified as injection-site metadata. |
| `TransactionAttributeNamespaces` | `(empty)` | Attribute namespaces classified as transaction metadata. |
| `ContainerAttributeNamespaces` | `(empty)` | Attribute namespaces classified as container stereotypes. |
| `WebControllerAttributeNamespaces` | `(empty)` | Attribute namespaces classified as a web-controller stereotype — the counterpart of the Java library's `webController` role. Empty in every preset: ASP.NET Core has no attribute that makes a class a controller, and none that could sit on an exception. The role exists so that `DCA-ERR-004` has the same contract in both languages and a project whose framework does have such an attribute can name it. |
| `RestControllerAttributeNamespaces` | `(empty)` | Attribute namespaces classified as a REST-controller stereotype — the counterpart of the Java library's `restController` role. `[ApiController]` is not classified here: it marks a controller, not a failure, and no exception can carry it. Empty in every preset, for the same reason as `WebControllerAttributeNamespaces`. |
| `ModuleDeclarationAttributeTypes` | `(empty)` | Full type names of a module system's per-package module declaration — the counterpart of the Java library's `moduleDeclaration` role, where Spring Modulith's `@ApplicationModule` fills it. `DCA-MAP-006` reads the declaration's `AllowedDependencies` and compares it with the `[Upstream]` declarations. Empty in every preset: .NET draws module boundaries with projects rather than with an attribute, so a project that has such an attribute names it. |
| `EventListenerAttributeNamespaces` | `(empty)` | Attribute namespaces classified as an event-listener stereotype — the counterpart of the Java library's `eventListener` role. Empty in every preset: .NET subscribes in code, not through an attribute. |
| `TransportStatusAttributeTypes` | `(empty)` | Full attribute type names that fix the protocol answer of the type they sit on — the role `DCA-ERR-004` forbids on the exceptions of the domain and application layers, because which status a failure earns is the incoming adapter's decision and a second adapter on another protocol has no use for it. Empty in every preset: the platform answers through a mapper type rather than through an attribute on the failure. A project that defines such an attribute itself adds it via a with-expression, and the Java library's `transportStatus` role is the same setting under the same rule. |
| `PresetNames` | `(empty)` | The names the presets are known under, for `dca.framework` and error messages. |
| `name` | `(empty)` | The preset registered under the given name, or `null` when there is none. This is what `dca.framework=<name>` in `dca-archunit.properties` resolves, matching `dca-archunit`'s `FrameworkAnnotations.preset(name)`. Names are compared case-insensitively.  Unlike the Java library this has no provider SPI yet: a framework without a preset here is configured in code with a `with` expression on `None`. |
| `role` | `(empty)` | Whether a role is configured (non-blank). |
| `ToString` | `(empty)` |  |

.NET has no injectable stereotype attribute; the Java rules that depend on one have no .NET reading and are listed as not applicable in the rule catalog.
