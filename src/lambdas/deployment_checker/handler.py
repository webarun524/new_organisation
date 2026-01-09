import asyncio
from typing import Any

import httpx
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext
from pydantic import ValidationError

from shared.bitbucket.bitbucket_client import BitbucketClient, BitbucketClientConfig
from shared.bitbucket.get_token_from_envs import get_token_from_envs
from shared.utils import create_error_response, create_response

from .models.errors import PipelineHasFailed
from .models.params import RequestParams
from .services.deployment_checker import DeploymentChecker

logger = Logger(service="deployment-checker")

REQUEST_TIMEOUT = 30.0


async def _trigger_pipeline(token: str, execution_uuid: str) -> bool:
    """Triggers Bitbucket Pipeline for selected environment"""
    async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
        bitbucket_config = BitbucketClientConfig(token)
        bitbucket_client = BitbucketClient(client=client, config=bitbucket_config)
        deployment_checker = DeploymentChecker(bitbucket_client=bitbucket_client)
        return await deployment_checker.check_if_finished(execution_uuid)


def lambda_handler(event: dict, context: LambdaContext) -> dict[str, Any]:
    """
    Lambda handler for checking dataops_deployments manual_deployment_from_branch pipeline
    """
    # Get and validate token
    try:
        token = get_token_from_envs()
    except ValueError as e:
        logger.error(f"Token validation failed: {e}")
        return create_error_response(500, str(e), "ConfigurationError")

    # Validate request parameters
    try:
        execution_uuid: str = RequestParams.model_validate(event).execution_uuid
    except ValidationError as e:
        logger.error(f"Request validation failed: {e}")
        error_details = "; ".join(
            [f"{err['loc'][0]}: {err['msg']}" for err in e.errors()]
        )
        return create_error_response(
            400, f"Invalid request parameters: {error_details}", "ValidationError"
        )

    # Check status
    try:
        is_completed = asyncio.run(
            _trigger_pipeline(token=token, execution_uuid=execution_uuid)
        )
        logger.info(f"Pipeline execution is completed: {is_completed}")

        return create_response(200, {"is_completed": is_completed})

    except PipelineHasFailed as e:
        logger.error(f"Bitbucket API error: {e}", exc_info=True)
        return create_error_response(
            502, f"Bitbucket API error: {str(e)}", type(e).__name__
        )

    except httpx.TimeoutException as e:
        logger.error(f"Request timeout: {e}")
        return create_error_response(
            504, "Request timed out while collecting commits", "TimeoutError"
        )

    except httpx.HTTPError as e:
        logger.error(f"HTTP error: {e}", exc_info=True)
        return create_error_response(502, f"HTTP error occurred: {str(e)}", "HTTPError")

    except Exception as e:
        logger.exception(f"Unexpected error in lambda_handler: {e}")
        return create_error_response(
            500, "An unexpected error occurred", "InternalError"
        )
