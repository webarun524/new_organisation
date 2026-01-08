import pytest
from playwright.sync_api import Page, expect

from e2e.tests.logger import get_logger

logger = get_logger(__name__)


@pytest.mark.data_portal_activation
def test_activate_platform(dp_page_auth: Page):
    """Test that users list displays user login."""
    page = dp_page_auth

    logger.info("Turn on platform")

    page.goto("/Settings")

    page.get_by_role("button", name="Platform Management Control").click()

    page.get_by_role("button", name="Turn on").click()
    page.get_by_role("button", name="Apply").click()
    expect(page.get_by_role("button", name="Turn on")).to_be_disabled(timeout=60000)

    logger.info("Platform turned on successfully")
