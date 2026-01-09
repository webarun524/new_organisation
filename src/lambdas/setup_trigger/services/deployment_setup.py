import logging
from typing import Any

from shared.bitbucket.bitbucket_client import BitbucketClient
from shared.bitbucket.type import BitbucketPipelineStatus

logger = logging.getLogger(__name__)


class DeploymentSetup:
    """Handles dataops_deployments manual_deployment_from_branch pipeline"""

    def __init__(
        self,
        bitbucket_client: BitbucketClient,
        repo_slug: str = "dataops-deployment",
    ) -> None:
        self._bitbucket_client = bitbucket_client
        self._repo_slug = repo_slug

    async def trigger_deployment_from_branch(
        self, bb_env_code: str, target_branch_name: str
    ) -> dict[str, Any]:
        """
        Triggers Bitbucket pipeline for deployment from branch.
        """
        body = self._bitbucket_client.prepare_pipeline_trigger_body(
            pipeline_name="manual-deployment-from-branch",
            branch_name="main",
            variables=[
                {"key": "ENV", "value": bb_env_code},
                {"key": "BRANCH_NAME", "value": target_branch_name},
                {"key": "SYNCHRONIZE_CODEBASE", "value": "False"},
            ],
        )
        return await self._bitbucket_client.trigger_pipeline(
            repo_slug=self._repo_slug,
            request_body=body,
        )

    async def check_status(self, pipeline_uuid: str) -> BitbucketPipelineStatus:
        """
        Check status
        """
        response = await self._bitbucket_client.check_pipeline_status(
            repo_slug=self._repo_slug, execution_uuid=pipeline_uuid
        )
        logger.debug(f"Pipeline status response: {response}", response)
        status = response["state"]["name"]
        return BitbucketPipelineStatus[status]
