from typing import Generic, NoReturn, TypeVar, get_args

from pomcorn import ComponentWithBaseLocator, Page, WebView, locators

# Here type ignore added because we can't specify TPage as generic
# for ComponentWithBaseLocator, but specifying Page is incorrect
TClass = TypeVar("TClass", bound=ComponentWithBaseLocator)  # type: ignore


class GetComponent(Generic[TClass]):
    """Descriptor for init component as attribute.

    Can be used for components inherited from `ComponentWithBaseLocator`.

    """

    def __init__(
        self,
        base_locator: locators.XPathLocator | None = None,
        wait_until_visible: bool = True,
    ) -> None:
        self._base_locator = base_locator
        self._wait_until_visible = wait_until_visible

    @property
    def _class(self) -> type[TClass]:
        """Return class passed in `TClass`."""
        return get_args(self.__orig_class__)[0]  # type: ignore

    def __get__(
        self,
        instance: Page | TClass | None,
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

    def __set__(self, *args, **kwargs) -> NoReturn:
        raise ValueError("You can't reset a component attribute value!")

    def _get_page(self, instance: Page | TClass) -> Page:
        if isinstance(instance, ComponentWithBaseLocator):
            return instance.page
        return instance


class ComponentByXpath(Generic[TClass], GetComponent[TClass]):
    """Descriptor for init component as attribute by xpath query."""

    def __init__(
        self,
        base_locator: str | None = None,
        wait_until_visible: bool = True,
    ) -> None:
        super().__init__(
            base_locator=locators.XPathLocator(base_locator)
            if base_locator
            else None,
            wait_until_visible=wait_until_visible,
        )


class ComponentByTag(Generic[TClass], GetComponent[TClass]):
    """Descriptor for init component as attribute by css tag."""

    def __init__(self, tag: str, wait_until_visible: bool = True) -> None:
        super().__init__(
            base_locator=locators.TagNameLocator(tag),
            wait_until_visible=wait_until_visible,
        )


class ComponentByProperty(Generic[TClass], GetComponent[TClass]):
    """Descriptor for init component as attribute by css property."""

    def __init__(
        self,
        prop: str,
        value: str,
        container: str = "*",
        exact: bool = False,
        wait_until_visible: bool = True,
    ) -> None:
        super().__init__(
            base_locator=locators.PropertyLocator(
                prop=prop,
                value=value,
                container=container,
                exact=exact,
            ),
            wait_until_visible=wait_until_visible,
        )


class ComponentByDataTestId(Generic[TClass], GetComponent[TClass]):
    """Descriptor for init component as attribute by "data-testid" property."""

    def __init__(
        self,
        value: str,
        container: str = "*",
        wait_until_visible: bool = True,
    ) -> None:
        super().__init__(
            base_locator=locators.DataTestIdLocator(value, container),
            wait_until_visible=wait_until_visible,
        )


class ComponentById(Generic[TClass], GetComponent[TClass]):
    """Descriptor for init component as attribute by id."""

    def __init__(
        self,
        value: str,
        container: str = "*",
        wait_until_visible: bool = True,
    ) -> None:
        super().__init__(
            base_locator=locators.IdLocator(value, container),
            wait_until_visible=wait_until_visible,
        )


class ComponentByName(Generic[TClass], GetComponent[TClass]):
    """Descriptor for init component as attribute by name."""

    def __init__(
        self,
        value: str,
        container: str = "*",
        wait_until_visible: bool = True,
    ) -> None:
        super().__init__(
            base_locator=locators.NameLocator(value, container),
            wait_until_visible=wait_until_visible,
        )


class ComponentByText(Generic[TClass], GetComponent[TClass]):
    """Descriptor for init component as attribute by text."""

    def __init__(
        self,
        text: str,
        element: str = "*",
        exact: bool = False,
        wait_until_visible: bool = True,
    ) -> None:
        super().__init__(
            base_locator=locators.ElementWithTextLocator(
                text=text,
                element=element,
                exact=exact,
            ),
            wait_until_visible=wait_until_visible,
        )


class ComponentByClass(Generic[TClass], GetComponent[TClass]):
    """Descriptor for init component as attribute by css class."""

    def __init__(
        self,
        class_name: str,
        container: str = "*",
        exact: bool = False,
        wait_until_visible: bool = True,
    ) -> None:
        super().__init__(
            base_locator=locators.ClassLocator(
                class_name=class_name,
                container=container,
                exact=exact,
            ),
            wait_until_visible=wait_until_visible,
        )
