# Custom waits conditions
import re
from collections.abc import Callable

from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
)
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.expected_conditions import (
    WebDriverOrWebElement,
)

from pomcorn.locators.base_locators import TLocator

from .element import PomcornElement


def url_not_matches(pattern: str) -> Callable[[WebDriver], bool]:
    """Represent `wait condition` to check that url doesn't match pattern."""

    def check_the_match(driver: WebDriver) -> bool:
        return re.search(pattern, driver.current_url) is None

    return check_the_match


def text_in_element_changes(
    element: PomcornElement[TLocator] | TLocator,
    old_text: str,
) -> Callable[[WebDriver], bool]:
    """Represent `wait condition` to check that text doesn't match old text.

    Args:
        element: The element in which the text will be checked.
        old_text: The old text that should disappear.

    """

    def check_the_match(driver: WebDriver) -> bool:
        target = element

        if isinstance(target, PomcornElement):
            return old_text != target.get_text()

        return old_text != driver.find_element(*target).text

    return check_the_match


def element_not_exists_in_dom(
    element: PomcornElement[TLocator] | TLocator,
) -> Callable[[WebDriver], bool]:
    """Represent `wait condition` to check that element not exists in DOM."""

    def check_the_match(driver: WebDriver) -> bool:
        target = element

        if isinstance(target, PomcornElement):
            return not target.exists_in_dom

        try:
            # Check if driver can find element.
            driver.find_element(*target)
        except (NoSuchElementException, StaleElementReferenceException):
            # In the case of NoSuchElement, returns true because the element is
            # not present in DOM.
            # In the case of StaleElementReference, returns true because stale
            # element reference implies that element is no longer visible.
            return True
        # We return `False` because if `driver` can find element without
        # exception, that means element exists in the DOM.
        return False

    return check_the_match


def text_not_to_be_present_in_element_attribute(
    locator: tuple[str, str],
    attribute_: str,
    text_: str,
) -> Callable[[WebDriverOrWebElement], bool]:
    """Represent `wait condition` that checks that text is not in attribute.

    NOTE: "_" in argument names added for consistent with selenium's built-in
    wait condition `text_to_be_present_in_element_attribute`

    Args:
        locator: A tuple with a By instance and a string value. You can get
            them from the Locators classes.
        attribute_: Attribute name.
        text_: Text that should disappear.

    """

    def check_the_match(driver: WebDriverOrWebElement) -> bool:
        try:
            attribute_text = driver.find_element(*locator).get_attribute(
                name=attribute_,
            )
            if attribute_text is None:
                # If attribute is empty, it means that it contains no text.
                return True
            return text_ not in attribute_text
        except StaleElementReferenceException:
            # If element doesn't exist, it means that its attribute doesn't
            # contain text.
            return True

    return check_the_match
