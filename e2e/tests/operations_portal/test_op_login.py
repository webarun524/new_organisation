import pytest
from playwright.sync_api import Page, expect

from e2e.tests.logger import get_logger
from e2e.tests.operations_portal.labels import (
    ALERT_USER_NOT_EXIST_TEXT,
    CATALOG_LABEL,
    ENTER_EMAIL_PLACEHOLDER,
    ENTER_PASSWORD_PLACEHOLDER,
    LOGIN_VERIFICATION_LABEL,
    MANAGE_USERS_LABEL,
    SIGN_IN_BUTTON_NAME,
)
from e2e.tests.operations_portal.models import OpTestConfig

logger = get_logger(__name__)


@pytest.mark.operations_portal
@pytest.mark.data_portal_teardown
def test_sign_in_success(op_page_unauth: Page, op_env_config: OpTestConfig):
    page = op_page_unauth
    page.goto("/login")

    logger.info(
        f"Starting sign-in success test for user: {op_env_config.user}, url: {op_env_config.url}"
    )

    user = op_env_config.user
    password = op_env_config.password
    assert user, "user env var missing"
    assert password, "password env var missing"

    expect(page.get_by_placeholder(ENTER_EMAIL_PLACEHOLDER)).to_be_visible()
    expect(page.get_by_placeholder(ENTER_PASSWORD_PLACEHOLDER)).to_be_visible()
    page.get_by_placeholder(ENTER_EMAIL_PLACEHOLDER).fill(user)
    expect(page.get_by_placeholder(ENTER_EMAIL_PLACEHOLDER)).to_have_value(user)
    page.get_by_placeholder(ENTER_PASSWORD_PLACEHOLDER).fill(password)
    expect(page.get_by_placeholder(ENTER_PASSWORD_PLACEHOLDER)).to_have_value(password)

    page.get_by_role("button", name=SIGN_IN_BUTTON_NAME).click()
    page.wait_for_url("**/home", timeout=30000)

    expect(page.get_by_role("alert")).not_to_be_visible()
    expect(page.get_by_test_id("subscription-portal-link")).to_contain_text(
        LOGIN_VERIFICATION_LABEL
    )
    expect(
        page.locator('[data-testid="sidebar-link-text"]', has_text=MANAGE_USERS_LABEL)
    ).to_be_visible()
    expect(
        page.locator('[data-testid="sidebar-link-text"]', has_text=CATALOG_LABEL)
    ).to_be_visible()

    logger.info("Finished sign-in success test")


@pytest.mark.operations_portal
@pytest.mark.data_portal_teardown
def test_sign_in_failure_invalid_user(op_page_unauth: Page):
    page = op_page_unauth
    page.goto("/login")

    logger.info("Starting sign-in failure test with invalid credentials")

    invalid_user = "invalid_user@example.com"
    invalid_password = "invalid_password"
    expect(page.get_by_placeholder(ENTER_EMAIL_PLACEHOLDER)).to_be_visible()
    expect(page.get_by_placeholder(ENTER_PASSWORD_PLACEHOLDER)).to_be_visible()
    page.get_by_placeholder(ENTER_EMAIL_PLACEHOLDER).fill(invalid_user)
    expect(page.get_by_placeholder(ENTER_EMAIL_PLACEHOLDER)).to_have_value(invalid_user)
    page.get_by_placeholder(ENTER_PASSWORD_PLACEHOLDER).fill(invalid_password)
    expect(page.get_by_placeholder(ENTER_PASSWORD_PLACEHOLDER)).to_have_value(
        invalid_password
    )

    page.get_by_role("button", name=SIGN_IN_BUTTON_NAME).click()
    expect(page.get_by_role("alert")).to_contain_text(ALERT_USER_NOT_EXIST_TEXT)

    logger.info("Finished sign-in failure test with invalid credentials")


@pytest.mark.operations_portal
@pytest.mark.data_portal_teardown
def test_auth_page_initialization_fixture(op_page_auth: Page):
    logger.info("Starting test_auth_page_initialization_fixture")

    page = op_page_auth
    page.goto("/home")
    expect(page.get_by_test_id("subscription-portal-link")).to_be_visible()

    logger.info("Finished test_auth_page_initialization_fixture")
