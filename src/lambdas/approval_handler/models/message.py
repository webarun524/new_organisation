from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class TechnicalContact(BaseModel):
    """Contact information"""

    Email: str
    FirstName: str
    JobTitle: str
    LastName: str


class ProductDeployment(BaseModel):
    """The main model representing a product deployment."""

    CreatedByUserId: UUID
    InternalProductCode: str
    OrganizationId: str
    ProductDeploymentId: UUID
    Status: str
    TechnicalContact: TechnicalContact
    WorkloadVersion: Optional[str] = None
    # We don't need that
    # ProductFulfillmentInformation
    # UpdatedAt: datetime
    # CreatedAt: datetime


class ParsedMessage(BaseModel):
    """All essential information extracted from approval message."""

    product_deployment_info: ProductDeployment
    approve_url: str
    reject_url: str
    approval_request_id: str
    # We don't need that
    # organization_info
