from typing import Any, Optional

from pydantic import BaseModel, field_validator

from shared.domain.models.status import StatusList


class ExecutionRecord(BaseModel):
    Id: str
    Status: StatusList
    WorkloadVersion: Optional[str] = None
    DeployedServices: Optional[dict[str, Any]] = None
    DataPortalUrl: Optional[str] = None
    DeploymentId: Optional[str] = None
    SubscriptionTestReportUrl: Optional[str] = None
    VerificationTestReportUrl: Optional[str] = None
    TeardownTestReportUrl: Optional[str] = None
    FailureReason: Optional[str] = None
    CreatedAt: str
    UpdatedAt: str

    @field_validator(
        "SubscriptionTestReportUrl",
        "VerificationTestReportUrl",
        "TeardownTestReportUrl",
        mode="before",
    )
    @classmethod
    def validate_urls(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if not isinstance(v, str) or not v.strip():
            raise ValueError("URL must be a non-empty string")
        if not (v.startswith("http://") or v.startswith("https://")):
            raise ValueError(f"URL must start with http:// or https://: {v}")
        return v
