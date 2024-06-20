from typing import Self

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver

from .exceptions import PageDidNotLoadedError
from .web_view import WebView


class Page(WebView):
    """The class for representing a web page.

    It contains the element and components of the page and utils methods for
    page manipulation.

    """

    APP_ROOT: str

    def __init__(
        self,
        webdriver: WebDriver,
        *,
        app_root: str | None = None,
        wait_timeout: int = 5,
        poll_frequency: float = 0.01,
    ):
        """Initialize page.

        Call `wait_until_loaded` method after initialization.

        Args:
            webdriver: Instance of a class for managing the browser.
            app_root: The URL of base page, by default the value of `APP_ROOT`
                attribute is used.
            wait_timeout: Number of seconds before timing out.
            poll_frequency: Time between checks of `wait` condition, lower
                interval - faster checks. This allows to improve overall tests
                speed.

        """
        super().__init__(
            webdriver,
            app_root=app_root or self.APP_ROOT,
            wait_timeout=wait_timeout,
            poll_frequency=poll_frequency,
        )
        self.wait_until_loaded()

    def check_page_is_loaded(self) -> bool:
        """Return result of check that the page is loaded.

        Some pages can be slow to load and cause problems checking for unloaded
        items. To be sure the page is loaded, this property should return the
        result of checking for the slowest parts of the page.

        """
        return True

    @classmethod
    def open(
        cls,
        webdriver: WebDriver,
        *,
        app_root: str | None = None,
    ) -> Self:
        """Open page and initialize page object.

        Args:
            webdriver: Instance of a WebDriver class for managing the browser.
            app_root: The URL of page, by default the value of `APP_ROOT`
                attribute is used.

        """
        webdriver.get(url=f"{app_root or cls.APP_ROOT}")
        # hack to not specify app_root in each page init method
        kwargs = {}
        if app_root:
            kwargs = {"app_root": app_root}

        # Mypy raise error on unpacking `kwargs`:
        # "Page" has incompatible type "**dict[str, str]"; expected "int"
        # "Page" has incompatible type "**dict[str, str]"; expected "float"
        return cls(webdriver, **kwargs)  # type: ignore

    @classmethod
    def open_from_url(
        cls,
        webdriver: WebDriver,
        *,
        path: str,
        app_root: str | None = None,
        **kwargs,
    ) -> Self:
        """Open page from relative path and initialize page object.

        Add `path` to `app_root` in browser URL.

        Args:
            webdriver: Instance of a WebDriver class for managing the browser.
            app_root: The URL of page, by default the value of `APP_ROOT`
                attribute is used.
            path: Relative URL.

        """
        # hack to not specify app_root in each page init method
        if app_root:
            kwargs["app_root"] = app_root

        # We don't use `page.navigate_relative` here because we need to
        # navigate to relative url before page is initialized, since otherwise
        # `wait_until_loaded` method in page `__init__` method might fail.
        webdriver.get(
            url=cls._get_full_relative_url(app_root or cls.APP_ROOT, path),
        )

        page = cls(webdriver, **kwargs)
        return page

    def refresh(self) -> None:
        """Refresh web page and wait until it is loaded."""
        self.webdriver.refresh()
        self.wait_until_loaded()

    def wait_until_loaded(self) -> None:
        """Wait until page is loaded."""
        try:
            self.wait.until(lambda _: self.check_page_is_loaded())
        except TimeoutException:
            raise PageDidNotLoadedError(
                f"Page `{self.__class__}` didn't loaded in "
                f"{self.wait_timeout} seconds! Didn't wait for `True` from "
                "`check_page_is_loaded` method.",
            )

    def navigate(self, url: str) -> None:
        """Navigate absolute URL.

        Replace the browser URL with the entered one.

        """
        self.webdriver.get(url)

    def navigate_relative(self, relative_url: str = "/") -> None:
        """Navigate to URL relative to application root.

        Args:
            relative_url (str): Relative URL

        """
        self.webdriver.get(
            self._get_full_relative_url(self.app_root, relative_url),
        )

    def click_on_page(self) -> None:
        """Click on (1, 1) coordinates of page (left upper corner).

        Allows you to move focus away from an element, for example, if it
        is currently unavailable for interaction.

        """
        from selenium.webdriver.common.actions.action_builder import (
            ActionBuilder,
        )

        action = ActionBuilder(self.webdriver)
        action.pointer_action.move_to_location(1, 1).click()
        action.perform()

    @staticmethod
    def _get_full_relative_url(app_root: str, relative_url: str) -> str:
        """Add relative URL to application root URL.

        Args:
            relative_url (str): Relative URL

        """
        if app_root.endswith("/"):
            # https://www.youtube.com/ -> https://www.youtube.com
            app_root = app_root[:-1]

        if relative_url.startswith("/"):
            # /watch_list -> watch_list
            relative_url = relative_url[1:]

        return f"{app_root}/{relative_url}"
