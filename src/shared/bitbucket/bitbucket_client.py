import json
import logging
from typing import Any

from httpx import AsyncClient, HTTPStatusError

from ..rest_client import RestClient, RestClientConfig
from .errors import (
    ArtifactFileError,
    InvalidResponseError,
    PipelineStatusError,
    PipelineTriggerError,
)

logger = logging.getLogger(__name__)


class BitbucketConstants:
    """Configuration constants for BitbucketClient"""

    # API paths
    PIPELINES_PATH = "/pipelines"
    DOWNLOADS_PATH = "/downloads"
    BITBUCKET_API_BASE = "https://api.bitbucket.org/2.0"

    # Default timeout for API requests (seconds)
    DEFAULT_TIMEOUT = 30


class BitbucketClientConfig(RestClientConfig):
    """Configuration for BitbucketClient including authentication and repository details"""

    def __init__(
        self,
        token: str,
        workspace: str = "47lining",
        timeout: float = BitbucketConstants.DEFAULT_TIMEOUT,
    ) -> None:
        self.token = token
        self.workspace = workspace
        self.timeout = timeout

    def apply(self, client: AsyncClient) -> None:
        client.headers.update({"Authorization": f"Bearer {self.token}"})
        client.timeout = self.timeout


class BitbucketClient(RestClient):
    """Provides shared Bitbucket API logic"""

    def __init__(self, client: AsyncClient, config: BitbucketClientConfig) -> None:
        super().__init__(client, config)
        self._config = config

    def _get_repo_api_url(self, repo_slug: str) -> str:
        """Build the repository API URL for the given repository slug"""
        return (
            f"{BitbucketConstants.BITBUCKET_API_BASE}/repositories/47lining/{repo_slug}"
        )

    def prepare_pipeline_trigger_body(
        self,
        pipeline_name: str,
        variables: list[dict],
        branch_name: str = "main",
    ) -> dict[str, Any]:
        return {
            "target": {
                "type": "pipeline_ref_target",
                "ref_type": "branch",
                "ref_name": branch_name,
                "selector": {
                    "type": "custom",
                    "pattern": pipeline_name,
                },
            },
            "variables": variables,
        }

    async def trigger_pipeline(
        self, repo_slug: str, request_body: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Triggers a Bitbucket pipeline.
        """
        try:
            response = await self._post(
                url=f"{self._get_repo_api_url(repo_slug)}{BitbucketConstants.PIPELINES_PATH}",
                json=request_body,
            )
            response.raise_for_status()

            try:
                response_data = response.json()
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON response: {e}")
                logger.error(f"Response content: {response.text}")
                raise InvalidResponseError(
                    f"Invalid JSON response from pipeline trigger: {e}"
                ) from e

            if "uuid" not in response_data:
                logger.error(f"Response missing 'uuid' field: {response_data}")
                raise InvalidResponseError(
                    "Pipeline response does not contain 'uuid' field"
                )

            logger.info(f"Pipeline triggered successfully: {response_data.get('uuid')}")
            return response_data

        except InvalidResponseError:
            raise
        except HTTPStatusError as e:
            logger.error(
                f"HTTP error triggering pipeline: {e.response.status_code} - {e.response.text}"
            )
            raise PipelineTriggerError(
                f"Failed to trigger pipeline: HTTP {e.response.status_code}"
            ) from e
        except Exception as e:
            logger.error(f"Unexpected error triggering pipeline: {e}")
            raise PipelineTriggerError(f"Unexpected error: {e}") from e

    async def check_pipeline_status(
        self, repo_slug: str, execution_uuid: str
    ) -> dict[str, Any]:
        """
        Checks the status of a Bitbucket pipeline.
        """
        try:
            pipeline_status_url = f"{self._get_repo_api_url(repo_slug)}{BitbucketConstants.PIPELINES_PATH}/{execution_uuid}"
            response = await self._get(pipeline_status_url)
            response.raise_for_status()

            try:
                response_data = response.json()
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse pipeline status JSON: {e}")
                logger.error(f"Response content: {response.text}")
                raise InvalidResponseError(
                    f"Invalid JSON response from pipeline status: {e}"
                ) from e

            if "state" not in response_data or "name" not in response_data.get(
                "state", {}
            ):
                logger.error(f"Response missing 'state.name' field: {response_data}")
                raise InvalidResponseError(
                    "Pipeline status response missing 'state.name' field"
                )

            return response_data

        except InvalidResponseError:
            raise
        except HTTPStatusError as e:
            logger.error(
                f"HTTP error checking pipeline status: {e.response.status_code} - {e.response.text}"
            )
            raise PipelineStatusError(
                f"Failed to check pipeline status: HTTP {e.response.status_code}"
            ) from e
        except Exception as e:
            logger.error(
                f"Unexpected error checking pipeline status for {execution_uuid}: {e}"
            )
            raise PipelineStatusError(f"Unexpected error: {e}") from e

    async def get_file_from_artifacts(self, repo_slug: str, filename: str) -> Any:
        """
        Retrieves file content from repository artifacts.
        """
        try:
            downloads_path = f"{self._get_repo_api_url(repo_slug)}{BitbucketConstants.DOWNLOADS_PATH}/{filename}"
            logger.info(f"Fetching file from artifacts: {filename}")

            response = await self._get(downloads_path, follow_redirects=True)
            response.raise_for_status()

            try:
                file_data = response.json()
                logger.info(
                    f"Successfully retrieved data for file {filename} from repo {repo_slug}"
                )
                return file_data
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse commits file JSON: {e}")
                logger.error(f"Response content: {response.text}")
                raise InvalidResponseError(f"Invalid JSON in commits file: {e}") from e

        except InvalidResponseError:
            raise
        except HTTPStatusError as e:
            logger.error(
                f"HTTP error fetching file: {e.response.status_code} - {e.response.text}"
            )
            raise ArtifactFileError(
                f"Failed to fetch artifact file: HTTP {e.response.status_code}"
            ) from e
        except Exception as e:
            logger.error(
                f"Unexpected error fetching {filename} file for {repo_slug} repo: {e}"
            )
            raise ArtifactFileError(
                f"Unexpected error fetching {filename} file: {e}"
            ) from e
