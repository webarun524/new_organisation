import asyncio
import logging
from typing import Any

from shared.bitbucket.bitbucket_client import BitbucketClient
from shared.bitbucket.errors import (
    ArtifactFileError,
    InvalidResponseError,
    PipelineFailedError,
    PipelineStatusError,
    PipelineTimeoutError,
    PipelineTriggerError,
)
from shared.bitbucket.type import BitbucketPipelineStatus
from shared.domain.type import OSDUVersion

logger = logging.getLogger(__name__)


class CommitCollectorConstants:
    """Configuration constants for CommitCollector"""

    # Timing configuration
    POLL_WAIT_TIME = 10  # seconds between status checks
    MAX_POLL_ATTEMPTS = 12  # maximum number of status check attempts


class CommitCollector:
    """Runs Bitbucket pipeline and extracts deployed commits"""

    def __init__(
        self,
        bitbucket_client: BitbucketClient,
        repo_slug: str = "dataops-deployment",
        poll_wait_time: int = CommitCollectorConstants.POLL_WAIT_TIME,
        max_poll_attempts: int = CommitCollectorConstants.MAX_POLL_ATTEMPTS,
    ) -> None:
        self._bitbucket_client = bitbucket_client
        self._poll_wait_time = poll_wait_time
        self._max_poll_attempts = max_poll_attempts
        self._repo_slug = repo_slug

    async def trigger_commit_collection(
        self, bb_env_name: str, osdu: OSDUVersion
    ) -> dict[str, Any]:
        """
        Triggers Bitbucket pipeline for deployed commit hashes collection.
        """
        body = self._bitbucket_client.prepare_pipeline_trigger_body(
            pipeline_name="deployed_commit_reporter",
            branch_name="main",
            variables=[
                {"key": "ENV", "value": bb_env_name},
                {"key": "OSDU", "value": osdu.value},
            ],
        )
        return await self._bitbucket_client.trigger_pipeline(
            repo_slug=self._repo_slug,
            request_body=body,
        )

    async def wait_for_completion(self, pipeline_uuid: str) -> None:
        """
        Waits for pipeline completion by polling status at regular intervals.
        """
        wait_time = self._poll_wait_time
        max_attempts = self._max_poll_attempts
        current_attempt = 1
        status = "INIT"

        logger.info(f"Waiting for pipeline {pipeline_uuid} to complete...")

        while current_attempt <= max_attempts:
            response = await self._bitbucket_client.check_pipeline_status(
                repo_slug=self._repo_slug, execution_uuid=pipeline_uuid
            )
            logger.debug(
                f"Pipeline status response (attempt {current_attempt}/{max_attempts}): {response}"
            )
            status = response["state"]["name"]
            status = BitbucketPipelineStatus[status].value

            if status == BitbucketPipelineStatus.COMPLETED.value:
                logger.info(f"Pipeline {pipeline_uuid} completed successfully")
                break
            elif status == BitbucketPipelineStatus.FAILED.value:
                error_msg = f"Pipeline {pipeline_uuid} failed with status: {response.get('state', {})}"
                logger.error(error_msg)
                raise PipelineFailedError(error_msg)

            logger.info(
                f"Pipeline {pipeline_uuid} status: {status}, waiting {wait_time}s..."
            )
            current_attempt += 1
            if current_attempt <= max_attempts:
                await asyncio.sleep(wait_time)

        if status != BitbucketPipelineStatus.COMPLETED.value:
            error_msg = f"Pipeline {pipeline_uuid} did not complete after {max_attempts * wait_time} seconds. Last status: {status}"
            logger.error(error_msg)
            raise PipelineTimeoutError(error_msg)

    async def get_commits(self, bb_env_name: str, osdu: OSDUVersion) -> dict[str, str]:
        """
        Orchestrates pipeline trigger, monitoring, and artifact retrieval to get deployed commits.
        """
        logger.info(
            f"Starting commit collection for env={bb_env_name}, osdu={osdu.value}"
        )

        try:
            pipeline_response = await self.trigger_commit_collection(
                bb_env_name=bb_env_name, osdu=osdu
            )
            uuid: str = pipeline_response["uuid"]
            logger.info(f"Pipeline triggered successfully with UUID: {uuid}")
        except (PipelineTriggerError, InvalidResponseError) as e:
            logger.error(
                f"Failed to trigger pipeline for env={bb_env_name}, osdu={osdu.value}: {e}"
            )
            raise

        try:
            await self.wait_for_completion(uuid)
            logger.info(f"Pipeline {uuid} completed successfully")
        except (PipelineFailedError, PipelineTimeoutError, PipelineStatusError) as e:
            logger.error(f"Pipeline {uuid} execution failed: {e}")
            raise

        try:
            # Bitbucket returns uuid in curly braces, normalize it
            uuid_clean = uuid.replace("{", "").replace("}", "")
            filename = f"commits-{uuid_clean}.json"
            commits_data = await self._bitbucket_client.get_file_from_artifacts(
                repo_slug=self._repo_slug, filename=filename
            )
            logger.info(
                f"Commit collection completed successfully for pipeline {uuid_clean}"
            )
            return commits_data
        except (ArtifactFileError, InvalidResponseError) as e:
            logger.error(f"Failed to retrieve artifact file for pipeline {uuid}: {e}")
            raise
