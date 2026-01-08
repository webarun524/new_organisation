import re

import pytest
from playwright.sync_api import Page

from e2e.tests.data_portal.models import DpTestConfig
from e2e.tests.logger import get_logger

logger = get_logger(__name__)


@pytest.mark.data_portal_verification
def test_copy_bearer_token_to_clipboard(
    dp_page_auth: Page, dp_env_config: DpTestConfig
):
    """Test that Bearer token can be copied to clipboard."""
    page = dp_page_auth
    context = page.context

    logger.info("Starting test: copy Bearer token to clipboard")

    context.grant_permissions(["clipboard-read", "clipboard-write"])
    page.goto("/")

    page.wait_for_selector(f"text='{dp_env_config.user}'", state="visible")

    page.get_by_role("button", name="handle-user-menu").click()
    page.get_by_role("menuitem", name="Copy Bearer Token").click()

    # Read clipboard content
    handle = page.evaluate_handle("() => navigator.clipboard.readText()")
    clipboard_content = handle.json_value()

    # Verify Bearer token format
    assert re.match(r"Bearer [\w\d.-]{900,1000}", clipboard_content), (
        f"Clipboard content does not match Bearer token pattern: {clipboard_content}"
    )

    logger.info("Bearer token successfully copied to clipboard")
def test_copy_bearer_token_to_clipboarda(
    dp_page_auth: Page, dp_env_config: DpTestConfig
):
    """Test that Bearer token can be copied to clipboard."""
    page = dp_page_auth
    context = page.context

    logger.info("Starting test: copy Bearer token to clipboard")

    context.grant_permissions(["clipboard-read", "clipboard-write"])
    page.goto("/")

    page.wait_for_selector(f"text='{dp_env_config.user}'", state="visible")

    page.get_by_role("button", name="handle-user-menu").click()
    page.get_by_role("menuitem", name="Copy Bearer Token").click()

    # Read clipboard content
    handle = page.evaluate_handle("() => navigator.clipboard.readText()")
    clipboard_content = handle.json_value()

    # Verify Bearer token format
    assert re.match(r"Bearer [\w\d.-]{900,1000}", clipboard_content), (
        f"Clipboard content does not match Bearer token pattern: {clipboard_content}"
    )

    logger.info("Bearer token successfully copied to clipboard")
