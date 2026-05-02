#!/usr/bin/env bash
# PA4 Task 2 — set roll to YOUR student roll digits (below matches existing rg/pa4 web app naming).
set -euo pipefail

ROLL="${ROLL:-25280068}"
RG="rg-sp26-${ROLL}"
ACR_NAME="pa4${ROLL}"
# README: 2027-10 -> ukwest; 2024/2025/2026-10 -> uaenorth
LOCATION="${LOCATION:-ukwest}"
REGISTRY="${ACR_NAME}.azurecr.io"
TAG="${TAG:-v1}"

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT}"

echo "Expecting ACR to exist already. One-time provision (Portal or CLI):"
echo "az acr create -g \"${RG}\" -n \"${ACR_NAME}\" --sku Basic -l \"${LOCATION}\" --admin-enabled true"
az acr show -g "${RG}" -n "${ACR_NAME}" --query "{loginServer:loginServer,adminUserEnabled:adminUserEnabled}" -o yaml

echo "Docker build (linux/amd64 — required from Apple Silicon)"
docker build --platform linux/amd64 -t validate-api:latest ./validate-api
docker build --platform linux/amd64 -t report-job:latest ./report-job
docker build --platform linux/amd64 -t func-app:latest ./function-app

echo "ACR login + tag + push"
az acr login --name "${ACR_NAME}"

docker tag validate-api:latest "${REGISTRY}/validate-api:${TAG}"
docker tag report-job:latest "${REGISTRY}/report-job:${TAG}"
docker tag func-app:latest "${REGISTRY}/func-app:${TAG}"

docker push "${REGISTRY}/validate-api:${TAG}"
docker push "${REGISTRY}/report-job:${TAG}"
docker push "${REGISTRY}/func-app:${TAG}"

echo "Repositories:"
az acr repository list --name "${ACR_NAME}" --output table
