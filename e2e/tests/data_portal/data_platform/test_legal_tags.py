from uuid import uuid4

import pytest
from playwright.sync_api import Page, expect

from e2e.tests.logger import get_logger

logger = get_logger(__name__)


@pytest.mark.data_portal_verification
def test_get_legal_tags(dp_page_auth: Page):
    """Test that legal tags page displays multiple tags."""
    page = dp_page_auth

    logger.info("Starting test: get legal tags")

    page.goto("data-portal/legal-tags-manager")

    page.get_by_role("link", name="Data Portal", exact=True).click()
    page.get_by_role("link", name="Legal Tags", exact=True).click()

    expect(page.get_by_role("article").first).to_be_visible(timeout=30000)

    articles = page.get_by_role("article").all()
    assert len(articles) >= 1, f"Expected more than 1 article, got {len(articles)}"

    logger.info(f"Legal tags page successfully displays {len(articles)} tags")


@pytest.mark.data_portal_verification
def test_update_legal_tag(dp_page_auth: Page):
    """Test updating a legal tag description."""
    page = dp_page_auth

    logger.info("Starting test: update legal tag")

    random_id = str(uuid4())

    page.goto("/data-portal/legal-tags-manager")

    # Edit first legal tag
    with page.expect_response("**/api/legal/v1/legaltags:properties"):
        page.get_by_role("article").first.get_by_role("button", name="Edit").click()

    logger.info(f"Updating legal tag description to: {random_id}")

    # Update description
    page.get_by_label("Description").fill(random_id)
    with page.expect_response("**/api/legal/v1/legaltags"):
        page.get_by_role("button", name="Apply").click()

    # Verify updated description is visible
    expect(page.get_by_role("article").first).to_contain_text(random_id)

    logger.info("Legal tag description successfully updated")


@pytest.mark.data_portal_verification
def test_create_legal_tag(dp_page_auth: Page):
    """Test creating a new legal tag."""
    page = dp_page_auth

    logger.info("Starting test: create legal tag")

    random_id = str(uuid4())

    logger.info(f"Creating legal tag with name: {random_id}")

    page.goto("/data-portal/legal-tags-manager")

    page.get_by_role("button", name="Create legal tag").click()

    # Fill basic information
    page.get_by_label("Name").fill(random_id)
    page.get_by_label("Originator").fill("some-originator")

    # --- set expiration date to next year ---
    page.get_by_role("spinbutton", name="Year").click()
    page.get_by_role("spinbutton", name="Year").press("ArrowUp")

    page.get_by_label("Contract ID").fill("someid")
    page.get_by_label("Description").fill("some decription")

    # Select Personal data types - first dropdown
    page.locator("span", has_text="Personal data types").get_by_role(
        "combobox"
    ).first.click()
    page.get_by_role("option", name="No Personal Data").click()

    # Select Personal data types - second dropdown
    page.locator("span").filter(has_text="Personal data typesNo").get_by_role(
        "combobox"
    ).nth(1).click()
    page.get_by_role("option", name="Public Domain Data").click()

    # Select Security classification - first dropdown
    page.locator("span", has_text="Security classification").get_by_role(
        "combobox"
    ).first.click()
    page.get_by_role("option", name="Public").click()

    # Select other relevant data countries
    page.get_by_placeholder("Other relevant data countries").click()
    page.get_by_role("option", name="United States", exact=True).click()

    # Select country of origin
    page.get_by_placeholder("Country of origin").click()
    page.get_by_role("option", name="United States", exact=True).click()

    # Select Security classification - second dropdown
    page.locator("span").filter(has_text="Security classification").get_by_role(
        "combobox"
    ).nth(1).click()
    page.get_by_role("option", name="No License Required").click()

    # Submit form
    page.get_by_role("button", name="Apply").click()

    # Verify created legal tag
    new_tag = page.locator("article", has_text=random_id)
    expect(new_tag).to_contain_text(f"osdu-{random_id}")
    expect(new_tag).to_contain_text("some decription")

    logger.info(f"Legal tag successfully created: osdu-{random_id}")
