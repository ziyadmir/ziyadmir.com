## **Author**: Ziyad Mir, Jun 2025

### **Background**

* **Windsurf** delivers LLM capabilities (code‑completion, chat).

* **MCP** wraps Windsurf (and other APIs) behind reusable “tools” (`get_pull_request`, `query_jxid`, etc.) that inject the right context.

* Developers now need **multi‑step tasks** (e.g., JDK upgrade, security scan → fix → PR) that string many MCP tools together, handle retries, and occasionally ask a human.

* Early proofs‑of‑concept (JDK Upgrader, Test‑Suite Generator) live as bespoke scripts and can’t scale.

---

### **Motivation**

| Gap | Consequence |
| ----- | ----- |
| One‑off scripts, no orchestration | Hard to reuse, brittle error handling. |
| No stateful memory | Agents forget prior steps; work cannot resume after failure. |
| Ad‑hoc human hand‑offs | Engineers ping each other in Slack, losing context. |
| No objective progress metric | Difficult to know if “AI is actually getting better”. |

EMUX turns isolated experiments into a **production‑grade, auditable platform**.

---

### **Proposed Solution Design**

| Layer | Role | Default Choice | Not‑Locked‑In Alternatives |
| ----- | ----- | ----- | ----- |
| **1\. AI Runner** | Execute individual step prompts/code. | **Claude Code** (Anthropic) | OpenAI GPT‑4o, Google Codey/Julep, *aider*, OSS Mixtral‑8x7B |
| **2\. Step Orchestration** | DAG execution, retries, timers. | **Temporal** | Airflow, Argo, Prefect |
| **3\. State Persistence** | Per‑agent JSON state, step history. | **DynamoDB** | Aurora‑Postgres, Cassandra |
| **4\. Human‑in‑the‑Loop** | Escalate unclear steps, collect approvals. | **Slack Bot** | Teams, e‑mail bridge |
| **5\. Versioning & Snapshots** | Commit each code‑modifying step. | **GitHub branches + PRs** | GitLab, Gerrit |
| **6\. Tool Catalog** | Call internal services safely. | **MCP‑exposed functions** | Direct REST/GRPC (discouraged) |
| **7\. No‑Code Builder UI** | Drag‑and‑drop step graph, env vars, triggers. | **EMUX Web (“Create Agent”)** | Dify‑style canvas, ComfyUI fork |

**Execution Flow**

1. *Graph Build* – User assembles steps in UI; JSON stored in DynamoDB.

2. *Run Trigger* – Temporal creates a workflow; each step pulls latest Git branch, executes via AI Runner, commits results.

3. *Human Check* – If a step emits `NEEDS_REVIEW`, Slack bot opens a threaded conversation; user reply resumes workflow.

4. *Finish* – Final PR raised; MCP logs usage; metrics pushed to Prometheus.

---

### **Benchmarking & Success Metrics**

| Metric | Definition | Baseline (Apr 2025) | Target (Q4 2025) |
| ----- | ----- | ----- | ----- |
| **Autonomous Completion Rate (ACR)** | `% steps finished without human input` | 38 % | 85 % |
| Mean Time‑to‑Complete workflow | `avg duration (s)` | 1 860 | 600 |
| Step Error Rate | `failed_steps / total_steps` | 22 % | \< 5 % |

The **hill‑climb** is simple: *increase ACR*. Each model upgrade or new MCP tool should move the metric upward; AB runs compare old vs. new agent versions on the same repo set.

---

### **Ownership & Collaboration**

* **Common Frameworks / EMUX** – Core platform, Temporal cluster, UI, KPIs.

* **MCP Owners** – Keep adding fine‑grained tools (e.g., `kickoff_jenkins_job`, `fetch_ci_logs`).

* **Domain Teams** – Supply reference workflows (Spring Upgrade, i18n extraction).

* **SRE / Security** – Define guardrails; approve auto‑merge thresholds.

---

### **Benefits**

1. **Reusable Automation** – Any engineer can compose tasks from vetted MCP tools.

2. **Observability by Design** – Every action logged, state persisted, PR diff shows exact changes.

3. **Progress You Can Measure** – Single north‑star metric (ACR) quantifies AI autonomy across all workflows.

4. **Safe Human Override** – Slack, Git branches, and Temporal replay make intervention trivial and traceable.

5. **Vendor Agility** – Swap AI runner, orchestrator, or DB without refactoring step graphs.

---

### **Summary**

EMUX unifies Windsurf’s LLM power, MCP’s tool catalog, and Temporal’s orchestration into a **single platform that can tackle end‑to‑end engineering workflows**. By tracking how many steps the AI completes alone—and relentlessly improving that number—Coupang will turn experimental agents into a reliable force‑multiplier for every developer.