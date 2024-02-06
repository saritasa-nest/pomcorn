from __future__ import annotations

from pages.base import PyPIPage
from pages.common import Search
from selenium.webdriver.remote.webdriver import WebDriver

from pomcorn.descriptors import ComponentDescriptor


class IndexPage(PyPIPage):
    """Represent the index page."""

    search2 = ComponentDescriptor["IndexPage", Search](Search)

    def __init__(
        self,
        webdriver: WebDriver,
        *,
        app_root: str | None = None,
        wait_timeout: int = 5,
        poll_frequency: float = 0.01,
    ):
        super().__init__(
            webdriver,
            app_root=app_root,
            wait_timeout=wait_timeout,
            poll_frequency=poll_frequency,
        )

    @property
    def search(self) -> Search:
        """Get the search component.

        Allows to work with the search field at the center of the page.

        """
        return Search(self)
