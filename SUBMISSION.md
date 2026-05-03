<div align="center">

# PA4 Submission: TaskFlow Pipeline

<img alt="GitHub only" src="https://img.shields.io/badge/Submit-GitHub%20URL%20Only-10b981?style=for-the-badge">
<img alt="Total points" src="https://img.shields.io/badge/Total-100%20points-7c3aed?style=for-the-badge">

</div>

<div style="background:#f5f3ff;color:#111827;border-left:6px solid #6330bc;padding:14px 18px;border-radius:10px;margin:18px 0;">
Screenshots referenced below live under <code>docs/</code>. Embed each image where marked TODO in Tasks 1–7. Task 8 write-up and diagram below are filled in; tune names to match your exact Azure resources.
</div>

## Student Information

| Field | Value |
|---|---|
| Name | YOUR NAME |
| Roll Number | 25280068 (example — use your LMS roll) |
| GitHub Repository URL | https://github.com/Rafay-Dil123/CS487-PA4 |
| Resource Group | `rg-sp26-25280068` |
| Assigned Region | `ukwest` (use `uaenorth` if your cohort rule says UAE North) |

## Evidence Rules

- Use relative image paths, for example: `![AKS nodes](docs/aks-nodes.png)`.
- Every image must have a 1-3 sentence description below it.
- Azure Portal screenshots must show the resource name and enough page context to identify the service.
- CLI screenshots must show the command and output.
- Mask secrets such as function keys, ACR passwords, and storage connection strings.


## Task 1: App Service Web App (15 points)

### Evidence 1.1: Forked Repository

TODO: Embed screenshot of your forked GitHub repository.

Description: TODO: Explain that this is your working fork and that it contains the PA4 starter structure.

### Evidence 1.2: App Service Overview

TODO: Embed screenshot of the Web App overview page showing `webapp-<rollnum>` and Running status.

Description: TODO: State the resource group, region, runtime, and public URL.

### Evidence 1.3: Deployment Center / GitHub Actions

TODO: Embed screenshot of Deployment Center or the successful GitHub Actions deployment.

Description: TODO: Explain how the Web App is connected to your GitHub fork.

### Evidence 1.4: Live Web UI

TODO: Embed screenshot of the TaskFlow page loaded in a browser.

Description: TODO: Explain that the App Service is serving the frontend successfully.

---

## Task 2: Azure Container Registry (15 points)

### Evidence 2.1: ACR Overview

TODO: Embed screenshot of `crpa4<rollnum>` overview.

Description: TODO: Identify the registry SKU and resource group.

### Evidence 2.2: Docker Builds

TODO: Embed screenshot showing successful local builds for `validate-api`, `report-job`, and `func-app`.

Description: TODO: Explain which folder produced each image.

### Evidence 2.3: ACR Repositories

TODO: Embed screenshot or CLI output showing all three repositories in ACR.

Description: TODO: Confirm `validate-api:v1`, `report-job:v1`, and `func-app:v1` were pushed.

---

## Task 3: Durable Function Implementation (12 points)

### Evidence 3.1: Completed Function Code

TODO: Link to your completed file: `[function_app.py](function-app/function_app.py)`.

Description: TODO: Summarize how your orchestrator chains validation and report generation.

### Evidence 3.2: Local Function Handler Listing

TODO: Embed screenshot of `func start` showing the HTTP starter, orchestrator, and activities.

Description: TODO: Explain that the Durable Functions runtime discovered your handlers.

---

## Task 4: Function App Container Deployment (8 points)

### Evidence 4.1: Function App Container Configuration

TODO: Embed screenshot showing the Function App uses your `func-app:v1` image from ACR.

Description: TODO: State the Function App name and image URI.

### Evidence 4.2: Orchestration Smoke Test

TODO: Embed screenshot of the `curl` output that starts an orchestration and returns status URLs.

Description: TODO: Explain what the returned `id` and `statusQueryGetUri` prove.

### Evidence 4.3: Expected Failed Status Before Downstream Wiring

TODO: Embed screenshot of the status query JSON showing the expected failure before `VALIDATE_URL` is configured.

Description: TODO: Explain why this failure is expected at this stage.

---

## Task 5: AKS Validator (15 points)

### Evidence 5.1: AKS Cluster

TODO: Embed screenshot of AKS overview showing `aks-<rollnum>` succeeded.

Description: TODO: State node count, node size, region, and resource group.

### Evidence 5.2: Kubernetes Nodes and Pods

TODO: Embed screenshot of `kubectl get nodes` and `kubectl get pods`.

Description: TODO: Explain that the validator pod is scheduled and running.

### Evidence 5.3: Kubernetes Service

TODO: Embed screenshot of `kubectl get service validate-service`.

Description: TODO: Identify the external IP and port exposed by the LoadBalancer.

### Evidence 5.4: Validator API Tests

TODO: Embed screenshot of `curl /health`, a valid `curl /validate`, and an invalid `curl /validate`.

Description: TODO: Explain the accepted path and the `qty > 100` rejection rule.

### Evidence 5.5: Function App `VALIDATE_URL`

TODO: Embed screenshot showing the Function App application setting `VALIDATE_URL`.

Description: TODO: Explain how the Durable Function reaches the AKS validator.

### Evidence 5.6: AKS Idle Behavior

TODO: Embed AKS metrics screenshot and/or `kubectl` output after the service is idle.

Description: TODO: Explain that the AKS node remains running even when there are no orders.

---

## Task 6: ACI Report Job (15 points)

### Evidence 6.1: Blob Container

TODO: Embed screenshot of the `reports` blob container.

Description: TODO: Explain where generated PDFs are stored.

### Evidence 6.2: Manual ACI Run

TODO: Embed screenshot of `az container show` for `ci-report-test`.

Description: TODO: State the final container state and why the job exits.

### Evidence 6.3: ACI Logs

TODO: Embed screenshot of `az container logs`.

Description: TODO: Explain what the report job printed after generating and uploading the PDF.

### Evidence 6.4: Generated PDF

TODO: Embed screenshot showing `TEST-001.pdf` in Blob Storage or opened from Blob Storage.

Description: TODO: Explain how this proves the ACI wrote to storage.

### Evidence 6.5: Function App Managed Identity and IAM

TODO: Embed screenshots of system-assigned identity enabled and Contributor role assignment on your resource group.

Description: TODO: Explain why the Function App needs this permission to create ACIs.

### Evidence 6.6: Report App Settings

TODO: Embed screenshot of `REPORT_*`, `ACR_*`, `STORAGE_CONN`, and `SUBSCRIPTION_ID` settings.

Description: TODO: Explain what each group of settings is used for. Mask secrets.

---

## Task 7: End-to-End Pipeline (15 points)

### Evidence 7.1: Web App Wiring

TODO: Embed screenshot showing `FUNCTION_START_URL` and `FUNCTION_STATUS_URL` configured on the Web App.

Description: TODO: Explain how the frontend starts and polls the Durable orchestration.

### Evidence 7.2: Happy Path UI

TODO: Embed screenshots of the form before submit, Running status, and Completed status with report URL.

Description: TODO: Explain the valid order payload and final result.

### Evidence 7.3: Backend Participation

TODO: Embed screenshots showing Function App invocation, AKS validator evidence, ACI evidence, and Blob PDF evidence.

Description: TODO: Trace the same order ID across services.

### Evidence 7.4: Reject Path UI

TODO: Embed screenshot of an order with `qty > 100` being rejected.

Description: TODO: Explain why no report ACI should be created for this order.

---

## Task 8: Write-up and Architecture Diagram (5 points)

### Evidence 8.1: Architecture Diagram

Canonical diagram (Mermaid, editable): **[`docs/architecture.md`](docs/architecture.md)**.

It shows **GitHub Actions / Deployment Center → App Service Web App**; **browser → Web App → Function App** (HTTP starter + Durable status polling); **Function → AKS validator** (`POST /validate`); **Function → ACI** (**ephemeral** `ci-report-<order_id>` per run via SDK); **ACI → Blob** (`reports` container); **ACR** supplying **validate-api**, **report-job**, and **func-app** images; and **user-assigned managed identity** `mi-pa4-<roll>` on the **Function App** (and **AZURE_CLIENT_ID** in the report container).

**TODO (optional PNG):** Export from [mermaid.live](https://mermaid.live) or Draw.io and embed: `![Architecture](docs/architecture.png)`.

---

### Question 8.2: Service selection (cost, scale, operations)

**App Service Web App.** The UI is a thin Node/Express dashboard with proxied routes to the Durable starter and status API. App Service provides **managed HTTPS**, **always-on** hosting on a predictable **plan SKU** (**Basic B1**), and **straightforward GitHub CI/CD** (`webapp/` subtree). Cost is mostly **flat monthly plan time** for this traffic class; scaling is **manual plan sizing**—appropriate for a demo entry point that must always answer the browser.

**Durable Functions on a dedicated Linux plan.** Ordering is a **multi-step workflow** (validate, then maybe long-running report), not a single request. Durable gives **durable orchestration state**, **replay-safe** branching, and a **status-query contract** the Web App can poll. Running on the **same App Service plan family as a custom container** satisfies the assignment constraint and avoids **Consumption cold starts** during demos. Operational model: **platform-managed runtime** + **storage-backed orchestration**; cost = **plan hours** + **minimal storage/executions** relative to bursts.

**AKS for the validator.** Validation is a **stable, always-reachable HTTP dependency** on **`/validate`** with a LoadBalancer. One **Standard_B2s** node illustrates **enterprise-style** microservice hosting: you pay for the **node VM uptime** continuously (“idle pod” still consumes the fleet). Operational overhead is higher (**kubectl**, Deployments, Services) but buys **explicit networking** and **Kubernetes-native** rollout semantics.

**ACI for the report job.** Report generation matches **batch** semantics: allocate CPU/mem, exit. ACI bills **seconds of allocation** while the container group exists; we **spin up per successful validation** and tear down afterward, aligning cost with **work done** instead of a second always-on replica on AKS.

---

### Question 8.3: ACI vs AKS — idle behaviour and abuse

After ~**10 minutes** without orders, **AKS remains warm**: the cluster **node**, **kube-system** components, and **validator Pods** stay scheduled; **idle** reflects **near-zero workload CPU**, not switched-off infra—**cost continues** mainly from **VM + LB** artefacts.  

For **ACI** in TaskFlow’s design, meaningful **idle** after a pipeline run means **zero long-lived report containers** once **`begin_delete` completes**. Intermittently you may briefly see **`Running`** while PDF work occurs; lingering manual test containers should be removed with **`az container delete`**.

If a attacker issued **1000 successful submissions/minute**, the dominant **incremental** spend becomes **many concurrent or serialized ACI executions** (**vCPU‑seconds × gigabyte‑seconds** each), likely exceeding incremental CPU on **one idle-priced AKS node** alone. Supporting evidence: **`az container list` / Metrics** bursts vs steady **Insights for node pool**.

---

### Question 8.4: Durable Functions vs chaining plain HTTP endpoints

**(1)** A monolithic synchronous HTTP handler would encapsulate validation **and ACI provisioning** in one externally invoked call, colliding with **timeouts** (**gateways/host limits**) while **`report-job` spins up**.

**(2)** **No automatic checkpoint**: duplicating retries could **double-spawn containers** absent custom idempotent stores Durable solves.

**(3)** **Runtime restarts lose in-memory chaining** unless you reinvent orchestration bookkeeping Durable persists.

Hence Durable separates **thin HTTP starter** vs **replayable orchestrator logic**.

---

### Question 8.5: Cost review

![Cost Analysis scoped to resource group](docs/task8-cost-analysis.png)

Drop your **Azure Portal → Cost Management → Cost analysis** export filtered on **`rg-sp26-25280068`** (date window covering experiments). Beneath screenshot, annotate **cost leader** (“AKS VM”, shared **ASP**, LB/NAT egress, …) and correlate **always-on baseline** versus **few ACI minutes during tests**.

*(If Spend is \$0 owing to allowances, explicitly state that expectation for production.)*

---

### Question 8.6: Challenges faced

**Monorepo deploy path.** Initial GitHub/Azure workflow invoked **`npm install`** at repo root → **ENOENT** on `package.json`. Adjusted **`main_pa4-<roll>.yaml`**/`deploy-webapp` to **`npm ci` under `webapp/`** pack correct artifact (**`node-app` flat layout** tweak after `upload-artifact`).

**CLI & container rough edges.** `az functionapp config appsettings` warned **Docker runtime unsupported** → used **`az webapp config appsettings`** for Function App tweaks; **`ACI --os-type`** required explicit **`Linux`** manual test; intermittent **`HTTPSConnection … Failed to resolve managment.azure.com`** flagged **local DNS/VPN proxy** resets.

**(Optional third)** Broken **`docker push`** (**write tcp …3128**) until **`unset HTTP_PROXY`** family.

Tune bullets to incidents you genuinely experienced prior to submitting.

---
