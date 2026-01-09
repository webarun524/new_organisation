import pytest
from playwright.sync_api import Page, expect

from e2e.tests.data_portal.commons import check_dashboard_access
from e2e.tests.data_portal.labels import LOGIN_LABELS
from e2e.tests.data_portal.models import DpTestConfig
from e2e.tests.logger import get_logger

logger = get_logger(__name__)


@pytest.mark.data_portal_verification
@pytest.mark.data_portal_activation
def test_dp_sign_in_success(dp_page_unauth: Page, dp_env_config: DpTestConfig):
    logger.info(f"Starting data portal login test for user {dp_env_config.user}")

    page = dp_page_unauth
    page.goto("/")

    page.wait_for_url("**/login*")

    expect(page.get_by_role("textbox", name=LOGIN_LABELS["username"])).to_be_visible()
    expect(page.get_by_role("textbox", name=LOGIN_LABELS["password"])).to_be_visible()
    expect(page.get_by_role("button")).to_be_visible()
    page.get_by_role("textbox", name=LOGIN_LABELS["username"]).fill(dp_env_config.user)
    page.get_by_role("textbox", name=LOGIN_LABELS["password"]).fill(
        dp_env_config.password
    )
    page.get_by_role("button", name=LOGIN_LABELS["submit"]).click()

    check_dashboard_access(page)

    logger.info("Finished data portal login test")


@pytest.mark.data_portal_verification
@pytest.mark.data_portal_activation
def test_dp_sign_in_failure(dp_page_unauth: Page, dp_env_config: DpTestConfig):
    logger.info(
        f"Starting data portal login failure test for user {dp_env_config.user}"
    )

    page = dp_page_unauth
    page.goto("/")

    page.wait_for_url("**/login*")

    expect(page.get_by_role("textbox", name=LOGIN_LABELS["username"])).to_be_visible()
    expect(page.get_by_role("textbox", name=LOGIN_LABELS["password"])).to_be_visible()
    expect(page.get_by_role("button")).to_be_visible()
    page.get_by_role("textbox", name=LOGIN_LABELS["username"]).fill(dp_env_config.user)
    page.get_by_role("textbox", name=LOGIN_LABELS["password"]).fill(
        "Incorrect password"
    )
    page.get_by_role("button", name=LOGIN_LABELS["submit"]).click()

    visible_form = page.locator(
        'form[name="cognitoSignInForm"]:has(#signInFormUsername:visible)'
    ).first
    error_message = visible_form.locator("#loginErrorMessage")
    expect(error_message).to_be_visible(timeout=10000)

    logger.info("Finished data portal login failure test")


@pytest.mark.data_portal_verification
@pytest.mark.data_portal_activation
def test_dp_auth_page_initialization_fixture(dp_page_auth: Page):
    logger.info("Starting test_dp_auth_page_initialization_fixture")

    page = dp_page_auth
    page.goto("/")

    check_dashboard_access(page)

    logger.info("Finished test_dp_auth_page_initialization_fixture")
