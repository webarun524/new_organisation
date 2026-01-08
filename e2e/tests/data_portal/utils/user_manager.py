from playwright.sync_api import Page, Response, expect


class UserManager:
    """Helper class for user management operations."""

    def __init__(self, page: Page):
        self.page = page

    async def _go_to_identity_and_access_management(self) -> None:
        """Navigate to Identity & Access Management section."""
        await self.page.goto("/Settings")
        await self.page.get_by_text("Identity & Access Management").click()

    async def disable_user(self, login_to_be_disabled: str) -> None:
        """
        Disable a user by login.

        Args:
            login_to_be_disabled: User login/email to disable
        """
        await self._go_to_identity_and_access_management()

        toggle_user = self.page.get_by_test_id(
            f"{login_to_be_disabled}-row"
        ).get_by_test_id("toggle-user")

        await expect(toggle_user).to_be_visible()

        # Check if already disabled
        if await toggle_user.text_content() == "Enable":
            return

        await toggle_user.click()

        # Wait for disable API response
        def check_disable_response(response: Response) -> bool:
            url_lower = response.url.lower()
            if "/users/disable" in url_lower:
                if response.status != 200:
                    raise Exception("Failed to disable user")
                return True
            return False

        await self.page.wait_for_response(check_disable_response)
        await expect(toggle_user).to_have_text("Enable")

    async def enable_user(self, login_to_be_enabled: str) -> None:
        """
        Enable a user by login.

        Args:
            login_to_be_enabled: User login/email to enable
        """
        await self._go_to_identity_and_access_management()

        toggle_user = self.page.get_by_role(
            "row", name=login_to_be_enabled
        ).get_by_test_id("toggle-user")

        # Check if already enabled
        if await toggle_user.text_content() == "Disable":
            return

        await toggle_user.click()

        # Wait for enable API response
        def check_enable_response(response: Response) -> bool:
            url_lower = response.url.lower()
            if "/users/enable" in url_lower:
                if response.status != 200:
                    raise Exception("Failed to enable user")
                return True
            return False

        await self.page.wait_for_response(check_enable_response)
        await expect(toggle_user).to_have_text("Disable")
