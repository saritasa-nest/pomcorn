from contextlib import contextmanager

from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from pomcorn.element import PomcornElement, XPathElement

from . import exceptions, locators, waits_conditions
from .locators.base_locators import TInitLocator


class WebView:
    """Class for storing basic shortcuts for interacting with the browser."""

    def __init__(
        self,
        webdriver: WebDriver,
        *,
        app_root: str,
        wait_timeout: int,
        poll_frequency=float(0),
    ):
        """Initialize webview.

        Args:
            webdriver: Instance of a class for managing the browser.
            app_root: The URL of browser.
            wait_timeout: Number of seconds before timing out.
            poll_frequency: Time between checks of `wait` condition, lower
                interval - faster checks. This allows to improve overall tests
                speed.

        """
        self.webdriver = webdriver
        self.app_root = app_root
        self.wait_timeout = wait_timeout
        self.wait = WebDriverWait(
            driver=webdriver,
            timeout=wait_timeout,
            poll_frequency=poll_frequency,
        )

    def init_element(
        self,
        locator: TInitLocator,
    ) -> PomcornElement[TInitLocator]:
        """Shortcut for initializing Element instances.

        Note: To be consistent with the method of the same name in
        ``Component``, try to use keyword when specifying the ``locator``
        argument whenever possible.

        Args:
            locator: Instance of a class to locate the element in the browser.

        """
        return PomcornElement(web_view=self, locator=locator)

    def init_elements(
        self,
        locator: locators.XPathLocator,
    ) -> list[XPathElement]:
        """Shortcut for initializing many Element instances via single locator.

        Note: Only supports Xpath locators.

        Note: To be consistent with the method of the same name in
        ``Component``, try to use keyword when specifying the ``locator``
        argument whenever possible.

        Args:
            locator: Instance of a class to locate the element in the browser.

        """
        assert isinstance(
            locator,
            locators.XPathLocator,
        ), "Only supports Xpath locators!"
        elements_count = len(self._get_elements(locator=locator))
        return [
            self.init_element(
                locator=locators.XPathLocator(
                    query=f"({locator.query})[{index + 1}]",
                ),
            )
            for index in range(elements_count)
        ]

    def iter_locators(
        self,
        locator: locators.XPathLocator,
        only_visible: bool = False,
    ) -> list[locators.XPathLocator]:
        """Get the list of the locators where each of them match an element.

        For example, there are multiple elements on the page that matches
        `XPathLocator("//a")`.

        This method return the set of locators like:
        * `XPathLocator("(//a)[1]")`
        * `XPathLocator("(//a)[2]")`

        Args:
            locator: Instance of a class to locate the element in the browser.
            only_visible: Flag for viewing visible elements. If this is `True`
                (default), then this method will only get visible elements,
                otherwise all the elements (including not visible) will be
                counted.

        """
        result = []
        elements_count = len(
            self._get_elements(locator=locator, only_visible=only_visible),
        )
        for index in range(1, elements_count + 1):
            # Need to wrap it into parentheses to iterate by index when locator
            # is complex: https://sqa.stackexchange.com/a/39465
            result.append(
                locators.XPathLocator(
                    query=f"({locator.query})[{index}]",
                ),
            )
        return result

    @property
    def current_url(self) -> str:
        """Return the current webdriver URL."""
        return self.webdriver.current_url

    def _get_element(
        self,
        locator: locators.Locator,
        only_visible: bool = True,
    ) -> WebElement:
        """Get WebElement from page by using locator.

        Args:
            locator: Instance of a class to locate the element in the browser.
            only_visible: Flag for viewing visible elements. If this is `True`
                (default), then this method will only get visible elements,
                otherwise all the elements (including not visible) will be
                counted.

        """
        if only_visible:
            self.wait_until_locator_visible(locator=locator)
        return self.webdriver.find_element(*locator)

    def _get_elements(
        self,
        locator: locators.Locator,
        only_visible: bool = False,
    ) -> list[WebElement]:
        """Get WebElements from page by using locator.

        Args:
            locator: Instance of a class to locate the element in the browser.
            only_visible: Flag for viewing visible elements. If this is `True`,
                then this method will only get visible elements, otherwise
                all (default) the elements (including not visible) will be
                counted.

        """
        if only_visible:
            self.wait_until_locator_visible(locator=locator)
        return self.webdriver.find_elements(*locator)

    def wait_until_url_contains(self, url: str):
        """Wait until browser's url contains input url.

        Raises:
            TimeoutException: If after `self.wait_timeout` seconds the wait
                has not ended.

        """
        try:
            self.wait.until(expected_conditions.url_contains(url))
        except TimeoutException:
            raise exceptions.UrlDoesContainError(
                f"Url doesn't contain `{url}` in {self.wait_timeout} seconds! "
                f"The current URL is `{self.current_url}`.",
            )

    def wait_until_url_not_contains(self, url: str):
        """Wait until browser's url doesn't not contains input url.

        Raises:
            TimeoutException: If after `self.wait_timeout` seconds the wait
                has not ended.

        """
        try:
            self.wait.until(waits_conditions.url_not_matches(url))
        except TimeoutException:
            raise exceptions.UrlDoesContainError(
                f"Url does contain `{url}` in {self.wait_timeout} seconds! "
                f"The current URL is `{self.current_url}`.",
            )

    def wait_until_url_changes(self, url: str | None = None):
        """Wait until url changes.

        Args:
            url: Browser URL which should be changed. If the argument is not
                input, will be used `self.current_url`.

        Raises:
            TimeoutException: If after `self.wait_timeout` seconds the wait
                has not ended.

        """
        url = url or self.current_url
        try:
            self.wait.until(expected_conditions.url_changes(url))
        except TimeoutException:
            raise exceptions.UrlDidNotChangedError(
                f"Url didn't changed from {url} in {self.wait_timeout} "
                f"seconds! The current URL is `{self.current_url}`.",
            )

    def wait_until_locator_visible(self, locator: locators.Locator):
        """Wait until element matching locator becomes visible.

        Args:
            locator: Instance of a class to locate the element in the browser.

        Raises:
            TimeoutException: If after `self.wait_timeout` seconds the wait
                has not ended.

        """
        try:
            self.wait.until(
                expected_conditions.visibility_of_element_located(
                    locator=(locator.by, locator.query),
                ),
            )
        except TimeoutException:
            raise exceptions.ElementIsNotVisibleError(
                f"Unable to locate {locator} in {self.wait_timeout} seconds!",
            )

    def wait_until_locator_invisible(self, locator: locators.Locator):
        """Wait until element matching locator becomes invisible.

        Args:
            locator: Instance of a class to locate the element in the browser.

        Raises:
            TimeoutException: If after `self.wait_timeout` seconds the wait
                has not ended.

        """
        try:
            self.wait.until(
                expected_conditions.invisibility_of_element_located(
                    locator=(locator.by, locator.query),
                ),
            )
        except TimeoutException:
            raise exceptions.ElementIsNotInvisibleError(
                f"{locator} is still visible in {self.wait_timeout} seconds!",
            )

    def wait_until_clickable(self, locator: locators.Locator):
        """Wait until element matching locator becomes clickable.

        Args:
            locator: Instance of a class to locate the element in the browser.

        Raises:
            TimeoutException: If after `self.wait_timeout` seconds the wait
                has not ended.

        """
        try:
            self.wait.until(
                expected_conditions.element_to_be_clickable(
                    mark=(locator.by, locator.query),
                ),
            )
        except TimeoutException:
            raise exceptions.ElementIsNotClickableError(
                f"{locator} isn't clickable after {self.wait_timeout} "
                "seconds!",
            )

    def wait_until_text_is_in_element(
        self,
        text: str,
        locator: locators.Locator,
    ):
        """Wait until text is present in the specified element by locator.

        Args:
            locator: Instance of a class to locate the element in the browser.
            text: Text that should be presented in element.

        Raises:
            TimeoutException: If after `self.wait_timeout` seconds the wait
                has not ended.

        """
        try:
            self.wait.until(
                expected_conditions.text_to_be_present_in_element(
                    locator=(locator.by, locator.query),
                    text_=text,
                ),
            )
        except TimeoutException:
            raise exceptions.TextIsNotInElementError(
                f"{locator} doesn't have `{text}` after {self.wait_timeout} "
                "seconds!",
            )

    def wait_until_not_exists_in_dom(
        self,
        element: PomcornElement[locators.TLocator] | locators.TLocator,
    ):
        """Wait until element ceases to exist in DOM.

        Args:
            locator: Instance of a class to locate the element in the browser
                or instance of element.

        Raises:
            TimeoutException: If after `self.wait_timeout` seconds the wait
                has not ended.

        """
        try:
            self.wait.until(
                waits_conditions.element_not_exists_in_dom(element),
            )
        except TimeoutException:
            raise exceptions.TextIsNotInElementError(
                f"{element} is still exists in DOM after {self.wait_timeout} "
                "seconds!",
            )

    def drag_and_drop(self, source: WebElement, target: WebElement):
        """Perform drag and drop.

        Args:
            source: The web element instance to drag.
            target: The web element instance to drag into.

        """
        ActionChains(self.webdriver).drag_and_drop(source, target).perform()

    def scroll_to(self, target: WebElement):
        """Scroll page to target.

        Scroll to the center of target vertically and to the center of target
        horizontally.

        Args:
            target: The web element instance to scroll to.

        """
        # behavior="instant" - to scroll without animation
        # block="center" - vertical scrolling up to center
        # inline="center"- horizontal scrolling up to center
        script = (
            "arguments[0].scrollIntoView("
            "{behavior: 'instant', block: 'center', inline: 'center'}"
            ");"
        )
        self.webdriver.execute_script(script, target)

    def scroll_to_top(self):
        """Scroll browser to top."""
        self.webdriver.execute_script(
            script="window.scrollBy(0, -document.body.scrollHeight)",
        )

    def scroll_to_bottom(self):
        """Scroll browser to bottom."""
        self.webdriver.execute_script(
            script="window.scrollBy(0, document.body.scrollHeight)",
        )

    def get_input_value(self, label: str) -> str:
        """Find input element by label and get it's value."""
        return self.init_element(
            locator=locators.InputByLabelLocator(label=label),
        ).get_value()

    def execute_javascript(self, script: str, *args):
        """Execute simple javascript.

        Args:
            script: JavaScript code as a string object.

        """
        self.webdriver.execute_script(script, *args)

    def switch_to_default(self):
        """Switch webdriver's focus to default content."""
        self.webdriver.switch_to.default_content()

    def switch_to_iframe(self, locator: locators.Locator):
        """Switch webdriver's focus to iframe.

        Args:
            locator: Instance of a class to locate the element in the browser.

        """
        self.webdriver.switch_to.frame(self._get_element(locator))

    @contextmanager
    def iframe_switcher_manager(self, locator: locators.Locator):
        """Context manager for interacting with iframes.

        Args:
            locator: Instance of a class to locate the element in the browser.

        """
        self.switch_to_iframe(locator=locator)
        yield
        self.switch_to_default()
