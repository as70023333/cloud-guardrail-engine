import os
import logging
from fastapi import FastAPI, HTTPException, Header, Depends, status
from pydantic import BaseModel
from providers.aws_quarantine import AWSQuarantineProvider
from providers.azure_quarantine import AzureQuarantineProvider

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("zero-trust-quarantine")

app = FastAPI(
    title="Zero-Trust Identity Quarantine Engine",
    description="Event-driven API daemon for instantaneous cross-cloud session revocation.",
    version="1.0.0"
)

API_SECRET_TOKEN = os.getenv("QUARANTINE_API_SECRET", "super-secret-token")

def verify_token(x_api_token: str = Header(...)):
    if x_api_token != API_SECRET_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Secret Token"
        )

class QuarantineRequest(BaseModel):
    user_principal_name: str  # e.g. alex.salazar@company.com
    aws_iam_role_name: str | None = None
    reason: str
    risk_score: float

class QuarantineResponse(BaseModel):
    status: str
    user_principal_name: str
    actions_taken: dict

@app.post("/api/v1/quarantine", response_model=QuarantineResponse, dependencies=[Depends(verify_token)])
async def trigger_quarantine(payload: QuarantineRequest):
    logger.warning(
        f"🚨 QUARANTINE TRIGGERED for {payload.user_principal_name} | "
        f"Reason: {payload.reason} | Risk Score: {payload.risk_score}"
    )

    actions = {"azure_entra": False, "aws_sts": False}

    # 1. Execute Azure Entra ID Revocation
    azure_provider = AzureQuarantineProvider()
    azure_success = await azure_provider.revoke_user_sessions(payload.user_principal_name)
    actions["azure_entra"] = azure_success

    # 2. Execute AWS IAM/STS Session Revocation
    if payload.aws_iam_role_name:
        aws_provider = AWSQuarantineProvider()
        aws_success = aws_provider.quarantine_iam_role(payload.aws_iam_role_name)
        actions["aws_sts"] = aws_success

    return QuarantineResponse(
        status="completed",
        user_principal_name=payload.user_principal_name,
        actions_taken=actions
    )

@app.get("/healthz")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
