from __future__ import annotations

from selenium.webdriver.remote.webdriver import WebDriver

from demo.pages.base import PyPIPage
from pomcorn import locators


class PackageDetailsPage(PyPIPage):
    """Represent the package details page."""

    @property
    def header(self) -> str:
        """Get the header text."""
        return self.init_element(
            locator=locators.ClassLocator("package-header__name"),
        ).get_text()

    @classmethod
    def open(
        cls,
        webdriver: WebDriver,
        package_name: str,
        *,
        app_root: str | None = None,
    ) -> PackageDetailsPage:
        """Search and open the package details page by its name."""
        from demo.pages import IndexPage

        search_page = IndexPage.open(
            webdriver,
            app_root=app_root,
        ).search.find(package_name)
        return search_page.results.get_item_by_text(package_name).open()
