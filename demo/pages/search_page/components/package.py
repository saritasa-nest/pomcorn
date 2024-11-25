from __future__ import annotations

from typing import TYPE_CHECKING

from demo.pages import PyPIComponent
from pomcorn import locators

if TYPE_CHECKING:
    from demo.pages import PackageDetailsPage


class Package(PyPIComponent):
    """Represent the single search result (package) on `SearchPage`."""

    @property
    def name(self) -> str:
        """Get the package name."""
        return self.init_element(
            relative_locator=locators.ClassLocator("package-snippet__name"),
        ).get_text()

    def open(self) -> PackageDetailsPage:
        """Click on the package and open its details page."""
        from demo.pages import PackageDetailsPage

        # The property `body` is available because the package is descendant of
        # `Component`. It allows us to interact with the body of the component
        # and we can check that the package is clickable.
        self.body.click()
        return PackageDetailsPage(self.webdriver)
