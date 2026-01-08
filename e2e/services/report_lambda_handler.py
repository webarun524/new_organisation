import json
import os

from ..models.enums import ExecutionHandlerStatusList as StatusList
from ..models.enums import TestMarker
from ..models.errors import InvalidTestMarkValue, MissingReportValue


class ReportLambdaHandler:
    def __init__(self, lambda_client, function_name: str):
        self._client = lambda_client
        self._function_name = function_name

    def _prepare_payload(
        self,
        test_marker: str,
        execution_id: str,
        report_url: str,
    ):
        # Extract from environment variables
        data_portal_domain: str = os.getenv("DP_DOMAIN", "")
        data_portal_url = (
            f"https://{data_portal_domain}"
            if data_portal_domain.startswith("https://")
            else data_portal_domain
        )
        workload_version = os.getenv("WORKLOAD_VERSION")
        deployment_id = os.getenv("DEPLOYMENT_ID")
        """
        Prepares payload based on test_marker value
        """

        if not all([execution_id, report_url]):
            raise MissingReportValue

        if test_marker == TestMarker.operations_portal.value:
            if not all([data_portal_url, deployment_id, workload_version]):
                raise MissingReportValue

            return {
                "Status": StatusList.operationsPortalTestsDone.value,
                "Id": execution_id,
                "DataPortalUrl": data_portal_url,
                "DeploymentId": deployment_id,
                "SubscriptionTestReportUrl": report_url,
                "WorkloadVersion": workload_version,
            }

        if test_marker == TestMarker.data_portal_verification.value:
            return {
                "Status": StatusList.dataPortalVerificationTestsDone.value,
                "Id": execution_id,
                "VerificationTestReportUrl": report_url,
            }

        if test_marker == TestMarker.data_portal_teardown.value:
            return {
                "Status": StatusList.dataPortalTeardownTestsDone.value,
                "Id": execution_id,
                "TeardownTestReportUrl": report_url,
            }

        raise InvalidTestMarkValue

    def _invoke(self, payload: dict) -> dict:
        return self._client.invoke(
            FunctionName=self._function_name,
            InvocationType="RequestResponse",
            Payload=json.dumps(payload),
        )

    def main(
        self,
        test_marker: str,
        report_url: str,
        execution_id: str,
    ):
        payload = self._prepare_payload(
            test_marker=test_marker,
            report_url=report_url,
            execution_id=execution_id,
        )

        return self._invoke(payload=payload)
