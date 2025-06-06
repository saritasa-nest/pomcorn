"""Module with `XPathLocator`.

Provide only `XPathLocator` because a locator of this type
is sufficient for all operations and
it also allows to combine locators with `/` operator.
It's better to use one type of locators for consistency.

Example:
  # Search button inside base element
  button_element_locator = base_locator / button_locator

"""

from __future__ import annotations

from collections.abc import Iterator
from typing import Literal, TypeVar

from selenium.webdriver.common.by import By


class Locator:
    """Base locator for looking for elements in page."""

    _ALLOWED_LOCATORS = (
        By.ID,
        By.XPATH,
        By.LINK_TEXT,
        By.PARTIAL_LINK_TEXT,
        By.NAME,
        By.TAG_NAME,
        By.CLASS_NAME,
        By.CSS_SELECTOR,
    )

    def __init__(self, by: str, query: str):
        """Init locator.

        Args:
            by: One of the supported selenium locator strategies.
            query: Query for the strategy.

        """
        if by not in self._ALLOWED_LOCATORS:
            raise ValueError(f"No valid `by` found -> `{by}`")
        self.by = by
        self.query: str = query

    def __iter__(self) -> Iterator[str]:
        """Unpack locator.

        This is necessary because selenium WebDriver methods use
        `By` and `value` tuples to find elements. Thanks to this we can use
        `*locator` for these methods.

        """
        return iter((self.by, self.query))

    def __repr__(self) -> str:
        return f"Locator<By `{self.by}`: Query `{self.query}`>"

    def __str__(self) -> str:
        return self.query


TLocator = TypeVar("TLocator", bound=Locator, covariant=True)

# This need only for element initialization because covariant generic can't be
# used as type for parameter of function
TInitLocator = TypeVar("TInitLocator", bound=Locator)


class XPathLocator(Locator):
    r"""Locator to looking for elements in page by XPath.

    XPathLocator overrides methods for `/` and `//` operators to provide
    "path-like" syntax for locators.

    So we can use `/` and `//` operators to concatenate locators query by `/`
    and `//` accordingly:

        # //\*[@class="class"]

        class_locator = ClassLocator("class")

        # //container[@prop="value"]

        property_locator = PropertyLocator(
            prop="prop",
            value="value",
            container="container",

        )

        # //\*[@class="class"]/container[@prop="value"]

        class_locator / property_locator

        # //\*[@class="class"]//container[@prop="value"]

        class_locator // property_locator

    To extend query of locator you can use `extend_query` method:
        new_locator = class_locator.extend_query("[@some_prop='value']")

        new_locator.query   # //\*[@class="class"][@some_prop="value"]

    All custom locators that inherit `XPathLocator` should be independent and
    start with `//`.

    """

    # We move it to constant to fix flake-8 warning B005:
    # https://pypi.org/project/flake8-bugbear/#:~:text=B005
    divider = "//"

    def __init__(self, query: str):
        """Set related query for locators concatenation.

        Args:
            query: Query for the XPath locator strategy.

        """
        self.related_query = query.lstrip(self.divider)
        super().__init__(by=By.XPATH, query=query)

    def __truediv__(self, other: XPathLocator | str) -> XPathLocator:
        """Override `/` operator to implement following XPath locators.

        "/" used to select the nearest children of the current node.

        """
        return self.prepare_relative_locator(other=other, separator="/")

    def __floordiv__(self, other: XPathLocator | str) -> XPathLocator:
        """Override `//` operator to implement nested XPath locators.

        "//" used to select all descendants (children, grandchildren,
        great-grandchildren, etc.) of current node, regardless of their level
        in hierarchy.

        """
        return self.prepare_relative_locator(other=other, separator="//")

    def __or__(self, other: XPathLocator) -> XPathLocator:
        r"""Override `|` operator to implement variant XPath locators.

        Example:
            span = XPathLocator("//span")
            div = XPathLocator("//div")
            img = XPathLocator("//img")

            (span | div) // img == XPathLocator("(//span | //div)//img")

            span | div // img == XPathLocator("(//span | //div//img)")

        """
        return XPathLocator(query=f"({self.query} | {other.query})")

    def __getitem__(self, value: int | str | XPathLocator) -> XPathLocator:
        """Allow to set xpath expressions or index into the locator query.

        Examples:
            div_locator = XPathLocator("//div") --> `//div`

            # Indexation
            div_locator[0]  --> `(//div)[1]`   # xpath numeration starts with 1
            div_locator[-1] --> `(//div)[last()]`

            # Attribute condition
            div_locator["@type='black'"] --> `//div[@type='black']

            # Checking if there are children
            child_locator = XPathLocator("//label").contains("Schedule")
                --> `//label[contains(., 'Star']`
            div_locator[child_locator] --> `//div[//label[contains(., 'Star']]`

        """
        query = f"({self.query})"

        if isinstance(value, XPathLocator):
            value = value.query

        if isinstance(value, str):
            return XPathLocator(f"{query}[{value}]")

        if value >= 0:
            # `+1` is used here because numeration in xpath starts with 1
            query += f"[{value + 1}]"
        elif value == -1:
            # To avoid ugly locators with `...)[last() - 0]`
            query += "[last()]"
        else:
            query += f"[last() - {abs(value + 1)}]"

        return XPathLocator(query)

    def __bool__(self) -> bool:
        """Return whether query of current locator is empty or not."""
        return bool(self.related_query)

    @classmethod
    def _escape_quotes(cls, text: str) -> str:
        """Escape single and double quotes in given text for use in locators.

        This method is useful when locating elements
        with text containing single or double quotes.

        For example, the text `He's 6'2"` will be transformed into:
        `concat("He", "'", "s 6", "'", "2", '"')`.

        The resulting string can be used in XPath expressions
        like `text()=...` or `contains(.,...)`.

        Returns:
            The escaped text wrapped in `concat()` for XPath compatibility,
            or the original text in double quotes if no escaping is needed.

        """
        if not text or ('"' not in text and "'" not in text):
            return f'"{text}"'

        escaped_parts = []
        buffer = ""  # Temporary storage for normal characters

        for char in text:
            if char not in ('"', "'"):
                buffer += char
                continue
            if buffer:
                escaped_parts.append(f'"{buffer}"')
                buffer = ""
            escaped_parts.append(
                "'" + char + "'" if char == '"' else '"' + char + '"',
            )

        if buffer:
            escaped_parts.append(f'"{buffer}"')

        return f"concat({', '.join(escaped_parts)})"

    def extend_query(self, extra_query: str) -> XPathLocator:
        """Return new XPathLocator with extended query."""
        return XPathLocator(query=self.query + extra_query)

    def contains(self, text: str, exact: bool = False) -> XPathLocator:
        """Return new XPathLocator with search on contained text.

        This is shortcut for the commonly used
        `.extend_query(f"[contains(., '{text}')])`.

        Args:
            text: The text that should be inside the tag.
            exact: Specify whether the text being searched must match exactly.
                By default, the search is based on a partial match.

        """
        partial_query = f"[contains(., {self._escape_quotes(text)})]"
        exact_query = f"[./text()={self._escape_quotes(text)}]"
        return self.extend_query(exact_query if exact else partial_query)

    def prepare_relative_locator(
        self,
        other: XPathLocator | str,
        separator: Literal["/", "//"] = "/",
    ) -> XPathLocator:
        """Prepare relative locator base on queries of two locators.

        If one of parent and other locator queries is empty, the method will
        return only the filled one.

        Args:
            other: Child locator object or str locator query.
            separator: Literal which will placed between locators queries - "/"
                used to select nearest children of current node and "//" used
                to select all descendants (children, grandchildren,
                great-grandchildren, etc.) of current node, regardless of their
                level in hierarchy.

        Raises:
            ValueError: If parent and child locators queries are empty.

        """
        related_query = self.related_query
        if not related_query.startswith("("):
            # Parent query can be bracketed, in which case we don't need to use
            # `//`
            # Example:
            #   (//li)[3] -> valid
            #   //(//li)[3] -> invalid
            related_query = f"//{self.related_query}"

        other = XPathLocator(other) if isinstance(other, str) else other

        locator = XPathLocator(
            query=f"{related_query}{separator}{other.related_query}",
        )

        if self and other:
            return locator

        if not (self or other):
            raise ValueError(
                f"Both of locators have empty query. The `{locator.query}` is "
                "not a valid locator.",
            )

        return self if self else other
