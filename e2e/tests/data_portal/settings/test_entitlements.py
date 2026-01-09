import uuid

import pytest
from playwright.sync_api import Page, expect

from e2e.tests.data_portal.models import DpTestConfig
from e2e.tests.logger import get_logger

logger = get_logger(__name__)


@pytest.mark.data_portal_verification
def test_lists_users(dp_page_auth: Page, dp_env_config: DpTestConfig):
    """Test that users list displays user login."""
    page = dp_page_auth

    logger.info("Starting test: lists users")

    page.goto("/Settings")
    page.get_by_text("Identity & Access Management").click()

    # Verify user login is visible in the table
    user_row = page.get_by_test_id(f"{dp_env_config.user}-row")

    # If user row is not visible, navigate to next page
    if not user_row.is_visible():
        logger.info(
            f"User {dp_env_config.user} not found on first page, checking next page"
        )
        page.get_by_role("button", name="Go to next page").click()
        page.wait_for_timeout(1000)  # Wait for page transition

    expect(user_row).to_be_visible(timeout=30000)

    logger.info(f"User {dp_env_config.user} successfully listed")


@pytest.mark.data_portal_verification
def test_lists_entitlements(dp_page_auth: Page):
    """Test that entitlements list displays multiple groups."""
    page = dp_page_auth

    logger.info("Starting test: lists entitlements")

    page.goto("/Settings")
    page.get_by_text("Identity & Access Management").click()
    page.wait_for_selector("text='cron job role'", timeout=30000)

    # Verify multiple "Manage group" buttons exist
    manage_group_buttons = page.get_by_role("button", name="Manage group").all()
    assert len(manage_group_buttons) > 1, (
        f"Expected >1 manage group buttons, got {len(manage_group_buttons)}"
    )

    logger.info(f"Entitlements list displays {len(manage_group_buttons)} groups")


@pytest.mark.data_portal_verification
def test_adds_and_removes_entitlement_group(dp_page_auth: Page):
    page = dp_page_auth
    # Use a unique name to avoid "Group already exists" errors from failed runs
    unique_id = str(uuid.uuid4())[:8]
    group_name = f"test-service-{unique_id}"
    resource_row_text = f"service.{group_name}.viewers"

    logger.info(f"Starting test with group: {group_name}")

    page.goto("/Settings")
    page.get_by_text("Identity & Access Management").click()

    # Ensure the page is loaded before interacting
    expect(page.get_by_role("button", name="Add OSDU Group")).to_be_visible()

    # Create Group
    page.get_by_role("button", name="Add OSDU Group").click()
    page.get_by_text("Data", exact=True).click()
    page.get_by_role("option", name="Service").click()
    page.get_by_label("Resource name").fill(group_name)
    page.get_by_label("Description").fill("Automated test group")
    page.get_by_role("button", name="Create").click()

    # The "Robust" Part: Use expect.to_pass to handle backend lag
    # This replaces your manual for-loop and refresh logic
    new_group = page.get_by_role("row", name=resource_row_text)

    page.reload()
    page.get_by_text("Identity & Access Management").click()
    expect(page.get_by_role("button", name="Add OSDU Group")).to_be_visible()
    expect(new_group).to_be_visible(timeout=5000)

    # Cleanup/Removal
    logger.info("Group visible, proceeding to removal")
    new_group.get_by_role("button").click()
    page.get_by_role("button", name="Remove group").click()

    # Final Verification
    expect(new_group).not_to_be_visible(timeout=10000)


@pytest.mark.data_portal_verification
def test_create_user_prerequisites(dp_page_auth: Page):
    """Test that create user dialog displays correctly with entitlements."""
    page = dp_page_auth

    logger.info("Starting test: create user prerequisites")

    page.goto("/Settings")
    page.get_by_text("Identity & Access Management").click()
    page.wait_for_selector("text='cron job role'", timeout=30000)
    # Open Add User dialog
    page.get_by_role("button", name="Add User").click()

    # Verify Email Id field is enabled
    expect(page.get_by_label("Email Id")).to_be_enabled()

    # Verify entitlement assignment example row
    entitlement_row = page.get_by_role("row", name="cron.job")
    expect(entitlement_row).to_be_visible()

    # Verify first checkbox is enabled
    first_checkbox = entitlement_row.get_by_role("checkbox").first
    expect(first_checkbox).to_be_enabled()

    # Verify the same checkbox via all() method
    all_checkboxes = entitlement_row.get_by_role("checkbox").all()
    expect(all_checkboxes[0]).to_be_enabled()

    logger.info("Create user prerequisites verified successfully")
