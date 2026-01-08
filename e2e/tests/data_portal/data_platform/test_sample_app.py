import pytest
from playwright.sync_api import Page, expect

from e2e.tests.logger import get_logger

logger = get_logger(__name__)


@pytest.mark.data_portal_verification
def test_finds_wells_and_creates_visualization(dp_page_auth: Page):
    """Test that OSDU visualization app can find wells and create visualization."""
    page = dp_page_auth

    logger.info("Starting test: OSDU visualization app")

    page.goto("/visualization-app")

    # Verify initial empty state
    expect(page.get_by_text("No Trajectory to display")).to_be_visible(timeout=30000)
    expect(page.get_by_text("Find well and click visualize")).to_be_visible()

    logger.info("Selecting well BIR-01 and creating visualization")

    # Select well and visualize
    page.get_by_text("BIR-01").click()
    page.get_by_role("button", name="Visualize").click()

    # Verify visualization is displayed
    expect(page.locator("canvas")).to_be_visible()
    expect(page.get_by_text("No Trajectory to display")).not_to_be_visible()
    expect(page.get_by_text("Find well and click visualize")).not_to_be_visible()

    logger.info("Visualization successfully created for well BIR-01")
