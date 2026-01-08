from enum import Enum


class StatusList(str, Enum):
    initialized = "initialized"
    deployedServices = "deployedServices"
    operationsPortalTestsDone = "operationsPortalTestsDone"
    dataPortalVerificationTestsDone = "dataPortalVerificationTestsDone"
    dataPortalTeardownTestsDone = "dataPortalTeardownTestsDone"
    finalReport = "finalReport"
    success = "success"
    failure = "failure"
