from __future__ import annotations

from typing import TYPE_CHECKING

from pages import PyPIComponentWithBaseLocator, PyPIPage
from selenium.webdriver.common.keys import Keys

from pomcorn import locators

if TYPE_CHECKING:
    from pages.search_page import SearchPage


class Search(PyPIComponentWithBaseLocator):
    """Component representing the search input field."""

    def __init__(
        self,
        page: PyPIPage,
        base_locator: locators.XPathLocator = locators.IdLocator("search"),
        wait_until_visible: bool = True,
    ):
        super().__init__(page, base_locator, wait_until_visible)

    def find(self, text: str) -> SearchPage:
        """Paste the text into the search field and send `Enter` key.

        Redirect to `SearchPage` and return its instance.

        """
        from pages.search_page import SearchPage

        self.body.fill(text)
        self.body.send_keys(Keys.ENTER)
        return SearchPage(self.webdriver)
