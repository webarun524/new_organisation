import pytest
from playwright.sync_api import Page, expect

from e2e.tests.logger import get_logger
from e2e.tests.operations_portal.labels import SIDEBAR_LABELS

logger = get_logger(__name__)


@pytest.mark.operations_portal
def test_all_menu_categories_visible(op_page_auth: Page):
    logger.info("Starting test_all_menu_categories_visible")

    page = op_page_auth
    page.goto("/home")

    expected_labels = [
        SIDEBAR_LABELS["home"],
        SIDEBAR_LABELS["subscriptions"],
        SIDEBAR_LABELS["catalog"],
        SIDEBAR_LABELS["manage_users"],
    ]

    sidebar_items = page.locator('span[data-testid="sidebar-link-text"]')

    for label in expected_labels:
        matching = sidebar_items.filter(has_text=label)
        expect(matching).to_be_visible()

    logger.info("Finished test_all_menu_categories_visible")
