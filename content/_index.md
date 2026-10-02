+++
title = "Home"
description = "Observability and edge tooling for small engineering teams. Kestrel builds the boring, reliable parts so you don't have to."
template = "index.html"

[extra.hero]
eyebrow = "Now in public beta"
title = 'Ship software you can <span class="text-gradient">actually reason about</span>.'
text = "Kestrel gives small teams the telemetry, alerting and edge primitives that used to need a platform team. Connect a repository, get a dashboard in minutes, and keep the pager quiet."
image = "/images/hero-dashboard.svg"
image_alt = "Illustration of a Kestrel observability dashboard with latency charts and an incident list"
actions = [
  { label = "Start free", url = "/contact/", variant = "primary", icon = "rocket" },
  { label = "Book a demo", url = "/contact/", variant = "secondary", icon = "calendar" },
]
meta = [
  { icon = "check-circle", text = "Free for 3 projects" },
  { icon = "check-circle", text = "No credit card" },
  { icon = "check-circle", text = "Cancel any time" },
]

[extra.hero.stat]
icon = "activity"
title = "p99 latency down 38%"
text = "Median across 214 teams after 90 days"

[extra.logos]
label = "Used in production by teams at"
items = [
  { name = "Northwind", logo = "/images/logos/northwind.svg" },
  { name = "Halcyon", logo = "/images/logos/halcyon.svg" },
  { name = "Perihelion", logo = "/images/logos/perihelion.svg" },
  { name = "Cobalt Bay", logo = "/images/logos/cobalt-bay.svg" },
  { name = "Ravelin", logo = "/images/logos/ravelin.svg" },
]

[extra.features]
eyebrow = "What you get"
title = "Everything the platform team would have built"
text = "Four products, one shared event pipeline, and no per-seat pricing that punishes you for growing."
items = [
  { icon = "chart", title = "Traces you can read", text = "Automatic service maps, waterfall views and tail-latency breakdowns that survive a high-cardinality week.", link = "/products/observe/", link_text = "Explore Kestrel Observe" },
  { icon = "bolt", title = "Alerts with a memory", text = "Deduplicated, grouped by cause, and quiet by default. If two symptoms share a root cause, you get one page.", link = "/products/relay/", link_text = "Explore Kestrel Relay" },
  { icon = "lock", title = "Secrets at the edge", text = "Short-lived credentials, audited access and rotation policies that do not require a restart.", link = "/products/vault/", link_text = "Explore Kestrel Vault" },
  { icon = "network", title = "One event pipeline", text = "Logs, metrics and traces share a schema, so a join is a thought rather than a migration project." },
  { icon = "gauge", title = "Cost ceilings", text = "Per-service budgets enforced at the collector. Overspend stops the pipeline instead of the finance meeting." },
  { icon = "git-branch", title = "Deploy-aware alerts", text = "Kestrel reads your release events and suppresses the noise that always follows a deploy." },
]

[extra.steps]
eyebrow = "Getting started"
title = "Three steps, about twenty minutes"
text = "No agents to install and no infrastructure diagram to design."
items = [
  { title = "Connect a repository", text = "Point Kestrel at your Git provider. It reads your service definitions and language manifests." },
  { title = "Deploy once", text = "Ship to staging as usual. Kestrel attaches itself to the build and instruments the paths it finds." },
  { title = "Read the dashboard", text = "A baseline appears within minutes: throughput, error rate and latency, already split by route." },
]

[extra.split]
eyebrow = "Built for small teams"
title = "The tools you need, minus the platform team"
text = "Most observability products are priced and scoped for companies with a hundred engineers. Kestrel is the opposite: a small product, priced plainly, that a team of three can run without asking permission."
flip = true
image = "/images/split-architecture.svg"
image_alt = "Diagram of services sending events to the Kestrel collector and on to storage and alerting"
items = [
  { text = "Per-project pricing, not per-seat, so adding a teammate is never a budget conversation." },
  { text = "Single-tenant data by default. Nothing is pooled into anyone else's aggregates." },
  { text = "Runs in your cloud account or ours — bring your own storage if audit requires it." },
  { text = "Export to OpenTelemetry at any time. Leaving is a config change, not a migration." },
]
actions = [
  { label = "Compare the products", url = "/products/", variant = "secondary", icon = "layers" },
  { label = "Talk to us", url = "/contact/", variant = "ghost", icon = "message" },
]

[extra.latest]
eyebrow = "From the blog"
title = "Notes on shipping software"
text = "What broke, what it cost, and the change that stopped it happening."

[extra.faq]
eyebrow = "Questions"
title = "Frequently asked"
items = [
  { q = "How long does setup actually take?", a = "<p>Connect your repository and ship to staging. Instrumentation is attached at build time, so there is nothing to install on a server and nothing to remember in a runbook. Most teams see their first baseline inside twenty minutes; heavy monorepos can take a little longer.</p>" },
  { q = "Do I have to move my data?", a = "<p>No. Kestrel writes to storage you control, in your own cloud account, if you prefer. If we host it, you can still export everything as OpenTelemetry or raw NDJSON at any point, and we will help you take it with you.</p>" },
  { q = "What happens when I outgrow the free tier?", a = "<p>Nothing breaks. Projects stay live and we email you before anything is charged. There is no hard limit that silently starts dropping events, which is the usual way this goes wrong.</p>" },
  { q = "Is there a self-hosted edition?", a = "<p>The collector and the query layer are both available under the Business plan as a container image you can run in your own cluster. Storage stays wherever you put it.</p>" },
  { q = "How do you handle high-cardinality data?", a = "<p>Aggregations happen at the collector, before anything is stored, using a per-tenant budget. You choose which attributes are worth keeping as dimensions; the rest are sampled with a documented rate.</p>" },
  { q = "Do you train models on our data?", a = "<p>No, and the contract says so. Telemetry is processed to give you your own answers and is never used to train anything shared.</p>" },
]

[extra.newsletter]
eyebrow = "Field notes"
title = "One email a month, about production"
text = "What broke, what it cost, and the change that stopped it happening. Written by the engineers who did the work."
note = "Sample form — it is not connected to a mailing list. See README.md."

[extra.cta]
title = "Ready to see it on your own code?"
text = "Bring one service. We will instrument it, show you the dashboard, and tell you honestly if Kestrel is the wrong tool."
actions = [
  { label = "Book a demo", url = "/contact/", variant = "primary", icon = "calendar" },
  { label = "Read the docs", url = "/products/", variant = "secondary", icon = "book" },
]
+++