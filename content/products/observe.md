+++
title = "Kestrel Observe"
description = "Traces, metrics and service maps from the code you already have. Connect a repository and get a baseline without installing an agent."
weight = 1
[extra]
icon = "chart"
price = "From $0"
cta_label = "Start a 30-day trial"
facts = ["Traces", "Metrics", "Service maps", "OpenTelemetry"]
eyebrow = "Product 01"
+++

Kestrel Observe is the part most teams adopt first. It reads your repository,
works out which services talk to which, and attaches instrumentation at build
time rather than asking you to install anything at runtime.

## What you get

A baseline the first time you deploy to staging: throughput, error rate and
latency, already split by route, version and region. Nothing to configure, and
no sampling decisions for you to get wrong.

### Service maps that update themselves

The map is derived from real traffic, not from a wiki page someone maintains.
When a team splits a service, the map follows the calls on the next deploy.

### Tail latency, not averages

Every percentile below p95 is available without a query, because the histogram
is built at the collector. Averages hide exactly the users who are having a
bad time.

### Cross-service joins

Logs, metrics and traces carry the same `trace_id`. Joining them is a click,
not an exercise in remembering which ID goes in which tool.

{% callout(type="tip") %}
Start with a single service. A useful baseline on one route is worth more than
a half-configured fleet.
{% end %}

## How it works

1. Connect a Git provider. Kestrel reads service definitions and language
   manifests to build an inventory.
2. Build. Instrumentation is injected into the artefact, so the deployed image
   is the only thing that changes.
3. Deploy as normal. The baseline appears within minutes.

There is no sidecar to schedule, no host to patch and no agent to forget about
when you rebuild a fleet.

## What it does not do

It does not do application performance monitoring in the marketing sense — no
business transaction recording, no user session replay. Those are different
tools for different questions, and pretending otherwise helps nobody.

## Export

Everything is OpenTelemetry end to end. If you leave, you take a valid
telemetry stream with you, not a folder of screenshots.

[extra.cta]
title = "See Observe against your own code"
text = "Thirty minutes, one service, and a dashboard you can keep or throw away."
actions = [{ label = "Book a demo", url = "/contact/", variant = "primary", icon = "calendar" }]
