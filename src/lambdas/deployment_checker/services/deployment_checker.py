import logging

from shared.bitbucket.bitbucket_client import BitbucketClient
from shared.bitbucket.type import BitbucketPipelineStatus

from ..models.errors import PipelineHasFailed

logger = logging.getLogger(__name__)


class DeploymentChecker:
    """Checks status of dataops_deployments manual_deployment_from_branch pipeline"""

    def __init__(
        self,
        bitbucket_client: BitbucketClient,
        repo_slug: str = "dataops-deployment",
    ) -> None:
        self._bitbucket_client = bitbucket_client
        self._repo_slug = repo_slug

    async def _check_status(self, execution_uuid: str) -> str:
        execution_data = await self._bitbucket_client.check_pipeline_status(
            repo_slug=self._repo_slug, execution_uuid=execution_uuid
        )

        status = execution_data["state"]["name"]
        logger.info(
            f"Pipeline execution {execution_uuid} for {self._repo_slug} status: {status}"
        )
        return BitbucketPipelineStatus[status].value

    async def check_if_finished(self, execution_uuid: str) -> bool:
        status = await self._check_status(execution_uuid)

        if status == BitbucketPipelineStatus.COMPLETED.value:
            return True
        if status == BitbucketPipelineStatus.FAILED.value:
            raise PipelineHasFailed(f"Pipeline {execution_uuid} has failed")
        return False
