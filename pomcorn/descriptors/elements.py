from typing import NoReturn

from pomcorn import XPathElement, locators
from pomcorn.web_view import WebView


class GetElement:
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
        return instance.init_element(locator=self._locator)

    def __set__(self, *args, **kwargs) -> NoReturn:
        raise ValueError("You can't reset an element attribute value!")


class ElementByXpath(GetElement):
    """Descriptor for init `Element` as attribute by xpath query."""

    def __init__(self, query: str) -> None:
        super().__init__(locator=locators.XPathLocator(query))


class ElementByTag(GetElement):
    """Descriptor for init `Element` as attribute by css tag."""

    def __init__(self, tag: str) -> None:
        super().__init__(locator=locators.TagNameLocator(tag))


class ElementByDataTestId(GetElement):
    """Descriptor for init `Element` as attribute by "data-testid" property."""

    def __init__(self, value: str, container: str = "*") -> None:
        super().__init__(locator=locators.DataTestIdLocator(value, container))


class ElementById(GetElement):
    """Descriptor for init `Element` as attribute by id."""

    def __init__(self, value: str, container: str = "*") -> None:
        super().__init__(locator=locators.IdLocator(value, container))


class ElementByName(GetElement):
    """Descriptor for init `Element` as attribute by name."""

    def __init__(self, value: str, container: str = "*") -> None:
        super().__init__(locator=locators.NameLocator(value, container))


class ButtonByText(GetElement):
    """Descriptor for init button `Element` as attribute by text."""

    def __init__(self, text: str, exact: bool = False) -> None:
        super().__init__(locator=locators.ButtonWithTextLocator(text, exact))


class InputByLabel(GetElement):
    """Descriptor for init input `Element` as attribute by label."""

    def __init__(self, label: str) -> None:
        super().__init__(locator=locators.InputByLabelLocator(label))


class TextAreaByLabel(GetElement):
    """Descriptor for init textarea `Element` as attribute by label."""

    def __init__(self, label: str) -> None:
        super().__init__(locator=locators.TextAreaByLabelLocator(label))


class ElementByProperty(GetElement):
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


class ElementByText(GetElement):
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


class ElementByClass(GetElement):
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
