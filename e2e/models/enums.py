from enum import Enum


class TestMarker(Enum):
    data_portal_teardown = "data_portal_teardown"
    data_portal_verification = "data_portal_verification"
    operations_portal = "operations_portal"
    data_portal_activation = "data_portal_activation"


class FolderName(Enum):
    data_portal_teardown = "data_portal_teardown_test_reports"
    data_portal_verification = "data_portal_verification_test_reports"
    operations_portal = "operation_portal_subscription_test_reports"


class ExecutionHandlerStatusList(str, Enum):
    initialized = "initialized"
    deployedServices = "deployedServices"
    operationsPortalTestsDone = "operationsPortalTestsDone"
    dataPortalVerificationTestsDone = "dataPortalVerificationTestsDone"
    dataPortalTeardownTestsDone = "dataPortalTeardownTestsDone"
    finalReport = "finalReport"
    success = "success"
    failure = "failure"
