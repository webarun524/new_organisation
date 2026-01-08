import pytest
from playwright.sync_api import Page, expect

from e2e.tests.logger import get_logger
from e2e.tests.operations_portal.labels import COMMON_LABELS, SUBSCRIPTIONS_LABELS
from e2e.tests.operations_portal.models import OpTestConfig

logger = get_logger(__name__)

ACTIVE_SUBSCRIPTION_STATUS = "Active"
UNSUBSCRIBE_CONFIRMATION_TEXT = "UNSUBSCRIBE"


@pytest.mark.data_portal_teardown
def test_trigger_data_portal_teardown(op_page_auth: Page, op_env_config: OpTestConfig):
    logger.info("Starting test_trigger_data_portal_teardown")

    assert op_env_config.deployment_id, "DEPLOYMENT_ID must be set for teardown test"

    page = op_page_auth
    page.goto("/subscriptions")

    logger.info(
        f"Finding active subscription for deployment ID: {op_env_config.deployment_id}"
    )
    row = (
        page.get_by_role("row")
        .filter(has_text=op_env_config.deployment_id)
        .filter(has_text=ACTIVE_SUBSCRIPTION_STATUS)
    )
    try:
        expect(row).to_have_count(1, timeout=30000)
    except TimeoutError:
        raise AssertionError(
            f"Expected exactly 1 row with deployment ID '{op_env_config.deployment_id}' "
            f"and status {ACTIVE_SUBSCRIPTION_STATUS}, but it was not found in subscriptions table."
        )
    row.first.click()

    unsubscribe_btn = page.get_by_role("button").filter(
        has_text=SUBSCRIPTIONS_LABELS["unsubscribe"]
    )
    expect(unsubscribe_btn).to_be_visible()
    expect(unsubscribe_btn).to_be_enabled()
    unsubscribe_btn.click()

    modal = page.get_by_role("dialog", name=SUBSCRIPTIONS_LABELS["confirm_unsubscribe"])
    expect(modal).to_be_visible()

    confirm_input = modal.locator("input#confirmInput")
    expect(confirm_input).to_be_visible()
    expect(confirm_input).to_be_enabled()
    confirm_input.fill(UNSUBSCRIBE_CONFIRMATION_TEXT)

    confirm_btn = modal.get_by_role("button", name=COMMON_LABELS["confirm"])
    cancel_btn = modal.get_by_role("button", name=COMMON_LABELS["cancel"])
    expect(confirm_btn).to_be_visible()
    expect(confirm_btn).to_be_enabled()
    expect(cancel_btn).to_be_visible()
    expect(cancel_btn).to_be_enabled()

    if not op_env_config.teardown_trigger_active:
        logger.info("Teardown trigger is active, proceeding to confirm teardown.")
        cancel_btn.click()
        expect(modal).not_to_be_visible()
        logger.info(
            "Finishing test_trigger_data_portal_teardown - teardown not triggered due to inactive flag"
        )

    else:
        confirm_btn.click()
        logger.info(
            "Finishing test_trigger_data_portal_teardown - teardown triggered successfully"
        )
        expect(modal).not_to_be_visible()
