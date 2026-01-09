import asyncio
import logging
import os
from typing import Any

import httpx
from aws_lambda_powertools.utilities.data_classes import SNSEvent
from aws_lambda_powertools.utilities.typing import LambdaContext

from shared.env_validator import EnvValidator
from shared.utils import create_error_response, create_response

from .models.const import AUTHOR_EMAIL
from .services.approval import ApprovalService

logger = logging.getLogger("approval_handler")
logger.setLevel(logging.INFO)

REQUEST_TIMEOUT = 60.0


async def _process_event(event: SNSEvent, author_email: str) -> list[dict[str, Any]]:
    """
    Process SNS event with approval service.
    """
    async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
        approval_service = ApprovalService(client=client)
        return await approval_service.process_records(
            records=event["Records"], author_email=author_email
        )


def lambda_handler(event: SNSEvent, context: LambdaContext) -> dict[str, Any]:
    logger.info(f"Processing SNS event: {event}")

    if not EnvValidator.all_env_vars_present([AUTHOR_EMAIL]):
        return create_error_response(
            500, "env_validation: Missing environmental variable: AUTHOR_EMAIL"
        )

    author_email = os.environ.get(AUTHOR_EMAIL, "")

    try:
        responses = asyncio.run(_process_event(event=event, author_email=author_email))
        return create_response(200, {"responses": responses})

    except Exception as e:
        logger.error(f"Error processing SNS event: {e}")
        return create_error_response(500, str(e))
