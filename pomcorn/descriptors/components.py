from typing import Any, Generic, NoReturn, TypeAlias, TypeVar

from pomcorn import ComponentWithBaseLocator, WebView, locators
from pomcorn.component import TPage

PageOrComponent: TypeAlias = TPage | ComponentWithBaseLocator[TPage]


# Here type ignore added because we can't specify TPage as generic
# for ComponentWithBaseLocator, but specifying Page is incorrect
TClass = TypeVar("TClass", bound=ComponentWithBaseLocator)  # type: ignore


class ComponentDescriptor(Generic[TPage, TClass]):
    """Descriptor for init component as attribute.

    Can be used for components inherited from `ComponentWithBaseLocator`.

    """

    def __init__(
        self,
        _class: type[TClass],
        base_locator: locators.XPathLocator | None = None,
        wait_until_visible: bool = True,
    ) -> None:
        self._class = _class
        self._base_locator = base_locator
        self._wait_until_visible = wait_until_visible

    def __get__(
        self,
        instance: PageOrComponent[TPage] | None,
        _type: type[WebView],
    ) -> TClass:
        """Init and return component."""
        if not instance:
            raise AttributeError("This descriptor is for instances only!")

        return self._class(
            page=self._get_page(instance),
            base_locator=self._base_locator,
            wait_until_visible=self._wait_until_visible,
        )

    def __set__(self, instance: WebView, value: Any) -> NoReturn:
        raise ValueError("You can't reset a component attribute value!")

    def _get_page(self, instance: PageOrComponent[TPage]) -> TPage:
        if isinstance(instance, ComponentWithBaseLocator):
            return instance.page
        return instance


class ComponentByXpath(
    Generic[TPage, TClass],
    ComponentDescriptor[TPage, TClass],
):
    """Descriptor for init component as attribute by xpath query."""

    def __init__(
        self,
        _class: type[TClass],
        base_locator: str | None = None,
        wait_until_visible: bool = True,
    ) -> None:
        locator: locators.XPathLocator | None

        if base_locator is not None:
            locator = locators.XPathLocator(base_locator)
        else:
            locator = base_locator

        super().__init__(_class, locator, wait_until_visible)


class ComponentByTag(
    Generic[TPage, TClass],
    ComponentDescriptor[TPage, TClass],
):
    """Descriptor for init component as attribute by css tag."""

    def __init__(
        self,
        _class: type[TClass],
        tag: str,
        wait_until_visible: bool = True,
    ) -> None:
        super().__init__(
            _class=_class,
            base_locator=locators.TagNameLocator(tag),
            wait_until_visible=wait_until_visible,
        )


class ComponentByProperty(
    Generic[TPage, TClass],
    ComponentDescriptor[TPage, TClass],
):
    """Descriptor for init component as attribute by css property."""

    def __init__(
        self,
        _class: type[TClass],
        prop: str,
        value: str,
        container: str = "*",
        exact: bool = False,
        wait_until_visible: bool = True,
    ) -> None:
        super().__init__(
            _class=_class,
            base_locator=locators.PropertyLocator(
                prop=prop,
                value=value,
                container=container,
                exact=exact,
            ),
            wait_until_visible=wait_until_visible,
        )


class ComponentByDataTestId(
    Generic[TPage, TClass],
    ComponentDescriptor[TPage, TClass],
):
    """Descriptor for init component as attribute by "data-testid" property."""

    def __init__(
        self,
        _class: type[TClass],
        value: str,
        container: str = "*",
        wait_until_visible: bool = True,
    ) -> None:
        super().__init__(
            _class=_class,
            base_locator=locators.DataTestIdLocator(value, container),
            wait_until_visible=wait_until_visible,
        )


class ComponentById(
    Generic[TPage, TClass],
    ComponentDescriptor[TPage, TClass],
):
    """Descriptor for init component as attribute by id."""

    def __init__(
        self,
        _class: type[TClass],
        value: str,
        container: str = "*",
        wait_until_visible: bool = True,
    ) -> None:
        super().__init__(
            _class=_class,
            base_locator=locators.IdLocator(value, container),
            wait_until_visible=wait_until_visible,
        )


class ComponentByName(
    Generic[TPage, TClass],
    ComponentDescriptor[TPage, TClass],
):
    """Descriptor for init component as attribute by name."""

    def __init__(
        self,
        _class: type[TClass],
        value: str,
        container: str = "*",
        wait_until_visible: bool = True,
    ) -> None:
        super().__init__(
            _class=_class,
            base_locator=locators.NameLocator(value, container),
            wait_until_visible=wait_until_visible,
        )


class ComponentByText(
    Generic[TPage, TClass],
    ComponentDescriptor[TPage, TClass],
):
    """Descriptor for init component as attribute by text."""

    def __init__(
        self,
        _class: type[TClass],
        text: str,
        element: str = "*",
        exact: bool = False,
        wait_until_visible: bool = True,
    ) -> None:
        super().__init__(
            _class=_class,
            base_locator=locators.ElementWithTextLocator(
                text=text,
                element=element,
                exact=exact,
            ),
            wait_until_visible=wait_until_visible,
        )


class ComponentByClass(
    Generic[TPage, TClass],
    ComponentDescriptor[TPage, TClass],
):
    """Descriptor for init component as attribute by css class."""

    def __init__(
        self,
        _class: type[TClass],
        class_name: str,
        container: str = "*",
        exact: bool = False,
        wait_until_visible: bool = True,
    ) -> None:
        super().__init__(
            _class=_class,
            base_locator=locators.ClassLocator(
                class_name=class_name,
                container=container,
                exact=exact,
            ),
            wait_until_visible=wait_until_visible,
        )
