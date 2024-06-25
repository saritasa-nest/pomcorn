from __future__ import annotations

import sys
from typing import TYPE_CHECKING, Generic

from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select

from pomcorn import locators

if TYPE_CHECKING:
    from pomcorn.web_view import WebView


class PomcornElement(Generic[locators.TLocator]):
    """The class to represent a simple element (tag) on the page.

    Contains methods for the interaction with an element on the browser page.

    """

    def __init__(self, web_view: WebView, locator: locators.TLocator):
        """Init page element.

        Args:
            web_view: Instance of a webview.
            locator: Instance of a class to locate the element in the browser.

        """
        self.web_view = web_view
        self.locator = locator

    def wait_until_visible(self):
        """Wait until element becomes visible.

        Raises:
            TimeoutException: If after `self.wait_timeout` seconds the wait
                has not ended.

        """
        self.web_view.wait_until_locator_visible(locator=self.locator)

    def wait_until_invisible(self):
        """Wait until element becomes invisible.

        Raises:
            TimeoutException: If after `self.wait_timeout` seconds the wait
                has not ended.

        """
        self.web_view.wait_until_locator_invisible(locator=self.locator)

    def wait_until_clickable(self):
        """Wait until element becomes clickable.

        Raises:
            TimeoutException: If after `self.wait_timeout` seconds the wait
                has not ended.

        """
        self.web_view.wait_until_clickable(locator=self.locator)

    def wait_until_text_is_in_element(self, text: str):
        """Wait until text is present in element.

        Raises:
            TimeoutException: If after `self.wait_timeout` seconds the wait
                has not ended.

        """
        self.web_view.wait_until_text_is_in_element(
            text=text,
            locator=self.locator,
        )

    def wait_until_not_exists_in_dom(self):
        """Wait until element ceases to exist in DOM.

        Raises:
            TimeoutException: If after `self.wait_timeout` seconds the wait
                has not ended.

        """
        self.web_view.wait_until_not_exists_in_dom(self.locator)

    def get_element(self, only_visible: bool = True) -> WebElement:
        """Get selenium instance(WebElement) of element.

        Args:
            only_visible: Flag for viewing visible elements. If this is `True`
                (default), then this method will only get visible elements,
                otherwise all the elements (including not visible) will be
                counted.

        """
        return self.web_view._get_element(
            locator=self.locator,
            only_visible=only_visible,
        )

    @property
    def exists_in_dom(self) -> bool:
        """Check if element is present in html, can be not visible."""
        return len(self.web_view._get_elements(locator=self.locator)) != 0

    @property
    def is_displayed(self) -> bool:
        """Check if element is displayed.

        If element is not present in the html, return `False`.

        """
        elements = self.web_view._get_elements(locator=self.locator)
        if not elements:
            return False

        try:
            return elements[0].is_displayed()
        except StaleElementReferenceException:
            # Sometimes an element may disappear before we check its visibility
            return False

    @property
    def is_enabled(self) -> bool:
        """Check if element is enabled.

        It is primarily used with buttons.

        """
        return self.get_element().is_enabled()

    @property
    def is_selected(self) -> bool:
        """Check if element is selected.

        It is predominantly used with radio buttons, dropdowns and checkboxes.

        """
        return self.get_element().is_selected()

    def fill(
        self,
        text: str,
        only_visible: bool = True,
        clear: bool = True,
    ):
        """Fill element with text.

        Args:
            text: The text that will be sent to the element to be filled.
            only_visible: Flag for viewing visible elements. If this is `True`
                (default), then this method will only get visible elements,
                otherwise all elements (including not visible) will be counted.
            clear: Whether the element needs to be cleared before filling it
                or not (default `True`).

        """
        if clear:
            self.clear(only_visible=only_visible)
        self.send_keys(str(text), only_visible=only_visible)

    def clear(self, only_visible: bool = True):
        """Clear element (input) and it's value.

        Args:
            only_visible: Flag for viewing visible elements. If this is `True`
                (default), then this method will only get visible elements,
                otherwise all the elements (including not visible) will be
                counted.

        """
        self.get_element(only_visible=only_visible)

        if sys.platform == "darwin":
            self.send_keys(Keys.COMMAND + "a")
        else:
            self.send_keys(Keys.CONTROL + "a")
        self.send_keys(Keys.BACK_SPACE)

    def send_keys(self, keys: str, only_visible: bool = True):
        """Send keys to element.

        Simulate user keystrokes.

        Args:
            keys: The names of the keys in the form of a single string.
                More keys: https://www.selenium.dev/selenium/docs/api/py/webdriver/selenium.webdriver.common.keys.html     # noqa
            only_visible: Flag for viewing visible elements. If this is `True`
                (default), then this method will only get visible elements,
                otherwise all the elements (including not visible) will be
                counted.

        """
        self.get_element(only_visible=only_visible).send_keys(*keys)

    def get_text(self, only_visible: bool = True) -> str:
        """Get text from element.

        Args:
            only_visible: Flag for viewing visible elements. If this is `True`
                (default), then this method will only get visible elements,
                otherwise all the elements (including not visible) will be
                counted.

        """
        return self.get_element(only_visible=only_visible).text

    def get_attribute(
        self,
        attribute_name: str,
        only_visible: bool = True,
    ) -> str:
        """Get value of attribute from element.

        If attribute is not found, return empty string.

        Args:
            attribute_name: Element attribute name..
            only_visible: Flag for viewing visible elements. If this is `True`
                (default), then this method will only get visible elements,
                otherwise all the elements (including not visible) will be
                counted.

        """
        return (
            self.get_element(only_visible=only_visible).get_attribute(
                name=attribute_name,
            )
            or ""
        )

    def set_attribute(
        self,
        attribute_name: str,
        value: str,
        only_visible: bool = True,
    ):
        """Set value to element attribute.

        Args:
            attribute_name: Element attribute name.
            value: New value for attribute.
            only_visible: Flag for viewing visible elements. If this is `True`
                (default), then this method will only get visible elements,
                otherwise all the elements (including not visible) will be
                counted.

        """
        element = self.get_element(only_visible=only_visible)
        self.web_view.execute_javascript(
            f"arguments[0].setAttribute('{attribute_name}',arguments[1])",
            element,
            value,
        )

    def get_value(self, only_visible: bool = True):
        """Get value of `value` attribute from element.

        Args:
            only_visible: Flag for viewing visible elements. If this is `True`
                (default), then this method will only get visible elements,
                otherwise all the elements (including not visible) will be
                counted.

        """
        return self.get_attribute(
            attribute_name="value",
            only_visible=only_visible,
        )

    def select(self, value: str, only_visible: bool = True):
        """Perform select on element.

        Args:
            value: Value for selecting an element based on visible text.
            only_visible: Flag for viewing visible elements. If this is `True`
                (default), then this method will only get visible elements.

        """
        Select(self.get_element(only_visible)).select_by_visible_text(value)

    def click(
        self,
        only_visible: bool = True,
        wait_until_clickable: bool = True,
    ):
        """Click on element.

        Args:
            only_visible: Flag for viewing visible elements. If this is `True`
                (default), then this method will only get visible elements.
            wait_until_clickable: Wait until the element is clickable before
                clicking, or not (default `True`).

        """
        if wait_until_clickable:
            self.wait_until_clickable()
        self.get_element(only_visible=only_visible).click()

    def drag_and_drop(
        self,
        target: PomcornElement[locators.TLocator],
        only_visible: bool = True,
    ):
        """Drag and drop page object on target object.

        Args:
            target: The element instance to drag into.
            only_visible: Flag for viewing visible elements. If this is `True`
                (default), then this method will only get visible elements.

        """
        self.web_view.drag_and_drop(
            source=self.get_element(only_visible=only_visible),
            target=target.get_element(only_visible=only_visible),
        )

    def scroll_to(self, only_visible: bool = True):
        """Scroll page until element is visible.

        Args:
            only_visible: Flag for viewing visible elements. If this is `True`
                (default), then this method will only get visible elements.

        """
        self.web_view.scroll_to(self.get_element(only_visible=only_visible))

    def hover_to(self, only_visible: bool = True):
        """Hover cursor to element.

        Args:
            only_visible: Flag for viewing visible elements. If this is `True`
                (default), then this method will only get visible elements.

        """
        action = ActionChains(self.web_view.webdriver).move_to_element(
            to_element=self.get_element(only_visible=only_visible),
        )
        action.perform()

    def get_value_of_css_property(
        self,
        property_name: str,
        only_visible: bool = True,
    ) -> str:
        """Return value of a CSS property.

        Args:
            property_name: Name of CSS property.
            only_visible: Flag for viewing visible elements. If this is `True`
                (default), then this method will only get visible elements.

        """
        return self.get_element(only_visible).value_of_css_property(
            property_name=property_name,
        )

    def add_debug_mark(self):
        """Set element background to red.

        Should be used only for debugging.

        """
        current_style = self.get_attribute("style")
        self.set_attribute("style", f"{current_style} background: red;")

    def remove_debug_mark(self):
        """Remove debug mark."""
        current_style = self.get_attribute("style")
        self.set_attribute(
            attribute_name="style",
            value=current_style.replace("background: red;", ""),
        )


XPathElement = PomcornElement[locators.XPathLocator]
