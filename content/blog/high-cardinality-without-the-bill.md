+++
title = "High cardinality without the bill"
description = "You do not have to choose between useful dimensions and affordable storage. You have to choose before you store."
date = 2026-04-09
template = "blog/page.html"
[extra]
icon = "chart"
tag = "Data"
image = "/images/posts/high-cardinality.svg"
image_alt = "Abstract illustration of many data points funneling into a narrow channel"
author = "Tomas Reinholt"
eyebrow = "Data"
+++

Every observability vendor eventually asks you to accept fewer dimensions, and
the answer always arrives with a chart showing a line going flat. The framing
is wrong. High cardinality is not a storage problem, it is an ordering problem.

## Do it before you store

The useful work is deciding what becomes a dimension and what becomes a value
inside a dimension. That decision has to happen at the collector, because
afterwards the information you need to make it is gone.

At the collector:

- Attributes on an explicit allowlist become dimensions.
- Everything else is sampled at a documented rate.
- Attributes that look like identifiers are dropped, with a log line saying so.

{% callout(type="note") %}
The log line matters more than the rule. A team that hits an unexpected drop
can fix its instrumentation; a team that hits a silent drop loses trust in the
whole system and never comes back.
{% end %}

## Pick a budget per project, not per account

Different services have genuinely different shapes. A checkout service needs
`payment_provider` as a dimension and does not need `user_id` anywhere. A
recommendation service needs `model_version` desperately.

We give each project a dimension budget and a monthly storage budget, chosen
together. The collector will tell you what happens when either runs out,
before it runs out.

## What it costs

The honest number: dimension budgets cut storage by roughly four fifths on our
fleet. The work of deciding what goes in the allowlist took about a day per
service, mostly spent arguing about `user_agent`.

That day is worth it. It replaces an ongoing, invisible argument about the
invoice.
