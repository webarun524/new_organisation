from playwright.sync_api import Page, expect


class Security:
    """Helper class for security and access control verification."""

    def __init__(self, page: Page):
        self.page = page

    def check_service_statuses(self) -> None:
        """
        Verify service status visibility in Settings.

        Checks that:
        - Platform health container is visible
        - Platform state is "On"
        - At least 20 service status divs exist
        """
        self.page.goto("/Settings")

        platform_container = self.page.get_by_test_id("platform-health-container")

        expect(platform_container).to_be_visible()
        expect(self.page.get_by_label("platform-state: On")).to_be_visible()

        # Verify at least 20 service status divs
        divs = platform_container.locator("div").all()
        assert len(divs) > 20, f"Expected >20 service divs, got {len(divs)}"

    def check_entitlements_access(self, should_expect_access: bool) -> None:
        """
        Verify Identity & Access Management visibility.

        Args:
            should_expect_access: True if button should be visible, False otherwise
        """
        self.page.goto("/Settings")

        iam_button = self.page.get_by_role(
            "button", name="Identity & Access Management"
        )

        if should_expect_access:
            expect(iam_button).to_be_visible()
        else:
            expect(iam_button).not_to_be_visible()

    def check_platform_management_access(self, should_expect_access: bool) -> None:
        """
        Verify Platform Management visibility.

        Args:
            should_expect_access: True if button should be visible, False otherwise
        """
        self.page.goto("/Settings")

        pm_button = self.page.get_by_role("button", name="Platform Management")

        if should_expect_access:
            expect(pm_button).to_be_visible()
        else:
            expect(pm_button).not_to_be_visible()
