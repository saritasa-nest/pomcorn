from __future__ import annotations

from typing import TYPE_CHECKING

from demo.pages import PyPIComponent
from pomcorn import Element, locators

if TYPE_CHECKING:
    from demo.pages.help_page import HelpPage


# `Component` implements methods of waiting until the component becomes
# visible / invisible, including in `__init__` method. This will allow to make
# tests more stable because the component will wait until it becomes visible
# before returning its instance.
class Navbar(PyPIComponent):
    """Component representing navigation bar in the top of web application."""

    base_locator = locators.ClassLocator(
        class_name="horizontal-menu",
        # We specify `container` here because the page has several `nav`
        # tags and several elements with a similar class name.
        container="nav",
    )

    help_button = Element(
        locator=locators.ElementWithTextLocator(text="Help", element="a"),
    )

    def open_help(self) -> HelpPage:
        """Click on `Help` button and redirect to HelpPage."""
        from demo.pages.help_page import HelpPage

        self.help_button.click()
        return HelpPage(self.webdriver)
