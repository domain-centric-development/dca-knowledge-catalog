---
type: Reference
title: "JAVA PACKAGE STRUCTURE — Structure Evolution Example: From Startup to Maturity"
tags: [reference]
evidence_for: "/guide/readme/java-package-structure.md#structure-evolution-example-from-startup-to-maturity"
---

[Full node and context](/guide/readme/java-package-structure.md#structure-evolution-example-from-startup-to-maturity). This is an evidence excerpt; retain the parent selection and caveats.

### Structure Evolution Example: From Startup to Maturity

This example shows how a bounded context's structure naturally evolves as complexity grows. For detailed progressive complexity guidelines, see the original structure above.

---

**Use Case Organization - Self-Contained Pattern:**

```
APPLICATION LAYER
├── createorder/                   (USE CASE - All related files together)
│   ├── CreateOrderInputPort.java      ← Input Port Interface
│   │   interface CreateOrderInputPort extends UseCase<CreateOrderCommand, CreateOrderResult>
│   ├── CreateOrderUseCase.java        ← Use Case Implementation
│   │   @Service class CreateOrderUseCase implements CreateOrderInputPort
│   ├── CreateOrderCommand.java        ← Input Model (Command for writes)
│   └── CreateOrderResult.java       ← Output Model
│
├── findorder/                     (USE CASE - All related files together)
│   ├── FindOrderInputPort.java        ← Input Port Interface
│   ├── FindOrderUseCase.java          ← Use Case Implementation
│   ├── OrderQuery.java                ← Input Model (Query for reads)
│   └── OrderResult.java             ← Output Model
│
├── cancelorder/                   (USE CASE - All related files together)
│   ├── CancelOrderInputPort.java      ← Input Port Interface
│   ├── CancelOrderUseCase.java        ← Use Case Implementation
│   ├── CancelOrderCommand.java        ← Input Model
│   └── CancelOrderResult.java       ← Output Model
│
└── shared/                        (SHARED OUTPUT PORTS)
    ├── OrderRepository.java           ← Output Port (used by multiple use cases)
    ├── PaymentGateway.java            ← Output Port
    ├── InventoryService.java          ← Output Port
    └── DomainEventPublisher.java      ← Output Port
```

**Key Principles:**

1. **Each use case is self-contained** in its own folder with ALL related files
2. **InputPort interface** lives WITH the use case, not in a separate port/in/ directory
3. **UseCase implementation** lives WITH the InputPort in the same folder
4. **Command/Query and Result** models live WITH the use case
5. **Output Ports** (repositories, gateways) are shared across use cases in `shared/` directory

**Naming Convention:**
- **Use Case Folders**: lowercase (e.g., `createorder`, `findorder`, `cancelorder`)
- **Input Ports**: `*InputPort extends UseCase<INPUT, OUTPUT>` (e.g., `CreateOrderInputPort extends UseCase<CreateOrderCommand, CreateOrderResult>`)
- **Output Ports**: Domain-specific names (e.g., `OrderRepository`, `PaymentGateway`, `DomainEventPublisher`)
- **Use Case Implementation**: `*UseCase implements *InputPort` (e.g., `CreateOrderUseCase implements CreateOrderInputPort`)
- **Commands**: `*Command` (e.g., `CreateOrderCommand`)
- **Queries**: `*Query` (e.g., `OrderQuery`)
- **Results**: `*Result` (e.g., `CreateOrderResult`) — top level only; part records nested in the result are named by content (`CartItemSummary`, `LineItemData`, `ProfileView`), never `*Result`
- **Assemblers**: `*Assembler` when result assembly outgrows a static factory or is shared by several use cases (e.g., `ProductArticleAssembler` in `application/shared`) — never `*Mapper`, `*Converter` or `*Helper` in the application layer
- **Adapters**: `*Adapter` or specific suffixes (e.g., `InMemoryOrderRepository`, `OrderPageController`, `OrderMcpToolProvider`)
- **Host-language spelling**: marker and port names follow the host language's convention — Java `AggregateRoot`, `UseCase<I, O>`, `OrderRepository`; C# `IAggregateRoot`, `IUseCase<TIn, TOut>`, `IOrderRepository` with `ExecuteAsync`/`FindByIdAsync`. The roles, folders and rule ids are the same; see [Language Mappings](/guide/language-mappings.md)

**Benefits:**
- ✅ **High Cohesion** - All files for one use case are together
- ✅ **Single Responsibility** - One folder = one business operation
- ✅ **Easy Navigation** - Find everything related to a use case in one place
- ✅ **Better Scalability** - Structure grows linearly with use cases
- ✅ **Minimal Coupling** - Use cases are independent, share only via output ports
- ✅ **Clear Dependencies** - Use case depends on domain + application output ports (local or shared)
- ✅ **Adapters clearly separated** - `adapter/incoming` and `adapter/outgoing`
- ✅ **Self-documenting** - Folder name = business operation name
- ✅ **Team-friendly** - Different developers can work on different use cases independently

**When the flat list outgrows itself — features:**

```
APPLICATION LAYER (grouped form)
├── ordering/                      (FEATURE - a term of the ubiquitous language)
│   ├── createorder/                   ← use case, unchanged inside
│   ├── updateorder/
│   └── cancelorder/
├── fulfilment/                    (FEATURE)
│   ├── shiporder/
│   └── trackshipment/
├── reporting/                     (FEATURE)
│   └── findorder/
└── shared/                        (CONTEXT-WIDE OUTPUT PORTS - not per feature)
    ├── OrderRepository.java
    └── PaymentGateway.java
```

The use-case packages are untouched by the move — only their parent changes. The domain layer is not
mirrored: `Order` serves `ordering`, `fulfilment` and `reporting` alike. See
[Grouping use cases into features](#grouping-use-cases-into-features) for the rules.
