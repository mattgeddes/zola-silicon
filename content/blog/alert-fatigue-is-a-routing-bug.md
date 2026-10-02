+++
title = "Alert fatigue is a routing bug, not a monitoring bug"
description = "Six engineers woke up for one database failover. The dashboard was fine the whole time. Here is what we changed."
date = 2026-08-18
template = "blog/page.html"
[extra]
icon = "bolt"
tag = "On-call"
image = "/images/posts/alert-routing.svg"
image_alt = "Abstract illustration of six alert paths converging on a single node"
author = "Nadia Okon"
eyebrow = "On-call"
+++

Six pages, one fault, forty minutes. The database failed over at 02:14, which
is exactly the sort of event an alert exists for. Everything that followed was
our own fault.

## What happened

The failover succeeded in eleven seconds. The monitoring was correct: error
rate went up, latency went up, saturation went up. Each of those had its own
rule, and each rule belonged to a different team.

Nobody had defined which rules were *about* the database, so the tooling
inferred nothing and paged everybody whose rule happened to be red at 02:14.

{% callout(type="note") %}
The first fix took twenty minutes of configuration. We had spent two months
adding rules and never once asked what the fleet would do if all of them went
off at once.
{% end %}

## The change

We stopped writing rules per symptom and started writing them per *cause*.

- Every rule declares what it is a symptom of.
- When several rules share a cause, they collapse into one notification with
  the rest as context.
- A cause that has no owner routes to a team channel, not to a person.

The failover still paged. It paged one team, once, with the six contributing
signals attached and the release history in the message.

## What we got wrong first

Our first attempt grouped purely by time window. Thirty seconds of overlap is
not evidence of a shared cause — it is evidence of a busy minute. That version
suppressed two real alerts in its first week, which is a faster way to lose
trust than paging six people.

Now the grouping has to agree on a cause, not merely on a timestamp. It is less
aggressive and it has not once been wrong in the four months since.

## What I would do earlier next time

Run the fire drill. Before the next busy quarter, push a synthetic fault
through staging and write down exactly who gets woken. The answer is almost
never the answer in the runbook.
