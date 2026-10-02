+++
title = "Shipping edge logic without regret"
description = "Edge functions look free until you count round trips. Four rules we now apply before anything gets deployed to nineteen regions."
date = 2026-05-27
template = "blog/page.html"
[extra]
icon = "network"
tag = "Architecture"
image = "/images/posts/edge-logic.svg"
image_alt = "Abstract illustration of requests fanning out from an edge to several regions"
author = "Nadia Okon"
eyebrow = "Architecture"
+++

Moving logic to the edge is almost always a latency win and almost always a
correctness problem. Here are the four checks we now run before anything gets
deployed to nineteen regions.

## 1. Count the round trips

An edge function that calls one regional API is a win. One that calls three
apis in sequence is three sequential timeouts in front of your user, and each
timeout should have a budget.

We write the call graph down first. If it is a chain, we either parallelise it
or move it back behind the region.

## 2. Decide what happens when the origin is slow

Not *whether* — *what*. An edge function with no timeout configured will hold
the connection open until the platform limit, which is longer than any human
will wait.

Our default is 300ms to first byte, 2s total, and a cached response on expiry.
The cached response is the part people forget.

{% callout(type="tip") %}
Decide the degraded behaviour while the service is healthy. Nobody invents a
good fallback while their dashboard is on fire.
{% end %}

## 3. Assume the edge is stale

Code is deployed to every region at once, almost instantly. Data is not. A
feature flag read from a database is nineteen slightly different answers until
it converges.

Anything that reads state at the edge gets an explicit staleness budget. Ours
is thirty seconds, and it is in the code rather than in the dashboard.

## 4. Keep the hard parts out

The edge is excellent at: authentication checks, redirects, geolocation,
caching responses, and rejecting obviously bad requests.

The edge is a poor place for: anything that must be exactly consistent, and
anything you will need to debug at three in the morning.

## What this looks like in practice

Nineteen regions, one deployment command, and a rollback that is another
deployment. The discipline is not in the platform — it is entirely in the four
checks above, done before the first region sees the code.
