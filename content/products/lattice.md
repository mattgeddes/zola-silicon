+++
title = "Kestrel Lattice"
description = "Deploy-aware service catalogue with ownership, dependencies and SLOs, kept in step with your infrastructure instead of a wiki page."
weight = 4
[extra]
icon = "network"
price = "From $29/mo"
cta_label = "Book a demo"
facts = ["Service catalogue", "Ownership", "SLO tracking", "Terraform sync"]
eyebrow = "Product 04"
+++

Most service catalogues are accurate for about three weeks after they are
written. Lattice derives the catalogue from your infrastructure and your
traffic, so it stays true without anyone maintaining it.

## What it knows

Services, their owners, their dependencies, their runtime and their deployment
cadence — read from Terraform, Kubernetes manifests and your CI provider.

## SLOs next to reality

Define a target and Lattice plots it against what actually happened, per
service and per route. Burn-rate alerts fire from the same numbers the
dashboard shows, which removes the usual argument about which tool is right.

## Ownership that routes

Ownership is not decoration: it is what Relay uses to work out who to wake.
One source of truth, used by alerting, review and the catalogue.

{% callout(type="info") %}
Lattice is the newest of the four and the least mature. It works well if your
infrastructure is described in Terraform or Kubernetes manifests, and there is
no point pretending it is useful if it is not.
{% end %}
