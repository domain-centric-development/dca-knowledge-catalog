---
type: Section
title: Team Types
chapter: Team Topologies Integration
source: guide
resource: implementing-domain-centric-architecture/team-topologies.md
tags: [guide, section]
---

### Stream-Aligned Team

**Definition:** Team aligned to a single, continuous flow of work (typically one bounded context)

**Characteristics:**
- **Owns one bounded context** (preferred)
- Full-stack capability (UI → Database)
- Can deliver value end-to-end
- Size: 5-9 members (ideal)
- Long-lived, stable team

**Responsibilities:**
- Own domain, application, and adapters (see [Domain-Centric Architecture](/guide/readme/dependency-structure.md))
- Build, deploy, run, maintain
- Respond to user needs
- Continuous delivery

**Example:**
```
Order Team (Stream-Aligned)
├── Owns: Order Bounded Context
├── Full stack: Backend + Frontend + Database
├── Independent deployment
└── End-to-end delivery: Order creation → Payment → Fulfillment
```

### Platform Team

**Definition:** Team providing internal platform/infrastructure as a service

**Characteristics:**
- **Reduces cognitive load** of stream-aligned teams
- Provides self-service capabilities
- Clear API/interface
- Treats stream-aligned teams as customers

**Services Provided:**
- Database provisioning
- Message broker (Kafka, RabbitMQ)
- CI/CD pipelines
- Monitoring/observability
- Cloud infrastructure
- Developer tools

**Example:**
```
Platform Team
├── Provides: Postgres Database as a Service
├── API: Self-service provisioning
├── SLA: 99.9% uptime
└── Customers: All stream-aligned teams
```

**Interaction Mode:** X-as-a-Service (stream-aligned teams consume platform services)

### Enabling Team

**Definition:** Team helping stream-aligned teams overcome obstacles and learn new capabilities

**Characteristics:**
- Deep technical expertise
- **Facilitating interaction mode**
- Time-limited engagement
- Teaches, doesn't do the work
- Doesn't own production systems

**Helps With:**
- Adopting new technologies
- Implementing architectural patterns (e.g., DDD, CQRS)
- Performance optimization
- Security practices
- Testing strategies

**Example:**
```
Enabling Team
├── Expertise: DDD, Event Sourcing, CQRS
├── Engagement: 2-week pairing with Inventory Team
├── Goal: Transfer knowledge on implementing Event Sourcing
└── Outcome: Inventory Team becomes self-sufficient
```

**Interaction Mode:** Facilitating (temporary knowledge transfer)

### Complicated-Subsystem Team

**Definition:** Team owning a complex technical component requiring specialist knowledge

**Characteristics:**
- High complexity requires dedicated focus
- Reduces cognitive load for stream-aligned teams
- Provides X-as-a-Service interface
- **Rare** - only when truly necessary

**Examples:**
- ML/AI models
- Complex pricing algorithms
- Video encoding/processing
- Geospatial calculations

**Example:**
```
Pricing Engine Team (Complicated-Subsystem)
├── Owns: Complex ML-based pricing algorithm
├── Provides: Pricing API
├── Hides: ML model complexity
└── Consumers: Order Team, Customer Team
```

**Interaction Mode:** X-as-a-Service (stream-aligned teams consume via API)
