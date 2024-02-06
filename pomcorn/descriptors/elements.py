from typing import Any, NoReturn

from pomcorn import XPathElement, locators
from pomcorn.web_view import WebView


class ElementDescriptor:
    """Descriptor for init `Element` as attribute by locator."""

    def __init__(self, locator: locators.XPathLocator) -> None:
        self._locator = locator

    def __get__(
        self,
        instance: WebView | None,
        _type: type[WebView],
    ) -> XPathElement:
        """Init and return element with stored locator."""
        if not instance:
            raise AttributeError("This descriptor is for instances only!")
        return instance.init_element(self._locator)

    def __set__(self, instance: WebView, value: Any) -> NoReturn:
        raise ValueError("You can't reset an element attribute value!")


class ElementByXpath(ElementDescriptor):
    """Descriptor for init `Element` as attribute by xpath query."""

    def __init__(self, query: str) -> None:
        super().__init__(locators.XPathLocator(query))


class ElementByTag(ElementDescriptor):
    """Descriptor for init `Element` as attribute by css tag."""

    def __init__(self, tag: str) -> None:
        super().__init__(locators.TagNameLocator(tag))


class ElementByDataTestId(ElementDescriptor):
    """Descriptor for init `Element` as attribute by "data-testid" property."""

    def __init__(self, value: str, container: str = "*") -> None:
        super().__init__(locators.DataTestIdLocator(value, container))


class ElementById(ElementDescriptor):
    """Descriptor for init `Element` as attribute by id."""

    def __init__(self, value: str, container: str = "*") -> None:
        super().__init__(locators.IdLocator(value, container))


class ElementByName(ElementDescriptor):
    """Descriptor for init `Element` as attribute by name."""

    def __init__(self, value: str, container: str = "*") -> None:
        super().__init__(locators.NameLocator(value, container))


class ButtonByText(ElementDescriptor):
    """Descriptor for init button `Element` as attribute by text."""

    def __init__(self, text: str, exact: bool = False) -> None:
        super().__init__(locators.ButtonWithTextLocator(text, exact))


class InputByLabel(ElementDescriptor):
    """Descriptor for init input `Element` as attribute by label."""

    def __init__(self, label: str) -> None:
        super().__init__(locators.InputByLabelLocator(label))


class TextAreaByLabel(ElementDescriptor):
    """Descriptor for init textarea `Element` as attribute by label."""

    def __init__(self, label: str) -> None:
        super().__init__(locators.TextAreaByLabelLocator(label))


class ElementByProperty(ElementDescriptor):
    """Descriptor for init `Element` as attribute by css property."""

    def __init__(
        self,
        prop: str,
        value: str,
        container: str = "*",
        exact: bool = False,
    ) -> None:
        super().__init__(
            locator=locators.PropertyLocator(
                prop=prop,
                value=value,
                container=container,
                exact=exact,
            ),
        )


class ElementByText(ElementDescriptor):
    """Descriptor for init `Element` as attribute by text."""

    def __init__(
        self,
        text: str,
        element: str = "*",
        exact: bool = False,
    ) -> None:
        super().__init__(
            locator=locators.ElementWithTextLocator(
                text=text,
                element=element,
                exact=exact,
            ),
        )


class ElementByClass(ElementDescriptor):
    """Descriptor for init `Element` as attribute by css class."""

    def __init__(
        self,
        class_name: str,
        container: str = "*",
        exact: bool = False,
    ) -> None:
        super().__init__(
            locator=locators.ClassLocator(
                class_name=class_name,
                container=container,
                exact=exact,
            ),
        )
