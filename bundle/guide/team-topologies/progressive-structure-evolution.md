---
type: Section
title: Progressive Structure Evolution
chapter: Team Topologies Integration
source: guide
resource: implementing-domain-centric-architecture/team-topologies.md
tags: [guide, section]
---

Teams and architecture should evolve together. For detailed package structure evolution, see [Domain-Centric Architecture - Progressive Complexity](/guide/readme/java-package-structure.md).

### Phase 1: New Stream-Aligned Team (Week 1-2)

**Team Context:**
- Team just formed
- Learning domain and DDD patterns
- **Enabling team may be embedded** to teach
- **Collaboration mode** with other teams for discovery

**Technical Structure:**
- Flat directories within each layer
- ~10-15 files total
- Focus on shipping value, not perfect structure

### Phase 2: Growing Team (Month 2-3)

**Team Context:**
- Team becoming autonomous
- **Transitioning to X-as-a-Service mode** with other teams
- Less enabling team involvement
- Focus on scaling features

**Technical Structure:**
- Added subdirectories for organization
- ~25-30 files
- Use cases still relatively flat

### Phase 3: Mature Team (Month 6+)

**Team Context:**
- **Team fully autonomous**
- **Clear team APIs** (Input Ports, Integration Events, REST)
- **X-as-a-Service mode** with all teams
- Team makes independent architectural decisions

**Technical Structure:**
- Full subdivision per layer
- 60+ files, well-organized
- DTOs, mappers, and ACLs separated
