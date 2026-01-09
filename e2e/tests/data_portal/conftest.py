import os
from typing import Iterator

import pytest
from playwright.sync_api import Browser, BrowserContext, Page, StorageState, expect

from e2e.tests.data_portal.labels import LOGIN_LABELS
from e2e.tests.data_portal.models import DpTestConfig
from e2e.tests.data_portal.utils.test_data_generator import DataGenerator
from e2e.tests.logger import get_logger

logger = get_logger(__name__)


# --- Config Fixture ---
@pytest.fixture(scope="session")
def dp_env_config() -> DpTestConfig:
    url = (
        os.getenv("DP_DOMAIN")
        if os.getenv("DP_DOMAIN", "").startswith("https://")
        else f"https://{os.getenv('DP_DOMAIN')}"
    )
    user = os.getenv("E2E_USER")
    password = os.getenv("DP_PASSWORD")

    missing = [
        name
        for name, value in [
            ("DP_DOMAIN", url),
            ("E2E_USER", user),
            ("DP_PASSWORD", password),
        ]
        if not value
    ]

    if missing:
        raise RuntimeError(f"Missing required environment variables: {missing}")

    return DpTestConfig(url=str(url), user=str(user), password=str(password))


# Unauthorized page
@pytest.fixture
def dp_page_unauth(browser: Browser, dp_env_config: DpTestConfig) -> Iterator[Page]:
    logger.info("Creating unauthenticated browser context for data portal")
    context: BrowserContext = browser.new_context(base_url=dp_env_config.url)
    page: Page = context.new_page()
    yield page
    logger.info("Closing unauthenticated browser context for operations portal")
    context.close()


# Authorized page
@pytest.fixture(scope="session")
def dp_auth_storage_state(
    browser: Browser, dp_env_config: DpTestConfig
) -> StorageState:
    context: BrowserContext = browser.new_context()
    page: Page = context.new_page()
    logger.info(f"Authenticating data portal user: {dp_env_config.user}")
    page.goto(dp_env_config.url)

    page.wait_for_url("**/login*")

    expect(page.get_by_role("textbox", name=LOGIN_LABELS["username"])).to_be_visible()
    expect(page.get_by_role("textbox", name=LOGIN_LABELS["password"])).to_be_visible()
    expect(page.get_by_role("button")).to_be_visible()
    page.get_by_role("textbox", name=LOGIN_LABELS["username"]).fill(dp_env_config.user)
    page.get_by_role("textbox", name=LOGIN_LABELS["password"]).fill(
        dp_env_config.password
    )
    page.get_by_role("button", name=LOGIN_LABELS["submit"]).click()

    page.wait_for_url(dp_env_config.url, timeout=15000)

    logger.info("Authentication successful — saving storage state")

    state = context.storage_state()
    context.close()
    logger.info("Saved storage state for operations portal")
    return state


@pytest.fixture
def dp_page_auth(
    browser: Browser, dp_auth_storage_state: StorageState, dp_env_config: DpTestConfig
) -> Iterator[Page]:
    logger.info("Creating authenticated browser context for data portal")
    context: BrowserContext = browser.new_context(
        base_url=dp_env_config.url, storage_state=dp_auth_storage_state
    )
    context.set_default_timeout(15000)
    context.set_default_navigation_timeout(15000)
    page: Page = context.new_page()
    try:
        yield page
    finally:
        logger.info("Closing authenticated browser context for data portal")
        context.close()


@pytest.fixture
def dp_test_data_generator(dp_env_config: DpTestConfig) -> DataGenerator:
    logger.info("Creating test data generator")
    return DataGenerator(base_api_url=dp_env_config.url)
