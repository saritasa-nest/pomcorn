from __future__ import annotations

from pages.base import PyPIPage
from selenium.webdriver.remote.webdriver import WebDriver

from pomcorn import Element, locators


class HelpPage(PyPIPage):
    """Represent the help page."""

    # Define element for title
    title_element = Element(locators.ClassLocator("page-title"))

    @classmethod
    def open(
        cls,
        webdriver: WebDriver,
        *,
        app_root: str | None = None,
    ) -> HelpPage:
        """Open the help page via the index page."""
        from pages.index_page import IndexPage

        # Reusing already implemented methods of opening a page instead of
        # overriding `app_root` allows us to be independent from URK changes:
        # we move from one page to another, interacting with the page as the
        # user does.
        return IndexPage.open(webdriver, app_root=app_root).navbar.open_help()

    def check_page_is_loaded(self) -> bool:
        """Return the check result that the page is loaded.

        Return whether help page title element are displayed or not.

        """
        return self.title_element.is_displayed
