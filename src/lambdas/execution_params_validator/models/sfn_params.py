import validators
from pydantic import BaseModel, Field, field_validator, model_validator

from shared.utils import to_snake_case


class SfnParams(BaseModel):
    osdu_version: str = Field(
        ...,
        pattern=r"^r3m\d{2}$",
        description="Pattern: r3mXX where XX are digits",
    )
    enterprise_product_type_active: bool
    data_portal_account_id: str = Field(
        ...,
        pattern=r"^\d{12}$",
        description="AWS Account ID (12 digits)",
    )
    deployment_role_name: str
    data_portal_domain: str
    data_portal_hosted_zone_id: str = Field(
        ...,
        pattern=r"^Z[A-Z0-9]{13,}$",
        description="AWS Route53 Hosted Zone ID (starts with 'Z')",
    )
    dry_run: bool
    skip_env_setup: bool
    teardown_trigger_active: bool

    @model_validator(mode="before")
    def snake_case_keys(cls, data):
        if isinstance(data, dict):
            return {to_snake_case(k): v for k, v in data.items()}
        return data

    @field_validator("deployment_role_name")
    def non_empty_role(cls, v):
        if not v.strip():
            raise ValueError("DeploymentRoleName/deployment_role_name cannot be empty")
        return v

    @field_validator("data_portal_domain")
    def correct_domain(cls, v):
        if not validators.domain(v):
            raise ValueError(
                "DataPortalDomain/data_portal_domain must be a valid domain"
            )
        return v
