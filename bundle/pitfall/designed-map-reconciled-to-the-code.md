---
type: Pitfall
title: Designed context map reconciled to the code
tags: [pitfall, strategic, context-map, bounded-context]
review: draft
owner: DCA catalog maintainers
evidence: [/rule/contextmap/dca-map-001.md]
---

A project keeps a context map written before the code — the contexts it means to have, their subdomain types, the relationships it intends and why — and, once the code exists, a second map generated from it. The two disagree, and someone "fixes" the difference: the designed map is edited until it matches what was built, or the generated one is copied over the designed one, or both are merged into one file.

## Why it is wrong

- **They answer different questions.** The designed map says what was decided; the generated map says what exists. A context that is designed and not built yet is not an error in either — it is work that has not been done. A dependency that exists and was never designed is not an error in the generated map — it is a decision nobody took.
- **Reconciling erases the finding.** A difference between intent and code is exactly the information a reviewer needs: a boundary crossed without a decision, a relationship that changed kind in passing, a context built that nobody asked for. Editing the designed map to match turns that into a record of whatever happened.
- **One file cannot hold both.** A generator overwrites what a person wrote into its output; a person who edits generated text loses it on the next run. A merged file drifts the first week.
- **The planned context disappears.** A story for a context that is designed but not built must still be possible. When the designed map follows the code, the context is not on it until someone has built it — so the first story for it looks like a request for a context nobody decided on.

## How to spot it

The designed map's history shows edits that follow code changes rather than decisions. A context appears on the designed map in the same change that introduced its code. The two maps are the same file, or one names no difference to the other at all.

## What forbids it

- [Declared relationships must match real dependencies](/rule/contextmap/dca-map-001.md) — where relationships are declared in code, the rule holds the code to its declarations; nothing holds the designed map to the code, and nothing should.
- [Generated context map or strategic context map](/decision/generated-context-map-vs-strategic-map.md) — why the two are two files with two owners.

## Do instead

**Keep them apart, with two owners.** The designed map is written by the people who decide the cut, before the code where a context is planned, and changes only when a decision changes. The generated map is rendered from the code and never edited.

**Read a difference as a finding.** Where the two disagree, say which way: planned and not built, built and not planned, related differently than designed. Each has one of two answers — the code follows the decision, or the decision is taken now, recorded, and the designed map follows it. Neither is a silent edit.

**Plan against the designed map.** A change for a context names a context the designed map carries, whether or not the code has it yet; a context on neither map is a question about the cut, answered before the change is written.
