from __future__ import annotations

from pages import IndexPage, PyPIPage
from selenium.webdriver.remote.webdriver import WebDriver

from pomcorn.descriptors import GetComponent

from .components import PackageList


class SearchPage(PyPIPage):
    """Representation of the page with search results."""

    # Get the `PackageList` component for work with the found packages
    results = GetComponent[PackageList]()

    @classmethod
    def open(cls, webdriver: WebDriver) -> SearchPage:
        """Open the search page."""
        # Open `IndexPage` and search for an empty query.
        # This will redirect us to the `SearchPage'.
        return IndexPage.open(webdriver).search.find("")
