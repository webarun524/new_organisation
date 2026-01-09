import pytest

from src.lambdas.execution_record_handler.services.execution_record_validator import (
    REQUIRED_FIELDS_BY_STATUS,
    ExecutionRecordValidator,
)
from src.shared.domain.models.status import StatusList


@pytest.mark.parametrize(
    "status,required_fields,extra_fields",
    [
        (StatusList.initialized, ["WorkloadVersion"], {}),
        (
            StatusList.deployedServices,
            ["Id", "DeployedServices"],
            {"WorkloadVersion": "v1"},
        ),
        (
            StatusList.operationsPortalTestsDone,
            [
                "Id",
                "DataPortalUrl",
                "DeploymentId",
                "SubscriptionTestReportUrl",
                "WorkloadVersion",
            ],
            {"WorkloadVersion": "v1"},
        ),
        (
            StatusList.dataPortalVerificationTestsDone,
            ["Id", "VerificationTestReportUrl"],
            {"WorkloadVersion": "v1"},
        ),
        (
            StatusList.dataPortalTeardownTestsDone,
            ["Id", "TeardownTestReportUrl"],
            {"WorkloadVersion": "v1"},
        ),
        (StatusList.finalReport, ["Id"], {"WorkloadVersion": "v1"}),
        (StatusList.failure, ["Id", "FailureReason"], {"WorkloadVersion": "v1"}),
        (StatusList.success, ["Id"], {"WorkloadVersion": "v1"}),
    ],
)
def test_validate_required_fields_by_status(status, required_fields, extra_fields):
    payload = {"Status": status.value}
    payload.update({field: f"test_{field}" for field in required_fields})
    payload.update(extra_fields)
    assert ExecutionRecordValidator.validate(payload) is True


@pytest.mark.parametrize(
    "status,missing_field",
    [
        (StatusList.deployedServices, "Id"),
        (StatusList.deployedServices, "DeployedServices"),
        (StatusList.operationsPortalTestsDone, "Id"),
        (StatusList.operationsPortalTestsDone, "DataPortalUrl"),
        (StatusList.operationsPortalTestsDone, "DeploymentId"),
        (StatusList.operationsPortalTestsDone, "WorkloadVersion"),
        (StatusList.operationsPortalTestsDone, "SubscriptionTestReportUrl"),
        (StatusList.dataPortalVerificationTestsDone, "Id"),
        (StatusList.dataPortalVerificationTestsDone, "VerificationTestReportUrl"),
        (StatusList.dataPortalTeardownTestsDone, "Id"),
        (StatusList.dataPortalTeardownTestsDone, "TeardownTestReportUrl"),
        (StatusList.finalReport, "Id"),
        (StatusList.failure, "Id"),
        (StatusList.failure, "FailureReason"),
        (StatusList.success, "Id"),
    ],
)
def test_validate_missing_required_field_by_status(status, missing_field):
    required_fields = REQUIRED_FIELDS_BY_STATUS[status]
    payload = {"Status": status.value}
    for field in required_fields:
        if field != missing_field:
            payload[field] = f"test_{field}"
    with pytest.raises(
        ValueError,
        match=f"Missing required fields for status '{status.value}': {missing_field}",
    ):
        ExecutionRecordValidator.validate(payload)


def test_validate_missing_status():
    payload = {"WorkloadVersion": "v1"}
    with pytest.raises(ValueError, match="Missing required field: Status"):
        ExecutionRecordValidator.validate(payload)


def test_validate_invalid_status():
    payload = {"Status": "not_a_status", "WorkloadVersion": "v1"}
    with pytest.raises(ValueError, match="Invalid Status value: not_a_status"):
        ExecutionRecordValidator.validate(payload)


def test_full_payload(full_execution_record_payload):
    assert ExecutionRecordValidator.validate(full_execution_record_payload) is True
