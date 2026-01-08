import os
from typing import Iterator

import pytest
from playwright.sync_api import Browser, BrowserContext, Page, StorageState, expect

from e2e.models.enums import TestMarker
from e2e.tests.logger import get_logger
from e2e.tests.operations_portal.labels import (
    ENTER_EMAIL_PLACEHOLDER,
    ENTER_PASSWORD_PLACEHOLDER,
    SIGN_IN_BUTTON_NAME,
)
from e2e.tests.operations_portal.models import OpTestConfig

logger = get_logger(__name__)


# config
@pytest.fixture(scope="session")
def op_env_config(tests_variants: list[TestMarker]) -> OpTestConfig:
    # common env vars
    url = os.getenv("OP_URL")
    user = os.getenv("E2E_USER")
    password = os.getenv("OP_PASSWORD")
    # OP subscription vars
    dp_deployment_role_name = os.getenv("DP_DEPLOYMENT_ROLE_NAME")
    dp_account_id = os.getenv("DP_ACCOUNT_ID")
    dp_domain = os.getenv("DP_DOMAIN")
    dp_hosted_zone_id = os.getenv("DP_HOSTED_ZONE_ID")
    osdu_version = os.getenv("OSDU_VERSION")
    enterprise_active = os.getenv("ENTERPRISE_ACTIVE")
    dry_run_active = os.getenv("DRY_RUN_ACTIVE")
    region = os.getenv("REGION")
    # DP teardown vars
    deployment_id = os.getenv("DEPLOYMENT_ID")
    teardown_trigger_active = os.getenv("TEARDOWN_TRIGGER_ACTIVE")

    # check if at least one variant from TestMarker.operations_portal or TestMarker.data_portal_teardown is present
    if not any(
        variant in tests_variants
        for variant in [TestMarker.operations_portal, TestMarker.data_portal_teardown]
    ):
        raise RuntimeError(
            "No valid test variant found. Ensure that tests are marked with either "
            f"'@pytest.mark.{TestMarker.operations_portal.value}' or '@pytest.mark.{TestMarker.data_portal_teardown.value}'."
        )

    # missing check
    missing = []
    if TestMarker.operations_portal in tests_variants:
        missing += [
            name
            for name, value in [
                ("OP_URL", url),
                ("E2E_USER", user),
                ("OP_PASSWORD", password),
                ("DP_DEPLOYMENT_ROLE_NAME", dp_deployment_role_name),
                ("DP_ACCOUNT_ID", dp_account_id),
                ("DP_DOMAIN", dp_domain),
                ("DP_HOSTED_ZONE_ID", dp_hosted_zone_id),
                ("OSDU_VERSION", osdu_version),
                ("ENTERPRISE_ACTIVE", enterprise_active),
                ("DRY_RUN_ACTIVE", dry_run_active),
                ("REGION", region),
            ]
            if not value
        ]
    if TestMarker.data_portal_teardown in tests_variants:
        missing += [
            name
            for name, value in [
                ("OP_URL", url),
                ("E2E_USER", user),
                ("OP_PASSWORD", password),
                ("DEPLOYMENT_ID", deployment_id),
                ("TEARDOWN_TRIGGER_ACTIVE", teardown_trigger_active),
            ]
            if not value
        ]
    if missing:
        raise RuntimeError(f"Missing required environment variables: {missing}")

    return OpTestConfig(
        # common env vars
        url=str(url),
        user=str(user),
        password=str(password),
        # OP subscription vars
        dp_deployment_role_name=str(dp_deployment_role_name)
        if TestMarker.operations_portal in tests_variants
        else None,
        dp_account_id=str(dp_account_id)
        if TestMarker.operations_portal in tests_variants
        else None,
        dp_domain=str(dp_domain)
        if TestMarker.operations_portal in tests_variants
        else None,
        dp_hosted_zone_id=str(dp_hosted_zone_id)
        if TestMarker.operations_portal in tests_variants
        else None,
        osdu_version=str(osdu_version)
        if TestMarker.operations_portal in tests_variants
        else None,
        enterprise_active=bool(
            enterprise_active and enterprise_active.lower() == "true"
        )
        if TestMarker.operations_portal in tests_variants
        else None,
        dry_run_active=bool(dry_run_active and dry_run_active.lower() == "true")
        if TestMarker.operations_portal in tests_variants
        else None,
        region=str(region) if TestMarker.operations_portal in tests_variants else None,
        # DP teardown vars
        deployment_id=str(deployment_id)
        if TestMarker.data_portal_teardown in tests_variants
        else None,
        teardown_trigger_active=bool(
            teardown_trigger_active and teardown_trigger_active.lower() == "true"
        )
        if TestMarker.data_portal_teardown in tests_variants
        else None,
    )


# Unauthorized page
@pytest.fixture
def op_page_unauth(browser: Browser, op_env_config: OpTestConfig) -> Iterator[Page]:
    logger.info("Creating unauthenticated browser context for operations portal")
    context: BrowserContext = browser.new_context(base_url=op_env_config.url)
    page: Page = context.new_page()
    yield page
    logger.info("Closing unauthenticated browser context for operations portal")
    context.close()


# Authorized page
@pytest.fixture(scope="session")
def op_auth_storage_state(
    browser: Browser, op_env_config: OpTestConfig
) -> StorageState:
    context: BrowserContext = browser.new_context()
    page: Page = context.new_page()
    logger.info(f"Authenticating operations portal user: {op_env_config.user}")
    page.goto(op_env_config.url + "/login")
    expect(page.get_by_placeholder(ENTER_EMAIL_PLACEHOLDER)).to_be_visible()
    expect(page.get_by_placeholder(ENTER_PASSWORD_PLACEHOLDER)).to_be_visible()
    page.get_by_placeholder(ENTER_EMAIL_PLACEHOLDER).fill(op_env_config.user)
    page.get_by_placeholder(ENTER_PASSWORD_PLACEHOLDER).fill(op_env_config.password)
    page.get_by_role("button", name=SIGN_IN_BUTTON_NAME).click()

    expect(page.get_by_role("alert")).not_to_be_visible()
    page.wait_for_url("**/home", timeout=30000)
    logger.info("Authentication successful — saving storage state")

    state = context.storage_state()
    context.close()
    logger.info("Saved storage state for operations portal")
    return state


@pytest.fixture
def op_page_auth(
    browser: Browser, op_auth_storage_state: StorageState, op_env_config: OpTestConfig
) -> Iterator[Page]:
    logger.info("Creating authenticated browser context for operations portal")
    context: BrowserContext = browser.new_context(
        base_url=op_env_config.url, storage_state=op_auth_storage_state
    )
    context.set_default_timeout(15000)
    context.set_default_navigation_timeout(15000)
    page: Page = context.new_page()
    try:
        yield page
    finally:
        logger.info("Closing authenticated browser context for operations portal")
        context.close()
