from pathlib import Path
from typing import Iterator

import pytest
from dotenv import load_dotenv
from playwright.sync_api import Browser, Playwright, sync_playwright

from e2e.models.enums import TestMarker
from e2e.services.outputs_handler import OutputsHandler
from e2e.tests.logger import get_logger 


# Dotenv loading
env_file = Path(__file__).resolve().parents[1] / ".env.test"
logger = get_logger(__name__)
if env_file.exists():
    load_dotenv(str(env_file))
    logger.info(f"Loaded environment file: {env_file}")
else:
    logger.warning(f"{env_file} not found — relying on system environment variables")


# Browser initialization
@pytest.fixture(scope="session")
def playwright_instance() -> Iterator[Playwright]:
    with sync_playwright() as p:
        yield p


# Additional pytest params
def pytest_addoption(parser):
    parser.addoption(
        "--slow_mo",
        action="store",
        default=None,
        help="Slow down Playwright actions (milliseconds)",
    )


@pytest.fixture(scope="session")
def browser(pytestconfig, playwright_instance: Playwright) -> Iterator[Browser]:
    # Allow headed runs if `--headed` param is passed to tests, default: True
    try:
        headless = not pytestconfig.getoption("headed")
    except ValueError:
        headless = True

    # Allow slowed runs if `--slow_mo` param is passed to tests, default: None
    try:
        raw_slow_mo_value = pytestconfig.getoption("slow_mo")
        slow_mo = float(raw_slow_mo_value) if raw_slow_mo_value is not None else None
    except ValueError:
        slow_mo = None

    browser = playwright_instance.chromium.launch(headless=headless, slow_mo=slow_mo)
    yield browser
    browser.close()


# require marks on tests
def pytest_collection_modifyitems(config, items):
    required_marks = {
        TestMarker.operations_portal.value,
        TestMarker.data_portal_verification.value,
        TestMarker.data_portal_teardown.value,
        TestMarker.data_portal_activation.value,
    }

    found_variants = set()

    for item in items:
        # Only enforce checks for tests under the e2e/ folder
        if "e2e/" not in str(item.fspath).replace("\\","/"):
            continue

        item_marks = {mark.name for mark in item.iter_markers()}
        matched = required_marks & item_marks

        # Enforce: every E2E test must have a variant marker
        if not matched:
            raise pytest.UsageError(
                f"E2E test '{item.nodeid}' is missing a required marker.\n"
                "Add one of:\n"
                + "\n".join(f"  @pytest.mark.{m}" for m in required_marks)
            )

        # Only collect variants from tests that will actually run (not deselected)
        # Check if the test will be deselected by checking for 'deselected' keyword
        if hasattr(item, "own_markers"):
            # Collect variant(s) used in this test run
            found_variants.update(matched)

    # After collection, filter to only include variants from selected items
    # Get the marker expression to determine which tests will actually run
    markexpr = config.getoption("-m", default="")

    if markexpr:
        # Re-scan items to find only matching variants
        selected_variants = set()
        for item in items:
            if "e2e/" not in str(item.fspath):
                continue

            # Check if item matches the marker expression
            item_marks = {mark.name for mark in item.iter_markers()}
            matched = required_marks & item_marks

            # Simple marker matching - check if any of the matched marks are in the expression
            for mark in matched:
                if mark in markexpr:
                    selected_variants.add(mark)

        found_variants = selected_variants

    if not found_variants:
        raise pytest.UsageError(
            "No E2E test variants detected. Ensure at least one E2E test is collected."
        )

    # Store resolved variant on session object
    config._test_variants = [TestMarker(variant) for variant in found_variants]


# require marks on run
def pytest_cmdline_main(config):
    markexpr = config.getoption("-m") or ""
    required = [
        TestMarker.data_portal_verification.value,
        TestMarker.data_portal_teardown.value,
        TestMarker.operations_portal.value,
        TestMarker.data_portal_activation.value,
    ]

    if not any(m in markexpr for m in required):
        raise pytest.UsageError(
            "You must run E2E tests with a mark: "
            f"-m {TestMarker.data_portal_verification.value}  OR  -m {TestMarker.data_portal_teardown.value}  OR  -m {TestMarker.operations_portal.value}  OR  -m {TestMarker.data_portal_activation.value}"
        )


# extract portal type
@pytest.fixture(scope="session")
def tests_variants(pytestconfig) -> list[TestMarker]:
    return pytestconfig._test_variants


# init JSON outputs file
@pytest.fixture(scope="session", autouse=True)
def init_outputs_file():
    OutputsHandler.initialize_outputs_file()
