import os

import pytest
from playwright.sync_api import Page, expect

from e2e.tests.logger import get_logger

logger = get_logger(__name__)


def delete_policy_by_id(page: Page, policy_id: str) -> None:
    """Delete a policy via API for cleanup."""
    base_api_url = os.getenv("REACT_APP_BASE_API_URL")
    if not base_api_url:
        raise RuntimeError("REACT_APP_BASE_API_URL is not set")

    api_context = page.context.browser.new_context()
    api_page = api_context.new_page()
    try:
        api_page.request.delete(f"{base_api_url}/api/policies/{policy_id}")
    finally:
        api_context.close()


# PolicyContainer tests


@pytest.mark.data_portal_verification
def test_display_policy_list_and_filter(dp_page_auth: Page):
    """Test that policy list displays with correct columns and data."""
    page = dp_page_auth

    logger.info("Starting test: display policy list")
    page.goto("/data-portal/policies-manager")

    # Verify column headers
    expect(page.get_by_role("columnheader", name="name")).to_be_visible(timeout=30000)
    expect(page.get_by_role("columnheader", name="kind")).to_be_visible()

    # Verify specific row data
    row = page.locator("tr", has_text="osdu/instance/dataauthz.rego")
    expect(row.locator("td").nth(0)).to_have_text("osdu/instance/dataauthz.rego")
    expect(row.locator("td").nth(1)).to_have_text("instance")

    logger.info("Policy list displayed correctly")


# PolicyTranslator tests


@pytest.mark.data_portal_verification
def test_show_error_for_no_query_in_body(dp_page_auth: Page):
    """Test that policy translator shows error for invalid input."""
    page = dp_page_auth

    logger.info("Starting test: policy translator error handling")
    page.goto("/data-portal/policies-manager")

    expect(page.get_by_role("columnheader", name="name")).to_be_visible(timeout=30000)

    # Open translator
    open_translator_button = page.get_by_role("button", name="translate policy")
    expect(open_translator_button).to_be_visible()
    open_translator_button.click()
    expect(page.get_by_text("Policy translator")).to_be_visible()

    logger.info("Policy translator opened, testing invalid JSON")

    # Fill Monaco editor with invalid JSON (missing 'query' field)
    page.locator(".monaco-editor .inputarea").fill('{"foo":"bar"}')

    # Translate
    page.get_by_role("button", name="translate").click()

    # Verify error messages
    expect(
        page.get_by_text(
            "The following errors were encountered during the data translation process on the server"
        )
    ).to_be_visible()
    expect(page.get_by_text("At body.query: Field required")).to_be_visible()

    logger.info("Error correctly displayed for invalid input")
