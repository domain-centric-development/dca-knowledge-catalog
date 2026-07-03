---
type: Section
title: Team Interaction Modes
chapter: Team Topologies Integration
source: guide
resource: implementing-domain-centric-architecture/team-topologies.md
tags: [guide, section]
---

### Collaboration Mode

**When:** Discovery and rapid learning

**Characteristics:**
- Two teams work closely together
- High communication bandwidth
- Time-limited (weeks to months)
- Use when building new capabilities
- Use when integration points are unclear

**Example:**
```
Order Team ↔ Inventory Team (Collaboration)
├── Goal: Define integration for stock reservation
├── Duration: 4 weeks
├── Activities: Pair programming, daily syncs, shared design
└── Outcome: Clear API contract, switch to X-as-a-Service
```

**Transition:** Switch to X-as-a-Service when interfaces stabilize

### X-as-a-Service Mode

**When:** Stable, well-defined interfaces

**Characteristics:**
- Clear API/interface between teams
- Minimal collaboration required
- Versioned APIs
- Service-level expectations defined
- Self-service where possible

**Example:**
```
Order Team → Platform Team (X-as-a-Service)
├── Order Team consumes: Database provisioning API
├── SLA: Database available in <10 minutes
├── Documentation: Self-service portal
└── Communication: Minimal (via API)
```

**Primary Mode For:**
- Stream-aligned ↔ Platform
- Stream-aligned ↔ Complicated-Subsystem
- Stable integrations between stream-aligned teams

### Facilitating Mode

**When:** Learning and capability building

**Characteristics:**
- Enabling team helps stream-aligned team
- Teaching and mentoring focus
- Time-limited engagement
- Stream-aligned team retains ownership
- Goal: increase capability, not create dependency

**Example:**
```
Enabling Team → Customer Team (Facilitating)
├── Request: Help implementing CQRS pattern
├── Engagement: 2 weeks embedded pairing
├── Ownership: Remains with Customer Team
└── Outcome: Customer Team can apply CQRS independently
```

**Primary Mode For:**
- Enabling team ↔ Stream-aligned team
