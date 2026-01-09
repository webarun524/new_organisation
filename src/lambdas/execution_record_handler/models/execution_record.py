import os

from pynamodb.attributes import (
    MapAttribute,
    UnicodeAttribute,
)
from pynamodb.indexes import AllProjection, GlobalSecondaryIndex
from pynamodb.models import Model

from ..const.env_variable_keys import (
    AWS_REGION_ENV_VAR,
    SECONDARY_INDEX_NAME_ENV_VAR,
    TABLE_NAME_ENV_VAR,
)


class StatusCreatedAtIndex(GlobalSecondaryIndex):
    class Meta:
        index_name = os.environ.get(SECONDARY_INDEX_NAME_ENV_VAR)
        read_capacity_units = 1
        write_capacity_units = 1
        projection = AllProjection()

    Status = UnicodeAttribute(hash_key=True)
    CreatedAt = UnicodeAttribute(range_key=True)


class DeployedServicesAttribute(MapAttribute):
    dataops_mb_vpc = UnicodeAttribute(null=True, attr_name="dataops-mb-vpc")
    dataops_mb_metering_service = UnicodeAttribute(
        null=True, attr_name="dataops-mb-metering-service"
    )
    dataops_mb_metering_console_service = UnicodeAttribute(
        null=True, attr_name="dataops-mb-metering-console-service"
    )
    osdu_r2_provider = UnicodeAttribute(null=True, attr_name="osdu-r2-provider")
    osdu_r1_manager = UnicodeAttribute(null=True, attr_name="osdu-r1-manager")
    dataops_mb_fulfillment_service = UnicodeAttribute(
        null=True, attr_name="dataops-mb-fulfillment-service"
    )
    dataops_mb_subscription_service = UnicodeAttribute(
        null=True, attr_name="dataops-mb-subscription-service"
    )
    dataops_mb_subscription_portal = UnicodeAttribute(
        null=True, attr_name="dataops-mb-subscription-portal"
    )
    r3m23 = UnicodeAttribute(null=True)
    r3m24 = UnicodeAttribute(null=True)
    r3m25 = UnicodeAttribute(null=True)
    osdu_console = UnicodeAttribute(null=True, attr_name="osdu-console")
    osdu_sample_visualization_app_backend = UnicodeAttribute(
        null=True, attr_name="osdu-sample-visualization-app-backend"
    )
    edi_shared = UnicodeAttribute(null=True, attr_name="edi-shared")
    osdu_user_management = UnicodeAttribute(null=True, attr_name="osdu-user-management")
    osdu_dataloading = UnicodeAttribute(null=True, attr_name="osdu-dataloading")
    osdu_tenant_usage_measurements = UnicodeAttribute(
        null=True, attr_name="osdu-tenant-usage-measurements"
    )
    osdu_partition_management = UnicodeAttribute(
        null=True, attr_name="osdu-partition-management"
    )
    osdu_platform_management = UnicodeAttribute(
        null=True, attr_name="osdu-platform-management"
    )

    def __init__(self, **attributes):
        # Map hyphenated keys to underscored attribute names
        mapped_attributes = {}
        for key, value in attributes.items():
            mapped_key = key.replace("-", "_")
            mapped_attributes[mapped_key] = value
        super().__init__(**mapped_attributes)


class ExecutionRecordModel(Model):
    class Meta:  # type: ignore
        table_name = os.environ.get(TABLE_NAME_ENV_VAR)
        region = os.environ.get(AWS_REGION_ENV_VAR)

    Id = UnicodeAttribute(hash_key=True)
    Status = UnicodeAttribute()
    WorkloadVersion = UnicodeAttribute(null=True)
    DeployedServices = DeployedServicesAttribute(null=True)
    DataPortalUrl = UnicodeAttribute(null=True)
    DeploymentId = UnicodeAttribute(null=True)
    SubscriptionTestReportUrl = UnicodeAttribute(null=True)
    VerificationTestReportUrl = UnicodeAttribute(null=True)
    TeardownTestReportUrl = UnicodeAttribute(null=True)
    FailureReason = UnicodeAttribute(null=True)
    CreatedAt = UnicodeAttribute()
    UpdatedAt = UnicodeAttribute()
    status_created_at_index = StatusCreatedAtIndex()

    def to_dict(self) -> dict:
        return {
            "Id": self.Id,
            "Status": self.Status,
            "WorkloadVersion": self.WorkloadVersion,
            "DeployedServices": self.DeployedServices.as_dict()
            if self.DeployedServices
            else None,
            "DataPortalUrl": self.DataPortalUrl,
            "DeploymentId": self.DeploymentId,
            "SubscriptionTestReportUrl": self.SubscriptionTestReportUrl,
            "VerificationTestReportUrl": self.VerificationTestReportUrl,
            "TeardownTestReportUrl": self.TeardownTestReportUrl,
            "FailureReason": self.FailureReason,
            "CreatedAt": self.CreatedAt,
            "UpdatedAt": self.UpdatedAt,
        }
