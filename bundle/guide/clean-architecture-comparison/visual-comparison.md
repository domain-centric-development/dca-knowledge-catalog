---
type: Section
title: Visual Comparison
chapter: Domain-Centric Architecture vs Clean Architecture
source: guide
resource: implementing-domain-centric-architecture/clean-architecture-comparison.md
tags: [guide, section]
---

### Clean Architecture Circle Diagram

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│   ┌───────────────────────────────────────────┐        │
│   │                                           │        │
│   │   ┌─────────────────────────────────┐    │        │
│   │   │                                 │    │        │
│   │   │   ┌───────────────────────┐    │    │        │
│   │   │   │                       │    │    │        │
│   │   │   │     ENTITIES          │    │    │        │
│   │   │   │  (Business Objects)   │    │    │        │
│   │   │   │                       │    │    │        │
│   │   │   └───────────────────────┘    │    │        │
│   │   │                                 │    │        │
│   │   │      USE CASES                  │    │        │
│   │   │   (Application Business         │    │        │
│   │   │       Rules)                    │    │        │
│   │   │                                 │    │        │
│   │   └─────────────────────────────────┘    │        │
│   │                                           │        │
│   │     INTERFACE ADAPTERS                    │        │
│   │  (Controllers, Gateways,                  │        │
│   │       Presenters)                         │        │
│   │                                           │        │
│   └───────────────────────────────────────────┘        │
│                                                         │
│     FRAMEWORKS & DRIVERS                                │
│  (Web, UI, Database, Devices, External)                │
│                                                         │
└─────────────────────────────────────────────────────────┘

Dependencies point INWARD →
```

### Domain-Centric Architecture

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│   ┌───────────────────────────────────────────┐        │
│   │                                           │        │
│   │   ┌─────────────────────────────────┐    │        │
│   │   │                                 │    │        │
│   │   │   ┌───────────────────────┐    │    │        │
│   │   │   │                       │    │    │        │
│   │   │   │     DOMAIN            │    │    │        │
│   │   │   │  Entities             │    │    │        │
│   │   │   │  Value Objects        │    │    │        │
│   │   │   │  Aggregates           │    │    │        │
│   │   │   │  Domain Services      │    │    │        │
│   │   │   │  Domain Events        │    │    │        │
│   │   │   │                       │    │    │        │
│   │   │   └───────────────────────┘    │    │        │
│   │   │                                 │    │        │
│   │   │      APPLICATION                │    │        │
│   │   │   Use Cases                     │    │        │
│   │   │   Input/Output Ports            │    │        │
│   │   │   Commands/Queries              │    │        │
│   │   │                                 │    │        │
│   │   └─────────────────────────────────┘    │        │
│   │                                           │        │
│   │     ADAPTER                               │        │
│   │  Input (Controllers, Consumers)           │        │
│   │  Output (Repositories, Publishers)        │        │
│   │                                           │        │
│   └───────────────────────────────────────────┘        │
│                                                         │
│     INFRASTRUCTURE                                      │
│  (Spring, JPA, Kafka, Configuration)                   │
│                                                         │
└─────────────────────────────────────────────────────────┘

Dependencies point INWARD →
+ Bounded Contexts organize horizontally
```
