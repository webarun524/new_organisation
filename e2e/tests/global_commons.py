import re

from playwright.sync_api import Page


def select_mui_option(page: Page, label: str | re.Pattern, value: str):
    page.get_by_label(label).click()
    option = page.get_by_role("option", name=value)
    if option.count() == 0:
        raise ValueError(f"Option '{value}' not found for '{label}'")
    option.click()
