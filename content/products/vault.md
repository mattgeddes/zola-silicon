+++
title = "Kestrel Vault"
description = "Short-lived credentials, audited access and rotation policies for services and edge functions, without a restart."
weight = 3
[extra]
icon = "lock"
price = "From $19/mo"
cta_label = "Start a 30-day trial"
facts = ["Short-lived tokens", "Audit log", "Automatic rotation", "Edge runtimes"]
eyebrow = "Product 03"
+++

Vault issues credentials that expire in minutes rather than months, and keeps
an append-only record of who asked for what and when.

## Short-lived by default

Tokens are minted per workload identity, valid for a configurable window, and
refreshed transparently. There is no long-lived key to leak, and rotating one
is not an outage.

## Rotation without a deploy

Credentials rotate on a schedule or on demand. The next call picks up the new
value, so nothing restarts and no cache goes stale.

## Audited, append-only

Every access is recorded with the workload identity, the purpose, and the
resulting action. The log is tamper-evident: entries are chained, so a gap is
detectable rather than merely inconvenient.

## Where it runs

Vault works for long-running services, serverless functions and edge runtimes
alike. The edge case is the one that usually breaks, so it is the one we built
for first.

{% callout(type="note") %}
Migrating from a static secrets file is usually the whole project. Vault reads
your existing environment variables first, so you can move one service at a
time without a coordinated cutover.
{% end %}
