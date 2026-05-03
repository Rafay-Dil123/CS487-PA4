# TaskFlow PA4 — Architecture Diagram

Rendered Mermaid diagram (GitHub preview). Naming matches typical PA rollout; align labels with **your** Web App URL, Function App hostname, ACR registry name (`pa4` + digits), AKS cluster name, and MI name (`mi-pa4-<digits>`).

```mermaid
flowchart TB
    subgraph CI["Continuous deployment"]
      GH["GitHub (fork)"]
      GA["GitHub Actions / Deployment Center"]
    end

    subgraph User["Browser"]
      U["User submits order"]
    end

    subgraph AppSvc["Azure — App Service (Linux plan)"]
      WEB["Web App\nNode / Express dashboard\n`/api/order` proxies starter\n`/api/status` proxies polling"]
      PLAN["Shared App Service plan\n(Basic B1)"]
      WEB --- PLAN
    end

    subgraph Func["Azure — Function App (Linux container)"]
      FA["pa4-<roll>-funcs\nDocker: func-app:v1"]
      DF["Durable orchestrator\nvalidate_activity • report_activity"]
      FA --- DF
    end

    subgraph K8s["Azure Kubernetes Service"]
      AKS["Cluster pa4-<roll>"]
      VAL["validate-api Deployment + Service\nLoadBalancer :8080"]
      AKS --- VAL
    end

    subgraph Jobs["On-demand compute"]
      ACI["ACI group `ci-report-<order>`\nephemeral, per run\nreport-job:v1"]
    end

    subgraph Data["Data & registry"]
      BLOB[("Blob Storage\ncontainer `reports`")]
      ACR[("ACR\nvalidate-api, report-job, func-app images")]
    end

    MI["User-assigned managed identity\nmi-pa4-<roll>\n(Azure SDK + report container)"]

    GH --> GA
    GA -->|"deploy `webapp/`"| WEB
    U -->|"HTTPS"| WEB
    WEB -->|"FUNCTION_START_URL\nPOST JSON order"| FA
    WEB -->|"FUNCTION_STATUS_URL prefix\nGET statusQueryGetUri"| FA
    DF -->|"VALIDATE_URL HTTP POST\n/validate"| VAL
    DF -->|"ContainerInstanceManagementClient\ncreate + poll + delete"| ACI
    ACI -->|"Managed identity\nupload PDF"| BLOB
    ACR -.->|"pull image"| VAL
    ACR -.->|"pull image"| ACI
    ACR -.->|"pull image"| FA
    MI -.->|"attached to Function App\nDefaultAzureCredential"| FA
    MI -.->|"ACI uses AZURE_CLIENT_ID"| ACI
```

## Legend (rubric alignment)

| Flow | Meaning |
|------|--------|
| GitHub → App Service | CI/CD for the web frontend only; images for backend come from ACR. |
| Web → Function | HTTP starter + Durable status polling via app settings. |
| Function → AKS | Synchronous HTTP validation on every accepted workflow path. |
| Function → ACI | Imperative **per-order** container group; deleted after completion in code paths. |
| ACI → Blob | One-shot PDF write using managed identity credentials. |
| ACR dashed lines | Pull secrets (AKS secret) / registry credentials (Function + ACI). |

For Tasks 7–8, export this page to PNG from GitHub (“…” → Download / or use Mermaid CLI) **or** redraw in draw.io following the same boxes and arrows.
