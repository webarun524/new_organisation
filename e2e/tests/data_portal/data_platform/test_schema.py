from datetime import datetime

import pytest
from playwright.sync_api import Page, expect

from e2e.tests.logger import get_logger

logger = get_logger(__name__)


@pytest.mark.data_portal_verification
def test_get_schemas(dp_page_auth: Page):
    """Test that schema page displays 10 schemas."""
    page = dp_page_auth

    logger.info("Starting test: get schemas")

    with page.expect_response(lambda r: "/api/schema-service/v1/schema" in r.url):
        page.goto("/Schema")

    articles = page.get_by_role("article").all()
    assert len(articles) == 10, f"Expected 10 articles, got {len(articles)}"

    logger.info("Schema page successfully displays 10 schemas")


@pytest.mark.data_portal_verification
def test_create_edit_schema(dp_page_auth: Page, dp_test_data_generator):
    """Test creating and editing a schema."""
    page = dp_page_auth

    logger.info("Starting test: create/edit schema")

    today = datetime.now().strftime("%m-%d-%Y")
    source = "test"
    entity_type = dp_test_data_generator.get_unique_name("TestEntity")

    logger.info(f"Creating schema with entity type: {entity_type}")

    page.goto("/Schema")
    page.get_by_role("button", name="Create schema").click()

    # Fill schema creation form
    page.get_by_label("Authority").fill("osdu")
    page.get_by_label("Source").fill(source)
    page.get_by_label("Entity type").fill(entity_type)
    page.get_by_placeholder("Pass or drop JSON file").fill(
        '{"data": {}, "x-osdu-virtual-properties":{}}'
    )

    # Create schema
    with page.expect_response(lambda r: "/api/schema-service/v1/schema" in r.url):
        page.get_by_role("button", name="Create", exact=True).click()

    # Filter to find created schema
    page.get_by_label("Source").fill(source)
    with page.expect_response(lambda r: "/api/schema-service/v1/schema" in r.url):
        page.get_by_label("Entity type").fill(entity_type)

    # Verify schema is visible with today's date and Development status
    expect(page.locator("article", has_text=today).first).to_be_visible()
    expect(page.locator("article", has_text="Development").first).to_be_visible()

    logger.info("Schema created successfully, editing status to Published")

    # Click edit button (3rd button in first article)
    page.locator("article").first.get_by_role("button").nth(2).click()

    # Change status from Development to Published
    page.get_by_text("Development").first.click()
    page.get_by_role("option", name="Published").click()

    page.get_by_role("button", name="Edit", exact=True).first.click()

    # Change status in the schema details
    comboboxes = page.get_by_label("The schema status").get_by_role("combobox").all()
    comboboxes[0].click()
    # comboboxes.click()
    page.get_by_role("option", name="Published").click()

    # Verify Published status is visible
    expect(page.locator("article", has_text="Published").first).to_be_visible()

    logger.info("Schema status successfully updated to Published")


@pytest.mark.data_portal_verification
def test_filter_schemas(dp_page_auth: Page):
    """Test filtering schemas by source and entity type."""
    page = dp_page_auth

    logger.info("Starting test: filter schemas")

    source = "wks"
    entity_type = "AbstractAccessControlList"

    page.goto("/Schema")

    # Filter by source and entity type
    page.get_by_label("Source").fill(source)
    page.get_by_label("Entity type").fill(entity_type)

    # Click first button in first article
    page.locator("article").first.get_by_role("button").first.click()

    # Verify filtered results
    expect(page.locator("article", has_text=source).first).to_be_visible()
    expect(page.locator("article", has_text=entity_type).first).to_be_visible()

    logger.info(
        f"Successfully filtered schemas by source '{source}' and entity type '{entity_type}'"
    )
