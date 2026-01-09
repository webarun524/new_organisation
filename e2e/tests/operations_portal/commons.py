from playwright.sync_api import Page, expect


def navigate_from_catalog_to_deployment_form(page: Page):
    page.goto("/catalog")

    container = page.get_by_test_id("navigation-container")
    subscribe_button = container.get_by_role("button", name="Subscribe")
    expect(subscribe_button).to_be_visible(timeout=15000)
    subscribe_button.click()

    expect(page).to_have_url("/deployment/create")
