---
type: Section
title: Several factories on one backlog
chapter: "Delivering a story: backlog, stages, gates"
source: guide
resource: dca-guide/process/factory.md
tags: [guide, section]
---

Two colleagues with a clone each see the same backlog, and both would start the same story: a factory knows only
which stories *it* runs. What keeps them apart needs no server of its own, only git. A push that would create a
branch the remote already has, from another commit, is refused — the first push wins, the second loses. So a
factory claims a story before it builds it: one empty commit that says who and which story, pushed create-only as
the story's branch. The one that loses skips the story and says who has it; the schedule shows it claimed
elsewhere. A remote that refuses the push for another reason — a branch rule — or a claim under the same id for a
different story is a question for a person, not a skip.

The factory never pushes the shared main line. A story is merged with the main line as the remote has it, delivered
on its branch — its state and the spec merge in one commit — and the branch is published for a person to merge,
through a merge request or a push. Once the main line says delivered, the next factory that looks deletes the
branch. Two published stories that touch one spec meet when the second is merged: it is delivered again against
the new main line, the spec merged again by key — never resolved by text. A claim nobody finishes stays until a
person gives it up; there is no lease.

It is cooperation, not security. Anyone who may push may delete a branch, and the claim keeps honest factories
apart; who may do what is the code host's permission model. Assigning stories to people, a tracker as the source,
opening merge requests — those are not part of it.
