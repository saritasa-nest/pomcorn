from __future__ import annotations

from typing import TYPE_CHECKING

from pages import PyPIComponent, PyPIPage

from pomcorn import locators

if TYPE_CHECKING:
    from pages.help_page import HelpPage


# `Component` implements methods of waiting until the component becomes
# visible / invisible, including in `__init__` method. This will allow to make
# tests more stable because the component will wait until it becomes visible
# before returning its instance.
class Navbar(PyPIComponent):
    """Component representing navigation bar in the top of web application."""

    def __init__(
        self,
        page: PyPIPage,
        base_locator: locators.XPathLocator = locators.ClassLocator(
            class_name="horizontal-menu",
            # We specify `container` here because the page has several `nav`
            # tags and several elements with a similar class name.
            container="nav",
        ),
        # If you don't need to wait for the component to become visible during
        # initialization, set `wait_until_visible` to `False`.
        wait_until_visible: bool = True,
    ):
        super().__init__(page, base_locator, wait_until_visible)
        self.help_button = self.init_element(
            # Specifying the argument name is required here, because depending
            # on the name `init_element` method can modify the passed locator.
            relative_locator=locators.ElementWithTextLocator(
                text="Help",
                element="a",
            ),
        )

    def open_help(self) -> HelpPage:
        """Click on `Help` button and redirect to HelpPage."""
        from pages.help_page import HelpPage

        self.help_button.click()
        return HelpPage(self.webdriver)
