import asyncio
import os
from typing import Any

import httpx
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext
from pydantic import ValidationError

from shared.bitbucket.bitbucket_client import BitbucketClient, BitbucketClientConfig
from shared.bitbucket.errors import (
    ArtifactFileError,
    InvalidResponseError,
    PipelineFailedError,
    PipelineStatusError,
    PipelineTimeoutError,
    PipelineTriggerError,
)
from shared.bitbucket.get_token_from_envs import get_token_from_envs
from shared.domain.type import (
    OSDUVersion,
)
from shared.utils import create_error_response, create_response

from .models.params import RequestParams
from .services.commit_collector import CommitCollector

# Configuration constants
REQUEST_TIMEOUT = int(os.environ.get("REQUEST_TIMEOUT", "140"))

logger = Logger(service="commit_collector")


async def _collect_hashes(
    token: str, bb_env_name: str, osdu: OSDUVersion
) -> dict[str, str]:
    """Collect commit hashes from Bitbucket pipeline"""
    async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
        bitbucket_config = BitbucketClientConfig(token)
        bitbucket_client = BitbucketClient(client=client, config=bitbucket_config)
        commit_collector = CommitCollector(bitbucket_client=bitbucket_client)
        return await commit_collector.get_commits(bb_env_name=bb_env_name, osdu=osdu)


def lambda_handler(event: dict, context: LambdaContext) -> dict[str, Any]:
    """
    Lambda handler for collecting commits from Bitbucket pipeline
    Requires BITBUCKET_TOKEN env
    """
    # Get and validate token
    try:
        token = get_token_from_envs()
    except ValueError as e:
        logger.error(f"Token validation failed: {e}")
        return create_error_response(500, str(e), "ConfigurationError")

    # Validate request parameters
    try:
        data = RequestParams.model_validate(event)
    except ValidationError as e:
        logger.error(f"Request validation failed: {e}")
        error_details = "; ".join(
            [f"{err['loc'][0]}: {err['msg']}" for err in e.errors()]
        )
        return create_error_response(
            400, f"Invalid request parameters: {error_details}", "ValidationError"
        )

    # map environment code to env name
    bb_env_name = data.bb_env_name
    osdu_version = data.osdu_version

    # Collect commits
    try:
        logger.info(
            f"Starting commit collection for env={bb_env_name}, osdu={osdu_version.value}"
        )
        commits_data = asyncio.run(
            _collect_hashes(token=token, bb_env_name=bb_env_name, osdu=osdu_version)
        )
        logger.info(
            f"Successfully collected commits for env={bb_env_name}, osdu={osdu_version.value}"
        )
        return create_response(200, commits_data)

    except PipelineFailedError as e:
        logger.error(f"Pipeline execution failed: {e}")
        return create_error_response(
            400, f"Pipeline execution failed: {str(e)}", "PipelineFailedError"
        )

    except PipelineTimeoutError as e:
        logger.error(f"Pipeline execution timeout: {e}")
        return create_error_response(
            504,
            f"Pipeline did not complete within timeout: {str(e)}",
            "PipelineTimeoutError",
        )

    except (
        PipelineTriggerError,
        PipelineStatusError,
        ArtifactFileError,
        InvalidResponseError,
    ) as e:
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
