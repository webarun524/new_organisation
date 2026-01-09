import pytest
from playwright.sync_api import Page, expect

from e2e.tests.logger import get_logger

logger = get_logger(__name__)


@pytest.mark.data_portal_verification
def test_load_record(dp_page_auth: Page, dp_test_data_generator):
    """Test loading a record via JSON input."""
    page = dp_page_auth

    logger.info("Starting test: load record")

    new_record = dp_test_data_generator.get_record()

    logger.info(f"Loading record with ID: {new_record.get_id()}")

    page.goto("/data-portal/storage/load-record")

    # Verify Send button is disabled initially
    send_button = page.get_by_role("button", name="Send")
    expect(send_button).to_be_disabled(timeout=30000)

    # Fill JSON data
    page.get_by_placeholder("Pass or drop JSON file").fill(new_record.stringify())

    # Verify Send button is enabled after filling data
    expect(send_button).to_be_enabled()

    # Submit record
    send_button.click()

    # Verify success - "Modified data" heading appears
    expect(page.get_by_role("heading", name="Modified data")).to_be_visible()

    logger.info("Record successfully loaded")
