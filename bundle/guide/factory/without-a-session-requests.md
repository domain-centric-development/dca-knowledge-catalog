---
type: Section
title: "Without a session: requests"
chapter: "Delivering a story: backlog, stages, gates"
source: guide
resource: dca-guide/process/factory.md
tags: [guide, section]
---

A person acts on the factory in one of two ways. In a session they talk to an agent, which runs the skill at once
and asks back in the chat. Without one — from a browser, a terminal, a tool that has no view of its own — they
write a **request**: one file that says what they want, checked when it is written, worked by the factory before
its next story. The factory then is a process of its own, started once (`up`) and ended between two stages
(`down`); a page on the same machine shows its views and turns every press into a request.

| | In a session | Through a request |
|---|---|---|
| who acts | the session's agent, in the chat | the factory, headless, with the tool the project names |
| when | at once | before the next story, between the stages of a running one |
| asking back | in the chat | as a decision record |
| needs | an open session | the factory up |

A request runs the skill a session would run, with the same words: a wish, a release, an answer, an acceptance, a
correction, a change to the description, a discovery. What the session gets from the person — the confirmation of
what they asked for — the request carries by being written; nothing is asked again. What the session would ask
and the files do not settle is not guessed: the skill writes it as a decision record, beside the story it
concerns or, where there is no story yet, as a record of the project's own, and ends. The request waits until a
person answers the record — on the page or in any session — and then runs again with the answer.

Three rules keep this deterministic. A request is checked when it is written and again when it is worked — an
answer to a record that has one, an option the record does not offer, a story that does not exist are refused with
the reason. The factory works requests in the order they were written, and never one about a story while that
story's stage runs. And what a request wrote is committed on its own, only the backlog and the description it
changed; a file a person had changed before stays as it was. The page decides nothing: which request a press
writes stands in the factory's own views, beside the session command the same press sends from a view in a
session. It is bound to the machine it runs on and opened with a token of its start, so no other web page can read
the factory or write to it.
