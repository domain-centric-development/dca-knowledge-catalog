---
type: Section
title: Checklist for new code
chapter: Quick Reference
source: guide
resource: dca-guide/architecture/quick-reference.md
tags: [guide, section]
---

- [ ] Does this carry business logic (domain) or technical concern (everything else)?
- [ ] Is this interface an input port (an actor calls it) or an output port (the application calls it)?
- [ ] Does this output port stand for something outside the process? Cookies, tokens and a question into the own context are not ports
- [ ] Do all dependencies point inward?
- [ ] Is the domain free of framework annotations?
- [ ] Are the domain model and the persistence model separate types?
- [ ] Does the incoming adapter *use* the input port, and the outgoing adapter *implement* the output port?
- [ ] Does infrastructure do nothing but wiring and configuration?
- [ ] Can the domain and the application layer be tested without a framework?
