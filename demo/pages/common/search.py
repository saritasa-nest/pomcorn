from __future__ import annotations

from typing import TYPE_CHECKING

from selenium.webdriver.common.keys import Keys

from demo.pages import PyPIComponent
from pomcorn import locators

if TYPE_CHECKING:
    from demo.pages.search_page import SearchPage


class Search(PyPIComponent):
    """Component representing the search input field."""

    # If you are not going to write anything in ``__init__`` and only want
    # to set up ``base_locator``, you can specify it as a class attribute
    base_locator = locators.IdLocator("search")

    def find(self, text: str) -> SearchPage:
        """Paste the text into the search field and send `Enter` key.

        Redirect to `SearchPage` and return its instance.

        """
        from demo.pages.search_page import SearchPage

        self.body.fill(text)
        self.body.send_keys(Keys.ENTER)
        return SearchPage(self.webdriver)
