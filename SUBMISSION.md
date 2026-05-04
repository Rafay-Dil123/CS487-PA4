<div align="center">

# PA4 Submission: TaskFlow Pipeline

<img alt="GitHub only" src="https://img.shields.io/badge/Submit-GitHub%20URL%20Only-10b981?style=for-the-badge">
<img alt="Total points" src="https://img.shields.io/badge/Total-100%20points-7c3aed?style=for-the-badge">

</div>

What follows is my evidence for PA4. I keep screenshots under `docs/` and reference them below. I masked any keys/passwords where a screenshot might have caught them.

## Student Information

| Field | Value |
|---|---|
| Name | Muhammad Rafay |
| Roll Number | 25280068 |
| GitHub Repository URL | https://github.com/Rafay-Dil123/CS487-PA4 |
| Resource Group | `rg-sp26-25280068` |
| Assigned Region | `ukwest` |

## Evidence Rules

- I use relative paths like `![AKS nodes](docs/aks-nodes.png)`.
- Under each image I wrote one short note in my own words.
- Portal shots show the resource name where I could fit it in frame.
- I blurred or cropped function keys, ACR passwords, and storage secrets if needed.


## Task 1: App Service Web App (15 points)

### Evidence 1.1: Forked Repository

**Screenshot to add:** `docs/task1-fork.png`

**What I’m showing:** I forked the course starter so pushes and GitHub Actions run against **my** repo (`Rafay-Dil123/CS487-PA4`), not the upstream org repo.

### Evidence 1.2: App Service Overview

**Screenshot to add:** `docs/task1-webapp-overview.png`

**What I’m showing:** My App Service web app **`pa4-25280068`** lives in **`rg-sp26-25280068`**, **UK West**, Linux stack, **Running**. Public URL: `https://pa4-25280068.azurewebsites.net`.

### Evidence 1.3: Deployment Center / GitHub Actions

**Screenshot to add:** `docs/task1-deployment-center-or-actions.png`

**What I’m showing:** I hooked deployment to my fork on **`main`** and used the existing workflow (`main_pa4-25280068.yml`) so pushes under `webapp/` deploy the Express app from the **`webapp/`** folder (not the repo root).

### Evidence 1.4: Live Web UI

**Screenshot to add:** `docs/task1-browser-ui.png`

**What I’m showing:** I loaded the live site in a browser—the TaskFlow form renders so App Service is actually serving my static + API bundle.


---

## Task 2: Azure Container Registry (15 points)

### Evidence 2.1: ACR Overview

**Screenshot to add:** `docs/task2-acr-overview.png`

**What I’m showing:** Registry **`pa425280068`**, **Basic** SKU, same resource group **`rg-sp26-25280068`**.

### Evidence 2.2: Docker Builds

**Screenshot to add:** `docs/task2-docker-build.png`

**What I’m showing:** I built all three images locally with `docker build --platform linux/amd64` from **`validate-api/`**, **`report-job/`**, and **`function-app/`** on my Mac.

### Evidence 2.3: ACR Repositories

**Screenshot to add:** `docs/task2-acr-repos.png`

**What I’m showing:** I tagged and pushed **`validate-api:v1`**, **`report-job:v1`**, and **`func-app:v1`** to **`pa425280068.azurecr.io`**.


---

## Task 3: Durable Function Implementation (12 points)

### Evidence 3.1: Completed Function Code

My implementation is in [`function-app/function_app.py`](function-app/function_app.py).

**In my words:** I wired **`my_orchestrator`** to call **`validate_activity`** first; if validation fails I return **`rejected`**. If it passes I call **`report_activity`**, which spins up ACI via the SDK, waits for **`Succeeded`**, deletes the group, and returns the PDF URL string.

### Evidence 3.2: Local Function Handler Listing

**Screenshot to add:** `docs/task3-func-start.png`

**What I’m showing:** When I ran **`func start`** (with Azurite for storage) the host listed my **HTTP starter**, **`my_orchestrator`**, **`validate_activity`**, and **`report_activity`**.


---

## Task 4: Function App Container Deployment (8 points)

### Evidence 4.1: Function App Container Configuration

**Screenshot to add:** `docs/task4-function-container.png`

**What I’m showing:** My Function App **`pa4-25280068-funcs`** pulls **`pa425280068.azurecr.io/func-app:v1`** from my ACR on the same Linux App Service plan I used for the web app.

### Evidence 4.2: Orchestration Smoke Test

**Screenshot to add:** `docs/task4-curl-start.png`

**What I’m showing:** I posted to the **HTTP starter** with **`curl`**; the JSON came back with an **`id`** and **`statusQueryGetUri`** so I know the extension bundle and routing work.

### Evidence 4.3: Expected Failed Status Before Downstream Wiring

**Screenshot to add:** `docs/task4-status-before-validate.png`

**What I’m showing:** Early on, **`validate_activity`** failed until I set **`VALIDATE_URL`**—that’s expected before Task 5 wiring.


---


## Task 5: AKS Validator (15 points)

### Evidence 5.1: AKS Cluster

**Screenshot to add:** `docs/task5-aks-overview.png`

**What I’m showing:** Cluster **`pa4-25280068`**, **1 × Standard_B2s** node, **`rg-sp26-25280068`**, **UK West**.

### Evidence 5.2: Kubernetes Nodes and Pods

**Screenshot to add:** `docs/task5-kubectl-nodes-pods.png`

**What I’m showing:** **`kubectl get nodes`** and **`kubectl get pods`**—my **`validate-deployment`** pod reached **Running**.

### Evidence 5.3: Kubernetes Service

**Screenshot to add:** `docs/task5-kubectl-service.png`

**What I’m showing:** **`kubectl get service validate-service`**—**LoadBalancer** exposed **`8080`** with a public **EXTERNAL-IP** (not pending).

### Evidence 5.4: Validator API Tests

**Screenshot to add:** `docs/task5-curl-tests.png`

**What I’m showing:** **`/health`** returns **`ok`**. A normal order returns **`valid: true`**. **`qty > 100`** returns **`valid: false`** with **`quantity exceeds limit`** per the starter **`app.py`**.

### Evidence 5.5: Function App `VALIDATE_URL`

**Screenshot to add:** `docs/task5-function-validate-url.png`

**What I’m showing:** I set **`VALIDATE_URL`** on **`pa4-25280068-funcs`** to **`http://<LB-IP>:8080/validate`** so **`validate_activity`** can reach my AKS **LoadBalancer**.

### Evidence 5.6: AKS Idle Behavior

**Screenshot to add:** `docs/task5-ak-idle-or-metrics.png`

**What I’m showing:** When nothing is ordering, CPU on the validator drops but **the node still runs**—I’m still paying for the **B2s** VM and the LB; “idle” here just means low request traffic.


---


## Task 6: ACI Report Job (15 points)

### Evidence 6.1: Blob Container

**Screenshot to add:** `docs/task6-blob-reports-container.png`

**What I’m showing:** I created the **`reports`** container on my storage account for PDF output (`stpa425280068` in my setup).

### Evidence 6.2: Manual ACI Run

**Screenshot to add:** `docs/task6-aci-show.png`

**What I’m showing:** **`az container show`** for **`ci-report-test`** ended in **`Succeeded`** after **`report-job`** ran once (`--restart-policy Never`).

### Evidence 6.3: ACI Logs

**Screenshot to add:** `docs/task6-aci-logs.png`

**What I’m showing:** Logs show ReportLab work and a line about uploading **`TEST-001.pdf`** to the **`reports`** container.

### Evidence 6.4: Generated PDF

**Screenshot to add:** `docs/task6-blob-test-pdf.png`

**What I’m showing:** **`TEST-001.pdf`** appears in Blob Storage—so the identity + **`STORAGE_ACCOUNT_URL`** path worked.

### Evidence 6.5: Function App Managed Identity and IAM

**Screenshot to add:** `docs/task6-function-identity.png` (and IAM if required)

**What I’m showing:** I attached the instructor **`mi-pa4-25280068`** user-assigned identity to **`pa4-25280068-funcs`** so **`DefaultAzureCredential`** can create ACIs without me pasting secrets in code.

### Evidence 6.6: Report App Settings

**Screenshot to add:** `docs/task6-function-report-settings.png`

**What I’m showing:** **`REPORT_IMAGE`**, **`REPORT_RG`**, **`REPORT_LOCATION`**, **`SUBSCRIPTION_ID`**, **`STORAGE_ACCOUNT_URL`**, **`AZURE_CLIENT_ID`**, **`ACR_*`** so **`report_activity`** matches what the handout expects. I masked **`ACR_PASSWORD`** in the shot.


---


## Task 7: End-to-End Pipeline (15 points)

### Evidence 7.1: Web App Wiring

**Screenshot to add:** `docs/task7-webapp-function-settings.png`

**What I’m showing:** On **`pa4-25280068`** I set **`FUNCTION_START_URL`** to the **Function App** host (**`pa4-25280068-funcs.azurewebsites.net`**, not the web hostname) with the **`http_starter`** key, and **`FUNCTION_STATUS_URL`** to the durable instances prefix so **`/api/status`** proxy accepts **`statusQueryGetUri`**.

### Evidence 7.2: Happy Path UI

**Screenshots to add:** `docs/task7-happy-form.png`, `docs/task7-happy-running.png`, `docs/task7-happy-done.png`, `docs/task7-pdf.png`

**What I’m showing:** I submitted a valid order (**qty ≤ 100**), saw **Running** with an instance id, then **Completed** with a report link, and opened the PDF.

### Evidence 7.3: Backend Participation

**Screenshots to add:** `docs/task7-monitor.png`, `docs/task7-aks-logs.png`, `docs/task7-aci-list.png`, `docs/task7-blob-order-pdf.png`

**What I’m showing:** Same **order id** shows up in Function invocations, validator traffic/AKS logs, an **`ci-report-…`** ACI, and the matching **`.pdf`** in **`reports`**.

### Evidence 7.4: Reject Path UI

**Screenshot to add:** `docs/task7-reject-ui.png`

**What I’m showing:** For **`qty > 100`** the UI shows **Rejected** / **quantity exceeds limit** and my run should not spin up a new **report** ACI for that order.


---


## Task 8: Write-up and Architecture Diagram (5 points)

### Evidence 8.1: Architecture Diagram

I drew the pipeline in Mermaid here: **[`docs/architecture.md`](docs/architecture.md)** (GitHub renders it on the repo page).

**In my own words:** I included GitHub deploying the web app, my browser hitting **App Service**, the proxies to **Durable** on **`pa4-25280068-funcs`**, **`POST /validate`** to **AKS**, SDK-created **ephemeral ACI** for **`report-job`**, upload to **Blob**, images from **ACR**, and **user-assigned MI** on the Function App.

If my instructor wants a PNG, I also exported **`docs/architecture.png`** from mermaid.live / Draw.io: `![Architecture](docs/architecture.png)` — I attach it if present.

---

### Question 8.2: Service selection (cost, scale, operations)

**Why I used App Service for the web UI**

I picked App Service for the dashboard because I needed a cheap, always-on HTTPS front door for a tiny Node/Express app. I’m on **Basic B1** with Linux, billing is basically “pay for the plan whether or not anyone clicks,” which is fine for our demo traffic. Scaling is manual (bigger SKU or more instances)—I didn’t need Kubernetes just to host static assets plus two proxy routes.

**Why I used Durable Functions for the backend**

My flow isn’t one HTTP call—it chains **validate** then maybe a **long report** step. Durable gives me **orchestration history**, **replay-safe code**, and the **`statusQueryGetUri`** my UI polls. I run it as a **Linux container** on a **dedicated plan** so I could use the same kind of **App Service plan** story as the web tier and avoid weird **Consumption** cold starts during demos. I pay plan time + a bit of storage for the Durable backend, not pay-per-invocation only.

**Why I put the validator on AKS**

The validator has to stay up with a **stable LoadBalancer IP** while orders come in—that’s classic microservice hosting. The assignment asked for **`Standard_B2s` / one node** so I’m paying for that **VM + control plane overhead** even when traffic is quiet. Operationally it cost me **`kubectl`**, manifests, and understanding Services, but I get the industry default for a long-lived HTTP **Service**.

**Why I used ACI for the report job**

Generating a PDF is a **batch**: run the container, exit. **ACI** bills per **vCPU / memory second** while the group exists. My code creates the group, waits for **Succeeded**, then deletes it, so I’m not keeping another 24/7 workload like the validator. That matches “short job, pay only while it runs,” which would waste money as another always-on pod on AKS for this class.

---

### Question 8.3: ACI vs AKS — idle and the “spam” thought experiment

**If my AKS cluster sits idle for ten minutes**

Nothing “turns off.” My **node pool VM** is still there, **kube-system** pods still run, and the **validator Deployment** keeps its pod scheduled. “Idle” really means **almost no traffic**—CPU graphs go flat—but I’m **still billed** for that **B2s** and the **public LoadBalancer** plumbing stays allocated.

**What “idle” means for ACI in *my* pipeline**

After **`report_activity`** finishes, I **`delete`** the container group. So when I’m not processing an order there’s **no report container** sitting in my RG costing money—unlike AKS where the cluster is always there. If I left **`ci-report-test`** around after experimenting I cleaned it up with **`az container delete`**.

**If someone spammed Submit 1000 times/min with valid small orders**

The painful part is **report generation**: I’d spawn **tons of ACI groups** (each 1 vCPU / 1.5 GiB for tens of seconds). That would spike **per-second ACI** charges way faster than the **AKS node** would move on its fixed price—unless validation started failing first. So **ACI cost** would likely dominate among the pieces *I* pay per burst.

I’m tying this back to my Task 7 evidence (AKS metrics / **`az container list`** screenshots) in **`docs/`**.

---

### Question 8.4: Durable Functions vs plain HTTP

If I tried two normal HTTP functions calling each other in one request, I’d probably hit **timeouts**—my report step can run close to a minute while ACI boots and uploads a blob, and front doors don’t like holding that long.

Also I’d have no built-in **checkpoint** between “validation passed” and “ACI finished”: if something retried I could accidentally **create duplicate ACIs** unless I built my own database locks. Durable already **persists orchestration state** and gives me **deterministic replay** semantics so I don’t re-run side effects blindly.

---

### Question 8.5: Cost review

![Cost Analysis scoped to resource group](docs/task8-cost-analysis.png)

**What I did:** I opened **Cost Management → Cost analysis**, filtered to **`rg-sp26-25280068`**, and grabbed the chart for the weeks I actually worked on PA4.

**How I read it:** In my run the biggest line item was usually **compute I leave switched on**—shared **App Service plan** (web + function) plus **AKS node** time add up because they never scale to zero in this design. My **ACI** shows up as smaller spikes because those jobs are short. If my subscription showed **\$0** because of for-credit credits I still describe what *would* dominate in production.

---

### Question 8.6: Challenges I actually hit

**GitHub Actions kept running `npm install` at repo root.**  
I didn’t have a root **`package.json`**, so CI failed until I pointed the workflow at **`webapp/`** (`npm ci`, deploy that folder). I compared the Azure-generated YAML to the paths Kudu expects and fixed the **artifact path** (`node-app` vs `webapp` after download).

**CLI weirdness around dockerized Functions and app settings.**  
`az functionapp config appsettings set` sometimes complained about **docker runtime** and weird **`null`** values when I accidentally left **`$IP` empty**. I switched to **`az webapp config appsettings set`** for some updates and double-checked **`FUNCTION_STATUS_URL`** matches **`statusQueryGetUri`**.

**Misc debugging.**  
I hit **`docker push`** failures through a proxy (`broken pipe`) until I **`unset` HTTP_PROXY vars. **`az`** sometimes couldn’t resolve **`management.azure.com`** until I fixed Wi‑Fi/DNS. For ACI **`az container create`** I needed **`--os-type Linux`** or the API returned **`InvalidOsType`**.

---

