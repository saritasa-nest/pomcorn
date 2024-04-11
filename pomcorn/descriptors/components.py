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
        is_relative: bool = True,
        wait_until_visible: bool = True,
    ) -> None:
        """Initialize descriptor.

        Args:
            base_locator: Instance of a class to locate the component in the
                browser.
            is_relative: Whether add parent ``base_locator`` to the current
                descriptors's `base_locator` or not.
            wait_until_visible: Whether to wait for the component to become
                visible before completing initialization or not.

        """
        self._base_locator = base_locator
        self._is_relative = is_relative
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

        if self._is_relative and not isinstance(instance, Page):
            if instance.base_locator and self._base_locator:
                self._base_locator = (
                    instance.base_locator // self._base_locator
                )

        return self._class(
            page=self._get_page(instance),
            base_locator=self._base_locator,
            wait_until_visible=self._wait_until_visible,
        )

    def __set__(self, *args, **kwargs) -> NoReturn:
        raise ValueError("You can't reset a component attribute value!")

    def _get_page(self, instance: Page | TClass) -> Page:
        """Get page from parent instance."""
        if isinstance(instance, ComponentWithBaseLocator):
            return instance.page
        return instance


class ComponentByXpath(Generic[TClass], GetComponent[TClass]):
    """Descriptor for init component as attribute by xpath query."""

    def __init__(
        self,
        base_locator: str | None = None,
        is_relative: bool = True,
        wait_until_visible: bool = True,
    ) -> None:
        locator = locators.XPathLocator(base_locator) if base_locator else None
        super().__init__(
            base_locator=locator,
            is_relative=is_relative,
            wait_until_visible=wait_until_visible,
        )


class ComponentByTag(Generic[TClass], GetComponent[TClass]):
    """Descriptor for init component as attribute by css tag."""

    def __init__(
        self,
        tag: str,
        is_relative: bool = True,
        wait_until_visible: bool = True,
    ) -> None:
        super().__init__(
            base_locator=locators.TagNameLocator(tag),
            is_relative=is_relative,
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
        is_relative: bool = True,
        wait_until_visible: bool = True,
    ) -> None:
        super().__init__(
            base_locator=locators.PropertyLocator(
                prop=prop,
                value=value,
                container=container,
                exact=exact,
            ),
            is_relative=is_relative,
            wait_until_visible=wait_until_visible,
        )


class ComponentByDataTestId(Generic[TClass], GetComponent[TClass]):
    """Descriptor for init component as attribute by "data-testid" property."""

    def __init__(
        self,
        value: str,
        container: str = "*",
        is_relative: bool = True,
        wait_until_visible: bool = True,
    ) -> None:
        super().__init__(
            base_locator=locators.DataTestIdLocator(value, container),
            is_relative=is_relative,
            wait_until_visible=wait_until_visible,
        )


class ComponentById(Generic[TClass], GetComponent[TClass]):
    """Descriptor for init component as attribute by id."""

    def __init__(
        self,
        value: str,
        container: str = "*",
        is_relative: bool = True,
        wait_until_visible: bool = True,
    ) -> None:
        super().__init__(
            base_locator=locators.IdLocator(value, container),
            is_relative=is_relative,
            wait_until_visible=wait_until_visible,
        )


class ComponentByName(Generic[TClass], GetComponent[TClass]):
    """Descriptor for init component as attribute by name."""

    def __init__(
        self,
        value: str,
        container: str = "*",
        is_relative: bool = True,
        wait_until_visible: bool = True,
    ) -> None:
        super().__init__(
            base_locator=locators.NameLocator(value, container),
            is_relative=is_relative,
            wait_until_visible=wait_until_visible,
        )


class ComponentByText(Generic[TClass], GetComponent[TClass]):
    """Descriptor for init component as attribute by text."""

    def __init__(
        self,
        text: str,
        element: str = "*",
        exact: bool = False,
        is_relative: bool = True,
        wait_until_visible: bool = True,
    ) -> None:
        super().__init__(
            base_locator=locators.ElementWithTextLocator(
                text=text,
                element=element,
                exact=exact,
            ),
            is_relative=is_relative,
            wait_until_visible=wait_until_visible,
        )


class ComponentByClass(Generic[TClass], GetComponent[TClass]):
    """Descriptor for init component as attribute by css class."""

    def __init__(
        self,
        class_name: str,
        container: str = "*",
        exact: bool = False,
        is_relative: bool = True,
        wait_until_visible: bool = True,
    ) -> None:
        super().__init__(
            base_locator=locators.ClassLocator(
                class_name=class_name,
                container=container,
                exact=exact,
            ),
            is_relative=is_relative,
            wait_until_visible=wait_until_visible,
        )
