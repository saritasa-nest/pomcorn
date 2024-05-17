from .base_locators import XPathLocator


class TagNameLocator(XPathLocator):
    """Locator to look for elements with tag by Xpath."""

    def __init__(self, tag: str):
        """Init XPathLocator.

        Specify the query as the string ``//tag``, where ``tag`` is the name of
        the html tag.

        """
        super().__init__(query=f"//{tag}")


class PropertyLocator(XPathLocator):
    """Locator to look for elements with property by XPath."""

    def __init__(
        self,
        prop: str,
        value: str,
        container: str = "*",
        exact: bool = False,
    ):
        """Init XPathLocator.

        Args:
            prop: The name of the html tag property.
            value: The value of property.
            container: The tag in which the property should be. The default is
                ``*``, which means "any tag".
            exact: Specify whether the value of the property being searched
                must match exactly. By default, the search is based on a
                partial match of the value.

        """
        partial_query = f'//{container}[contains(@{prop}, "{value}")]'
        exact_query = f'//{container}[@{prop}="{value}"]'

        super().__init__(query=exact_query if exact else partial_query)


class DataTestIdLocator(PropertyLocator):
    """Locator to look for elements with custom `testid` property.

    Inherits from ``PropertyLocator`` and sets the default values
    ``prop="data-testid"`` and ``exact=True``.

    """

    def __init__(
        self,
        value: str,
        container: str = "*",
    ):
        """Init XPathLocator.

        Args:
            value: The value of ``testid`` property.
            container: The tag in which the property should be. The default is
                ``*``, which means "any tag".

        """
        super().__init__(
            prop="data-testid",
            value=value,
            container=container,
            exact=True,
        )


class IdLocator(PropertyLocator):
    """Locator to look for elements with ID by Xpath.

    Inherits from ``PropertyLocator`` and sets the default values ``prop="id"``
    and ``exact=True``.

    """

    def __init__(
        self,
        value: str,
        container: str = "*",
    ):
        """Init XPathLocator.

        Args:
            value: The value of ``id`` property.
            container: The tag in which the property should be. The default is
                ``*``, which means "any tag".

        """
        super().__init__(
            prop="id",
            value=value,
            container=container,
            exact=True,
        )


class NameLocator(PropertyLocator):
    """Locator to look for elements with name by Xpath.

    Inherits from ``PropertyLocator`` and sets the default values
    ``prop="name"`` and ``exact=True``.

    """

    def __init__(self, value: str, container: str = "*"):
        """Init XPathLocator.

        Args:
            value: The value of ``name`` property.
            container: The tag in which the property should be. The default is
                ``*``, which means "any tag".

        """
        super().__init__(
            prop="name",
            value=value,
            container=container,
            exact=True,
        )


class ElementWithTextLocator(XPathLocator):
    """Locator to look for elements with text by XPath."""

    def __init__(self, text: str, element: str = "*", exact: bool = False):
        """Init XPathLocator.

        Args:
            text: The text that should be inside the tag.
            element: The tag in which the text should be. The default is
                ``*``, which means "any tag".
            exact: Specify whether the value of the property being searched
                must match exactly. By default, the search is based on a
                partial match of the value.

        """
        exact_query = f'//{element}[./text()="{text}"]'
        partial_query = f'//{element}[contains(.,"{text}")]'

        super().__init__(query=exact_query if exact else partial_query)


class ClassLocator(PropertyLocator):
    """Locator to look for elements with partial class by XPath.

    Inherits from ``PropertyLocator`` and sets the default value
    ``prop="class"``.

    """

    def __init__(
        self,
        class_name: str,
        container: str = "*",
        exact: bool = False,
    ):
        """Init XPathLocator.

        Args:
            class_name: The name of tag class.
            container: The tag in which the property should be. The default is
                ``*``, which means "any tag".
            exact: Specify whether the value of the property being searched
                must match exactly. By default, the search is based on a
                partial match of the value.

        """
        super().__init__(
            prop="class",
            value=class_name,
            container=container,
            exact=exact,
        )


class ButtonWithTextLocator(ElementWithTextLocator):
    """Locator to looking for button with text by XPath.

    Inherits from ``ElementWithTextLocator`` and sets the default value
    ``element="button"``.

    """

    def __init__(self, text: str, exact: bool = False):
        """Init XPathLocator.

        Args:
            text: The text that should be inside the button tag.
            exact: Specify whether the value of the property being searched
                must match exactly. By default, the search is based on a
                partial match of the value.

        """
        super().__init__(text=text, element="button", exact=exact)


class InputInLabelLocator(XPathLocator):
    """Locator to looking for input with label by XPath.

    Specify the query as the string
    ``//label[contains(., "label")]//input``, where ``label`` is the text of
    the input label.

    .. code-block:: html

        # Example
        <label>Title</label>
            <input value="Value">
        </label>

    """

    def __init__(self, label: str):
        """Init XPathLocator."""
        super().__init__(
            query=f'//label[contains(., "{label}")]//input',
        )


class InputByLabelLocator(XPathLocator):
    """Locator to looking for input next to label by XPath.

    Specify the query as the string
    ``//label[contains(., "label")]/following-sibling::input``, where ``label``
    is the text of the input label.

    .. code-block:: html

        # Example
        <div>
            <label for="InputWithLabel">Title</label>
            <input id="InputWithLabel" value="Value">
        </div>

    """

    def __init__(self, label: str):
        """Init XPathLocator."""
        super().__init__(
            query=f'//label[contains(., "{label}")]/following-sibling::input',
        )


class TextAreaByLabelLocator(XPathLocator):
    """Locator to looking for textarea with label by XPath.

    Specify the query as the string
    ``//*[label[contains(text(), "{label}")]]/textarea``, where ``label``
    is the text of the textarea label.

    """

    def __init__(self, label: str):
        """Init XPathLocator."""
        super().__init__(
            query=f'//*[label[contains(text(), "{label}")]]/textarea',
        )
