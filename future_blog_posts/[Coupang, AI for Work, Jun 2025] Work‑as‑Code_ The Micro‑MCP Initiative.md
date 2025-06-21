## **Author**: Ziyad Mir, Jun 2025

### **Background**

Infrastructure‑as‑Code (IaC) transformed how Coupang ships servers and networks by treating every resource as declarative code. **But 90 % of an engineer’s day is still executed ad‑hoc via dashboards, CLI snippets, and tribal know‑how.** Model Context Protocol (MCP) already exposes a handful of large “tools” (Jira search, Git PR fetch). To unlock full AI orchestration, we must shrink that granularity: **thousands of single‑purpose MCP functions, each codifying one atomic task**.

---

### **Motivation**

| Pain‑Point | Impact |
| ----- | ----- |
| Siloed tribal commands (“just run this script on prod‑tool‑01”) | Hard for AI agents or new hires to discover & reuse. |
| Coarse MCP surface (dozens, not thousands) | Agents need brittle prompt hacking to achieve sub‑tasks. |
| Manual toil remains | Performance checks, quota look‑ups, config toggles still require humans. |

A systematic “Work‑as‑Code” push—**Micro‑MCPs**—makes every action callable, observable, and composable.

---

### **Program Vision**

| Pillar | Description | Key Components |
| ----- | ----- | ----- |
| **1\. MCP Factory** | Self‑service CLI (`mcp create <verb>`) scaffolds a new function with TypeScript/Java, auth stub, tests, and auto‑docs. | Yeoman‑style templates, GitHub Actions for lint & publish. |
| **2\. Registry & Discovery** | Central catalog (`registry.coupang.net/mcps`) with OpenAPI \+ examples; searchable via VS Code & EMUX UI. | Postgres \+ Swagger UI; MCP SDK autocompletion. |
| **3\. Contracts & Observability** | Each MCP declares idempotency, SLA, auth scope, and emits structured logs \+ Prom metrics. | JSON schema, OpenTelemetry hooks, Grafana dashboard set. |
| **4\. Security & Access** | Fine‑grained IAM roles: AI agents get the minimum‐required MCP scopes; human override possible. | AWS IAM, Service Tokens, Vault. |
| **5\. Composition Layer** | EMUX and other agent platforms orchestrate micro‑MCPs into workflows. | Temporal workflows, YAML DAGs. |
| **6\. Governance & Quality** | MCP Review Board (design doc \+ code review) ensures naming, test coverage, backward‑compat. | GitHub CODEOWNERS, automated contract tests. |

**Example Micro‑MCPs (≤ 100 LOC)**

* `check_service_health(serviceId)`

* `toggle_feature_flag(env, flagName, state)`

* `fetch_top_grafana_alerts(sinceMinutes)`

* `estimate_lambda_cost(functionName, duration)`

---

### **Benchmarks & Hill‑Climb Metric**

| KPI | Baseline (Today) | Target (EOY) |
| ----- | ----- | ----- |
| **Micro‑MCP Count** | 42 | 1 000+ |
| **Median Time‑to‑Publish** | 8 days | 1 day |
| **AI Autonomy Index**\* | 38 % | 70 % |

\*AI Autonomy Index \= *steps completed by agents without human aid / total steps*—rises as granular MCPs remove “unknowns” for the AI.

---

### **Implementation Roadmap**

| Phase | Goal | Duration |
| ----- | ----- | ----- |
| **0\. Bootstrap** | Ship MCP Factory CLI; convert 20 high‑value scripts (health check, capacity query). | 2 w |
| **1\. Inner‑Source Drive** | Run “100 MCPs in 30 days” hackathon; catalog live. | 1 m |
| **2\. Workflow Integration** | EMUX agents migrate to micro‑MCPs; measure AI Autonomy gain. | 1 m |
| **3\. Org‑Wide Expansion** | Mandate “no new script without MCP wrapper”; governance board active. | ongoing |

---

### **Ownership**

* **Common Frameworks** – MCP SDK, Factory CLI, registry infra.

* **Domain Teams** – Supply & maintain task‑specific MCPs.

* **AI Platform / EMUX** – Consume MCPs, surface gaps, report KPI.

* **Security** – Approve scopes, audit logs.

---

### **Benefits**

1. **Programmatic Everything** – Any task is a function call; reproducible and testable.

2. **AI‑Ready Surface** – Agents compose workflows reliably, no brittle screen‑scraping.

3. **Reduced Toil** – Humans intervene only for ambiguous logic, not rote data pulls.

4. **Observability & Compliance** – Unified logging, metrics, and access policy per MCA.

5. **Velocity Loop** – Faster onboarding, easier delegation to junior engineers and AI alike.

---

### **Summary**

The **Micro‑MCP Initiative** is to operational tasks what IaC was to servers: *turn every discrete unit of work into deterministic code*. By flooding Coupang’s ecosystem with small, discoverable MCP functions, we enable AI agents—and humans—to orchestrate complex workflows safely and autonomously, measurable through a clear AI Autonomy Index.

