import json

from aws_lambda_powertools import Logger

from shared.domain.models.status import StatusList

from .validator import Validator

logger = Logger(service="report_lambda_handler")


class ReportLambdaHandler:
    def __init__(
        self, lambda_client, function_name: str | None, execution_id: str
    ) -> None:
        self._client = lambda_client
        self._function_name = function_name

        if not execution_id:
            raise Exception("Missing execution ID")

        self.execution_id = execution_id

    def _prepare_payload(
        self,
    ):
        return {"Id": self.execution_id, "Status": StatusList.finalReport.value}

    def _invoke(self, payload: dict) -> dict:
        """
        Invoke record handler lambda function
        """
        return self._client.invoke(
            FunctionName=self._function_name,
            InvocationType="RequestResponse",
            Payload=json.dumps(payload),
        )

    def _extract_record(self, response: dict) -> dict:
        """
        Extract record from response, perform validation
        """
        try:
            payload_body = response.get("Payload")
            if not payload_body:
                raise ValueError("Missing Payload in response")

            response_content = payload_body.read()
            response_content = json.loads(response_content).get("body", {})
            logger.info("Successfully parsed lambda response payload", response_content)
        except Exception as e:
            logger.error(f"Error reading payload: {str(e)}")
            raise

        message = response_content.get("message")
        if message != "Record saved successfully":
            logger.warning(f"Unexpected response message: {message}")

        record: dict = response_content.get("db_record", {})

        Validator._validate_execution_record(record)

        return record

    def main(
        self,
    ) -> dict:
        """
        Orchestrate lambda call, record extraction and validation
        """
        payload = self._prepare_payload()
        response = self._invoke(payload=payload)
        record = self._extract_record(response)

        return record
