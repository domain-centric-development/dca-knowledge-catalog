---
type: Section
title: "7a. Framing: a Second Question, Not a Consequence of the First"
chapter: JWT Implementation Guide
source: guide
resource: dca-guide/topics/jwt-implementation-guide.md
tags: [guide, section]
---

An application with cookie identity is eventually put in someone else's iframe — a slide deck, a
documentation page, a partner portal, a demo. Two settings decide whether that works, and they are
often collapsed into one because both say "embedded". They answer different questions:

| | Decided by | What counts |
|---|---|---|
| May another page frame this application? | `X-Frame-Options` / `frame-ancestors` | the **origin** — scheme, host *and port* |
| Do the cookies travel into that frame? | `SameSite` | the **site** — registrable domain; the port does **not** count |

The consequence is the part that surprises people: a page on `localhost:3030` framing an
application on `localhost:8080` is a *different origin* but the *same site*. Framing has to be
allowed, and the `Lax` cookies travel unchanged — no cookie policy needs relaxing. A page on
another domain is both, and only then is `SameSite=None` required, which in turn requires `Secure`
and therefore HTTPS.

Derive one from the other and you get a setting that is either too weak or unusable:

- **Framing derived from the cookie policy** forces `SameSite=None` on a deployment that only ever
  gets framed from a neighbouring port, widening the CSRF surface for nothing — and on a stack that
  refuses to issue a token for a `Secure` cookie over plain HTTP it takes local development down
  with it.
- **The cookie policy derived from framing** hands out cross-site cookies to every embedding, which
  is exactly the exposure `SameSite` exists to prevent.

**Recommended shape:** one setting for framing, one for the cookie policy, both off by default in a
real deployment. A reference or demo application may ship with framing on — being embeddable is
what it is for — as long as that is a stated default and not a side effect of something else.

### Where the header belongs

Frameworks differ in a way worth knowing before you compare two implementations. Spring Security
writes `X-Frame-Options` on **every** response. ASP.NET Core writes it only on responses that emit
an antiforgery token, which is every page with a form and nothing else — so an application can
appear framable while the page inside the frame is refused. Where the same behaviour is expected
from two stacks, set the header in one place of your own rather than inheriting two defaults, and
assert it on a response that renders no form.

---
