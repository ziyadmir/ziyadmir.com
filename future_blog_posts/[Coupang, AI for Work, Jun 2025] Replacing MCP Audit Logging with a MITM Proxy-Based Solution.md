## **Author**: Ziyad Mir, Jun 2025

## **Background**

Coupang’s internal Generative AI IDE (AI IDE) will soon serve \~2.5k active developers, becoming central to daily workflows. It uses a **Model Context Protocol (MCP)** plugin framework to enrich user prompts with context before calling external Large Language Models (LLMs). For compliance and security, the current MCP-layer audit logger records each prompt and its LLM response whenever sensitive internal data could be involved. This ensures an audit trail for any proprietary information sent to third-party LLMs. However, having the model decide when and what to log at runtime introduces overhead and complexity in the AIIDE client and MCP services.

## **Motivation**

The MCP-based audit logging approach, while functionally correct, has notable drawbacks:

* **Performance Overhead:** Logging at the application layer adds extra processing and network hops to each LLM request/response cycle, resulting in user-visible latency. This slows down code completions and chat responses, undermining developer experience.

* **Reliability & UX Issues:** If the logging pipeline (e.g. writing to a database or remote service) is slow or fails, it can delay or interrupt LLM interactions. The tight coupling of logging with prompt processing creates points of failure that can degrade the IDE’s responsiveness.

* **Maintenance Burden:** Embedding audit logic in MCP means the AIIDE/MCP code must constantly be updated to handle new logging requirements or edge cases. This increases client complexity and may not easily scale to new GenAI use cases outside the IDE.

These challenges motivate a shift to a more transparent, robust mechanism that doesn’t interfere with the user’s flow.

## **Proposed Solution Design**

**Leverage Zscaler Proxy for Outbound LLM Traffic:** We propose offloading audit logging to Coupang’s existing Zscaler Internet Access (ZIA) cloud proxy, which already performs man-in-the-middle HTTPS inspection on outbound traffic. Zscaler’s proxy architecture can decrypt and inspect **full payloads** of TLS connections, not just URLs (behavior as of Q2 2025), enabling it to see the complete request content (prompt plus context) destined for external LLM endpoints (such as `windsurf.com`, the Codeium/Windsurf API domain).

**Custom DLP Extraction:** Using Zscaler’s Data Loss Prevention (DLP) engine and custom patterns, we will configure a policy to specifically inspect **outbound LLM API calls**. A custom detection rule (e.g. a regex or user-defined dictionary that matches all content for the target domain) will trigger on every request to the LLM service. This rule will extract the relevant fields (the prompt and any added context in the payload) and log them as a security event. Essentially, the proxy will capture the *final enriched prompt* leaving our network and record it in a secure log store. (If needed, response data from the LLM can be logged similarly, though the primary goal is to log what we send out.) The extraction logic will be developed in partnership with Zscaler to ensure it reliably captures the necessary JSON payload fields.

**Transparent In-line Operation:** Because Zscaler already proxies all internet-bound traffic, this logging will be transparent to users and requires no changes in the IDE client. The LLM request still goes out through the same proxy path; the only difference is that Zscaler will now **record the payload** for audit purposes. The proxy’s cloud-native design performs inspection with minimal latency impact, so developers should not notice any change in responsiveness. Crucially, the logging occurs out-of-band from the application’s perspective – even if the logging backend is slow or down, Zscaler will still pass the LLM request through (unless we explicitly configure it to block), so the user experience remains unaffected. All captured log events can be streamed to our security log repository or SIEM for retention and review.

## **Ownership & Collaboration**

Implementing this solution requires coordination across teams and our vendor:

* **Engineering Efficiency (AI Platform Team):** Owns the AIIDE and MCP. This team will define the logging requirements (what fields to capture) and assist in validating that the proxy logs contain the necessary information. They will also simplify the MCP by removing the old logging code once the new system is in place.

* **Security Team (InfoSec/IT Security):** Owns Zscaler policy configuration and compliance. They will create and maintain the DLP policies and custom rules in Zscaler, and ensure the logs are properly collected, stored, and monitored. They are also responsible for access control to these sensitive logs and for responding to any policy violations.

* **Zscaler (External Vendor):** Provides the cloud proxy platform and will support custom **User-Defined Function** or DLP rule development needed for this use case. Zscaler’s team may assist in writing advanced content-match rules or scripts to extract the prompt/context from the HTTPS payload. They will also advise on best practices so that logging is thorough yet does not inadvertently capture unrelated data.

This joint ownership model ensures the solution is robust: EE provides domain knowledge of the AIIDE traffic, Security ensures compliance and handles log management, and Zscaler enables the technical capability within their platform.

## **Benefits**

This proxy-based audit logging design offers multiple clear benefits over the status quo:

* **No Impact on User Experience:** Developers experience the same fast IDE interactions, since logging is handled at the network layer with virtually no added latency. There is no extra pop-up or delay from the audit logging process, preserving the “in flow” coding experience.

* **Comprehensive Security Coverage:** Every outbound LLM request is captured automatically, ensuring full auditability of GenAI usage. This covers all scenarios (present and future) where code or data might be sent to external models, without relying on each application to implement logging. The proxy sees *all* traffic, so nothing can bypass the audit as long as it goes through the corporate network.

* **Reduced Application Burden:** The MCP and AIIDE client no longer need custom code to decide and record audit logs. This removal of in-app logging simplifies the system and eliminates a potential point of failure. The AI platform team can focus on core functionality rather than logging mechanics.

* **Improved Reliability & Maintainability:** Logging at the network layer decouples it from the application runtime. Even if the logging storage or analysis pipeline encounters issues, it will not block or slow down LLM calls. The solution uses Zscaler’s scalable cloud infrastructure for logging, which is built for high throughput and security. Maintenance is also easier – updates to what is logged can often be made by adjusting the proxy policy, without deploying new application code.

* **Centralized Audit Data:** All LLM audit logs will reside in centralized security logs (via Zscaler’s Nanolog or SIEM integration) alongside other DLP and security events. This makes it easier to perform compliance audits, generate reports, or run anomaly detection on AI usage. Security and engineering leadership can jointly query these records as needed for investigations or metrics, knowing that the data is complete and immutable.

In summary, shifting from MCP-based logging to a Zscaler proxy-based solution addresses the performance and reliability pain points while **strengthening our security posture**. This design taps into an existing, proven infrastructure to log all outbound AI IDE traffic in a scalable way. By removing friction from the developer’s workflow and centralizing audit capabilities, we achieve both **engineering efficiency and security compliance** – a methodical win-win solution for Coupang’s GenAI initiative.

