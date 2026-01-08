import pytest
from playwright.sync_api import Page, expect

from e2e.tests.logger import get_logger

logger = get_logger(__name__)


@pytest.mark.data_portal_verification
def test_search_init_page_shows_results(dp_page_auth: Page):
    """Test that search initialization page displays results."""
    page = dp_page_auth

    logger.info("Starting test: search init page shows results")

    page.goto("/data-portal/search")

    expect(page.get_by_text("Rows per page")).to_be_visible(timeout=150000)

    # Verify 10 rows are displayed
    row_headers = page.get_by_role("rowheader")
    expect(row_headers.first).to_be_visible(timeout=150000)
    assert len(row_headers.all()) == 10, (
        f"Expected 10 row headers, got {len(row_headers.all())}"
    )

    logger.info("Search init page successfully displays 10 results")


@pytest.mark.data_portal_verification
def test_search_by_exact_id(dp_page_auth: Page):
    """Test that search by exact ID filters to single result."""
    page = dp_page_auth

    logger.info("Starting test: search by exact ID")

    page.goto("/data-portal/search")

    # Get first article ID
    first_article_id = page.get_by_role("rowheader").first
    expect(first_article_id).to_be_visible(timeout=30000)
    first_id = first_article_id.text_content()

    logger.info(f"Searching for exact ID: {first_id}")

    # Search by exact ID
    page.get_by_label("Query", exact=True).fill(f'"{first_id}"')
    page.get_by_role("button", name="Search").click()

    # Wait for progressbar to disappear
    page.get_by_role("progressbar").first.wait_for(state="detached", timeout=30000)

    # Verify only 1 row is displayed
    row_headers = page.get_by_role("rowheader").all()
    assert len(row_headers) == 1, f"Expected 1 row header, got {len(row_headers)}"

    logger.info("Search by exact ID successfully filtered to 1 result")
