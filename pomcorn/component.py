import abc
from typing import Generic, TypeVar, overload

from . import locators
from .element import XPathElement
from .page import Page
from .web_view import WebView

TPage = TypeVar("TPage", bound=Page)


class Component(Generic[TPage], WebView):
    """The class to represent a page component.

    It contains page elements and utils methods for page manipulation, but as a
    separate entity that can be reused for different pages with common
    elements.

    """

    def __init__(self, page: TPage):
        super().__init__(
            page.webdriver,
            app_root=page.app_root,
            wait_timeout=page.wait_timeout,
        )
        self.page = page


class ComponentWithBaseLocator(Generic[TPage], Component[TPage]):
    """The class to represent a page component that depends on base locator.

    Implement wait methods until the component becomes visible or invisible.

    """

    def __init__(
        self,
        page: TPage,
        base_locator: locators.XPathLocator,
        wait_until_visible: bool = True,
    ):
        """Initialize component.

        Args:
            page: An instance of the page that uses this component.
            base_locator: locator: Instance of a class to locate the element in
                the browser. Used in relative element initialization methods
                and visibility waits.
            wait_until_visible: Whether to wait for the component to become
                visible before completing initialization or not.

        """
        super().__init__(page)
        self.base_locator = base_locator
        self.body = self.init_element(locator=base_locator)

        if wait_until_visible:
            self.wait_until_visible()

    @overload
    def init_element(self, *, locator: locators.XPathLocator) -> XPathElement:
        ...

    @overload
    def init_element(
        self,
        *,
        relative_locator: locators.XPathLocator,
    ) -> XPathElement:
        ...

    def init_element(
        self,
        *,
        relative_locator: locators.XPathLocator | None = None,
        locator: locators.XPathLocator | None = None,
    ) -> XPathElement:
        """Initialize element including base locator.

        Use `relative_locator` if you need to include `base_locator`, otherwise
        use `locator`.

        Raises:
            ValueError: If both arguments were passed or neither.

        """
        return super().init_element(
            locator=self._prepare_locator(
                locator=locator,
                relative_locator=relative_locator,
            ),
        )

    @overload
    def init_elements(
        self,
        *,
        locator: locators.XPathLocator | None = None,
    ) -> list[XPathElement]:
        ...

    @overload
    def init_elements(
        self,
        *,
        relative_locator: locators.XPathLocator | None = None,
    ) -> list[XPathElement]:
        ...

    def init_elements(
        self,
        *,
        relative_locator: locators.XPathLocator | None = None,
        locator: locators.XPathLocator | None = None,
    ) -> list[XPathElement]:
        """Initialize list of elements including base locator.

        Use `relative_locator` if you need to include `base_locator`, otherwise
        use `locator`.

        Raises:
            ValueError: If both arguments were passed or neither.

        """
        return super().init_elements(
            locator=self._prepare_locator(
                locator=locator,
                relative_locator=relative_locator,
            ),
        )

    def _prepare_locator(
        self,
        *,
        relative_locator: locators.XPathLocator | None = None,
        locator: locators.XPathLocator | None = None,
    ) -> locators.XPathLocator:
        """Prepare a locator by arguments.

        Check that only one locator argument is passed, or none.
        If only `relative_locator` was passed, `base_locator` will be added to
        it. If only `locator` was passed, it will return itself.

        Raises:
            ValueError: If both arguments were passed or neither.

        """
        if relative_locator and locator:
            raise ValueError(
                "You need to pass only one of the arguments: "
                "`locator` or `relative_locator`.",
            )

        if not relative_locator:
            if not locator:
                raise ValueError(
                    "You need to pass one of the arguments: "
                    "`locator` or `relative_locator`.",
                )
            return locator
        return self.base_locator // relative_locator

    def wait_until_visible(self, **kwargs):
        """Wait until component becomes visible."""
        self.body.wait_until_visible()

    def wait_until_invisible(self, **kwargs):
        """Wait until component becomes invisible."""
        self.body.wait_until_invisible()


# Here type ignore added because we can't specify TPage as generic
# for ComponentWithBaseLocator, but specifying Page is incorrect
ListItemType = TypeVar(
    "ListItemType",
    bound=ComponentWithBaseLocator,  # type: ignore
)


class ListComponent(
    Generic[ListItemType, TPage],
    ComponentWithBaseLocator[TPage],
):
    """Class to represent a list-like component.

    It contains standard properties and methods for working with list-like
    components:

    * count
    * all
    * get_item_by_text()

    Waits for `base_item_locator` property to be implemented and value of
    `item_class` to be set.

    """

    item_class: type[ListItemType]

    @abc.abstractproperty
    def base_item_locator(self) -> locators.XPathLocator:
        """Get the base locator of list item."""
        raise NotImplementedError

    @property
    def count(self) -> int:
        """Get count of list items."""
        return len(self._get_elements(self.base_item_locator))

    @property
    def all(self) -> list[ListItemType]:
        """Get all items of list."""
        # Sometimes `base_item_locator` exists in dom but is not visible
        # and method returns an empty list. That's why we add waiting for this
        if (
            base_item := self.init_element(locator=self.base_item_locator)
        ).exists_in_dom:
            base_item.wait_until_visible()

        items: list[ListItemType] = []
        for locator in self.iter_locators(self.base_item_locator):
            items.append(self.item_class(self.page, locator))
        return items

    def get_item_by_text(self, text: str) -> ListItemType:
        """Get list item by text."""
        locator = self.base_item_locator.extend_query(
            extra_query=f"[contains(.,'{text}')]",
        )
        return self.item_class(page=self.page, base_locator=locator)

    def __repr__(self) -> str:
        return (
            "ListComponent("
            f"component={self.__class__}, "
            f"item_class={self.item_class}, "
            f"base_item_locator={self.base_item_locator}, "
            f"count={self.count}, "
            f"items={self.all}, "
            f"page={self.page}"
            ")"
        )

    def __str__(self) -> str:
        return f"{self.all}"
