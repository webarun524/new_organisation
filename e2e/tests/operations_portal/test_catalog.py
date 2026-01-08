import pytest
from playwright.sync_api import Page, expect

from e2e.tests.logger import get_logger
from e2e.tests.operations_portal.labels import CATALOG_LABELS
from e2e.tests.operations_portal.models import OpTestConfig

logger = get_logger(__name__)


@pytest.mark.operations_portal
def test_express_product_catalog(op_page_auth: Page, op_env_config: OpTestConfig):
    if op_env_config.enterprise_active:
        logger.info("Skipping express - test_express_product_catalog")
        return

    logger.info("Starting catalog express product catalog test")

    page = op_page_auth
    page.goto("/catalog")

    multitenant_offering = page.get_by_text(CATALOG_LABELS["express_multitenant"])
    saas_offering = page.get_by_text(CATALOG_LABELS["express_saas"])
    paas_offering = page.get_by_text(CATALOG_LABELS["express_paas"])

    expect(multitenant_offering).to_be_visible()
    expect(saas_offering).to_be_visible()
    expect(paas_offering).to_be_visible()

    logger.info("Finished catalog express product catalog test")


@pytest.mark.operations_portal
def test_enterprise_product_catalog(op_page_auth: Page, op_env_config: OpTestConfig):
    if not (op_env_config.enterprise_active):
        logger.info("Skipping enterprise - test_enterprise_product_catalog")
        return

    logger.info("Starting catalog enterprise product catalog test")

    page = op_page_auth
    page.goto("/catalog")

    enterprise_element = page.get_by_text(CATALOG_LABELS["enterprise"])
    expect(enterprise_element).to_be_visible()

    container = page.get_by_test_id("navigation-container")
    subscribe_button = container.get_by_role(
        "button", name=CATALOG_LABELS["subscribe_button"]
    )
    expect(subscribe_button).to_be_visible()

    logger.info("Finished catalog enterprise product catalog test")
