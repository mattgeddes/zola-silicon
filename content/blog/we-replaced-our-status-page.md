+++
title = "We replaced our status page with a cron job"
description = "Status pages are where you go to confirm an outage is real. Ours now derives entirely from the same telemetry our customers already have."
date = 2026-02-11
template = "blog/page.html"
[extra]
icon = "globe"
tag = "Operations"
image = "/images/posts/status-page.svg"
image_alt = "Abstract illustration of a status indicator turning from red to green"
author = "Nadia Okon"
eyebrow = "Operations"
+++

Our status page used to be a human writing words during an incident. During the
worst incident of last year, the most-visited page on our site was a stale
green banner while the product was down for forty minutes.

## The change

The page is now generated. Component status comes from the same health checks
the platform runs, aggregated into four buckets, and published on a two-minute
cycle.

Nobody types a sentence during an incident any more, which removes the task
that was quietly making incidents worse.

## The parts that needed judgement

- **Buckets, not services.** Thirty services grouped into four buckets is what
  a customer actually cares about. Thirty rows is not, and the rows that
  flicker are noise.
- **Silence is not health.** A missing check now reads as unknown rather than
  operational. We learned that the hard way during a collector outage in
  November.
- **Words still come from a human.** The generated page says which component
  is degraded. The explanation of why still arrives through a status comment,
  written once, when there is something to say.

{% callout(type="info") %}
Generating the page did not save engineering time. It saved correctness, which
is a different thing and the reason it was worth doing.
{% end %}
