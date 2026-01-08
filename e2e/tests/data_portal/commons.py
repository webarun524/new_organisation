from playwright.sync_api import Page, expect


def check_dashboard_access(page: Page):
    expect(page.get_by_role("heading", name="Data Portal", level=5)).to_be_visible(
        timeout=20000
    )
