import pytest
from playwright.sync_api import Page, Response

from e2e.services.outputs_handler import OutputsHandler
from e2e.tests.logger import get_logger
from e2e.tests.operations_portal.commons import navigate_from_catalog_to_deployment_form
from e2e.tests.operations_portal.models import OpTestConfig
from e2e.tests.operations_portal.variables import (
    OUTPUT_WORKLOAD_SPECIFICATIONS_KEY,
    OUTPUTS_FILE,
    WORKLOAD_SPECS_REQ_NAME,
)

logger = get_logger(__name__)


@pytest.mark.operations_portal
def test_capture_workload_specifications(
    op_page_auth: Page, op_env_config: OpTestConfig
):
    logger.info("Starting test_capture_workload_specifications")
    if not (op_env_config.enterprise_active):
        logger.info("Skipping enterprise - test_capture_workload_specifications")
        return

    page = op_page_auth
    navigate_from_catalog_to_deployment_form(page)

    logger.info(f"Capturing /{WORKLOAD_SPECS_REQ_NAME} response")

    with page.expect_response(
        lambda r: f"/{WORKLOAD_SPECS_REQ_NAME}" in r.url
    ) as response_info:
        response: Response = response_info.value
        logger.info(f"Captured response: {response.url} with status {response.status}")

        try:
            new_data: dict = response.json()
        except Exception as e:
            logger.error(f"Failed to parse response as JSON: {e}")
            raise e

        OutputsHandler.save_outputs(OUTPUT_WORKLOAD_SPECIFICATIONS_KEY, new_data)
        logger.info(
            f"Saved response under '{WORKLOAD_SPECS_REQ_NAME}' in {OUTPUTS_FILE}"
        )
    logger.info("Finished test_capture_workload_specifications")
