---
type: Section
title: "Escalation: the three answers a run may not give itself"
chapter: "Delivering a story: backlog, stages, gates"
source: guide
resource: dca-guide/process/factory.md
tags: [guide, section]
---

The judge returns exactly one of three verdicts, and the third is the reason this list exists:

- **pass** — the criteria are met and no confirmed defect blocks them.
- **changes-requested** — confirmed defects go back to the build stage with their evidence. Count
  the rounds and stop at three: a loop that will not converge needs a human, not a fourth attempt.
- **story-conflict** — the story or the plan is wrong. This never goes back to the build stage. A
  correction that changes an agreed criterion must not happen silently; the story is the contract,
  and a human decides it.

Two more questions belong to a human by construction, and a run that meets one of them stops and
says so instead of answering it:

- **A new bounded context, or a new relationship between contexts.** That is a decision about
  language boundaries and ownership, recorded as a decision and reflected on the context map — never
  smuggled in by a story.
- **A surface the story's actor does not have.** If the criteria can only be observed through a page
  or an endpoint the context does not offer, adding one is a product decision, and where the surface
  needs a guard it is an authorisation decision as well. A guard nobody decided is a guard no test
  holds.

**The question is a file, and so is the answer.** A run that stops writes the question as a record
of its own — the story it blocks, the stage that asked, the options it sees, its recommendation —
never into a chat and never as an answer. Whoever decides writes the answer into that record with
their name and the time; a recommendation, a default, a timeout or an unsigned draft is not one.
The stage that asked runs again with the answer in front of it, and a check that reads the record
— not the stage's word — refuses the story while the question is open and marks the record applied
once the stage has taken it up. Three things follow: the question survives the session, a second
person can answer it without the first one's transcript, and nobody can mistake a suggestion for a
decision.
