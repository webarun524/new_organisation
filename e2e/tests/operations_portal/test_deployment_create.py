import re
from datetime import datetime

import pytest
from playwright.sync_api import Page, Response, expect

from e2e.services.outputs_handler import OutputsHandler
from e2e.tests.global_commons import select_mui_option
from e2e.tests.logger import get_logger
from e2e.tests.operations_portal.commons import navigate_from_catalog_to_deployment_form
from e2e.tests.operations_portal.labels import COMMON_LABELS, FORM_LABELS
from e2e.tests.operations_portal.models import OpTestConfig
from e2e.tests.operations_portal.variables import (
    CONFIRM_PRODUCT_DEPLOYMENT_REQ_KEY,
    LIFECYCLE_RELEASED_VALUE,
    LIFECYCLE_STATE_KEY,
    OUTPUT_DEPLOYMENT_ID_KEY,
    OUTPUT_WORKLOAD_VERSION_KEY,
    PRODUCT_DEPLOYMENT_ID_KEY,
    RELEASE_DATE_KEY,
    SAVE_PRODUCT_DEPLOYMENT_REQ_KEY,
    WORKLOAD_SPECS_REQ_NAME,
    WORKLOAD_VERSION_KEY,
)

logger = get_logger(__name__)


@pytest.mark.operations_portal
def test_capture_latest_workload_version(
    op_page_auth: Page, op_env_config: OpTestConfig
):
    logger.info("Starting test_capture_latest_workload_version")
    if not (op_env_config.enterprise_active):
        logger.info("Skipping enterprise - test_capture_latest_workload_version")
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

        released_items = [
            item
            for item in new_data["Results"]
            if item[LIFECYCLE_STATE_KEY] == LIFECYCLE_RELEASED_VALUE
        ]
        latest_item = max(
            released_items, key=lambda x: datetime.fromisoformat(x[RELEASE_DATE_KEY])
        )
        logger.info(f"Found Latest item {latest_item}")
        logger.info(
            f"Latest released workload specification: {latest_item[WORKLOAD_VERSION_KEY]} released on {latest_item[RELEASE_DATE_KEY]}"
        )
        OutputsHandler.save_outputs(
            OUTPUT_WORKLOAD_VERSION_KEY, latest_item[WORKLOAD_VERSION_KEY]
        )

    logger.info("Finished test_capture_latest_workload_version")


@pytest.mark.operations_portal
def test_validate_form(op_page_auth: Page, op_env_config: OpTestConfig):
    if not (op_env_config.enterprise_active):
        logger.info("Skipping enterprise - test_validate_form")
        return

    page = op_page_auth
    navigate_from_catalog_to_deployment_form(page)

    logger.info("Validating deployment form fields")

    page.get_by_label(re.compile(FORM_LABELS["email"])).is_visible()
    assert (
        page.get_by_label(re.compile(FORM_LABELS["email"])).input_value()
        == op_env_config.user
    )
    page.get_by_label(re.compile(FORM_LABELS["job_title"])).is_visible()
    page.get_by_label(re.compile(FORM_LABELS["first_name"])).is_visible()
    page.get_by_label(re.compile(FORM_LABELS["last_name"])).is_visible()
    page.get_by_label(re.compile(FORM_LABELS["privacy_agreement_partial"])).is_visible()
    page.get_by_label(re.compile(FORM_LABELS["region"])).is_visible()
    page.get_by_label(re.compile(FORM_LABELS["role_name"])).is_visible()
    page.get_by_label(re.compile(FORM_LABELS["target_account_id"])).is_visible()
    page.get_by_label(re.compile(FORM_LABELS["product_version"])).is_visible()
    page.get_by_label(re.compile(FORM_LABELS["external_id"])).is_visible()
    page.get_by_label(re.compile(FORM_LABELS["external_id"])).is_disabled()
    assert (
        len(page.get_by_label(re.compile(FORM_LABELS["external_id"])).input_value()) > 0
    )
    page.get_by_label(re.compile(FORM_LABELS["custom_domain"])).is_visible()
    page.get_by_label(re.compile(FORM_LABELS["hosted_zone_id"])).is_visible()
    page.get_by_label(COMMON_LABELS["next"]).is_visible()

    logger.info("Finished test_validate_form")


@pytest.mark.operations_portal
def test_trigger_deployment(op_page_auth: Page, op_env_config: OpTestConfig):
    if not (op_env_config.enterprise_active):
        logger.info("Skipping enterprise - test_trigger_deployment")
        return

    logger.info("Starting test_trigger_deployment")
    page = op_page_auth
    navigate_from_catalog_to_deployment_form(page)

    with page.expect_response(
        lambda r: f"/{WORKLOAD_SPECS_REQ_NAME}" in r.url
    ) as workload_response_info:
        logger.info(
            f"Captured response: {workload_response_info.value.url} with status {workload_response_info.value.status}"
        )

        logger.info(f"Triggering deployment from deployment form: {op_env_config}")

        page.get_by_label(re.compile(FORM_LABELS["job_title"])).fill(
            COMMON_LABELS["test"]
        )
        page.get_by_label(re.compile(FORM_LABELS["first_name"])).fill(
            COMMON_LABELS["test"]
        )
        page.get_by_label(re.compile(FORM_LABELS["last_name"])).fill(
            COMMON_LABELS["test"]
        )
        page.get_by_label(re.compile(FORM_LABELS["privacy_agreement_partial"])).check()
        select_mui_option(page, re.compile(FORM_LABELS["region"]), op_env_config.region)
        page.get_by_label(re.compile(FORM_LABELS["role_name"])).fill(
            op_env_config.dp_deployment_role_name
        )
        page.get_by_label(re.compile(FORM_LABELS["target_account_id"])).fill(
            op_env_config.dp_account_id
        )
        select_mui_option(
            page,
            re.compile(FORM_LABELS["product_version"]),
            f"osdu-{op_env_config.osdu_version}",
        )
        page.get_by_label(FORM_LABELS["load_sample_data"]).uncheck()
        page.get_by_label(re.compile(FORM_LABELS["custom_domain"])).fill(
            op_env_config.dp_domain
        )
        page.get_by_label(re.compile(FORM_LABELS["hosted_zone_id"])).fill(
            op_env_config.dp_hosted_zone_id
        )

        latest_workflow_version: str = OutputsHandler.get_outputs(
            OUTPUT_WORKLOAD_VERSION_KEY
        )
        logger.info(f"Selecting latest workflow version: {latest_workflow_version}")
        select_mui_option(
            page, re.compile(FORM_LABELS["workload_version"]), latest_workflow_version
        )

        page.get_by_role("button", name=COMMON_LABELS["next"]).click()

        logger.info(f"Capturing /{SAVE_PRODUCT_DEPLOYMENT_REQ_KEY} response")
        with page.expect_response(
            lambda r: f"/{SAVE_PRODUCT_DEPLOYMENT_REQ_KEY}" in r.url
        ) as response_info:
            expect(page).to_have_url("/deployment/confirm", timeout=15000)

            response: Response = response_info.value
            logger.info(
                f"Captured response: {response.url} with status {response.status}"
            )

            try:
                new_data: dict = response.json()
            except Exception as e:
                logger.error(f"Failed to parse response as JSON: {e}")
                raise e

            logger.info(
                f"Logging {SAVE_PRODUCT_DEPLOYMENT_REQ_KEY} response: {new_data}"
            )
            deployment_id = new_data[PRODUCT_DEPLOYMENT_ID_KEY]
            assert deployment_id, "Deployment ID is missing in the response"
            logger.info(f"Captured Deployment ID: {deployment_id}")

            OutputsHandler.save_outputs(OUTPUT_DEPLOYMENT_ID_KEY, deployment_id)

            page.get_by_role("button", name=COMMON_LABELS["previous"]).is_visible()
            page.get_by_role("button", name=COMMON_LABELS["confirm"]).is_visible()

            if op_env_config.dry_run_active:
                logger.info(
                    f"Dry run is active - not confirming deployment. Deployment ID: {deployment_id}"
                )
                return

            page.get_by_role("button", name=COMMON_LABELS["confirm"]).click()

            logger.info(f"Capturing /{CONFIRM_PRODUCT_DEPLOYMENT_REQ_KEY} response")
            with page.expect_response(
                lambda r: f"/{CONFIRM_PRODUCT_DEPLOYMENT_REQ_KEY}" in r.url
            ) as confirm_response_info:
                logger_message = f"Captured response: {confirm_response_info.value.url} with status {confirm_response_info.value.status} and text {confirm_response_info.value.text()}"
                if confirm_response_info.value.status != 200:
                    logger.error(logger_message)
                else:
                    logger.info(logger_message)
                assert confirm_response_info.value.status == 200, (
                    f"Deployment confirmation failed - {confirm_response_info.value.text()}"
                )
                expect(page).to_have_url("/subscriptions", timeout=15000)

    logger.info("Finished test_trigger_deployment")
