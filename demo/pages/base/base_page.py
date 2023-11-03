from __future__ import annotations

from typing import TYPE_CHECKING

from selenium.webdriver.remote.webdriver import WebDriver

from pomcorn import Page, locators

if TYPE_CHECKING:
    from pages import IndexPage
    from pages.common import Navbar


class PyPIPage(Page):
    """Base representation of the page for PyPI.

    This is the base page for all following pages, so here we have to implement
    only properties and methods common to all pages of application.

    """

    # Be sure to redefine this attribute:
    # specify the base domain of your app here.
    APP_ROOT = "https://pypi.org/"

    def __init__(
        self,
        webdriver: WebDriver,
        *,
        app_root: str | None = None,
        # Next arguments have default values, so you can delete/specify them.
        wait_timeout: int = 5,
        poll_frequency: float = 0.01,
    ):
        super().__init__(
            webdriver,
            app_root=app_root,
            wait_timeout=wait_timeout,
            poll_frequency=poll_frequency,
        )

        # The Logo will be on all the pages of the application so we initialize
        # it in base page class.
        self.logo = self.init_element(
            locator=locators.ClassLocator("site-header__logo"),
        )

    # We recommend adding components to the page as properties, because it
    # helps us to run `waits_until_visible` method every time this component is
    # accessed. But if you need to perform some actions before manipulating
    # this component (e.g. clicking, hovering, etc.), it's better to create
    # opening methods on page (like `open_navbar`).
    @property
    def navbar(self) -> Navbar:
        """Get a component for working with the page navigation panel."""
        from pages.common import Navbar

        return Navbar(self)

    # Some pages can be slow to load and cause problems checking for unloaded
    # items. To be sure the page is loaded, this property should return the
    # result of checking for the slowest parts of the page.
    @property
    def is_loaded(self) -> bool:
        """Return the result of checking that the page is loaded.

        Check that `main` tag is displayed.

        """
        return self.init_element(
            locator=locators.TagNameLocator("main"),
        ).is_displayed

    def click_on_logo(self) -> IndexPage:
        """Click on the logo and redirect to `IndexPage`."""
        from pages import IndexPage

        self.logo.click()
        return IndexPage(self.webdriver)
