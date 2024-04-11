from typing import NoReturn

from pomcorn import ComponentWithBaseLocator, XPathElement, locators
from pomcorn.web_view import WebView


class GetElement:
    """Descriptor for init `Element` as attribute by locator."""

    def __init__(
        self,
        locator: locators.XPathLocator,
        is_relative: bool = True,
    ) -> None:
        """Initialize descriptor.

        Args:
            locator: Instance of a class to locate the element in
                the browser.
            is_relative: Whether add parent ``base_locator`` to the current
                descriptors's `base_locator` or not.

        """
        self._is_relative = is_relative
        self._locator = locator

    def __get__(
        self,
        instance: WebView | None,
        _type: type[WebView],
    ) -> XPathElement:
        """Init and return element with stored locator."""
        if not instance:
            raise AttributeError("This descriptor is for instances only!")

        if self._is_relative and isinstance(
            instance,
            ComponentWithBaseLocator,
        ):
            self._locator = instance.base_locator // self._locator

        return instance.init_element(locator=self._locator)

    def __set__(self, *args, **kwargs) -> NoReturn:
        raise ValueError("You can't reset an element attribute value!")


class ElementByXpath(GetElement):
    """Descriptor for init `Element` as attribute by xpath query."""

    def __init__(self, query: str, is_relative: bool = True) -> None:
        super().__init__(
            locator=locators.XPathLocator(query),
            is_relative=is_relative,
        )


class ElementByTag(GetElement):
    """Descriptor for init `Element` as attribute by css tag."""

    def __init__(self, tag: str, is_relative: bool = True) -> None:
        super().__init__(
            locator=locators.TagNameLocator(tag),
            is_relative=is_relative,
        )


class ElementByDataTestId(GetElement):
    """Descriptor for init `Element` as attribute by "data-testid" property."""

    def __init__(
        self,
        value: str,
        container: str = "*",
        is_relative: bool = True,
    ) -> None:
        super().__init__(
            locator=locators.DataTestIdLocator(value, container),
            is_relative=is_relative,
        )


class ElementById(GetElement):
    """Descriptor for init `Element` as attribute by id."""

    def __init__(
        self,
        value: str,
        container: str = "*",
        is_relative: bool = True,
    ) -> None:
        super().__init__(
            locator=locators.IdLocator(value, container),
            is_relative=is_relative,
        )


class ElementByName(GetElement):
    """Descriptor for init `Element` as attribute by name."""

    def __init__(
        self,
        value: str,
        container: str = "*",
        is_relative: bool = True,
    ) -> None:
        super().__init__(
            locator=locators.NameLocator(value, container),
            is_relative=is_relative,
        )


class ButtonByText(GetElement):
    """Descriptor for init button `Element` as attribute by text."""

    def __init__(
        self,
        text: str,
        exact: bool = False,
        is_relative: bool = True,
    ) -> None:
        super().__init__(
            locator=locators.ButtonWithTextLocator(text, exact),
            is_relative=is_relative,
        )


class InputByLabel(GetElement):
    """Descriptor for init input `Element` as attribute by label."""

    def __init__(self, label: str, is_relative: bool = True) -> None:
        super().__init__(
            locator=locators.InputByLabelLocator(label),
            is_relative=is_relative,
        )


class TextAreaByLabel(GetElement):
    """Descriptor for init textarea `Element` as attribute by label."""

    def __init__(self, label: str, is_relative: bool = True) -> None:
        super().__init__(
            locator=locators.TextAreaByLabelLocator(label),
            is_relative=is_relative,
        )


class ElementByProperty(GetElement):
    """Descriptor for init `Element` as attribute by css property."""

    def __init__(
        self,
        prop: str,
        value: str,
        container: str = "*",
        exact: bool = False,
        is_relative: bool = True,
    ) -> None:
        super().__init__(
            locator=locators.PropertyLocator(
                prop=prop,
                value=value,
                container=container,
                exact=exact,
            ),
            is_relative=is_relative,
        )


class ElementByText(GetElement):
    """Descriptor for init `Element` as attribute by text."""

    def __init__(
        self,
        text: str,
        element: str = "*",
        exact: bool = False,
        is_relative: bool = True,
    ) -> None:
        super().__init__(
            locator=locators.ElementWithTextLocator(
                text=text,
                element=element,
                exact=exact,
            ),
            is_relative=is_relative,
        )


class ElementByClass(GetElement):
    """Descriptor for init `Element` as attribute by css class."""

    def __init__(
        self,
        class_name: str,
        container: str = "*",
        exact: bool = False,
        is_relative: bool = True,
    ) -> None:
        super().__init__(
            locator=locators.ClassLocator(
                class_name=class_name,
                container=container,
                exact=exact,
            ),
            is_relative=is_relative,
        )
