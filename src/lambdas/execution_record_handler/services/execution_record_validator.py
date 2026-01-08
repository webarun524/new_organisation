from shared.domain.models.status import StatusList

REQUIRED_FIELDS_BY_STATUS = {
    StatusList.initialized: [],
    StatusList.deployedServices: ["Id", "DeployedServices"],
    StatusList.operationsPortalTestsDone: [
        "Id",
        "DataPortalUrl",
        "DeploymentId",
        "WorkloadVersion",
        "SubscriptionTestReportUrl",
    ],
    StatusList.dataPortalVerificationTestsDone: ["Id", "VerificationTestReportUrl"],
    StatusList.dataPortalTeardownTestsDone: ["Id", "TeardownTestReportUrl"],
    StatusList.finalReport: ["Id"],
    StatusList.failure: ["Id", "FailureReason"],
    StatusList.success: ["Id"],
}


class ExecutionRecordValidator:
    @staticmethod
    def validate(payload: dict) -> bool:
        status = payload.get("Status")
        if not status:
            raise ValueError("Missing required field: Status")
        try:
            status_enum = StatusList(status)
        except ValueError:
            raise ValueError(f"Invalid Status value: {status}")

        missing = [
            f for f in REQUIRED_FIELDS_BY_STATUS[status_enum] if not payload.get(f)
        ]
        if missing:
            raise ValueError(
                f"Missing required fields for status '{status_enum.value}': {', '.join(missing)}"
            )
        return True
