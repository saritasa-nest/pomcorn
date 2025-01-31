import typing
from inspect import isclass
from typing import (
    Any,
    Generic,
    Literal,
    TypeVar,
    get_args,
    get_origin,
    overload,
)

from . import locators
from .element import XPathElement
from .page import Page
from .web_view import WebView

TPage = TypeVar("TPage", bound=Page)


class _EmptyValue:
    """Singleton to use as default value for empty class attribute."""

    def __bool__(self) -> Literal[False]:
        """Allow `EmptyValue` to be used in bool expressions."""
        return False


EmptyValue: Any = _EmptyValue()


class Component(Generic[TPage], WebView):
    """The class to represent a page component that depends on base locator.

    It contains page elements, components and utils methods for page
    manipulation, but as a separate entity that can be reused for different
    pages with common elements.

    Implement wait methods until the component becomes visible or invisible.

    """

    base_locator: locators.XPathLocator

    def __init__(
        self,
        page: TPage,
        base_locator: locators.XPathLocator | None = None,
        wait_until_visible: bool = True,
    ):
        """Initialize component.

        Args:
            page: An instance of the page that uses this component.
            base_locator: Instance of a class to locate the component in the
                browser. Used in relative element initialization methods and
                visibility waits. You also can specify it as attribute.
            wait_until_visible: Whether to wait for the component to become
                visible before completing initialization or not.

        """
        super().__init__(
            page.webdriver,
            app_root=page.app_root,
            wait_timeout=page.wait_timeout,
        )
        self.page = page
        self.base_locator = base_locator or self.base_locator
        self.body = self.init_element(locator=self.base_locator)

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


# Here type ignore added because we can't specify TPage as generic for
# Component, but specifying Page is incorrect
ListItemType = TypeVar("ListItemType", bound=Component)  # type: ignore


class ListComponent(Generic[ListItemType, TPage], Component[TPage]):
    """Class to represent a list-like component.

    It contains standard properties and methods for working with list-like
    components:

    * count
    * all
    * get_item_by_text()

    Waits for `base_item_locator` property  to be overridden or one of the
    attributes (`item_locator` or `relative_item_locator`) to be specified.

    """

    _item_class: type[ListItemType] = EmptyValue

    item_locator: locators.XPathLocator | None = None
    relative_item_locator: locators.XPathLocator | None = None

    def __class_getitem__(cls, item: tuple[type, ...]) -> Any:
        """Create parameterized versions of generic classes.

        This method is called when the class is used as a parameterized type,
        such as MyGeneric[int] or MyGeneric[List[str]].

        We override this method to store values passed in generic parameters.

        Args:
            cls - The generic class itself.
            item - The type used for parameterization.

        Returns:
            type: A parameterized version of the class with the specified type.

        """
        list_cls = super().__class_getitem__(item)  # type: ignore
        cls.__generic_parameters__ = item  # type: ignore
        return list_cls

    def __init__(
        self,
        page: TPage,
        base_locator: locators.XPathLocator | None = None,
        wait_until_visible: bool = True,
    ) -> None:
        # If `_item_class` was not specified in `__init_subclass__`, this means
        # that `ListComponent` is used as a parameterized type
        # (e.g., `List[ItemClass, Page]`).
        if isinstance(self._item_class, _EmptyValue):
            # In this way we check the stored generic parameters and, if first
            # from them is valid, set it as `_item_class`
            first_generic_param = self.__generic_parameters__[0]
            if self.is_valid_item_class(first_generic_param):
                self._item_class = first_generic_param
        super().__init__(page, base_locator, wait_until_visible)

    def __init_subclass__(cls) -> None:
        """Run logic for getting/overriding item_class attr for subclasses."""
        super().__init_subclass__()

        # If class has valid `_item_class` attribute from a parent class
        if cls.is_valid_item_class(cls._item_class):
            # We leave using of parent `item_class`
            return

        # Try to get `item_class` from first generic variable
        list_item_class = cls.get_list_item_class()

        if not list_item_class:
            # If `item_class` is not specified in generic we leave it empty
            # because it maybe not specified in base class but will be
            # specified in child
            return

        cls._item_class = list_item_class

    @property
    def base_item_locator(self) -> locators.XPathLocator:
        """Get the base locator of list item.

        Raises:
            ValueError: If both attributes are specified.
            NotImplementedError: If no attribute has been specified,

        """
        if self.relative_item_locator and self.item_locator:
            raise ValueError(
                "You only need to specify one of the attributes: "
                "`relative_item_locator` - if you want locator nested within "
                "`base_locator`, `item_locator` - otherwise. "
                "Or override `base_item_locator` property.",
            )
        if not self.relative_item_locator:
            if not self.item_locator:
                raise NotImplementedError(
                    "You need to specify one of the arguments: "
                    "`relative_item_locator` - if you want locator nested "
                    "within `base_locator`, `item_locator` - otherwise. "
                    "Or override `base_item_locator` property.",
                )
            return self.item_locator
        return self.base_locator // self.relative_item_locator

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
            items.append(
                self._item_class(page=self.page, base_locator=locator),
            )
        return items

    @classmethod
    def get_list_item_class(cls) -> type[ListItemType] | None:
        """Return class passed in `Generic[ListItemType]`."""
        base_class = next(
            _class
            for _class in cls.__orig_bases__  # type: ignore
            if isclass(get_origin(_class))
            and issubclass(get_origin(_class), ListComponent)
        )

        # Get first generic variable and return it if it is valid item class
        item_class = get_args(base_class)[0]
        if cls.is_valid_item_class(item_class):
            return item_class

        return None

    @classmethod
    def is_valid_item_class(cls, item_class: Any) -> bool:
        """Check that specified ``item_class`` is valid.

        Valid ``item_class`` should be
        * a class and subclass of ``Component``
        * or TypeAlias based on ``Component``

        """
        if isclass(item_class) and issubclass(item_class, Component):
            return True

        if isinstance(item_class, typing._GenericAlias):  # type: ignore
            type_alias = item_class.__origin__  # type: ignore
            return isclass(type_alias) and issubclass(type_alias, Component)

        return False

    def get_item_by_text(self, text: str) -> ListItemType:
        """Get list item by text."""
        locator = self.base_item_locator.extend_query(
            extra_query=(
                f"[contains(., {self.base_item_locator._escape_quotes(text)})]"
            ),
        )
        return self._item_class(page=self.page, base_locator=locator)

    def __repr__(self) -> str:
        return (
            "ListComponent("
            f"component={self.__class__}, "
            f"item_class={self._item_class}, "
            f"base_item_locator={self.base_item_locator}, "
            f"count={self.count}, "
            f"items={self.all}, "
            f"page={self.page}"
            ")"
        )

    def __str__(self) -> str:
        return f"{self.all}"
