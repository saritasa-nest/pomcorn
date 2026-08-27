from typing import Generic, TypeAlias, TypeVar

import pytest

from pomcorn import Component, ListComponent, Page, locators

TItem = TypeVar("TItem", bound=Component[Page])
TPage = TypeVar("TPage", bound=Page)


class ItemClass(Component[Page]):
    """Common test component for represent item class."""


def test_set_item_class_in_parent_class(fake_page: Page) -> None:
    """Check that we can specify only `item_class` in base class.

    And after specifying other generic arguments in subclasses, `item_class`
    will still be correct.

    """

    class BaseList(ListComponent[ItemClass, TPage], Generic[TPage]):
        """Base list component with specified item_class in Generic."""

        base_locator = locators.XPathLocator("html")  # required

        def wait_until_visible(
            self,
            timeout: float | None = None,
            **kwargs,
        ) -> None:
            """To not wait anything."""

    # Inherit from `BaseList` and specify page generic variable
    class InheritedList(BaseList[Page]): ...

    # Ensure that `InheritedList.item_class` has correct type
    list_cls = InheritedList(fake_page)
    assert list_cls._item_class is ItemClass


def test_no_set_item_class(fake_page: Page) -> None:
    """Check that we can't not specify `item_class`."""

    class BaseList(ListComponent[TItem, TPage], Generic[TItem, TPage]):
        """Base list component without specified Generic variables."""

        base_locator = locators.XPathLocator("html")  # required
        relative_item_locator = locators.XPathLocator("body")  # required

        def wait_until_visible(
            self,
            timeout: float | None = None,
            **kwargs,
        ) -> None:
            """To not wait anything."""

    # Inherit from `BaseList` and specify only page generic variable
    class InheritedList(BaseList[TItem, Page], Generic[TItem]): ...

    list_cls = InheritedList(fake_page)  # type: ignore

    assert not list_cls._item_class
    with pytest.raises(TypeError, match=r"object is not callable"):
        list_cls.get_item_by_text("item")


def test_set_item_class_in_child_via_generic(fake_page: Page) -> None:
    """Check that we can specify `item_class` only in the child class."""

    class BaseList(ListComponent[TItem, TPage], Generic[TItem, TPage]):
        """Base list component without specified Generic variables."""

        base_locator = locators.XPathLocator("html")  # required

        def wait_until_visible(
            self,
            timeout: float | None = None,
            **kwargs,
        ) -> None:
            """To not wait anything."""

    # Prepare base list component without specified Generic variables
    class InheritedList(BaseList[ItemClass, Page]): ...

    # Ensure that `InheritedList.item_class` has correct type
    list_cls = InheritedList(fake_page)
    assert list_cls._item_class is ItemClass


def test_specify_all_generic_variables(fake_page: Page) -> None:
    """Check that item_class will be correct if fill all generic variables."""

    class List(ListComponent[ItemClass, Page]):
        base_locator = locators.XPathLocator("html")  # required

        def wait_until_visible(
            self,
            timeout: float | None = None,
            **kwargs,
        ) -> None:
            """To not wait anything."""

    list_cls = List(fake_page)
    assert list_cls._item_class is ItemClass


def test_set_item_class_with_extra_generic_variable(fake_page: Page) -> None:
    """Check that item_class will be correct if add new generic variable."""
    TParam = TypeVar("TParam")

    class BaseList(ListComponent[ItemClass, Page], Generic[TParam]):
        """Base list component with new generic variable."""

        base_locator = locators.XPathLocator("html")  # required

        def wait_until_visible(
            self,
            timeout: float | None = None,
            **kwargs,
        ) -> None:
            """To not wait anything."""

    # Inherit from `BaseList` and specify new generic variable
    class Param(Component[Page]): ...

    class List(BaseList[Param]): ...

    # Ensure that `List.item_class` has correct type
    list_cls = List(fake_page)
    assert list_cls._item_class is ItemClass


def test_set_item_class_without_inheritance(fake_page: Page) -> None:
    """Check that item_class will be correct in not inherited class."""

    class BaseList(ListComponent[TItem, TPage], Generic[TItem, TPage]):
        """Base list component without specified Generic variables."""

        base_locator = locators.XPathLocator("html")  # required
        relative_item_locator = locators.XPathLocator("body")  # required

        def wait_until_visible(
            self,
            timeout: float | None = None,
            **kwargs,
        ) -> None:
            """To not wait anything."""

    # Prepare base list component without specified Generic variables
    list_cls = BaseList[ItemClass, Page](fake_page)
    # Ensure that `InheritedList.item_class` has correct type
    assert list_cls._item_class is ItemClass


# Type alias for check that ItemClass can be also a TypeAlias
TypeAliasItemClass: TypeAlias = Component[Page]


def test_item_class_can_be_type_alias(fake_page: Page) -> None:
    """Check that item_class can be a type alias based on ``Component``."""

    class List(ListComponent[TypeAliasItemClass, Page]):
        base_locator = locators.XPathLocator("html")  # required

        def wait_until_visible(
            self,
            timeout: float | None = None,
            **kwargs,
        ) -> None:
            """To not wait anything."""

    list_cls = List(fake_page)
    assert list_cls._item_class is TypeAliasItemClass
