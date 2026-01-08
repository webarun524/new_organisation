import asyncio
import logging
from typing import TYPE_CHECKING, Any

from httpx import AsyncClient, HTTPStatusError

from lambdas.approval_handler.models.message import ParsedMessage
from lambdas.approval_handler.parsers.message import MessageParser
from shared.rest_client import RestClient

if TYPE_CHECKING:
    from httpx import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class ApprovalService(RestClient):
    def __init__(self, client: AsyncClient) -> None:
        super().__init__(client)

    async def approve(self, parsed_message: ParsedMessage) -> "Response":
        """
        Approves received request.
        """
        approval_url = parsed_message.approve_url
        approval_id = parsed_message.approval_request_id
        full_url = f"{approval_url}={approval_id}"

        logger.info(f"Sending approval request to: {full_url}")
        response = await self._get(full_url)

        try:
            response.raise_for_status()
            logger.info(
                f"Approval successful for request ID {approval_id}: Status {response.status_code}"
            )
        except HTTPStatusError:
            logger.error(
                f"Approval failed for request ID {approval_id}: Status {response.status_code}, Body: {response.text}"
            )
            raise

        return response

    def _should_approve(self, parsed_message: ParsedMessage, author_email: str) -> bool:
        """
        Determine if a message should be approved based on the author email.
        """
        author = parsed_message.product_deployment_info.TechnicalContact.Email
        if author != author_email:
            logger.info(f"Deployment requested by {author}. Skipping...")
            return False
        logger.info(f"Deployment requested by {author}. Approving...")
        return True

    async def process_records(
        self, records: list, author_email: str
    ) -> list[dict[str, Any]]:
        """
        Process multiple SNS records and approve them concurrently.
        """
        tasks_to_approve = []

        for record in records:
            sns_message = record["Sns"]
            topic_arn = sns_message["TopicArn"]
            message_id = sns_message["MessageId"]
            payload = sns_message["Message"]

            logger.info(f"Received message ID: {message_id} from Topic: {topic_arn}")
            logger.info(f"Message: {payload}")
            parsed_message = MessageParser.parse(payload)
            logger.info(f"Parsed message: {parsed_message.model_dump_json()}")
            if not self._should_approve(parsed_message, author_email):
                continue

            tasks_to_approve.append(self.approve(parsed_message))

        responses = await asyncio.gather(*tasks_to_approve, return_exceptions=True)

        results = []
        for response in responses:
            if isinstance(response, Exception):
                logger.error(f"Approval task failed with exception: {response}")
                results.append({"status_code": 500, "body": str(response)})
            else:
                results.append(
                    {"status_code": response.status_code, "body": response.text}
                )

        return results
