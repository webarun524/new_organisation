# Mock workflow data for integration tests
# Template variable: WORKFLOW_NAME

WORKFLOW_DATA = {
    "workflowName": "WORKFLOW_NAME",
    "description": "This prints a storage record sent to the system",
    "registrationInstructions": {
        "concurrentWorkflowRun": 5,
        "concurrentTaskRun": 5,
        "workflowDetailContent": "",
        "active": True,
    },
}
