import pytest
from playwright.sync_api import Page, expect

from e2e.tests.logger import get_logger

logger = get_logger(__name__)


@pytest.mark.data_portal_verification
def test_load_manifest(dp_page_auth: Page, dp_test_data_generator):
    """Test loading a manifest with workflow registration."""
    page = dp_page_auth

    logger.info("Starting test: load manifest")

    page.goto("/data-portal/workload/load-manifest")

    new_workflow = dp_test_data_generator.get_workflow()
    new_manifest = dp_test_data_generator.get_manifest()

    logger.info(f"Registering new workflow: {new_workflow.get_id()}")

    # Select workflow name combobox
    workflow_name_select = page.get_by_role("combobox")
    expect(workflow_name_select).to_be_visible(timeout=30000)

    # Fix for playwright scrolling issue
    workflow_name_select.focus()
    workflow_name_select.click()

    # Register new workflow
    page.get_by_role("option", name="Register new workflow").click()
    page.get_by_label("Workflow", exact=True).fill(new_workflow.stringify())
    page.get_by_role("button", name="Register").click()

    logger.info("Workflow registered, uploading manifest")

    # Upload manifest
    page.get_by_label("Manifest", exact=True).fill(new_manifest.stringify())
    page.get_by_role("button", name="Upload").click()

    # Verify success
    expect(page.get_by_text("Modified data")).to_be_visible()

    logger.info("Manifest successfully loaded")
