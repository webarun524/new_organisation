import pytest
from playwright.sync_api import Page

from e2e.tests.logger import get_logger

logger = get_logger(__name__)


@pytest.mark.data_portal_verification
def test_map_viewer(dp_page_auth: Page):
    """Test that map viewer marker navigation works correctly."""
    page = dp_page_auth

    logger.info("Starting test: map viewer navigation")

    page.goto("/map-viewer")

    # Click first map marker
    map_marker = page.get_by_role("button", name="11").first
    map_marker.focus()
    map_marker.click()

    # Click first map marker
    map_marker = page.get_by_role("button", name="Marker").first
    map_marker.focus()
    map_marker.click()

    logger.info("Clicked map marker")

    # Click "Show in Data Portal" link
    well_link = page.get_by_role("link", name="Show in Data Portal")
    well_link.focus()

    # Wait for search API response
    with page.expect_response(lambda r: "/api/search/v2/query" in r.url.lower()):
        well_link.click()

    logger.info("Clicked 'Show in Data Portal' link")

    # Verify exactly 1 row is displayed
    row_headers = page.get_by_role("rowheader").all()
    assert len(row_headers) == 1, f"Expected 1 row header, got {len(row_headers)}"

    logger.info("Map viewer navigation successfully filtered to 1 result")
