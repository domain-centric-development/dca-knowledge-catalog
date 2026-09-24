---
type: Section
title: The product scope
chapter: "Delivering a story: backlog, stages, gates"
source: guide
resource: dca-guide/process/factory.md
tags: [guide, section]
---

Before the first story, one file describes the product: what is built and for whom, how each actor
reaches it, how it works, how it looks, which qualities it needs, and what it will not do.

| Heading | Says |
|---|---|
| What and for whom | the product in two or three sentences, and its actors |
| Surfaces | pages, notifications, an API, a tool — and on which devices |
| How it works | the main flow across epics; where state lives and what is persisted |
| Look and feel | style direction, language, accessibility level, the styling approach |
| Qualities | security and authorisation stance, privacy, performance, availability |
| Not part of the product | what it deliberately will not do |

It holds product decisions, never code design. "The client keeps the draft; the server stores what
is submitted" belongs in it; an endpoint or a package does not. It is written with the person who
decides what is built, one question per heading, and nothing in it is invented: a stage that reads
an invented look builds it.

Two failures make it the first artefact rather than an optional one. A product decision nobody took
lands in the first story that needs it. There it surfaces as a plan that stops for a human, at the
moment nobody is there to answer. And what no artefact states does not get built: a build stage
that makes the smallest change that works builds a page without a stylesheet, correctly, when no
look was stated. So the backlog skill writes no story while the product scope is missing, the
stages plan and build within it, and a change that contradicts it is a review finding.
