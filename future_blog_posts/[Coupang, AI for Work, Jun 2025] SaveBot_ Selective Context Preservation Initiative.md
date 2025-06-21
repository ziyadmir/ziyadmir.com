## **Author**: Ziyad Mir, Jun 2025

## **Summary**

* **Problem:** Aggressive data retention policies (e.g. Slack 10 days, Email 30 days, OneDrive 15 months, Wiki 1 year unless labeled) are causing rapid loss of historical context and knowledge.

* **Impact:** Critical discussions and decisions vanish, undermining long-term productivity and forcing teams to rediscover information that was once shared.

* **Proposal – SaveBot:** A centralized, employee-triggered “context preservation” system that lets engineers proactively save high-value Slack threads, emails, and Wiki pages beyond normal retention limits (with an associated Jira ticket or business justification).

* **How it Works:** Users invoke SaveBot (e.g. Slack `/save` command or forwarding to **savebot@coupang.com**) to archive important conversations. The content and context are stored in persistent repositories (GitHub, SharePoint, or a secure internal DB) and indexed via the Model Context Protocol (MCP) Gateway for easy future retrieval.

* **Governance:** Every preserved item requires a justification label and is logged for Security/Privacy audit. This ensures compliance and provides feedback loops to refine usage.

* **MVP:** A Slack-integrated SaveBot (by Q3 2025\) with a web interface (through MCP) for retrieval. Subsequent phases will extend support to Email and Wiki content, enabling organization-wide knowledge retention.

## **Problem: Knowledge Lost under Current Retention Limits**

Recent changes to data retention at Coupang have created a **knowledge retention gap**. Key collaboration channels now auto-delete content quickly – Slack messages after 10 days, emails after 30 days, OneDrive files after 15 months, and Wiki pages after 1 year unless specially labeled. While these policies improve security and reduce clutter, they unintentionally **erase valuable historical context**. Teams have found that decisions made in Slack or design rationale shared via email often disappear before anyone transfers them to long-term documentation. This loss of institutional memory is **harming productivity**: employees spend extra time re-asking old questions and making decisions with incomplete past context. Preserving organizational knowledge is crucial for efficiency and decision-making, yet our current toolset provides no easy way to retain important information selectively under the new policies.

## **Proposed Solution: “SaveBot” Context Preservation System**

**SaveBot** is a proposed internal service and bot ecosystem that empowers employees to **selectively preserve high-value context** from ephemeral channels, with minimal friction and proper oversight. The idea is to give every engineer a one-click (or one-command) method to save critical information *at the moment it’s recognized* as important, bridging the gap between transient communication and long-term knowledge bases.

* **Slack Integration:** A custom Slack bot (`/save`) will allow users to save a channel thread, direct message, or snippet. The user provides a reference (e.g. a Jira ticket, project ID, or brief justification) when saving. SaveBot will capture the message history (and any file attachments) and mark it for long-term retention. For example, a tech lead can save a design discussion thread and tag it with the related Project Jira ID, ensuring it persists beyond Slack’s 10-day window.

* **Email Integration:** For email, users can CC or forward important threads to **savebot@coupang.com** (or use an Outlook add-in). The SaveBot service parses the email content (subject, body, attachments) and saves it under the specified project or category. This way, decisions or approvals that occur over email aren’t lost after 30 days.

* **Wiki Integration:** Confluence Wiki pages are already retained for 1 year by default. SaveBot will provide an easy way to mark pages for permanent retention (applying a “do-not-expire” label behind the scenes). For instance, an engineer can comment `@SaveBot preserve` on a wiki page or use a web UI toggle, and SaveBot will ensure that page’s content is flagged to **persist indefinitely** (preventing scheduled deletion).

**Under the Hood:** All preserved content is centralized in a secure long-term store. Rather than invent new storage, SaveBot will leverage existing **persistent repositories**:

* Slack messages and email texts could be saved as Markdown or HTML documents in **GitHub private repositories** (grouped by team or project), or as records in an **internal database**.

* Files and rich media might be stored in **SharePoint or S3** and linked accordingly.

* Wiki pages remain in Confluence but with non-expiring labels (or are periodically backed up to a repository).

Each saved item is annotated with metadata: who saved it, when, original source, and the justification tag (e.g. linked Jira ID or a short description). This metadata is crucial for both indexing and governance.

## **Solution Architecture and MCP Integration**

All SaveBot-captured content is indexed through the **Model Context Protocol (MCP) Gateway**, Coupang’s centralized context index and retrieval service. MCP integration means that any authorized person or AI agent can later retrieve preserved knowledge by querying the MCP with relevant identifiers or keywords. For example:

* A developer onboarding a year later can ask an internal AI assistant (powered by MCP) for “design decisions on Project X”, and the assistant will fetch the Slack thread preserved by SaveBot, because it was tagged with Project X’s ID.

* An engineer can manually search the MCP Portal using a Jira ticket number to find all related saved conversations or emails.

Access control is enforced via personal access tokens and the original justification tags. **Only** users who have rights (e.g. part of the project team or specified by the original saver) can retrieve the content, and all accesses are logged. The MCP’s role is to provide a unified gateway – one place to search and fetch context – so that knowledge doesn’t remain hidden in a silo. By integrating SaveBot with MCP, we ensure *saved knowledge is not only retained, but also discoverable* and usable in future workflows (including agentic AI workflows that Coupang is adopting via the AI-for-Work program).

Below is a comparison of possible storage backends for SaveBot and their trade-offs:

| Storage Option | Pros | Cons |
| ----- | ----- | ----- |
| **GitHub Private Repos** (by team or project) | \- Leverages existing version-controlled repos \- Developer-friendly: easy to link to code and PRs \- Git history provides audit trail of changes | \- Not optimized for storing chat or email text (no structured search out of the box) \- Permission management by repo (might need many repos or complex ACL setup) \- Possible cost for large volumes or binary files |
| **SharePoint** or **Confluence** (existing collaboration platforms) | \- Familiar to non-dev users \- Strong built-in search and metadata tagging \- Fine-grained access control with AD groups \- Long-term retention supported natively | \- Less natural for developers to use in daily workflow \- Inconsistency: Slack messages as documents may be awkward to consume in SharePoint \- Additional licensing or storage costs if usage grows |
| **Internal Database & Service** (custom-built archive with UI) | \- Most flexible: can tailor data schema for Slack threads, emails, etc. \- Easy integration with MCP for search (direct indexing) \- Precise access control per item and detailed auditing | \- Requires building and maintaining a new service and UI \- Up-front engineering cost and ongoing operations burden \- Needs robust backup and security since it becomes a source of truth |

Our approach could start lean (e.g. use GitHub or an existing wiki space for initial storage in the MVP) and later transition to a more scalable solution (like a purpose-built internal service) as adoption grows.

## **Security, Privacy, and Governance**

Security and privacy are paramount. **SaveBot will enforce justification tagging and auditing for every action:** when saving content, users must provide a reason or link it to a ticket. All saved data entries will record the requester, date, and justification. This log is accessible to Security/Privacy teams, who will periodically review saved content to ensure policies aren’t being circumvented (e.g. preventing someone from saving large amounts of trivial or sensitive data without cause). If misuse is detected, the process includes a feedback loop to the user or their manager, and the ability to purge improperly saved data. We will also integrate Privacy’s guidelines to ensure, for example, that personal data or legally protected information isn’t being inappropriately retained. By involving Security and Privacy early – making them stakeholders in designing SaveBot’s rules – the system is built with compliance in mind rather than as an afterthought.

Crucially, SaveBot **does not undermine** the overall retention policy: it provides a *safety valve* for exceptional cases of high business value. The default for most Slack messages and emails remains ephemeral, reducing noise and risk. SaveBot relies on employees to actively identify and preserve the *signal* in that noise. Every SaveBot action is transparent and justified.

## **MVP Plan and Next Steps**

**Short-term MVP (Q3 2025):** Focus on Slack, the most immediate pain point (10-day message deletion). We will implement the Slack `/save` command and a basic web interface (within the MCP Portal) where users can see and search their saved threads. This phase will involve:

* Developing the Slack bot and backend service to capture messages and attachments.

* Storing the data in a simple repository (initially, a secure GitHub repo or Confluence space accessible via MCP).

* Integrating with MCP search/index – so a user can retrieve saved content by querying by tag or keyword.

* User testing with a small group (e.g. one engineering org) to gather feedback on usability and to refine security audit processes.

**Next Phases (Q4 2025 and beyond):** Extend SaveBot to other platforms:

* **Email:** Deploy the savebot@ email ingestion and Outlook add-in, so that important email threads can be preserved with one click. Ensure the email content is searchable via MCP just like Slack content.

* **Wiki/Docs:** Work with the Knowledge Management team to make labeling easier and maybe automate backup of labeled pages to a repository for extra safety. Possibly extend SaveBot to monitor wiki pages that haven’t been labeled but have high view counts or links, and suggest preserving them (as an AI-powered enhancement).

* **OneDrive/Files:** Evaluate if a similar mechanism is needed for files (15 months retention). Perhaps integrate with OneDrive/SharePoint APIs to allow a “Save Copy” action for files, moving them to a long-term archive folder if they are linked to key projects.

* **Scale and Hardening:** As usage grows, re-assess the storage backend. We may build a dedicated internal archive service with a database for faster search and more structured data handling. Also, implement more robust access management (possibly integration with company SSO/AD groups to automatically permit project team members to see certain saved content).

Throughout these phases, we will maintain close collaboration with **horizontal teams** (Security, Privacy, IT, Knowledge Management) and **engineering leadership** to ensure SaveBot meets cross-team needs. The ultimate vision is that **no valuable context ever slips through the cracks**: any engineer can seamlessly preserve and later retrieve the knowledge that fuels better decisions and innovation across Coupang.

**Key Artifacts & Stakeholders:**

* *Artifacts:* Draft Design Doc – “Context Preservation (SaveBot) Architecture”, Slack SaveBot Prototype (Repo link), Data Retention Policy Overview 2025\.

* *Engineering Owners:* Productivity Engineering Team (development), Collaboration Tools Team (Slack/Email integration).

* *Partners:* **InfoSec & Privacy** (audit and compliance), **Knowledge Management** (Wiki integration), **IT** (OneDrive/SharePoint support).

* *Executive Sponsors:* (Proposed) CTO/Head of Engineering and CFO (for productivity ROI focus).

By introducing SaveBot, Coupang can proactively combat the unintended downsides of strict retention policies. This initiative frames a short narrative from problem to solution: we identified a critical productivity risk, architected a lightweight but extensible tool to address it, and laid out a path for company-wide adoption. The result will be a more resilient organizational memory – empowering both humans and AI assistants to reuse hard-earned knowledge, long after the original messages would have been lost.