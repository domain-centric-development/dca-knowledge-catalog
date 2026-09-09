---
type: Reference
title: "DcaLayout — Settings and defaults (.NET)"
tags: [reference]
evidence_for: "/reference/layout.md#settings-and-defaults-net"
---

[Full node and context](/reference/layout.md#settings-and-defaults-net). This is an evidence excerpt; retain the parent selection and caveats.

### Settings and defaults (.NET)

Create the default layout with `DcaLayout.ForRootNamespace(string)`.

| Setting | Default | Override |
|---|---|---|
| `SharedKernelSegment` | `SharedKernel` | `WithSharedKernelSegment(...)` |
| `DomainSegment` | `Domain` | `WithDomainSegment(...)` |
| `ApplicationSegment` | `Application` | `WithApplicationSegment(...)` |
| `AdapterSegment` | `Adapter` | `WithAdapterSegment(...)` |
| `IncomingSegment` | `Incoming` | `WithIncomingSegment(...)` |
| `OutgoingSegment` | `Outgoing` | `WithOutgoingSegment(...)` |
| `InfrastructureSegment` | `Infrastructure` | `WithInfrastructureSegment(...)` |
| `ApiSegment` | `Api` | `WithApiSegment(...)` |
| `EventsSegment` | `Events` | `WithEventsSegment(...)` |
| `UseCaseSuffix` | `UseCase` | `WithUseCaseSuffix(...)` |
| `ControllerSuffix` | `Controller` | `WithControllerSuffix(...)` |
| `RestControllerSuffix` | `Controller` | `WithRestControllerSuffix(...)` |
