+++
title = "The cost ceiling pattern"
description = "Instead of a monthly budget alarm, we made the collector enforce a per-service ceiling at ingestion. Overspend now stops the pipeline, not the finance meeting."
date = 2026-07-02
template = "blog/page.html"
[extra]
icon = "gauge"
tag = "Cost"
image = "/images/posts/cost-ceiling.svg"
image_alt = "Abstract illustration of a rising usage chart meeting a horizontal limit line"
author = "Tomas Reinholt"
eyebrow = "Cost"
+++

We discovered a telemetry bill of $11,400 in a month we expected to cost
$900. The spike was one service, one endpoint, and a retry loop that made bad
things worse.

## The usual answer, and why it failed

Every vendor we looked at offers a budget alert: email me when you pass $500.
It is genuinely useful and it is far too late. By the time the alert lands you
have nine days of bill and no idea which of your three hundred services
produced it.

Attribution helps. It turns out you can identify the service — you just cannot
identify it *before* spending.

## What we changed

Every service gets a hard daily ceiling at the collector. The collector
aggregates first, then compares against the budget for that service, and
degrades its own sampling rate before it exceeds it.

The important part: it degrades *itself*, not the service emitting events. A
service that is retrying hard still runs. It just stops being the reason the
bill is large.

{% callout(type="warning") %}
Hard ceilings need a floor that someone chose. Ours is "95% of the daily
budget", and the last 5% is headroom for the alert itself. Set the ceiling at
100% and you have built an outage.
{% end %}

## The parts that took longer than the pattern

- **Choosing the budgets.** We started with equal shares, which was wrong —
  our ingest-heavy service and our query-heavy service cost the same to serve
  and produce very different numbers.
- **Telling anyone.** A ceiling that silently degrades telemetry is worse than
  one that breaks loudly. It now posts to the owning team every time it
  engages, and the first question is always "is this number right?".
- **Not optimising prematurely.** Two services hit their ceiling. Both were
  genuinely doing something wrong. Neither needed us to tell them; they needed
  the ceiling to make the problem visible.

## Result

Worst month since: $1,180. The retry loop is still there, but it now costs
about forty dollars a month instead of nine thousand.
