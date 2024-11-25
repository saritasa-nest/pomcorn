from __future__ import annotations

from selenium.webdriver.remote.webdriver import WebDriver

from demo.pages import IndexPage, PyPIPage

from .components import PackageList


class SearchPage(PyPIPage):
    """Representation of the page with search results."""

    @classmethod
    def open(
        cls,
        webdriver: WebDriver,
        *,
        app_root: str | None = None,
    ) -> SearchPage:
        """Open the search page."""
        # Open `IndexPage` and search for an empty query.
        # This will redirect us to the `SearchPage'.
        return IndexPage.open(webdriver).search.find("")

    @property
    def results(self) -> PackageList:
        """Get the component for work with the found packages."""
        return PackageList(self)
