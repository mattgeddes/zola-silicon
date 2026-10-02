+++
title = "Kestrel Relay"
description = "Alerting that groups by cause instead of by symptom, stays quiet by default, and knows when a deploy already explains the spike."
weight = 2
[extra]
icon = "bolt"
price = "From $19/mo"
cta_label = "Start a 30-day trial"
facts = ["Grouping", "On-call routing", "Deploy awareness", "Slack & PagerDuty"]
eyebrow = "Product 02"
+++

Most paging fatigue is not a monitoring failure. It is a routing failure: the
right person is not woken, or six people are woken for one fault. Relay attacks
the second problem.

## Grouping by cause

When an error rate climbs, Relay looks for the shared upstream change — a
deploy, a dependency, a saturation event — and sends one notification with the
rest as context. If it cannot find a cause, it says so instead of guessing
five times.

## Quiet by default

New alerts start muted. A rule has to earn its way into the pager by firing
correctly a few times in staging, which is how you end up with a rotation
people trust.

## Deploy awareness

Relay reads your release events. A regression introduced eleven minutes ago
gets annotated on the chart and folded into the alert, so the first thing in
the message is the last thing that changed.

{% callout(type="warning") %}
If you route by team rather than by service, you need the on-call map Relay
suggests before you enable paging. Routing to a chat channel is much easier to
undo than routing to a person.
{% end %}

## Integrations

Slack, PagerDuty, Opsgenie and generic webhooks. Messages are formatted for
each target rather than being one blob of Markdown, and every notification
links back to the exact query that produced it.
