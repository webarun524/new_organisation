import pytest
from playwright.sync_api import Page, expect

from e2e.tests.logger import get_logger
from e2e.tests.operations_portal.labels import (
    ENTER_EMAIL_PLACEHOLDER,
    ENTER_PASSWORD_PLACEHOLDER,
    NAVBAR_LABELS,
)

logger = get_logger(__name__)


@pytest.mark.operations_portal
def test_logout(op_page_auth: Page):
    logger.info("Starting test_logout")
    op_page_auth.goto("/home")

    op_page_auth.get_by_test_id("user-menu").get_by_label(
        NAVBAR_LABELS["hamburger_menu"]
    ).click()
    sign_out_item = op_page_auth.get_by_role("menuitem", name=NAVBAR_LABELS["sign_out"])
    expect(sign_out_item).to_be_visible()
    sign_out_item.click()

    expect(op_page_auth.get_by_placeholder(ENTER_EMAIL_PLACEHOLDER)).to_be_visible()
    expect(op_page_auth.get_by_placeholder(ENTER_PASSWORD_PLACEHOLDER)).to_be_visible()
    logger.info("Finished test_logout")
