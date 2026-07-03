---
type: Section
title: Migration Path
chapter: Domain-Centric Architecture vs Clean Architecture
source: guide
resource: implementing-domain-centric-architecture/clean-architecture-comparison.md
tags: [guide, section]
---

### From Clean Architecture to Domain-Centric Architecture

If you have a Clean Architecture application and want to adopt Domain-Centric patterns:

**Step 1: Identify Bounded Contexts**
- Analyze your domain
- Identify natural boundaries
- Group related use cases

**Step 2: Introduce DDD Patterns**
- Enrich Entities with behavior
- Introduce Value Objects
- Define Aggregates
- Add Domain Services

**Step 3: Add Domain Events**
- Identify domain events
- Implement event publishing
- Add event handlers

**Step 4: Reorganize Packages**
- Group by bounded context
- Maintain layer structure within contexts
- Separate domain/integration events

**Step 5: Define Strategic Patterns**
- Create Context Map
- Define context relationships
- Add Anti-Corruption Layers

### From Domain-Centric Architecture to Clean Architecture

If Domain-Centric Architecture is too complex for your needs:

**Step 1: Simplify Domain Model**
- Convert complex Aggregates to simple Entities
- Remove Domain Events if not needed
- Simplify Value Objects to primitives

**Step 2: Flatten Structure**
- Remove bounded context grouping
- Organize by layer only
- Merge contexts if appropriate

**Step 3: Adopt Presenter Pattern** (optional)
- Replace DTOs with Presenters
- Add View Models
- Separate presentation logic
