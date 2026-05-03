import azure.functions as func
import azure.durable_functions as df
import json
import os
import re
import time

import requests

app = df.DFApp(http_auth_level=func.AuthLevel.FUNCTION)


@app.route(route="orchestrators/my_orchestrator", methods=["POST"])
@app.durable_client_input(client_name="client")
async def http_starter(req: func.HttpRequest, client: df.DurableOrchestrationClient):
    order = req.get_json()
    instance_id = await client.start_new("my_orchestrator", client_input=order)
    return client.create_check_status_response(req, instance_id)


@app.orchestration_trigger(context_name="context")
def my_orchestrator(context: df.DurableOrchestrationContext):
    order = context.get_input()
    validation = yield context.call_activity("validate_activity", order)
    if not validation.get("valid"):
        return {"status": "rejected", "reason": validation.get("reason", "unknown")}
    report_url = yield context.call_activity("report_activity", order)
    return {"status": "completed", "report_url": report_url}


@app.activity_trigger(input_name="order")
def validate_activity(order: dict) -> dict:
    validate_url = os.environ["VALIDATE_URL"]
    r = requests.post(validate_url, json=order, timeout=120)
    r.raise_for_status()
    return r.json()


def _container_group_name(order_id: str) -> str:
    """DNS-safe ACI resource name (letters, digits, hyphens only)."""
    base = re.sub(r"[^a-zA-Z0-9-]", "-", order_id.lower()).strip("-") or "job"
    base = re.sub(r"-{2,}", "-", base)
    name = f"ci-report-{base}"
    return name[:63].rstrip("-")


@app.activity_trigger(input_name="order")
def report_activity(order: dict) -> str:
    from azure.identity import DefaultAzureCredential
    from azure.mgmt.containerinstance import ContainerInstanceManagementClient
    from azure.mgmt.containerinstance.models import (
        Container,
        ContainerGroup,
        ContainerGroupIdentity,
        ContainerGroupRestartPolicy,
        EnvironmentVariable,
        ImageRegistryCredential,
        OperatingSystemTypes,
        ResourceIdentityType,
        ResourceRequests,
        ResourceRequirements,
        UserAssignedIdentities,
    )

    sub_id = os.environ["SUBSCRIPTION_ID"]
    rg = os.environ["REPORT_RG"]
    loc = os.environ["REPORT_LOCATION"]
    image = os.environ["REPORT_IMAGE"]
    order_id = order["order_id"]
    name = _container_group_name(order_id)

    client = ContainerInstanceManagementClient(DefaultAzureCredential(), sub_id)

    rollnum = rg.split("-")[-1]
    mi_id = (
        f"/subscriptions/{sub_id}/resourcegroups/{rg}/providers/"
        f"Microsoft.ManagedIdentity/userAssignedIdentities/mi-pa4-{rollnum}"
    )

    group = ContainerGroup(
        location=loc,
        os_type=OperatingSystemTypes.LINUX,
        restart_policy=ContainerGroupRestartPolicy.NEVER,
        identity=ContainerGroupIdentity(
            type=ResourceIdentityType.USER_ASSIGNED,
            user_assigned_identities={
                mi_id: UserAssignedIdentities(),
            },
        ),
        image_registry_credentials=[
            ImageRegistryCredential(
                server=os.environ["ACR_SERVER"],
                username=os.environ["ACR_USERNAME"],
                password=os.environ["ACR_PASSWORD"],
            )
        ],
        containers=[
            Container(
                name="report",
                image=image,
                resources=ResourceRequirements(
                    requests=ResourceRequests(cpu=1.0, memory_in_gb=1.5)
                ),
                environment_variables=[
                    EnvironmentVariable(name="ORDER_ID", value=order_id),
                    EnvironmentVariable(name="ORDER_JSON", value=json.dumps(order)),
                    EnvironmentVariable(
                        name="STORAGE_ACCOUNT_URL",
                        value=os.environ["STORAGE_ACCOUNT_URL"],
                    ),
                    EnvironmentVariable(
                        name="AZURE_CLIENT_ID", value=os.environ["AZURE_CLIENT_ID"]
                    ),
                ],
            )
        ],
    )

    client.container_groups.begin_create_or_update(rg, name, group).result()

    state = None
    deadline = time.time() + 300
    while time.time() < deadline:
        info = client.container_groups.get(rg, name)
        state = info.instance_view.state if info.instance_view else None
        if state in ("Succeeded", "Failed"):
            break
        time.sleep(5)

    try:
        client.container_groups.begin_delete(rg, name).result()
    except Exception:
        pass

    if state != "Succeeded":
        raise RuntimeError(f"report-job ACI ended with state={state!r}")

    base_url = os.environ["STORAGE_ACCOUNT_URL"].rstrip("/")
    return f"{base_url}/reports/{order_id}.pdf"
